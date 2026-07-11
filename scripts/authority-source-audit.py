#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
authority-source-audit.py
=========================

只读审计：度量 struct/ 文档“权威来源”段所引用链接的权威性，回答
“100% 对齐网络国际权威内容”在**引用来源质量**维度的达成度。

  - 定位各 Markdown 文件中标题含 “权威来源/权威链接/参考/References/参考资料/来源” 的段落；
  - 提取段内 URL（尖括号 <...> 与裸 URL），按域名分类：
      official  — 国际/国家标准组织与官方治理机构
      academic  — 学术/会议/论文
      vendor    — 厂商官方文档/开源项目官方站点
      secondary — 博客/媒体/个人/聚合（二手）
  - 输出 reports/authority-source-audit.md：全项目占比 + 非 official 链接清单（供人工判断是否替换为一手来源）。

只读、零改动。
"""

import datetime
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STRUCT_DIR = PROJECT_ROOT / "struct"
REPORT_FILE = PROJECT_ROOT / "reports" / "authority-source-audit.md"

OFFICIAL_DOMAINS = {
    "iso.org", "www.iso.org", "iec.ch", "www.iec.ch", "webstore.iec.ch",
    "ieee.org", "standards.ieee.org", "www.ieee.org",
    "nist.gov", "www.nist.gov", "csrc.nist.gov", "nvlpubs.nist.gov", "airc.nist.gov",
    "opengroup.org", "www.opengroup.org", "pubs.opengroup.org",
    "omg.org", "www.omg.org", "www.omgwiki.org",
    "w3.org", "www.w3.org", "ietf.org", "www.ietf.org", "rfc-editor.org",
    "owasp.org", "www.owasp.org", "genai.owasp.org",
    "openssf.org", "www.openssf.org", "baseline.openssf.org",
    "cncf.io", "www.cncf.io", "tag-app-delivery.cncf.io",
    "linuxfoundation.org", "www.linuxfoundation.org",
    "opcfoundation.org", "reference.opcfoundation.org",
    "plcopen.org", "www.plcopen.org",
    "oasis-open.org", "www.oasis-open.org",
    "eclipse.org", "www.eclipse.org", "apache.org", "www.apache.org",
    "iso25000.com", "www.iso25000.com",
    "obamawhitehouse.archives.gov", "archives.gov",
    # 补充：各行业/开源官方治理机构
    "slsa.dev", "www.slsa.dev", "a2a-protocol.org", "www.a2a-protocol.org",
    "industrialdigitaltwin.org", "www.industrialdigitaltwin.org",
    "finops.org", "www.finops.org", "isa.org", "www.isa.org",
    "eur-lex.europa.eu", "cisa.gov", "www.cisa.gov",
    "tmforum.org", "www.tmforum.org", "cyclonedx.org", "www.cyclonedx.org",
    "1.ieee802.org", "bian.org", "www.bian.org",
    "asyncapi.com", "www.asyncapi.com", "component-model.bytecodealliance.org",
    "dodcio.defense.gov", "nsa.nato.int", "cloudevents.io", "www.cloudevents.io",
    "cmmiinstitute.com", "www.cmmiinstitute.com", "alloytools.org", "www.alloytools.org",
    "rocq-prover.org", "www.rocq-prover.org", "coq.inria.fr",
    "greensoftware.foundation", "www.greensoftware.foundation", "sci.greensoftware.foundation",
    "scorecard.dev", "lamport.azurewebsites.net", "kubernetes.io", "www.kubernetes.io",
    "computer.org", "www.computer.org",
    "spdx.org", "www.spdx.org", "openssl.org", "www.openssl.org",
    "incose.org", "www.incose.org", "nasa.gov", "ntrs.nasa.gov", "swehb.nasa.gov",
    "spec.openapis.org", "openapis.org", "knative.dev", "www.knative.dev",
    "gateway-api.sigs.k8s.io", "sigs.k8s.io", "dora.dev", "spdx.dev",
    "platformengineering.org", "www.platformengineering.org", "aaif.io", "www.aaif.io",
    "foundation.tlapl.us", "isa-afp.org", "www.isa-afp.org",
    "digitale-technologien.de", "www.digitale-technologien.de", "spdx.github.io",
}
ACADEMIC_DOMAINS = {
    "arxiv.org", "www.arxiv.org", "dl.acm.org", "ieeexplore.ieee.org",
    "springer.com", "link.springer.com", "sciencedirect.com", "researchgate.net",
    "semanticscholar.org", "dblp.org", "doi.org",
}
VENDOR_HINTS = (
    "docs.", "developer.", "learn.", "github.com", "gitlab.com",
    "microsoft.com", "google.com", "cloud.google.com", "aws.amazon.com",
    "azure.microsoft.com", "redhat.com", "rust-lang.org", "rustlang.org",
    "kotlinlang.org", "go.dev", "python.org", "nodejs.org",
    "backstage.io", "temporal.io", "envoyproxy.io", "istio.io",
    "anthropic.com", "modelcontextprotocol.io",
    "spring.io", "cilium.io", "linkerd.io", "microservices.io", "osv.dev",
    "br-automation.com", "biglever.com", "3ds.com", "github.io",
    "grpc.io", "semver.org", "adacore.com", "camunda.com",
)

AUTH_HEAD = re.compile(r"^#{1,6}\s*.*(权威来源|权威链接|参考资料|参考来源|参考文献|References?|Sources?|参考)\s*$", re.I)
URL_RE = re.compile(r"<(https?://[^>]+)>|(?<!\()(https?://[^\s)<>\"]+)")


def classify(url: str) -> str:
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return "secondary"
    if host in OFFICIAL_DOMAINS:
        return "official"
    if any(host == d or host.endswith("." + d) for d in OFFICIAL_DOMAINS):
        return "official"
    # 政府/官方机构域名后缀
    if host.endswith(".gov") or host.endswith(".gov.uk") or host.endswith(".nato.int") or host.endswith(".defense.gov") or host.endswith(".europa.eu"):
        return "official"
    if host in ACADEMIC_DOMAINS or any(host.endswith("." + d) for d in ACADEMIC_DOMAINS):
        return "academic"
    # 学术机构域名后缀（.edu / .ac.xx / 大学子域）
    if host.endswith(".edu") or ".ac." in host or host.endswith(".ac.uk") or host.endswith(".ethz.ch") or host.endswith(".mpi-sws.org"):
        return "academic"
    if any(h in host for h in VENDOR_HINTS):
        return "vendor"
    return "secondary"


def extract_authority_urls(text: str) -> list:
    """提取“权威来源/参考”段内的 URL（段：标题到下一同级/更高级标题间）。"""
    urls = []
    lines = text.splitlines()
    in_sec = False
    for i, line in enumerate(lines):
        if AUTH_HEAD.match(line):
            in_sec = True
            continue
        if in_sec and re.match(r"^#{1,6}\s+", line):
            in_sec = False
        if in_sec:
            for m in URL_RE.finditer(line):
                u = m.group(1) or m.group(2)
                if u:
                    urls.append(u.rstrip(".,;"))
    return urls


def main() -> int:
    total = Counter()
    non_official = []  # (cls, url, file)
    files_with_sec = 0
    for md in sorted(STRUCT_DIR.rglob("*.md")):
        if "_ARCHIVE" in md.parts or "_HISTORICAL" in md.parts:
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        urls = extract_authority_urls(text)
        if not urls:
            continue
        files_with_sec += 1
        rel = md.relative_to(PROJECT_ROOT).as_posix()
        for u in urls:
            cls = classify(u)
            total[cls] += 1
            if cls != "official":
                non_official.append((cls, u, rel))

    grand = sum(total.values()) or 1
    lines = [
        "# 权威来源质量审计（只读）",
        "",
        f"> 生成时间: {datetime.datetime.now().isoformat(timespec='seconds')}",
        "> 范围: struct/ 各文档 “权威来源/参考” 段 URL",
        "> 目标: 度量“对齐网络国际权威内容”在引用来源质量维度的达成度；非 official 链接供人工判断是否替换为一手来源。",
        "",
        "## 摘要",
        "",
        f"- 含权威来源段的文件: **{files_with_sec}**",
        f"- 权威段 URL 总计: **{sum(total.values())}**",
        "",
        "| 类别 | 数量 | 占比 |",
        "|------|------|------|",
    ]
    for cls in ("official", "academic", "vendor", "secondary"):
        c = total.get(cls, 0)
        lines.append(f"| {cls} | {c} | {c*100/grand:.1f}% |")
    off = total.get("official", 0)
    lines += ["", f"**官方一手来源占比: {off*100/grand:.1f}%**", ""]
    lines += ["## 非官方链接清单（待人工复核是否可替换为一手）", ""]
    if not non_official:
        lines.append("全部权威段链接均为官方一手来源。")
    else:
        lines.append("| 类别 | URL | 文件 |")
        lines.append("|------|-----|------|")
        for cls, u, rel in non_official[:200]:
            lines.append(f"| {cls} | {u} | {rel} |")
        if len(non_official) > 200:
            lines.append(f"| … | 另有 {len(non_official)-200} 条省略 | |")
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"权威段 URL: {sum(total.values())}（文件 {files_with_sec}）")
    for cls in ("official", "academic", "vendor", "secondary"):
        print(f"  {cls}: {total.get(cls, 0)} ({total.get(cls, 0)*100/grand:.1f}%)")
    print(f"官方一手占比: {off*100/grand:.1f}%")
    print(f"报告: {REPORT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
