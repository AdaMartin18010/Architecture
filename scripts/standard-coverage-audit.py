#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
standard-coverage-audit.py
==========================

只读审计：对比“权威基准表 authoritative-sources-v2.md（85 条）”与
“struct 正文实际引用的标准（KG Standard 实体）”，输出覆盖差集：

  - v2_only  : v2 表列出但 struct 正文 0 引用（候选：冗余/待补充引用）
  - kg_only  : struct 正文引用但 v2 表未列（候选：权威基准表覆盖缺口，需人工判断是否补入 v2）

只读、零改动；为“100% 对齐权威来源覆盖度”提供度量与待办清单。
"""

import datetime
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KG_ENTITIES = PROJECT_ROOT / "struct" / "99-reference" / "knowledge-graph" / "kg-entities.jsonl"
V2_FILE = PROJECT_ROOT / "struct" / "99-reference" / "standards-index" / "authoritative-sources-v2.md"
REPORT_FILE = PROJECT_ROOT / "reports" / "standard-coverage-audit.md"


def norm(name: str) -> str:
    """归一化标准名用于比较：去版本/组织前缀差异、小写、去多余空白。"""
    s = name.replace("**", "").replace("`", "")
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("iso/iec/ieee ", "").replace("iso/iec ", "").replace("iec ", "").replace("iso ", "")
    s = s.replace("nist ", "").replace("owasp ", "")
    s = re.sub(r"[:\s]\d{4}$", "", s)       # 去尾部年份
    s = re.sub(r"\s+v?\d+(\.\d+)*$", "", s)  # 去尾部版本号
    return s.strip()


def load_kg_standards() -> dict:
    out = {}
    with KG_ENTITIES.open(encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            o = json.loads(ln)
            if o.get("type") == "Standard":
                out.setdefault(norm(o["name"]), o["name"])
    return out


def load_v2_standards() -> dict:
    out = {}
    text = V2_FILE.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        name = cells[0]
        if not name or name.lower() in ("标准/框架", "标准", "----------") or set(name) <= set("-: "):
            continue
        out.setdefault(norm(name), name)
    return out


def main() -> int:
    kg = load_kg_standards()
    v2 = load_v2_standards()
    kg_keys, v2_keys = set(kg), set(v2)
    v2_only = sorted(v2_keys - kg_keys)
    kg_only = sorted(kg_keys - v2_keys)
    both = sorted(kg_keys & v2_keys)

    lines = [
        "# 标准覆盖度审计（v2 权威表 × struct 引用，只读）",
        "",
        f"> 生成时间: {datetime.datetime.now().isoformat(timespec='seconds')}",
        "> v2 表: struct/99-reference/standards-index/authoritative-sources-v2.md",
        "> struct 引用: KG Standard 实体（canonical 归一后）",
        "> 说明: 按归一化标准名比较（忽略组织前缀/年份/版本大小写）；差集为候选，需人工判断。",
        "",
        "## 摘要",
        "",
        f"- v2 权威表标准数（归一）: **{len(v2_keys)}**",
        f"- struct 引用标准数（KG Standard，归一）: **{len(kg_keys)}**",
        f"- 二者交集: **{len(both)}**",
        f"- v2 有但 struct 0 引用（v2_only）: **{len(v2_only)}**",
        f"- struct 引用但 v2 未列（kg_only，权威表覆盖缺口候选）: **{len(kg_only)}**",
        "",
        "## kg_only：struct 引用但 v2 权威表未列（候选补入 v2）",
        "",
    ]
    if not kg_only:
        lines.append("无：struct 引用的标准均已在 v2 权威表覆盖。")
    else:
        lines.append("| 归一名 | KG 实体名 |")
        lines.append("|--------|-----------|")
        for k in kg_only:
            lines.append(f"| {k} | {kg[k]} |")
    lines += ["", "## v2_only：v2 表列出但 struct 正文 0 引用（候选补充引用/或冗余）", ""]
    if not v2_only:
        lines.append("无：v2 权威表标准均被 struct 引用。")
    else:
        lines.append("| 归一名 | v2 表名 |")
        lines.append("|--------|---------|")
        for k in v2_only:
            lines.append(f"| {k} | {v2[k]} |")
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"v2={len(v2_keys)} KG={len(kg_keys)} 交集={len(both)}")
    print(f"kg_only（权威表缺口候选）: {len(kg_only)}")
    print(f"v2_only（v2 冗余/待引用）: {len(v2_only)}")
    print(f"报告: {REPORT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
