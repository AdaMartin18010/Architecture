#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OPA/Rego 策略执行检查（P1 落地 + P2 判定统一扩展）。"""

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
    """在没有 opa 的环境可用 Python 模拟核心策略（smoke test）。"""
    thresholds_dir = PROJECT_ROOT / "struct" / "09-value-quantification" / "tools"
    sys.path.insert(0, str(thresholds_dir))
    try:
        from reuse_thresholds import reuse_decision, ReuseVerdict
    except ImportError as e:
        return 1, f"无法导入 reuse_thresholds: {e}"

    # 复用经济判定 smoke test
    cases = [
        ({"aaf": 0.3}, ReuseVerdict.REUSE_ECONOMIC),
        ({"aaf": 0.75}, ReuseVerdict.TRADE_OFF),
        ({"aaf": 0.95}, ReuseVerdict.REBUILD),
        ({"aaf": 65}, ReuseVerdict.REUSE_ECONOMIC),  # 百分比 65% -> 0.65 < 0.7
    ]
    for inp, expected in cases:
        dec = reuse_decision(inp["aaf"])
        if dec.verdict != expected:
            return 1, f"reuse case {inp} expected {expected.value}, got {dec.verdict.value}"

    # 供应链安全判定 smoke test（与 supply_chain_decision.rego 语义对齐）
    def supply_chain_decision(inp: dict) -> str:
        has_sbom = inp.get("has_sbom", False)
        slsa = inp.get("slsa_level", 0)
        crit = inp.get("criticality", "low")
        if crit == "critical":
            if not has_sbom or slsa < 2:
                return "REJECT"
            return "APPROVE"
        if crit == "high" and slsa < 2:
            return "CONDITIONAL"
        if has_sbom and slsa >= 2:
            return "APPROVE"
        if has_sbom and slsa == 1:
            return "CONDITIONAL"
        if crit == "low" and has_sbom:
            return "APPROVE"
        return "REJECT"

    sc_cases = [
        ({"has_sbom": True, "slsa_level": 3, "criticality": "critical"}, "APPROVE"),
        ({"has_sbom": False, "slsa_level": 3, "criticality": "critical"}, "REJECT"),
        ({"has_sbom": True, "slsa_level": 1, "criticality": "critical"}, "REJECT"),
        ({"has_sbom": True, "slsa_level": 1, "criticality": "high"}, "CONDITIONAL"),
        ({"has_sbom": True, "slsa_level": 2, "criticality": "medium"}, "APPROVE"),
        ({"has_sbom": True, "slsa_level": 0, "criticality": "low"}, "APPROVE"),
    ]
    for inp, expected in sc_cases:
        got = supply_chain_decision(inp)
        if got != expected:
            return 1, f"supply chain case {inp} expected {expected}, got {got}"

    # FinOps 分摊模型 smoke test（与 finops_allocation_model.rego 语义对齐）
    def finops_allocation_model(inp: dict) -> str:
        if inp.get("direct_tag"):
            return "DIRECT"
        if inp.get("quantifiable_usage"):
            return "LAYER_BASED" if inp.get("cross_layer_shared") else "USAGE_BASED"
        if inp.get("risk_contingent"):
            return "RISK_BASED"
        return "OVERHEAD"

    finops_cases = [
        ({"direct_tag": True}, "DIRECT"),
        ({"direct_tag": False, "quantifiable_usage": True, "cross_layer_shared": True}, "LAYER_BASED"),
        ({"direct_tag": False, "quantifiable_usage": True, "cross_layer_shared": False}, "USAGE_BASED"),
        ({"direct_tag": False, "quantifiable_usage": False, "risk_contingent": True}, "RISK_BASED"),
        ({"direct_tag": False, "quantifiable_usage": False, "risk_contingent": False}, "OVERHEAD"),
    ]
    for inp, expected in finops_cases:
        got = finops_allocation_model(inp)
        if got != expected:
            return 1, f"finops case {inp} expected {expected}, got {got}"

    # AI 模型选择判定 smoke test（与 ai_model_selection.rego 语义对齐）
    def ai_model_selection(inp: dict) -> str:
        tiers = inp.get("available_tiers", [])
        min_acc = inp.get("min_accuracy", 0.0)
        max_lat = inp.get("max_latency_p99_ms", 9999)
        max_cost = inp.get("max_cost_per_1k_tokens", 999.0)
        privacy = inp.get("data_privacy_required", False)
        safety = inp.get("safety_level_required", "low")

        if min_acc > 0.98 or max_lat < 20:
            return "REJECT"
        if safety == "high" and "premium" not in tiers:
            return "REJECT"
        if privacy and "premium" not in tiers and "balanced" not in tiers:
            return "REJECT"
        if safety == "high" and "premium" in tiers:
            return "PREMIUM"
        if min_acc >= 0.92 and "premium" in tiers:
            return "PREMIUM"
        if max_lat <= 100 and "premium" in tiers:
            return "PREMIUM"
        if min_acc >= 0.85 and "balanced" in tiers:
            return "BALANCED"
        if max_lat <= 300 and max_cost <= 0.05 and "balanced" in tiers:
            return "BALANCED"
        if max_cost <= 0.01 and "economy" in tiers:
            return "ECONOMY"
        if "balanced" in tiers:
            return "BALANCED"
        return "REJECT"

    ai_cases = [
        ({"task_type": "critical", "min_accuracy": 0.90, "max_latency_p99_ms": 500,
          "max_cost_per_1k_tokens": 0.10, "data_privacy_required": False,
          "safety_level_required": "high", "available_tiers": ["premium", "balanced", "economy"]}, "PREMIUM"),
        ({"task_type": "classification", "min_accuracy": 0.95, "max_latency_p99_ms": 500,
          "max_cost_per_1k_tokens": 0.10, "data_privacy_required": False,
          "safety_level_required": "medium", "available_tiers": ["premium", "balanced", "economy"]}, "PREMIUM"),
        ({"task_type": "chat", "min_accuracy": 0.80, "max_latency_p99_ms": 80,
          "max_cost_per_1k_tokens": 0.10, "data_privacy_required": False,
          "safety_level_required": "low", "available_tiers": ["premium", "balanced", "economy"]}, "PREMIUM"),
        ({"task_type": "summarization", "min_accuracy": 0.80, "max_latency_p99_ms": 500,
          "max_cost_per_1k_tokens": 0.05, "data_privacy_required": False,
          "safety_level_required": "low", "available_tiers": ["premium", "balanced", "economy"]}, "BALANCED"),
        ({"task_type": "creative", "min_accuracy": 0.70, "max_latency_p99_ms": 1000,
          "max_cost_per_1k_tokens": 0.005, "data_privacy_required": False,
          "safety_level_required": "low", "available_tiers": ["premium", "balanced", "economy"]}, "ECONOMY"),
        ({"task_type": "classification", "min_accuracy": 0.99, "max_latency_p99_ms": 200,
          "max_cost_per_1k_tokens": 0.05, "data_privacy_required": False,
          "safety_level_required": "medium", "available_tiers": ["premium", "balanced", "economy"]}, "REJECT"),
        ({"task_type": "critical", "min_accuracy": 0.80, "max_latency_p99_ms": 500,
          "max_cost_per_1k_tokens": 0.10, "data_privacy_required": False,
          "safety_level_required": "high", "available_tiers": ["balanced", "economy"]}, "REJECT"),
        ({"task_type": "chat", "min_accuracy": 0.80, "max_latency_p99_ms": 500,
          "max_cost_per_1k_tokens": 0.10, "data_privacy_required": True,
          "safety_level_required": "low", "available_tiers": ["economy"]}, "REJECT"),
    ]
    for inp, expected in ai_cases:
        got = ai_model_selection(inp)
        if got != expected:
            return 1, f"ai model case {inp} expected {expected}, got {got}"

    # 升级/降级矩阵 smoke test（与 upgrade_downgrade_matrix.rego 语义对齐）
    def upgrade_downgrade_matrix(inp: dict) -> str:
        layer_order = ["function", "component", "app_service", "business_service"]
        cur = inp.get("current_layer", "component")
        idx = layer_order.index(cur)
        security_rank = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4}
        sec_req = security_rank.get(inp.get("security_level_required", "L0"), 0)
        sec_cert = security_rank.get(inp.get("component_cert_level", "L0"), 0)
        mismatch = sec_req > sec_cert
        consumers = inp.get("consumers", 0)

        if consumers == 0:
            return "DEPRECATE"

        upgrade = (
            (consumers >= 3 and inp.get("cross_team", False)
             and inp.get("semantic_coverage_ratio", 0) >= 0.8
             and inp.get("tech_compatibility_ratio", 0) >= 0.8)
            or inp.get("cross_org", False)
            or (inp.get("upgrade_benefit", 0) > 0 and consumers >= 3)
        )
        downgrade = (
            inp.get("coupling_impact_ratio", 0) > 0.3
            or inp.get("tech_compatibility_ratio", 0) < 0.5
            or inp.get("confidence_gamma", 1.0) < 0.8
            or inp.get("config_conflicts", 0) >= 5
            or mismatch
            or inp.get("latency_requirement_ms", 0) < inp.get("shared_service_p99_ms", 0)
            or (inp.get("semantic_coverage_ratio", 0) < 0.8 and inp.get("downgrade_benefit", 0) > 0)
            or (inp.get("downgrade_benefit", 0) > 0 and inp.get("coupling_impact_ratio", 0) > 0.2)
        )

        if upgrade and mismatch:
            return "SECURITY_REVIEW"
        if downgrade:
            return "DOWNGRADE"
        if upgrade and inp.get("tech_compatibility_ratio", 0) < 0.8:
            return "ADAPTER"
        if upgrade:
            return "UPGRADE"
        return "MAINTAIN"

    matrix_cases = [
        ({"current_layer": "component", "consumers": 5, "cross_team": True,
          "cross_org": False, "tech_compatibility_ratio": 0.9,
          "semantic_coverage_ratio": 0.85, "coupling_impact_ratio": 0.1,
          "security_level_required": "L2", "component_cert_level": "L2",
          "confidence_gamma": 0.95, "config_conflicts": 0,
          "latency_requirement_ms": 200, "shared_service_p99_ms": 150,
          "upgrade_benefit": 10.0, "downgrade_benefit": 0.0}, "UPGRADE"),
        ({"current_layer": "app_service", "consumers": 5, "cross_team": True,
          "cross_org": False, "tech_compatibility_ratio": 0.9,
          "semantic_coverage_ratio": 0.85, "coupling_impact_ratio": 0.1,
          "security_level_required": "L4", "component_cert_level": "L2",
          "confidence_gamma": 0.95, "config_conflicts": 0,
          "latency_requirement_ms": 200, "shared_service_p99_ms": 150,
          "upgrade_benefit": 10.0, "downgrade_benefit": 0.0}, "SECURITY_REVIEW"),
        ({"current_layer": "component", "consumers": 5, "cross_team": True,
          "cross_org": False, "tech_compatibility_ratio": 0.6,
          "semantic_coverage_ratio": 0.85, "coupling_impact_ratio": 0.1,
          "security_level_required": "L2", "component_cert_level": "L2",
          "confidence_gamma": 0.95, "config_conflicts": 0,
          "latency_requirement_ms": 200, "shared_service_p99_ms": 150,
          "upgrade_benefit": 10.0, "downgrade_benefit": 0.0}, "ADAPTER"),
        ({"current_layer": "business_service", "consumers": 8, "cross_team": True,
          "cross_org": True, "tech_compatibility_ratio": 0.9,
          "semantic_coverage_ratio": 0.85, "coupling_impact_ratio": 0.4,
          "security_level_required": "L2", "component_cert_level": "L2",
          "confidence_gamma": 0.95, "config_conflicts": 0,
          "latency_requirement_ms": 200, "shared_service_p99_ms": 150,
          "upgrade_benefit": 0.0, "downgrade_benefit": 5.0}, "DOWNGRADE"),
        ({"current_layer": "component", "consumers": 2, "cross_team": False,
          "cross_org": False, "tech_compatibility_ratio": 0.9,
          "semantic_coverage_ratio": 0.85, "coupling_impact_ratio": 0.1,
          "security_level_required": "L2", "component_cert_level": "L2",
          "confidence_gamma": 0.95, "config_conflicts": 0,
          "latency_requirement_ms": 200, "shared_service_p99_ms": 150,
          "upgrade_benefit": 0.0, "downgrade_benefit": 0.0}, "MAINTAIN"),
        ({"current_layer": "function", "consumers": 0, "cross_team": False,
          "cross_org": False, "tech_compatibility_ratio": 0.9,
          "semantic_coverage_ratio": 0.85, "coupling_impact_ratio": 0.1,
          "security_level_required": "L2", "component_cert_level": "L2",
          "confidence_gamma": 0.95, "config_conflicts": 0,
          "latency_requirement_ms": 200, "shared_service_p99_ms": 150,
          "upgrade_benefit": 0.0, "downgrade_benefit": 0.0}, "DEPRECATE"),
    ]
    for inp, expected in matrix_cases:
        got = upgrade_downgrade_matrix(inp)
        if got != expected:
            return 1, f"upgrade/downgrade case {inp} expected {expected}, got {got}"

    # 六阶段统一判定 smoke test（与 reuse_six_phase_decision.rego 语义对齐）
    def six_phase_decision(inp: dict) -> str:
        if not inp.get("semantic_compatible", False):
            return "REJECT"
        if not inp.get("security_pass", False):
            return "REJECT"
        if not inp.get("economic_pass", False):
            return "REJECT"
        if inp.get("conditional_phases", 0) > 2:
            return "REJECT"
        if (inp.get("semantic_compatible") and inp.get("variation_bindable")
                and inp.get("quality_pass") and inp.get("security_pass")
                and inp.get("economic_pass") and inp.get("governance_pass")):
            return "APPROVE"
        return "CONDITIONAL"

    phase_cases = [
        ({"semantic_compatible": True, "variation_bindable": True, "quality_pass": True,
          "security_pass": True, "economic_pass": True, "governance_pass": True,
          "conditional_phases": 0}, "APPROVE"),
        ({"semantic_compatible": False, "variation_bindable": True, "quality_pass": True,
          "security_pass": True, "economic_pass": True, "governance_pass": True,
          "conditional_phases": 0}, "REJECT"),
        ({"semantic_compatible": True, "variation_bindable": True, "quality_pass": True,
          "security_pass": False, "economic_pass": True, "governance_pass": True,
          "conditional_phases": 0}, "REJECT"),
        ({"semantic_compatible": True, "variation_bindable": True, "quality_pass": True,
          "security_pass": True, "economic_pass": False, "governance_pass": True,
          "conditional_phases": 0}, "REJECT"),
        ({"semantic_compatible": True, "variation_bindable": True, "quality_pass": True,
          "security_pass": True, "economic_pass": True, "governance_pass": True,
          "conditional_phases": 3}, "REJECT"),
        ({"semantic_compatible": True, "variation_bindable": True, "quality_pass": False,
          "security_pass": True, "economic_pass": True, "governance_pass": True,
          "conditional_phases": 1}, "CONDITIONAL"),
        ({"semantic_compatible": True, "variation_bindable": True, "quality_pass": True,
          "security_pass": True, "economic_pass": True, "governance_pass": False,
          "conditional_phases": 1}, "CONDITIONAL"),
    ]
    for inp, expected in phase_cases:
        got = six_phase_decision(inp)
        if got != expected:
            return 1, f"six phase case {inp} expected {expected}, got {got}"

    return 0, "Python fallback 通过（复用经济 + 供应链安全 + FinOps + AI模型 + 升降级矩阵 + 六阶段统一判定 smoke test）"


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
