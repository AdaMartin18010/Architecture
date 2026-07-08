#!/usr/bin/env python3
"""
standard-tracker.py
===================

标准跟踪监控脚本。

功能：
- 监控 10+ 项国际标准/行业框架的官方状态页和 RSS/Atom feed
- 对状态页发起 HEAD 请求，检测链接健康度
- 解析 RSS/Atom feed，列出最新条目（用于发现新版本/征求意见稿）
- 输出 Markdown 报告或 JSON 状态快照
- 与 standards-version-audit.py 联动生成季度综合报告

用法：
    python standard-tracker.py --check-all
    python standard-tracker.py --standard iso-42042
    python standard-tracker.py --generate-report
    python standard-tracker.py --quarterly-report
    python standard-tracker.py --snapshot
    python standard-tracker.py --rss-feed mcp --limit 5

"""

import argparse
import json
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# 监控配置 — 权威来源列表
# ---------------------------------------------------------------------------
STANDARDS: Dict[str, Dict] = {
    "iso-42042": {
        "name": "ISO/IEC/IEEE DIS 42042 — Reference Architectures",
        "status_url": "https://www.iso.org/standard/87310.html",
        "rss_url": None,
        "mailing_list": None,
        "current_status": "DIS (Stage 40.60) — enquiry 已于 2026-01-30 结束",
        "last_checked": "2026-06-10",
        "expected_release": "2026–2027",
        "action_on_release": "更新 01-meta-model-standards/01-iso-420xx-family/iso-42024-42042-dis-alignment.md",
    },
    "iso-42024": {
        "name": "ISO/IEC/IEEE DIS 42024 — Architecture Fundamentals",
        "status_url": "https://www.iso.org/standard/87510.html",
        "rss_url": None,
        "mailing_list": None,
        "current_status": "DIS (Stage 40.60) — enquiry 已于 2026-01-12 结束",
        "last_checked": "2026-06-10",
        "expected_release": "2026–2027",
        "action_on_release": "更新 01-meta-model-standards/01-iso-420xx-family/iso-42024-42042-dis-alignment.md",
    },
    "slsa": {
        "name": "SLSA (Supply-chain Levels for Software Artifacts)",
        "status_url": "https://slsa.dev/spec/v1.2/",
        "rss_url": "https://slsa.dev/blog/feed.xml",
        "mailing_list": "slsa-discussion@googlegroups.com",
        "current_status": "v1.2 已发布 (Multi-Track: Build/Source/Build Environment)",
        "last_checked": "2026-06-10",
        "expected_release": "v1.3 / Build L4 正式发布",
        "action_on_release": "更新 10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md",
    },
    "mcp": {
        "name": "Model Context Protocol (MCP)",
        "status_url": "https://modelcontextprotocol.io/specification/2025-11-25",
        "rss_url": "https://github.com/modelcontextprotocol/specification/releases.atom",
        "mailing_list": "https://github.com/modelcontextprotocol/specification/discussions",
        "current_status": "2025-11-25 稳定版 (Linux Foundation Agentic AI Foundation)；2026-07-28 新版 RC 预期",
        "last_checked": "2026-07-08",
        "expected_release": "2026-07-28 RC / 2026 下半年正式版",
        "action_on_release": "更新 12-ai-native-reuse/01-mcp-protocol/",
    },
    "a2a": {
        "name": "Agent-to-Agent Protocol (A2A)",
        "status_url": "https://a2aprotocol.io/",
        "rss_url": "https://github.com/a2a-protocol/documentation/releases.atom",
        "mailing_list": "https://github.com/a2a-protocol/documentation/discussions",
        "current_status": "v1.0.0 已发布（2026-03-12）",
        "last_checked": "2026-06-12",
        "expected_release": "v1.1/v2.0 规划待官方公布",
        "action_on_release": "更新 12-ai-native-reuse/02-a2a-protocol/",
    },
    "wasi": {
        "name": "WASI (WebAssembly System Interface)",
        "status_url": "https://wasi.dev/",
        "rss_url": "https://bytecodealliance.org/articles/feed.xml",
        "mailing_list": "https://groups.google.com/g/web-assembly",
        "current_status": "WASI 0.3 preview（Wasmtime 37+），WASI 1.0 目标 2026 末/2027 初",
        "last_checked": "2026-06-10",
        "expected_release": "WASI 1.0 稳定版",
        "action_on_release": "更新 13-emerging-trends/03-webassembly-components/wasm-wasi-03-boundaries.md",
    },
    "iso-25010": {
        "name": "ISO/IEC 25010:2023 — SQuaRE Quality Models",
        "status_url": "https://www.iso.org/standard/78175.html",
        "rss_url": None,
        "mailing_list": None,
        "current_status": "2023-11-15 已发布（取代 2011 版，新增 AI/ML 质量考量）；不存在 2024 版",
        "last_checked": "2026-06-12",
        "expected_release": "已稳定",
        "action_on_release": "N/A — 已是最新版",
    },
    "iso-26566": {
        "name": "ISO/IEC 26566:2026 — Methods and tools for product line texture",
        "status_url": "https://www.iso.org/standard/81437.html",
        "rss_url": None,
        "mailing_list": None,
        "current_status": "2026-05 正式发布",
        "last_checked": "2026-06-10",
        "expected_release": "已稳定",
        "action_on_release": "N/A — 已是最新版",
    },
    "archimate": {
        "name": "ArchiMate Specification",
        "status_url": "https://www.opengroup.org/archimate-licensed-downloads",
        "rss_url": "https://www.opengroup.org/press-releases/feed",
        "mailing_list": "https://www.opengroup.org/archimate-forum",
        "current_status": "ArchiMate 4 Specification 已于 2026-04-27 正式发布（Document C260），与 3.2 向后兼容",
        "last_checked": "2026-06-12",
        "expected_release": "已稳定",
        "action_on_release": "N/A — 已更新为正式发布状态",
    },
    "cncf-platform": {
        "name": "CNCF Platform Engineering Maturity Model",
        "status_url": "https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/",
        "rss_url": None,
        "mailing_list": "https://github.com/cncf/tag-app-delivery/discussions",
        "current_status": "五维度模型 (Investment/Adoption/Interfaces/Operations/Measurement)",
        "last_checked": "2026-06-12",
        "expected_release": "持续演进",
        "action_on_release": "更新 13-emerging-trends/01-platform-engineering/platform-maturity-model.md",
    },
    "iso-12207": {
        "name": "ISO/IEC/IEEE 12207:2026 — Software Life Cycle Processes",
        "status_url": "https://www.iso.org/standard/90219.html",
        "rss_url": None,
        "mailing_list": None,
        "current_status": "2026-04-29 已发布，取代 2017 版",
        "last_checked": "2026-06-12",
        "expected_release": "已稳定",
        "action_on_release": "N/A — 已更新为 2026 版",
    },
    "nist-ssdf-1-2": {
        "name": "NIST SP 800-218 Rev.1 / SSDF v1.2",
        "status_url": "https://csrc.nist.gov/publications/detail/sp/800-218r1/draft",
        "rss_url": "https://csrc.nist.gov/news/feed",
        "mailing_list": "https://csrc.nist.gov/Contact-Us",
        "current_status": "Initial Public Draft（征求意见稿，2025-12-17 发布），非最终版；最终版预计 2026-Q3",
        "last_checked": "2026-07-08",
        "expected_release": "2026-Q3 最终版",
        "action_on_release": "更新 10-supply-chain-security/06-case-studies/nist-ssdf-1-2-alignment.md",
    },
    "iec-61508-ed3": {
        "name": "IEC 61508 Ed.3 — Functional Safety of E/E/PE Systems",
        "status_url": "https://webstore.iec.ch/searchform&q=61508",
        "rss_url": None,
        "mailing_list": None,
        "current_status": "CDV 已完成，预计 2026 末–2027 初发布",
        "last_checked": "2026-07-08",
        "expected_release": "2026 末–2027 初",
        "action_on_release": "创建 11-industrial-iot-otit/06-functional-safety/iec-61508-ed3-transition-guide.md",
    },
    "iso-26262-ed3": {
        "name": "ISO 26262 Ed.3 — Road Vehicles Functional Safety",
        "status_url": "https://www.iso.org/standard/",
        "rss_url": None,
        "mailing_list": None,
        "current_status": "新工作项已注册（2026 初），目标 ~2029",
        "last_checked": "2026-07-08",
        "expected_release": "~2029",
        "action_on_release": "跟踪并在 11-industrial-iot-otit/06-functional-safety/ 更新路线图",
    },
}

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def http_get(url: str, timeout: int = 10) -> bytes:
    """对 URL 发起 GET 请求并返回响应体。"""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Architecture-Reuse-Tracker/2.0 (Standard Tracker Bot)",
            "Accept": "application/rss+xml,application/atom+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def check_url(url: str, timeout: int = 10) -> Dict:
    """检查 URL 可达性，返回状态信息。"""
    try:
        req = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "Architecture-Reuse-Tracker/2.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {
                "reachable": True,
                "status_code": resp.status,
                "final_url": resp.geturl(),
                "content_type": resp.headers.get("Content-Type", "unknown"),
            }
    except urllib.error.HTTPError as e:
        return {
            "reachable": False,
            "status_code": e.code,
            "error": str(e.reason),
        }
    except Exception as e:
        return {"reachable": False, "status_code": None, "error": str(e)}


def parse_rss_or_atom(xml_bytes: bytes, limit: int = 5) -> List[Dict[str, str]]:
    """用标准库解析 RSS/Atom feed，返回最近 limit 条条目。"""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        return [{"title": f"[解析失败: {e}]", "link": "", "published": ""}]

    # 移除命名空间前缀，简化元素匹配
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items: List[ET.Element] = []

    if root.tag == "rss" or root.tag.endswith("rss"):
        channel = root.find("channel")
        if channel is not None:
            items = channel.findall("item")[:limit]
        entries = []
        for item in items:
            title = item.findtext("title", default="").strip()
            link = item.findtext("link", default="").strip()
            pub_date = item.findtext("pubDate", default="").strip()
            entries.append({"title": title, "link": link, "published": pub_date})
        return entries

    if root.tag == "{%s}feed" % ns["atom"] or root.tag == "feed":
        atom_items = root.findall("{%s}entry" % ns["atom"])[:limit]
        entries = []
        for entry in atom_items:
            title = entry.findtext("{%s}title" % ns["atom"], default="").strip()
            link_el = entry.find("{%s}link" % ns["atom"])
            link = link_el.get("href", "").strip() if link_el is not None else ""
            pub = (
                entry.findtext("{%s}updated" % ns["atom"], default="").strip()
                or entry.findtext("{%s}published" % ns["atom"], default="").strip()
            )
            entries.append({"title": title, "link": link, "published": pub})
        return entries

    return [{"title": "[未知 feed 格式]", "link": "", "published": ""}]


def fetch_feed(url: str, limit: int = 5) -> List[Dict[str, str]]:
    """获取并解析 feed。"""
    try:
        xml_bytes = http_get(url, timeout=15)
        return parse_rss_or_atom(xml_bytes, limit=limit)
    except Exception as e:
        return [{"title": f"[获取失败: {e}]", "link": url, "published": ""}]


# ---------------------------------------------------------------------------
# 主监控逻辑
# ---------------------------------------------------------------------------

def check_all() -> List[Dict]:
    """检查所有监控标准的链接健康状态。"""
    results = []
    for key, info in STANDARDS.items():
        result = {
            "key": key,
            "name": info["name"],
            "status_url_check": check_url(info["status_url"]),
            "current_status": info["current_status"],
            "last_checked": datetime.now(timezone.utc).isoformat(),
            "expected_release": info["expected_release"],
            "action_on_release": info["action_on_release"],
            "mailing_list": info.get("mailing_list"),
        }
        if info["rss_url"]:
            result["rss_url_check"] = check_url(info["rss_url"])
        results.append(result)
    return results


def generate_report(results: List[Dict]) -> str:
    """生成 Markdown 格式的监控报告。"""
    lines = [
        "# 标准跟踪监控报告",
        f"> 生成时间: {datetime.now(timezone.utc).isoformat()}",
        f"> 监控范围: {len(STANDARDS)} 项国际标准/行业框架",
        "",
        "| 标准 | 链接状态 | 当前状态 | 预期发布 | 建议行动 |",
        "|------|----------|----------|----------|----------|",
    ]
    for r in results:
        url_ok = "✅ 可达" if r["status_url_check"]["reachable"] else "❌ 不可达"
        lines.append(
            f"| {r['name']} | {url_ok} | {r['current_status']} | {r['expected_release']} | {r['action_on_release']} |"
        )
    lines.extend([
        "",
        "## 监控频率建议",
        "",
        "- **ISO 标准**: 每月检查 `iso.org` 状态页",
        "- **MCP / SLSA / WASI / A2A**: 每周检查 GitHub releases / 官方博客",
        "- **ArchiMate / TOGAF**: 每季度检查 The Open Group 新闻发布",
        "- **CNCF 框架**: 每半年检查成熟度模型更新",
        "- **NIST / IEC**: 每月检查官方新闻 feed 与征求意见稿状态",
        "",
        "---",
        "> 本报告由 `99-reference/tools/standard-tracker.py` 自动生成",
    ])
    return "\n".join(lines)


def generate_snapshot(results: List[Dict]) -> Dict:
    """生成结构化的 JSON 状态快照。"""
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tracker_version": "2.0",
        "total_standards": len(STANDARDS),
        "summary": {
            "reachable": sum(1 for r in results if r["status_url_check"]["reachable"]),
            "unreachable": sum(1 for r in results if not r["status_url_check"]["reachable"]),
        },
        "standards": results,
    }


def save_snapshot(snapshot: Dict, path: Optional[Path] = None) -> Path:
    """保存 JSON 状态快照到文件。"""
    if path is None:
        path = Path(__file__).resolve().parent / "standard-tracker-snapshot.json"
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def run_version_audit() -> str:
    """调用 standards-version-audit.py 获取项目内版本一致性报告。"""
    audit_script = Path(__file__).resolve().parent / "standards-version-audit.py"
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    try:
        result = subprocess.run(
            [sys.executable, str(audit_script), str(project_root)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"[ERROR] 运行 standards-version-audit.py 失败: {e}"


def generate_quarterly_report(results: List[Dict]) -> str:
    """生成季度综合报告：外部标准跟踪 + 内部版本一致性审计。"""
    lines = [
        "# 季度标准跟踪与一致性报告",
        f"> 生成时间: {datetime.now(timezone.utc).isoformat()}",
        "> 范围: 外部标准权威来源 + 项目内部引用一致性",
        "",
        "## 1. 外部标准跟踪",
        "",
        "| 标准 | 链接状态 | 当前状态 | 预期发布 | 建议行动 |",
        "|------|----------|----------|----------|----------|",
    ]
    for r in results:
        url_ok = "✅ 可达" if r["status_url_check"]["reachable"] else "❌ 不可达"
        lines.append(
            f"| {r['name']} | {url_ok} | {r['current_status']} | {r['expected_release']} | {r['action_on_release']} |"
        )
    lines.extend([
        "",
        "## 2. 项目内部标准版本一致性审计",
        "",
        "```text",
    ])
    audit_output = run_version_audit()
    lines.append(audit_output)
    lines.extend([
        "```",
        "",
        "## 3. 下季度重点跟踪项",
        "",
        "1. MCP 2026-07-28 RC / 2026 下半年正式版是否按期发布",
        "2. NIST SSDF 1.2 IPD 反馈期后是否进入正式版",
        "3. IEC 61508 Ed.3 / ISO 26262 Ed.3 进展",
        "4. ISO/IEC/IEEE DIS 42024 / DIS 42042 投票结果与最终发布时间",
        "5. WASI 1.0 发布计划更新",
        "6. A2A v1.1/v2.0 官方路线图",
        "",
        "---",
        "> 本报告由 `99-reference/tools/standard-tracker.py --quarterly-report` 自动生成",
    ])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="标准跟踪监控脚本 v2.0")
    parser.add_argument("--check-all", action="store_true", help="检查所有标准链接健康状态")
    parser.add_argument("--standard", type=str, help="检查指定标准 (如 iso-42042)")
    parser.add_argument("--generate-report", action="store_true", help="生成 Markdown 监控报告")
    parser.add_argument("--quarterly-report", action="store_true", help="生成季度综合报告（外部跟踪 + 内部审计）")
    parser.add_argument("--snapshot", action="store_true", help="生成 JSON 状态快照")
    parser.add_argument("--rss-feed", type=str, help="解析指定标准的 RSS/Atom feed (如 mcp, slsa)")
    parser.add_argument("--limit", type=int, default=5, help="feed 条目数量上限 (默认 5)")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    args = parser.parse_args()

    if args.check_all:
        results = check_all()
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                print(f"[{r['key']}] {r['name']}")
                print(f"  链接: {'✅' if r['status_url_check']['reachable'] else '❌'}")
                print(f"  状态: {r['current_status']}")
                print(f"  预期: {r['expected_release']}")
                print(f"  行动: {r['action_on_release']}")
                print()
        return 0

    if args.standard:
        if args.standard not in STANDARDS:
            print(f"未知标准: {args.standard}")
            print(f"支持的标准: {', '.join(STANDARDS.keys())}")
            return 1
        info = STANDARDS[args.standard]
        print(f"标准: {info['name']}")
        print(f"状态页: {info['status_url']}")
        print(f"当前状态: {info['current_status']}")
        print(f"预期发布: {info['expected_release']}")
        print(f"发布后的行动: {info['action_on_release']}")
        if info["mailing_list"]:
            print(f"讨论列表: {info['mailing_list']}")
        url_check = check_url(info['status_url'])
        print(f"链接检查: {'✅ 可达' if url_check['reachable'] else '❌ 不可达'}")
        return 0

    if args.generate_report:
        results = check_all()
        report = generate_report(results)
        report_path = Path(__file__).resolve().parent / "standard-tracker-report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"报告已生成: {report_path}")
        return 0

    if args.quarterly_report:
        results = check_all()
        report = generate_quarterly_report(results)
        report_path = Path(__file__).resolve().parent / "standard-tracker-quarterly-report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"季度报告已生成: {report_path}")
        return 0

    if args.snapshot:
        results = check_all()
        snapshot = generate_snapshot(results)
        snapshot_path = save_snapshot(snapshot)
        if args.json:
            print(json.dumps(snapshot, ensure_ascii=False, indent=2))
        print(f"状态快照已保存: {snapshot_path}")
        return 0

    if args.rss_feed:
        if args.rss_feed not in STANDARDS:
            print(f"未知标准: {args.rss_feed}")
            print(f"支持的标准: {', '.join(STANDARDS.keys())}")
            return 1
        info = STANDARDS[args.rss_feed]
        if not info["rss_url"]:
            print(f"[{args.rss_feed}] 暂无 RSS/Atom feed")
            return 0
        print(f"[{args.rss_feed}] {info['name']}")
        print(f"Feed: {info['rss_url']}")
        entries = fetch_feed(info["rss_url"], limit=args.limit)
        for idx, entry in enumerate(entries, start=1):
            print(f"\n  {idx}. {entry['title']}")
            if entry["published"]:
                print(f"     日期: {entry['published']}")
            if entry["link"]:
                print(f"     链接: {entry['link']}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
