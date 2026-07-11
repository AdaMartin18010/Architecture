#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
standard-status-checker.py
==========================

标准状态自动复核脚本 v2.0。

功能：
- 读取 struct/99-reference/standards-index/authoritative-sources-v2.md
- 提取所有带官方 URL 的标准条目
- 对每个 URL 发起 HEAD 请求（best-effort）检测可访问性
- **新增**: 缓存上次结果，支持趋势告警（新增失效、状态变化、重定向目标变化）
- **新增**: 可配置已知受限/无需告警的域名白名单
- **新增**: 输出 JSON 状态快照，供 standard-tracker.py 与 CI 使用
- 输出 Markdown 报告到 reports/standard-status-report.md
- 控制台打印汇总统计
- 退出码固定为 0，仅作信息报告，不导致 CI 失败

用法：
    python scripts/standard-status-checker.py
    python scripts/standard-status-checker.py --json
    python scripts/standard-status-checker.py --follow-redirects
    python scripts/standard-status-checker.py --no-cache

环境：
    仅使用 Python 标准库（urllib），无需安装第三方依赖。
"""

import argparse
import json
import re
import ssl
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

# ---------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FILE = PROJECT_ROOT / "struct" / "99-reference" / "standards-index" / "authoritative-sources-v2.md"
REPORT_FILE = PROJECT_ROOT / "reports" / "standard-status-report.md"
CACHE_FILE = PROJECT_ROOT / "reports" / "standard-status-cache.json"
SNAPSHOT_FILE = PROJECT_ROOT / "reports" / "standard-status-snapshot.json"

TIMEOUT_SECONDS = 10
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.0 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.0"
)

# 在当前运行环境中经常被限制或超时的域名
# 这些域名即使请求失败，也标记为“网络受限，需人工复核”
RESTRICTED_HOSTS = {
    "github.com",
    "www.github.com",
    "raw.githubusercontent.com",
    "github.io",
    "gist.github.com",
    "gitlab.com",
    "www.gitlab.com",
    "iso.org",
    "www.iso.org",
    "iec.ch",
    "www.iec.ch",
    "opengroup.org",
    "www.opengroup.org",
    "csrc.nist.gov",
    "nist.gov",
    "www.nist.gov",
}

# 已知会返回 3xx 重定向但仍为有效官方来源的域名
# 用于抑制“不必要的重定向告警”，但仍会在报告中列出
REDIRECT_WHITELIST_HOSTS = {
    "www.iso.org",
    "iso.org",
    "www.opengroup.org",
    "opengroup.org",
    "www.iec.ch",
    "iec.ch",
    "csrc.nist.gov",
    "www.nist.gov",
    "slsa.dev",
    "www.slsa.dev",
    "modelcontextprotocol.io",
    "www.modelcontextprotocol.io",
    "a2aprotocol.io",
    "www.a2aprotocol.io",
    "a2a-protocol.org",
    "www.a2a-protocol.org",
}

# ---------------------------------------------------------------------
# 类型与常量
# ---------------------------------------------------------------------

STATUS_OK = "正常"
STATUS_REDIRECT = "重定向"
STATUS_BROKEN = "失效或受限"
STATUS_UNREACHABLE = "无法访问"
STATUS_RESTRICTED = "网络受限，需人工复核"


# ---------------------------------------------------------------------
# Markdown 表格解析
# ---------------------------------------------------------------------

def extract_table_rows(text: str) -> list[dict[str, str]]:
    """
    从 Markdown 文本中提取所有标准表格的行。

    规则：
    - 识别以 '|' 分隔的表格行；
    - 跳过表头分隔行（仅包含 '-', ':', '|', 空格）；
    - 假设表头包含“标准/框架”、“官方 URL”等列；
    - 返回字典列表，键为表头单元格（去首尾空格），值为对应单元格内容。
    """
    rows: list[dict[str, str]] = []
    header: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]
        # 空行跳过
        if not any(cells):
            continue

        # 表头分隔行
        if all(re.fullmatch(r"[:\- ]+", cell) for cell in cells if cell):
            continue

        if not header:
            header = cells
            continue

        # 列数不一致时，用空字符串补齐
        row = dict(zip(header, cells + [""] * (len(header) - len(cells))))
        rows.append(row)

    return rows


def extract_first_url(cell: str) -> str | None:
    """
    从单元格文本中提取第一个 URL（Markdown 尖括号 <> 或普通链接）。
    返回 None 表示未找到 URL。
    """
    # 优先匹配 Markdown 尖括号 URL：<https://...>
    match = re.search(r"<\s*(https?://[^>]+)\s*>", cell)
    if match:
        return match.group(1).strip()

    # 兜底：普通 http(s) 链接
    match = re.search(r"https?://[^\s\)\]\"]+", cell)
    if match:
        return match.group(0).strip().rstrip(".)")

    return None


def parse_entries(text: str) -> list[dict[str, str]]:
    """
    解析 Markdown 内容，返回所有带官方 URL 的标准条目。

    每个条目包含：
    - name: 标准/框架名称
    - version: 版本
    - status: 状态
    - url: 官方 URL
    - note: 备注
    """
    rows = extract_table_rows(text)
    entries = []

    for row in rows:
        # 寻找官方 URL 列；兼容不同表头大小写/空格
        url_cell = (
            row.get("官方 URL")
            or row.get("官方URL")
            or row.get("官方 Url")
            or row.get("官方 url")
        )
        if not url_cell:
            continue

        url = extract_first_url(url_cell)
        if not url:
            continue

        entries.append(
            {
                "name": row.get("标准/框架", "").strip("* "),
                "version": row.get("版本", ""),
                "status": row.get("状态", ""),
                "url": url,
                "note": row.get("备注", ""),
            }
        )

    return entries


# ---------------------------------------------------------------------
# URL 检测
# ---------------------------------------------------------------------

def is_restricted_host(url: str) -> bool:
    """判断 URL 是否属于已知在当前环境受限的域名。"""
    try:
        host = urlparse(url).hostname or ""
        return host.lower() in RESTRICTED_HOSTS
    except Exception:
        return False


def is_redirect_whitelisted(url: str, final_url: str | None) -> bool:
    """判断重定向是否发生在白名单域名内部（通常可忽略）。"""
    try:
        host = urlparse(url).hostname or ""
        final_host = urlparse(final_url or url).hostname or ""
        return host.lower() in REDIRECT_WHITELIST_HOSTS or final_host.lower() in REDIRECT_WHITELIST_HOSTS
    except Exception:
        return False


def check_url(url: str, follow_redirects: bool = False) -> dict[str, Any]:
    """
    对指定 URL 发起 HEAD 请求并返回结果字典。

    返回字段：
    - status: 可读状态（正常/重定向/失效或受限/无法访问/网络受限）
    - http_status: HTTP 状态码，若无法获得则为 None
    - final_url: 重定向目标，若存在
    - redirect_count: 重定向次数（follow_redirects=True 时）
    - error: 错误信息，若存在
    """
    result: dict[str, Any] = {
        "status": None,
        "http_status": None,
        "final_url": None,
        "redirect_count": 0,
        "error": None,
    }

    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "identity",
            "Connection": "keep-alive",
        },
    )

    # 某些站点证书链不完整，允许继续访问
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(
            request,
            timeout=TIMEOUT_SECONDS,
            context=context,
        ) as response:
            code = response.getcode()
            result["http_status"] = code
            result["final_url"] = response.geturl()

            if 200 <= code < 300:
                result["status"] = STATUS_OK
            elif 300 <= code < 400:
                result["status"] = STATUS_REDIRECT
                result["final_url"] = response.headers.get("Location") or response.geturl()
            else:
                result["status"] = STATUS_BROKEN

    except HTTPError as exc:
        result["http_status"] = exc.code
        if 300 <= exc.code < 400:
            result["status"] = STATUS_REDIRECT
            result["final_url"] = exc.headers.get("Location")
        elif 400 <= exc.code < 600:
            result["status"] = STATUS_BROKEN
            result["error"] = f"HTTP {exc.code}"
            # 对已知反爬/限流域名，403 视为受限而非失效
            if exc.code == 403 and is_restricted_host(url):
                result["status"] = STATUS_RESTRICTED
                result["error"] = f"HTTP 403（反爬受限）"
        else:
            result["status"] = STATUS_UNREACHABLE
            result["error"] = str(exc.reason)

    except URLError as exc:
        result["status"] = STATUS_UNREACHABLE
        result["error"] = str(exc.reason)

    except TimeoutError:
        result["status"] = STATUS_UNREACHABLE
        result["error"] = "请求超时"

    except Exception as exc:  # noqa: BLE001
        result["status"] = STATUS_UNREACHABLE
        result["error"] = str(exc)

    # 如果最终状态是不可访问且域名已知受限，则标记为需人工复核
    if result["status"] == STATUS_UNREACHABLE and is_restricted_host(url):
        result["status"] = STATUS_RESTRICTED

    # 可选：跟随重定向（最多 3 层），获得最终状态
    if follow_redirects and result["status"] == STATUS_REDIRECT and result["final_url"]:
        if result.get("redirect_count", 0) < 3:
            result["redirect_count"] = result.get("redirect_count", 0) + 1
            next_result = check_url(result["final_url"], follow_redirects=True)
            # 合并结果：保留原始 final_url 作为最终 landing URL
            result["status"] = next_result["status"]
            result["http_status"] = next_result["http_status"]
            result["final_url"] = next_result.get("final_url") or result["final_url"]
            result["error"] = next_result.get("error")

    return result


# ---------------------------------------------------------------------
# 缓存与趋势告警
# ---------------------------------------------------------------------

def load_cache() -> dict[str, Any]:
    """加载上次缓存的状态。"""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_cache(data: dict[str, Any]) -> None:
    """保存本次状态到缓存。"""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def compute_trend_alerts(
    entries: list[dict[str, str]],
    results: list[dict[str, Any]],
    previous: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    比较当前结果与上次缓存，生成趋势告警。

    告警类型：
    - NEW_BROKEN: 上次正常/重定向，本次失效或无法访问
    - NEW_REDIRECT: 上次正常，本次出现重定向
    - REDIRECT_CHANGED: 重定向目标发生变化
    - FIXED: 上次失效，本次恢复
    """
    alerts: list[dict[str, Any]] = []
    prev_by_url = {item.get("url", ""): item for item in previous.get("items", [])}

    for entry, result in zip(entries, results):
        url = entry["url"]
        prev = prev_by_url.get(url)
        if not prev:
            continue

        prev_status = prev.get("status")
        curr_status = result["status"]
        prev_final = prev.get("final_url")
        curr_final = result.get("final_url")

        # 恢复
        if prev_status in {STATUS_BROKEN, STATUS_UNREACHABLE, STATUS_RESTRICTED} and curr_status == STATUS_OK:
            alerts.append({
                "type": "FIXED",
                "severity": "info",
                "name": entry["name"],
                "url": url,
                "message": f"链接已恢复可达（上次: {prev_status}）",
            })
            continue

        # 新增失效
        if prev_status in {STATUS_OK, STATUS_REDIRECT} and curr_status in {STATUS_BROKEN, STATUS_UNREACHABLE}:
            alerts.append({
                "type": "NEW_BROKEN",
                "severity": "warning",
                "name": entry["name"],
                "url": url,
                "message": f"链接由 {prev_status} 变为 {curr_status}",
            })
            continue

        # 新增重定向（白名单域名内部通常可忽略）
        if prev_status == STATUS_OK and curr_status == STATUS_REDIRECT:
            if not is_redirect_whitelisted(url, curr_final):
                alerts.append({
                    "type": "NEW_REDIRECT",
                    "severity": "info",
                    "name": entry["name"],
                    "url": url,
                    "message": f"出现新的重定向到 {curr_final}",
                })
            continue

        # 重定向目标变化
        if prev_status == STATUS_REDIRECT and curr_status == STATUS_REDIRECT:
            if prev_final and curr_final and prev_final != curr_final:
                alerts.append({
                    "type": "REDIRECT_CHANGED",
                    "severity": "info",
                    "name": entry["name"],
                    "url": url,
                    "message": f"重定向目标由 {prev_final} 变为 {curr_final}",
                })

    return alerts


def generate_snapshot(entries: list[dict[str, str]], results: list[dict[str, Any]]) -> dict[str, Any]:
    """生成 JSON 状态快照。"""
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "checker_version": "2.0",
        "total": len(entries),
        "items": [
            {
                "name": entry["name"],
                "version": entry["version"],
                "status": entry["status"],
                "url": entry["url"],
                "check_status": result["status"],
                "http_status": result["http_status"],
                "final_url": result.get("final_url"),
                "error": result.get("error"),
            }
            for entry, result in zip(entries, results)
        ],
    }


# ---------------------------------------------------------------------
# 报告生成
# ---------------------------------------------------------------------

def generate_report(
    entries: list[dict],
    results: list[dict],
    alerts: list[dict],
    follow_redirects: bool = False,
) -> str:
    """生成 Markdown 报告。"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    total = len(results)
    counts = {
        STATUS_OK: 0,
        STATUS_REDIRECT: 0,
        STATUS_BROKEN: 0,
        STATUS_UNREACHABLE: 0,
        STATUS_RESTRICTED: 0,
    }
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    lines = [
        "# 标准状态自动复核报告",
        "",
        f"> **生成时间**: {now}",
        f"> **源文件**: `struct/99-reference/standards-index/authoritative-sources-v2.md`",
        f"> **复核方式**: HEAD 请求 best-effort 检测（超时 {TIMEOUT_SECONDS} 秒）",
        f"> **跟随重定向**: {'是' if follow_redirects else '否'}",
        "> **说明**: 本报告仅供参考，不导致 CI 失败。",
        "",
        "## 摘要",
        "",
        f"- 总条目数: {total}",
        f"- {STATUS_OK}: {counts[STATUS_OK]}",
        f"- {STATUS_REDIRECT}: {counts[STATUS_REDIRECT]}",
        f"- {STATUS_BROKEN}: {counts[STATUS_BROKEN]}",
        f"- {STATUS_UNREACHABLE}: {counts[STATUS_UNREACHABLE]}",
        f"- {STATUS_RESTRICTED}: {counts[STATUS_RESTRICTED]}",
        "",
    ]

    if alerts:
        lines.extend([
            "## 趋势告警",
            "",
            "| 类型 | 级别 | 标准/框架 | 说明 |",
            "|------|------|-----------|------|",
        ])
        for alert in alerts:
            lines.append(
                f"| {alert['type']} | {alert['severity']} | {alert['name']} | {alert['message']} |"
            )
        lines.append("")

    lines.extend([
        "## 详细结果",
        "",
        "| 标准/框架 | 版本 | 状态 | 检测结果 | HTTP 状态 | 新位置/错误信息 | 备注 |",
        "|-----------|------|------|----------|-----------|-----------------|------|",
    ])

    for entry, result in zip(entries, results):
        http_status = result.get("http_status")
        http_status_str = str(http_status) if http_status is not None else "—"

        extra = result.get("final_url") or result.get("error") or "—"
        # 避免表格单元格内换行导致格式破坏
        extra = extra.replace("|", "\\|").replace("\n", " ")

        note = entry.get("note", "").replace("|", "\\|").replace("\n", " ")
        name = entry.get("name", "").replace("|", "\\|")

        lines.append(
            f"| {name} | {entry.get('version', '')} | {entry.get('status', '')} | "
            f"{result['status']} | {http_status_str} | {extra} | {note} |"
        )

    lines.extend(
        [
            "",
            "## 图例",
            "",
            f"- **{STATUS_OK}**: HEAD 请求返回 HTTP 2xx。",
            f"- **{STATUS_REDIRECT}**: HEAD 请求返回 HTTP 3xx，通常表示 URL 已变更。",
            f"- **{STATUS_BROKEN}**: HEAD 请求返回 HTTP 4xx/5xx，链接可能失效或需要授权。",
            f"- **{STATUS_UNREACHABLE}**: 请求超时或连接失败，可能是临时网络问题。",
            f"- **{STATUS_RESTRICTED}**: 属于当前环境已知受限域名（如 GitHub），需人工复核。",
            "",
            "## 配置说明",
            "",
            "- 缓存文件：`reports/standard-status-cache.json`",
            "- 快照文件：`reports/standard-status-snapshot.json`",
            "- 使用 `--follow-redirects` 可跟随 3xx 重定向最多 3 层。",
            "- 使用 `--no-cache` 可跳过缓存读取与写入。",
        ]
    )

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------

def main() -> int:
    """脚本入口。"""
    parser = argparse.ArgumentParser(description="标准状态自动复核脚本 v2.0")
    parser.add_argument("--json", action="store_true", help="输出 JSON 快照到控制台")
    parser.add_argument("--follow-redirects", action="store_true", help="跟随 3xx 重定向（最多 3 层）")
    parser.add_argument("--no-cache", action="store_true", help="不使用缓存，也不保存缓存")
    args = parser.parse_args()

    if not SOURCE_FILE.exists():
        print(f"错误：源文件不存在: {SOURCE_FILE}", file=sys.stderr)
        return 0  # 不导致 CI 失败

    text = SOURCE_FILE.read_text(encoding="utf-8")
    entries = parse_entries(text)

    if not entries:
        print("未从源文件中提取到任何带官方 URL 的条目。", file=sys.stderr)
        return 0

    print(f"开始复核 {len(entries)} 个标准条目...")

    results: list[dict] = []
    for idx, entry in enumerate(entries, start=1):
        url = entry["url"]
        print(f"  [{idx}/{len(entries)}] {entry['name']} -> {url}")
        result = check_url(url, follow_redirects=args.follow_redirects)
        results.append(result)

    # 加载/保存缓存与告警
    previous = {} if args.no_cache else load_cache()
    alerts = compute_trend_alerts(entries, results, previous)
    snapshot = generate_snapshot(entries, results)

    if not args.no_cache:
        save_cache(snapshot)

    # 写入快照
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    # 写入报告
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report = generate_report(entries, results, alerts, follow_redirects=args.follow_redirects)
    REPORT_FILE.write_text(report, encoding="utf-8")

    # 控制台摘要
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    print("\n===== 复核摘要 =====")
    print(f"总条目数: {len(entries)}")
    print(f"{STATUS_OK}: {counts.get(STATUS_OK, 0)}")
    print(f"{STATUS_REDIRECT}: {counts.get(STATUS_REDIRECT, 0)}")
    print(f"{STATUS_BROKEN}: {counts.get(STATUS_BROKEN, 0)}")
    print(f"{STATUS_UNREACHABLE}: {counts.get(STATUS_UNREACHABLE, 0)}")
    print(f"{STATUS_RESTRICTED}: {counts.get(STATUS_RESTRICTED, 0)}")
    if alerts:
        print(f"\n趋势告警: {len(alerts)} 条")
        for alert in alerts:
            print(f"  [{alert['severity'].upper()}] {alert['type']}: {alert['name']} — {alert['message']}")
    print(f"\n报告已保存: {REPORT_FILE}")
    print(f"快照已保存: {SNAPSHOT_FILE}")
    if not args.no_cache:
        print(f"缓存已保存: {CACHE_FILE}")

    if args.json:
        print("\n===== JSON 快照 =====")
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
