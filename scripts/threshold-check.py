#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阈值一致性检查脚本（Threshold Registry Gate）

检查内容：
1. 结构校验：threshold-registry.yaml 每个条目必须含 id/name/value/operator/sources，
   operator ∈ {>, >=, <, <=, ==}，value 可解析为数值，id 不重复。
2. 数值一致性：对 registry 中每个阈值，在 struct/ 全量扫描其名称/别名，
   将别名附近（±80 字符窗口）出现的数值与注册值比对。

判定分级（宁可漏报，控制误报）：
- 高置信度绑定（影响退出码）：别名与数值在同一行、间距 <= 40 字符、中间无句末标点，
  且满足以下任一：
    a) 别名本身含阈值语义（如 AAF_ECONOMIC_FLOOR / pass_threshold），或
       别名与数值之间存在阈值语义线索词（阈值/下限/上限/默认/取/为/是/须/应/不低于/至少/floor/threshold）；
    b) 别名为"特异别名"（长度 >= 4，如 语义覆盖率/技术栈兼容性/置信度 γ），
       且别名与数值之间存在比较算子（= < > ≥ ≤）。
  绑定数值 ≠ 注册值且不在合法取值集内 → 高置信度不一致。
- 模糊命中（不影响退出码）：数值落在 ±80 字符窗口内但不满足高置信度绑定条件，
  列入报告"待人工复核"节。

合法取值集 = {value} ∪ allow_values ∪ {downgrade_value} ∪ canonical_range 端点 ∪ weights 值。
百分数归一化：注册值 <= 2 时，文档中 "80%" 按 0.8 比对。

豁免机制：
1. 路径含 _ARCHIVE / _HISTORICAL_ / CHANGELOG / audit 的文件整体跳过；
2. 命中行 ±10 行内含反例/历史/演进/deprecated/草案等关键词（参考 cross-index-check.py）→ 豁免；
3. registry 条目 allow_values / downgrade_value / canonical_range / weights 声明的取值合法；
4. threshold-registry.yaml 自身与 unified-reuse-decision-model.md 为引用方，跳过数值比对。

退出码：结构错误或非豁免的高置信度不一致 → 1，否则 → 0。
报告输出：reports/threshold-check.md

用法：
    python scripts/threshold-check.py
    python scripts/threshold-check.py --registry struct/99-reference/tools/threshold-registry.yaml --root struct
"""

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml

VALID_OPERATORS = {">", ">=", "<", "<=", "=="}
SCAN_EXTENSIONS = {".md", ".py", ".json", ".yaml", ".yml", ".als"}
EXEMPT_PATH_MARKERS = ("_ARCHIVE", "_HISTORICAL_", "CHANGELOG", "audit")
# 引用方文件：只做来源登记，不做数值比对
REFERENCE_ONLY_FILES = {
    "99-reference/tools/threshold-registry.yaml",
    "06-cross-layer-governance/06-up-downgrade-matrix/unified-reuse-decision-model.md",
}

WINDOW = 80          # 别名前后模糊匹配窗口（字符）
BIND_MAX_GAP = 40    # 高置信度绑定：别名与数值间最大字符数
CONTEXT_LINES = 10   # 豁免关键词上下文（行）

# 豁免关键词（参考 scripts/cross-index-check.py 的 HISTORICAL_CONTEXT_RE，增补"反模型"）
EXEMPT_CONTEXT_RE = re.compile(
    r"反例|反模型|历史|旧版|旧标准|前一版本|前版|前身|演进|对照|对比|timeline|roadmap|"
    r"deprecated|obsolete|previously|former|superseded|legacy|"
    r"evolution|草案|draft",
    re.IGNORECASE,
)

# 阈值语义线索词（用于非特异别名的高置信度绑定）
# 注意：不使用“取/为/是”等高频字（会误命中“取消”“提取”“…为…”）
CUE_RE = re.compile(
    r"阈值|下限|上限|默认值|默认|取值|不低于|至少|floor|threshold",
    re.IGNORECASE,
)

COMPARATOR_RE = re.compile(r"[=＝<>≥≤]")
SENTENCE_PUNCT_RE = re.compile(r"[。，；、：？！\n]")
# 复合/选择条件阻断词：别名与数值之间存在这些词时，数值属于另一分支条件，不视为绑定
BIND_BLOCK_RE = re.compile(r"或|或者|是否")

NUM_RE = re.compile(r"(\d+(?:\.\d+)?)(%|％)?")


@dataclass
class Threshold:
    entry: dict
    tid: str
    name: str
    value: float
    aliases: List[str]
    allowed: Set[float] = field(default_factory=set)

    @property
    def alias_patterns(self) -> List[Tuple[str, re.Pattern]]:
        pats = []
        for a in self.aliases:
            if re.fullmatch(r"[A-Za-z0-9_]+", a):
                # ASCII 别名：大小写敏感 + 单词边界，避免命中 estimated_aaf / AAFF
                pats.append((a, re.compile(r"(?<![A-Za-z0-9_])" + re.escape(a) + r"(?![A-Za-z0-9_])")))
            else:
                pats.append((a, re.compile(re.escape(a))))
        return pats


@dataclass
class Hit:
    tid: str
    alias: str
    file: str
    line: int
    doc_value: float
    raw: str
    snippet: str
    bound: bool        # 高置信度绑定
    exempt: bool


def _to_float(v) -> Optional[float]:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def load_registry(path: Path) -> Tuple[List[Threshold], List[str]]:
    """加载并结构校验 registry，返回 (阈值列表, 结构错误列表)。"""
    errors: List[str] = []
    if not path.exists():
        return [], [f"registry 文件不存在: {path}"]
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [], [f"registry YAML 解析失败: {e}"]
    if not isinstance(data, dict) or not isinstance(data.get("thresholds"), list):
        return [], ["registry 缺少 thresholds 列表"]

    thresholds: List[Threshold] = []
    seen_ids: Set[str] = set()
    for i, entry in enumerate(data["thresholds"]):
        loc = f"thresholds[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{loc}: 条目不是映射")
            continue
        for key in ("id", "name", "value", "operator", "sources"):
            if key not in entry:
                errors.append(f"{loc}: 缺少必填字段 {key}")
        tid = entry.get("id", loc)
        if tid in seen_ids:
            errors.append(f"{loc}: id 重复 {tid}")
        seen_ids.add(tid)
        if entry.get("operator") not in VALID_OPERATORS:
            errors.append(f"{tid}: operator 非法 {entry.get('operator')!r}，须为 {sorted(VALID_OPERATORS)}")
        value = _to_float(entry.get("value"))
        if value is None:
            errors.append(f"{tid}: value 不可解析为数值: {entry.get('value')!r}")
            continue
        sources = entry.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{tid}: sources 必须为非空列表")

        allowed: Set[float] = {value}
        for key in ("allow_values",):
            av = entry.get(key)
            if av is not None:
                if not isinstance(av, list):
                    errors.append(f"{tid}: {key} 必须为列表")
                else:
                    for x in av:
                        fx = _to_float(x)
                        if fx is None:
                            errors.append(f"{tid}: {key} 含非数值 {x!r}")
                        else:
                            allowed.add(fx)
        for key in ("downgrade_value",):
            fx = _to_float(entry.get(key))
            if fx is not None:
                allowed.add(fx)
        cr = entry.get("canonical_range")
        if cr is not None:
            if isinstance(cr, list) and len(cr) == 2:
                for x in cr:
                    fx = _to_float(x)
                    if fx is None:
                        errors.append(f"{tid}: canonical_range 含非数值 {x!r}")
                    else:
                        allowed.add(fx)
            else:
                errors.append(f"{tid}: canonical_range 须为 [min, max]")
        weights = entry.get("weights")
        if isinstance(weights, dict):
            for x in weights.values():
                fx = _to_float(x)
                if fx is not None:
                    allowed.add(fx)

        aliases = [str(a) for a in entry.get("aliases", [])]
        if entry.get("name"):
            aliases.append(str(entry["name"]))
        if not aliases:
            errors.append(f"{tid}: 缺少 name/aliases，无法扫描")
        # 去重保序
        seen: Set[str] = set()
        aliases = [a for a in aliases if not (a in seen or seen.add(a))]

        thresholds.append(Threshold(
            entry=entry, tid=str(tid), name=str(entry.get("name", "")),
            value=value, aliases=aliases, allowed=allowed,
        ))
    return thresholds, errors


def collect_files(root: Path) -> List[Path]:
    files = []
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        rel = p.relative_to(root).as_posix()
        if any(m in rel for m in EXEMPT_PATH_MARKERS):
            continue
        files.append(p)
    return files


def _line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _is_exempt(lines: List[str], line_no: int) -> bool:
    lo = max(0, line_no - 1 - CONTEXT_LINES)
    hi = min(len(lines), line_no + CONTEXT_LINES)
    return bool(EXEMPT_CONTEXT_RE.search("\n".join(lines[lo:hi])))


def _normalize(doc_num: float, is_percent: bool, reg_value: float) -> float:
    if is_percent and abs(reg_value) <= 2:
        return doc_num / 100.0
    return doc_num


def _is_bound(alias: str, between: str, other_aliases: List[Tuple[str, re.Pattern]]) -> bool:
    """判断别名与数值是否高置信度绑定。between 为二者之间的文本（同一行已在外部保证）。"""
    if len(between) > BIND_MAX_GAP or SENTENCE_PUNCT_RE.search(between):
        return False
    if BIND_BLOCK_RE.search(between):
        return False
    # 中间文本出现其他阈值的别名 → 数值归属于另一阈值（交叉提及），不绑定
    for _a, apat in other_aliases:
        if apat.search(between):
            return False
    specific = len(alias) >= 4
    if CUE_RE.search(alias) or CUE_RE.search(between):
        return True
    if specific and COMPARATOR_RE.search(between):
        return True
    return False


def scan_file(path: Path, rel: str, thresholds: List[Threshold]) -> List[Hit]:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    lines = text.splitlines()
    hits: List[Hit] = []
    seen_hits: set = set()
    all_patterns = [(t.tid, a, p) for t in thresholds for a, p in t.alias_patterns]
    for th in thresholds:
        other_aliases = [(a, p) for tid, a, p in all_patterns if tid != th.tid]
        for alias, pat in th.alias_patterns:
            for m in pat.finditer(text):
                a_start, a_end = m.span()
                win_lo = max(0, a_start - WINDOW)
                win_hi = min(len(text), a_end + WINDOW)
                line_no = _line_no(text, a_start)
                exempt = _is_exempt(lines, line_no)
                seen_vals: Set[Tuple[float, bool]] = set()
                for nm in NUM_RE.finditer(text, win_lo, win_hi):
                    num_str = nm.group(1)
                    if len(num_str) > 1 and num_str.startswith("0") and "." not in num_str:
                        continue  # 前导零编号（如 09-1 章节号），非数值
                    if re.search(r"[Vv]\.[A-Z]?$", text[max(0, nm.start() - 3):nm.start()]):
                        continue  # 版本/定理编号（如 V.1、V.T1），非数值
                    num = float(num_str)
                    is_pct = bool(nm.group(2))
                    key = (num, is_pct)
                    if key in seen_vals:
                        continue
                    seen_vals.add(key)
                    doc_val = _normalize(num, is_pct, th.value)
                    # 仅考虑与别名在同一行的数值（跨行窗口噪声过大）
                    if nm.start() >= a_end:
                        between = text[a_end:nm.start()]
                    else:
                        between = text[nm.end():a_start]
                    if "\n" in between:
                        continue
                    bound = _is_bound(alias, between, other_aliases)
                    if any(abs(doc_val - av) < 1e-9 for av in th.allowed):
                        continue  # 合法取值
                    snippet = lines[line_no - 1].strip() if line_no - 1 < len(lines) else ""
                    hit_key = (th.tid, rel, line_no, doc_val, bound)
                    if hit_key in seen_hits:
                        continue
                    seen_hits.add(hit_key)
                    hits.append(Hit(
                        tid=th.tid, alias=alias, file=rel, line=line_no,
                        doc_value=doc_val, raw=nm.group(0).strip(),
                        snippet=snippet[:120], bound=bound, exempt=exempt,
                    ))
    return hits


def write_report(path: Path, struct_errors: List[str], n_thresholds: int,
                 hard: List[Hit], review: List[Hit], exempted: List[Hit], verified: int):
    lines = [
        "# 阈值一致性检查报告",
        "",
        f"- 登记阈值数: {n_thresholds}",
        f"- 结构错误: {len(struct_errors)}",
        f"- 高置信度不一致（非豁免）: {len(hard)}",
        f"- 待人工复核（模糊命中，不影响门禁）: {len(review)}",
        f"- 豁免命中: {len(exempted)}",
        "",
    ]
    lines.append("## 1. 结构校验")
    lines.append("")
    if struct_errors:
        for e in struct_errors:
            lines.append(f"- ❌ {e}")
    else:
        lines.append("- ✅ registry 结构完整（id/name/value/operator/sources 齐全，operator 合法，value 可解析）")
    lines.append("")

    lines.append("## 2. 高置信度不一致（阻断门禁）")
    lines.append("")
    if hard:
        lines.append("| 阈值 | 位置 | 文档值 | 注册合法值 | 命中行 |")
        lines.append("|------|------|--------|-----------|--------|")
        for h in hard:
            lines.append(f"| {h.tid} | `{h.file}`:{h.line} | {h.doc_value:g} | 见 registry | {h.snippet} |")
    else:
        lines.append("- ✅ 未发现非豁免的高置信度不一致")
    lines.append("")

    lines.append("## 3. 待人工复核（模糊命中，不影响退出码）")
    lines.append("")
    lines.append("> 别名 ±80 字符窗口内出现与注册值不同的数值，但绑定关系不明确"
                 "（可能为实例取值、推导中间值或另一语义的同名符号）。")
    lines.append("")
    if review:
        for h in review[:60]:
            lines.append(f"- **{h.tid}**（别名 `{h.alias}`）`{h.file}`:{h.line} — 文档值 {h.doc_value:g}：`{h.snippet}`")
        if len(review) > 60:
            lines.append(f"- ... 还有 {len(review) - 60} 处")
    else:
        lines.append("- 无")
    lines.append("")

    lines.append("## 4. 豁免命中统计")
    lines.append("")
    if exempted:
        by_reason: Dict[str, int] = defaultdict(int)
        for h in exempted:
            by_reason[h.tid] += 1
        for tid, cnt in sorted(by_reason.items()):
            lines.append(f"- {tid}: {cnt} 处（反例/历史/演进/deprecated/草案语境）")
    else:
        lines.append("- 无")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="阈值登记表一致性与结构校验")
    parser.add_argument("--root", default="struct", help="扫描根目录（默认 struct/）")
    parser.add_argument("--registry", default="struct/99-reference/tools/threshold-registry.yaml",
                        help="阈值登记表路径")
    parser.add_argument("--report", default="reports/threshold-check.md", help="Markdown 报告输出路径")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    root = (project_root / args.root).resolve()
    registry_path = (project_root / args.registry).resolve()
    report_path = project_root / args.report

    thresholds, struct_errors = load_registry(registry_path)
    print(f"registry: {registry_path}（{len(thresholds)} 条阈值，结构错误 {len(struct_errors)}）")

    hard: List[Hit] = []
    review: List[Hit] = []
    exempted: List[Hit] = []

    if root.exists():
        files = collect_files(root)
        print(f"扫描文件: {len(files)} 个")
        for p in files:
            rel = p.relative_to(root).as_posix()
            if rel in REFERENCE_ONLY_FILES:
                continue
            for hit in scan_file(p, rel, thresholds):
                if hit.exempt:
                    exempted.append(hit)
                elif hit.bound:
                    hard.append(hit)
                else:
                    review.append(hit)
    else:
        struct_errors.append(f"扫描根目录不存在: {root}")

    write_report(report_path, struct_errors, len(thresholds), hard, review, exempted, 0)
    print(f"高置信度不一致: {len(hard)}；待人工复核: {len(review)}；豁免: {len(exempted)}")
    for h in hard[:10]:
        print(f"  ❌ {h.tid} {h.file}:{h.line} 文档值 {h.doc_value:g} ≠ 注册值 | {h.snippet}")
    print(f"报告: {report_path}")

    has_error = bool(struct_errors) or bool(hard)
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
