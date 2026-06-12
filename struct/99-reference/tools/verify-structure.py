#!/usr/bin/env python3
"""
verify-structure.py
轻量形式化规约结构检查脚本。
不依赖完整 TLA+/Alloy 工具链，仅验证文件结构、关键语法元素和引用完整性。

用法:
    python verify-structure.py [path]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path("e:/_src/Architecture")
FORMAL_DIR = PROJECT_ROOT / "struct" / "07-formal-verification"


def find_specs() -> Tuple[List[Path], List[Path]]:
    """返回 (TLA+ 文件列表, Alloy 文件列表)。"""
    tla_files = list(FORMAL_DIR.rglob("*.tla"))
    als_files = list(FORMAL_DIR.rglob("*.als"))
    return tla_files, als_files


def check_tla(path: Path) -> List[str]:
    """检查 TLA+ 文件结构。"""
    issues: List[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        issues.append(f"无法读取: {e}")
        return issues

    module_match = re.search(r"^-{4,}\s*MODULE\s+([A-Za-z0-9_]+)\s*-{4,}", text, re.M)
    if not module_match:
        issues.append("缺少 MODULE 声明")
    else:
        module_name = module_match.group(1)
        expected_end = f"===="
        if expected_end not in text:
            issues.append("缺少 ==== 结束标记")
        # 检查文件名（归一化连字符/下划线）是否与模块名一致
        normalized_stem = path.stem.replace("-", "_")
        if normalized_stem != module_name:
            issues.append(f"文件名 '{path.stem}' 与模块名 '{module_name}' 不一致（归一化后：{normalized_stem}）")

    # 检查常见必需元素
    if "EXTENDS" not in text:
        issues.append("未使用 EXTENDS 导入模块")
    if "==" not in text:
        issues.append("未找到定义/操作符（==）")

    # 检查未闭合注释 (* ... *)
    open_comments = text.count("(*")
    close_comments = text.count("*)")
    if open_comments != close_comments:
        issues.append(f"注释未闭合: (*={open_comments}, *)={close_comments}")

    return issues


def check_alloy(path: Path) -> List[str]:
    """检查 Alloy 文件结构。"""
    issues: List[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        issues.append(f"无法读取: {e}")
        return issues

    # Alloy 模型通常至少有一个 sig
    if not re.search(r"\bsig\s+\w+", text):
        issues.append("未定义 sig（Alloy 模型的基本构造）")

    # 检查常见元素
    has_fact = "fact" in text
    has_pred = "pred" in text
    has_run = "run" in text or "check" in text
    has_assert = "assert" in text
    if not (has_fact or has_pred or has_assert):
        issues.append("未找到 fact/pred/assert 约束定义")
    if not has_run:
        issues.append("未找到 run/check 命令（模型不可执行分析）")

    # 检查未闭合块注释（/* */）
    open_block = text.count("/*")
    close_block = text.count("*/")
    if open_block != close_block:
        issues.append(f"块注释未闭合: /*={open_block}, */={close_block}")

    # 检查括号基本平衡，忽略注释行和字符串字面量中的括号
    code_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("--") or stripped.startswith("/*") or stripped.startswith("*"):
            continue
        # 移除双引号字符串
        line_no_strings = re.sub(r'"[^"]*"', '""', line)
        code_lines.append(line_no_strings)
    code_text = "\n".join(code_lines)
    for left, right in [("{", "}"), ("[", "]"), ("(", ")")]:
        if code_text.count(left) != code_text.count(right):
            issues.append(f"括号不平衡: {left}={code_text.count(left)}, {right}={code_text.count(right)}")

    return issues


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT_ROOT
    tla_files, als_files = find_specs()

    print(f"检查 TLA+ 文件: {len(tla_files)} 个")
    print(f"检查 Alloy 文件: {len(als_files)} 个")
    print("=" * 60)

    total_issues = 0
    for path in sorted(tla_files):
        rel = path.relative_to(PROJECT_ROOT)
        issues = check_tla(path)
        if issues:
            total_issues += len(issues)
            print(f"\n[TLA+] {rel}")
            for issue in issues:
                print(f"  ⚠️  {issue}")
        else:
            print(f"  ✅ {rel}")

    for path in sorted(als_files):
        rel = path.relative_to(PROJECT_ROOT)
        issues = check_alloy(path)
        if issues:
            total_issues += len(issues)
            print(f"\n[Alloy] {rel}")
            for issue in issues:
                print(f"  ⚠️  {issue}")
        else:
            print(f"  ✅ {rel}")

    print("\n" + "=" * 60)
    if total_issues == 0:
        print("✅ 所有形式化规约结构检查通过")
        return 0
    else:
        print(f"⚠️  共发现 {total_issues} 处结构问题")
        return 1


if __name__ == "__main__":
    sys.exit(main())
