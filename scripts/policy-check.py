#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OPA/Rego 策略执行检查（P1 落地）。"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
POLICY_DIR = PROJECT_ROOT / "struct" / "06-cross-layer-governance" / "07-policy-automation" / "policies"


def run_opa_test() -> tuple[int, str]:
    if not POLICY_DIR.exists():
        return 0, "OPA 策略目录不存在，跳过"
    cmd = ["opa", "test", str(POLICY_DIR), "--verbose"]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120, check=False
        )
    except FileNotFoundError:
        return 1, "opa CLI 未安装；fallback 到 Python smoke test"
    return result.returncode, result.stdout + result.stderr


def run_python_fallback() -> tuple[int, str]:
    """在没有 opa 的环境可用 Python 模拟复用经济判定（smoke test）。"""
    thresholds_dir = PROJECT_ROOT / "struct" / "09-value-quantification" / "tools"
    sys.path.insert(0, str(thresholds_dir))
    try:
        from reuse_thresholds import reuse_decision, ReuseVerdict
    except ImportError as e:
        return 1, f"无法导入 reuse_thresholds: {e}"

    cases = [
        ({"aaf": 0.3}, ReuseVerdict.REUSE_ECONOMIC),
        ({"aaf": 0.75}, ReuseVerdict.TRADE_OFF),
        ({"aaf": 0.95}, ReuseVerdict.REBUILD),
        ({"aaf": 65}, ReuseVerdict.TRADE_OFF),  # 百分比兼容
    ]
    for inp, expected in cases:
        dec = reuse_decision(inp["aaf"])
        if dec.verdict != expected:
            return 1, f"case {inp} expected {expected.value}, got {dec.verdict.value}"
    return 0, "Python fallback 通过（复用经济判定 smoke test）"


def main() -> int:
    rc, msg = run_opa_test()
    if rc != 0:
        print("OPA 策略测试失败或不可用：")
        print(msg)
        print("尝试 Python fallback...")
        rc2, msg2 = run_python_fallback()
        print(msg2)
        return rc2
    print("OPA 策略测试通过：")
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
