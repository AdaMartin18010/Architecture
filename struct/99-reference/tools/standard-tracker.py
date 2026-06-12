#!/usr/bin/env python3
"""
标准跟踪监控脚本
按 SUBSEQUENT_PLAN_2026.md 决策 5 建立自动化 RSS 监控机制

用法:
    python standard-tracker.py --check-all
    python standard-tracker.py --standard iso-42042
    python standard-tracker.py --generate-report
"""

import argparse
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

# ---------------------------------------------------------------------------
# 监控配置 — 权威来源列表
# ---------------------------------------------------------------------------
STANDARDS: Dict[str, Dict] = {
    "iso-42042": {
        "name": "ISO/IEC/IEEE DIS 42042 — Reference Architectures",
        "status_url": "https://www.iso.org/standard/87310.html",
        "rss_url": None,
        "current_status": "DIS (Stage 40.60) — 征询阶段",
        "last_checked": "2026-06-10",
        "expected_release": "2026-2027",
        "action_on_release": "更新 01-meta-model-standards/01-iso-420xx-family/iso-42024-42042-dis-alignment.md",
    },
    "slsa": {
        "name": "SLSA (Supply-chain Levels for Software Artifacts)",
        "status_url": "https://slsa.dev/spec/v1.2/",
        "rss_url": "https://slsa.dev/blog/feed.xml",
        "current_status": "v1.2 已发布 (Multi-Track: Build/Source/Build Environment)",
        "last_checked": "2026-06-10",
        "expected_release": "v1.3 / Build L4 正式发布",
        "action_on_release": "更新 10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md",
    },
    "mcp": {
        "name": "Model Context Protocol (MCP)",
        "status_url": "https://modelcontextprotocol.io/specification/2025-11-25",
        "rss_url": "https://github.com/modelcontextprotocol/specification/releases.atom",
        "current_status": "2025-11-25 稳定版 (Linux Foundation Agentic AI Foundation)",
        "last_checked": "2026-06-10",
        "expected_release": "2026 下半年新版本",
        "action_on_release": "更新 12-ai-native-reuse/01-mcp-protocol/",
    },
    "wasi": {
        "name": "WASI (WebAssembly System Interface)",
        "status_url": "https://wasi.dev/roadmap",
        "rss_url": "https://bytecodealliance.org/articles/feed.xml",
        "current_status": "WASI 0.3 preview (Wasmtime 37+)，WASI 1.0 目标 2026末/2027初",
        "last_checked": "2026-06-10",
        "expected_release": "WASI 1.0 稳定版",
        "action_on_release": "更新 13-emerging-trends/03-webassembly-components/wasm-wasi-03-boundaries.md",
    },
    "iso-25010": {
        "name": "ISO/IEC 25010:2023 — SQuaRE Quality Models",
        "status_url": "https://www.iso.org/standard/78175.html",
        "rss_url": None,
        "current_status": "2023-11-15 已发布（取代 2011 版，新增 AI/ML 质量考量）；不存在 2024 版",
        "last_checked": "2026-06-12",
        "expected_release": "已稳定",
        "action_on_release": "N/A — 已是最新版",
    },
    "iso-26566": {
        "name": "ISO/IEC 26566:2026 — Reuse Maturity",
        "status_url": "https://www.iso.org/standard/81437.html",
        "rss_url": None,
        "current_status": "2026-05 正式发布",
        "last_checked": "2026-06-10",
        "expected_release": "已稳定",
        "action_on_release": "N/A — 已是最新版",
    },
    "archimate": {
        "name": "ArchiMate Specification",
        "status_url": "https://www.opengroup.org/archimate-forum",
        "rss_url": "https://www.opengroup.org/press-releases/feed",
        "current_status": "ArchiMate 4 Specification 已于 2026-04-27 正式发布（Document C260），与 3.2 向后兼容",
        "last_checked": "2026-06-12",
        "expected_release": "已稳定",
        "action_on_release": "N/A — 已更新为正式发布状态",
    },
    "cncf-platform": {
        "name": "CNCF Platform Engineering Maturity Model",
        "status_url": "https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/",
        "rss_url": None,
        "current_status": "五维度模型 (Investment/Adoption/Interfaces/Operations/Measurement)",
        "last_checked": "2026-06-12",
        "expected_release": "持续演进",
        "action_on_release": "更新 13-emerging-trends/01-platform-engineering/platform-maturity-model.md",
    },
    "iso-12207": {
        "name": "ISO/IEC/IEEE 12207:2026 — Software Life Cycle Processes",
        "status_url": "https://www.iso.org/standard/90219.html",
        "rss_url": None,
        "current_status": "2026-04-29 已发布，取代 2017 版",
        "last_checked": "2026-06-12",
        "expected_release": "已稳定",
        "action_on_release": "N/A — 已更新为 2026 版",
    },
    "nist-ssdf-1-2": {
        "name": "NIST SP 800-218 Rev.1 / SSDF v1.2",
        "status_url": "https://csrc.nist.gov/News/2025/draft-ssdf-version-1-2",
        "rss_url": "https://csrc.nist.gov/news/feed",
        "current_status": "Initial Public Draft（征求意见稿，2025-12-17 发布），非最终版",
        "last_checked": "2026-06-12",
        "expected_release": "最终版发布时间待定",
        "action_on_release": "更新 10-supply-chain-security/06-case-studies/nist-ssdf-1-2-alignment.md",
    },
}

# ---------------------------------------------------------------------------
# 监控逻辑
# ---------------------------------------------------------------------------


def check_url(url: str, timeout: int = 10) -> Dict:
    """检查 URL 可达性，返回状态信息。"""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Architecture-Reuse-Tracker/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {
                "reachable": True,
                "status_code": resp.status,
                "content_type": resp.headers.get("Content-Type", "unknown"),
            }
    except Exception as e:
        return {"reachable": False, "error": str(e)}


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
            "action_on_release": info["action_on_release"],
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
        "> 监控范围: 10 项国际标准/行业框架",
        "",
        "| 标准 | 链接状态 | 当前状态 | 建议行动 |",
        "|------|----------|----------|----------|",
    ]
    for r in results:
        url_ok = "✅ 可达" if r["status_url_check"]["reachable"] else "❌ 不可达"
        lines.append(
            f"| {r['name']} | {url_ok} | {r['current_status']} | {r['action_on_release']} |"
        )
    lines.extend([
        "",
        "## 监控频率建议",
        "",
        "- **ISO 标准**: 每月检查 `iso.org` 状态页",
        "- **MCP / SLSA / WASI**: 每周检查 GitHub releases / 官方博客",
        "- **ArchiMate / TOGAF**: 每季度检查 The Open Group 新闻发布",
        "- **CNCF 框架**: 每半年检查成熟度模型更新",
        "",
        "---",
        "> 本报告由 `99-reference/tools/standard-tracker.py` 自动生成",
    ])
    return "\n".join(lines)


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
        "| 标准 | 链接状态 | 当前状态 | 建议行动 |",
        "|------|----------|----------|----------|",
    ]
    for r in results:
        url_ok = "✅ 可达" if r["status_url_check"]["reachable"] else "❌ 不可达"
        lines.append(
            f"| {r['name']} | {url_ok} | {r['current_status']} | {r['action_on_release']} |"
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
        "1. MCP 2026-07-28 RC 是否按期发布",
        "2. NIST SSDF 1.2 IPD 反馈期后是否进入正式版",
        "3. IEC 61508 Ed.3 / ISO 26262 Ed.3 进展",
        "4. ISO/IEC/IEEE DIS 42024 / DIS 42042 投票结果",
        "5. WASI 1.0 发布计划更新",
        "",
        "---",
        "> 本报告由 `99-reference/tools/standard-tracker.py --quarterly-report` 自动生成",
    ])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="标准跟踪监控脚本")
    parser.add_argument("--check-all", action="store_true", help="检查所有标准链接健康状态")
    parser.add_argument("--standard", type=str, help="检查指定标准 (如 iso-42042)")
    parser.add_argument("--generate-report", action="store_true", help="生成 Markdown 监控报告")
    parser.add_argument("--quarterly-report", action="store_true", help="生成季度综合报告（外部跟踪 + 内部审计）")
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

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
