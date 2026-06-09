#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复用决策引擎单元测试

运行方式:
    python -m pytest test_decision_engine.py -v
    或: python test_decision_engine.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# 确保当前目录在路径中
sys.path.insert(0, str(Path(__file__).resolve().parent))

from decision_engine import (
    AssetProfile,
    ContextProfile,
    DecisionResult,
    DecisionStatus,
    FinalDecision,
    ReuseDecisionEngine,
    RiskItem,
    PhaseResult,
    create_engine_from_data_dir,
)


class TestReuseDecisionEngine(unittest.TestCase):
    """决策引擎核心功能测试"""

    @classmethod
    def setUpClass(cls) -> None:
        """在所有测试前加载引擎"""
        cls.data_dir = Path(__file__).resolve().parent / "data"
        cls.engine = create_engine_from_data_dir(cls.data_dir)

    # -----------------------------------------------------------------------
    # 引擎初始化测试
    # -----------------------------------------------------------------------

    def test_engine_loads_rules(self) -> None:
        """测试引擎成功加载决策规则"""
        self.assertIn("phases", self.engine.rules)
        self.assertEqual(len(self.engine.rules["phases"]), 6)

    def test_engine_loads_patterns(self) -> None:
        """测试引擎成功加载复用模式"""
        self.assertIn("patterns", self.engine.patterns)
        self.assertGreaterEqual(len(self.engine.patterns["patterns"]), 3)

    def test_engine_loads_standards(self) -> None:
        """测试引擎成功加载标准索引"""
        self.assertIn("standards", self.engine.standards)
        self.assertIn("iso42010", self.engine.standards["standards"])

    def test_engine_loads_maturity(self) -> None:
        """测试引擎成功加载成熟度矩阵"""
        self.assertIn("dimensions", self.engine.maturity)
        self.assertGreaterEqual(len(self.engine.maturity["dimensions"]), 3)

    # -----------------------------------------------------------------------
    # 六阶段决策评估测试
    # -----------------------------------------------------------------------

    def test_perfect_asset_gets_approved(self) -> None:
        """测试理想资产应获得批准"""
        asset = AssetProfile(
            asset_id="TEST-001",
            name="完美组件",
            domain_scope=["电商", "金融"],
            supported_tech=["Kubernetes", "Java", "gRPC"],
            variation_points=["配置", "主题"],
            binding_times=["运行期", "部署期"],
            rrl=4.5,
            maturity=5,
            reliability=0.95,
            maintainability=0.90,
            license="MIT",
            security_level="L3",
            slsa_level=2,
            aaf_typical=0.20,
            npv_positive=True,
            roi_years=1.0,
            required_org_maturity=2,
            process_standardized=True,
            asset_catalog_required=True,
        )
        context = ContextProfile(
            name="测试上下文",
            required_domain=["电商"],
            tech_constraints=["Kubernetes", "Java"],
            required_variations=["配置"],
            preferred_binding_time="运行期",
            min_rrl=3.0,
            min_maturity=3,
            min_reliability=0.85,
            min_maintainability=0.80,
            approved_licenses=["MIT", "Apache-2.0"],
            min_security_level="L2",
            min_slsa_level=1,
            max_payback_years=3.0,
            org_maturity_level=4,
            process_standardized=True,
            asset_catalog_exists=True,
            extra={"estimated_aaf": 0.20, "estimated_npv": 5.0},
        )

        result = self.engine.evaluate(asset, context)
        self.assertIsInstance(result, DecisionResult)
        self.assertEqual(result.asset_id, "TEST-001")
        # 理想情况下应该通过或条件通过（取决于具体规则）
        self.assertIn(
            result.final_decision,
            [FinalDecision.APPROVE, FinalDecision.CONDITIONAL_APPROVE],
        )
        self.assertGreaterEqual(result.final_score, 50.0)

    def test_unsuitable_asset_gets_rejected(self) -> None:
        """测试不适合的资产应被拒绝"""
        asset = AssetProfile(
            asset_id="TEST-002",
            name="不兼容组件",
            domain_scope=["嵌入式"],
            supported_tech=["C", "RTOS"],
            rrl=1.5,
            maturity=1,
            reliability=0.60,
            maintainability=0.50,
            license="GPL-3.0",
            security_level="L1",
            slsa_level=1,
            aaf_typical=0.85,
            npv_positive=False,
            required_org_maturity=5,
        )
        context = ContextProfile(
            name="云原生上下文",
            required_domain=["电商", "金融"],
            tech_constraints=["Kubernetes", "Java"],
            min_rrl=3.5,
            min_maturity=4,
            min_reliability=0.90,
            approved_licenses=["MIT", "Apache-2.0", "BSD"],
            min_security_level="L3",
            org_maturity_level=2,
            extra={"estimated_aaf": 0.85, "estimated_npv": -2.0},
        )

        result = self.engine.evaluate(asset, context)
        self.assertEqual(result.final_decision, FinalDecision.REJECT)
        self.assertTrue(len(result.risks) > 0)
        # 应包含多条拒绝理由
        reject_phases = [p for p in result.phase_results if p.status == DecisionStatus.REJECT]
        self.assertGreaterEqual(len(reject_phases), 1)

    def test_conditional_approval_with_risks(self) -> None:
        """测试条件通过场景：资产基本可用但存在中等风险"""
        asset = AssetProfile(
            asset_id="TEST-003",
            name="条件通过组件",
            domain_scope=["电商"],
            supported_tech=["Kubernetes", "Java"],
            rrl=3.2,
            maturity=3,
            reliability=0.88,
            maintainability=0.82,
            license="MIT",
            security_level="L2",
            slsa_level=1,
            aaf_typical=0.55,
            npv_positive=True,
            required_org_maturity=3,
            process_standardized=True,
        )
        context = ContextProfile(
            name="标准上下文",
            required_domain=["电商"],
            tech_constraints=["Kubernetes"],
            min_rrl=3.0,
            min_maturity=3,
            min_reliability=0.85,
            approved_licenses=["MIT"],
            min_security_level="L2",
            org_maturity_level=3,
            process_standardized=True,
            asset_catalog_exists=True,
            extra={"estimated_aaf": 0.55, "estimated_npv": 1.5},
        )

        result = self.engine.evaluate(asset, context)
        # AAF=0.55 触发条件通过，应产生条件批准或批准
        self.assertIn(
            result.final_decision,
            [FinalDecision.APPROVE, FinalDecision.CONDITIONAL_APPROVE],
        )

    # -----------------------------------------------------------------------
    # 序列化测试
    # -----------------------------------------------------------------------

    def test_result_serialization(self) -> None:
        """测试决策结果可正确序列化为字典"""
        asset = AssetProfile(asset_id="SER-001", name="序列化测试")
        context = ContextProfile(name="测试上下文")
        result = self.engine.evaluate(asset, context)

        d = result.to_dict()
        self.assertEqual(d["asset_id"], "SER-001")
        self.assertIn("phase_results", d)
        self.assertIn("risks", d)
        self.assertIn("recommendations", d)
        self.assertIsInstance(d["final_score"], (int, float))

    # -----------------------------------------------------------------------
    # 标准对齐检查测试
    # -----------------------------------------------------------------------

    def test_check_standard_found(self) -> None:
        """测试检查已存在的标准"""
        report = self.engine.check_standard_alignment("iso42010")
        self.assertTrue(report["found"])
        self.assertEqual(report["standard"], "iso42010")
        self.assertIn("alignment_checklist", report)

    def test_check_standard_not_found(self) -> None:
        """测试检查不存在的标准"""
        report = self.engine.check_standard_alignment("nonexistent-standard-xyz")
        self.assertFalse(report["found"])

    def test_check_standard_version_mismatch(self) -> None:
        """测试版本不一致警告"""
        report = self.engine.check_standard_alignment("iso42010", version="2011")
        self.assertIn("version_warning", report)

    # -----------------------------------------------------------------------
    # 成熟度评估测试
    # -----------------------------------------------------------------------

    def test_assess_maturity_valid(self) -> None:
        """测试有效的成熟度评估"""
        result = self.engine.assess_maturity(3)
        self.assertNotIn("error", result)
        self.assertEqual(result["target_level"], 3)
        self.assertTrue(len(result["gap_analysis"]) > 0)

    def test_assess_maturity_invalid_level(self) -> None:
        """测试无效的成熟度等级"""
        result = self.engine.assess_maturity(0)
        self.assertIn("error", result)

    def test_assess_maturity_specific_dimension(self) -> None:
        """测试特定维度的成熟度评估"""
        result = self.engine.assess_maturity(4, dimension="D1")
        self.assertNotIn("error", result)
        self.assertEqual(len(result["gap_analysis"]), 1)
        self.assertEqual(result["gap_analysis"][0]["dimension_id"], "D1")

    # -----------------------------------------------------------------------
    # 决策卡片生成测试
    # -----------------------------------------------------------------------

    def test_generate_card_markdown(self) -> None:
        """测试生成 Markdown 决策卡片"""
        card = self.engine.generate_decision_card("PAT-MICRO-002", fmt="markdown")
        self.assertIn("复用决策卡片", card)
        self.assertIn("六阶段评估详情", card)

    def test_generate_card_json(self) -> None:
        """测试生成 JSON 决策卡片"""
        card = self.engine.generate_decision_card("PAT-MICRO-002", fmt="json")
        import json

        data = json.loads(card)
        self.assertIn("asset_id", data)
        self.assertIn("phase_results", data)

    def test_generate_card_unknown_asset(self) -> None:
        """测试未知资产生成默认卡片"""
        card = self.engine.generate_decision_card("UNKNOWN-ASSET-999", fmt="markdown")
        self.assertIn("UNKNOWN-ASSET-999", card)

    # -----------------------------------------------------------------------
    # COCOMO / 财务计算测试
    # -----------------------------------------------------------------------

    def test_calculate_esloc(self) -> None:
        """测试 ESLOC 计算"""
        esloc = ReuseDecisionEngine.calculate_cocomo_esloc(ksloc_reused=50.0, aaf=0.4)
        self.assertAlmostEqual(esloc, 20.0)

    def test_calculate_effort(self) -> None:
        """测试 COCOMO 工作量计算"""
        effort = ReuseDecisionEngine.calculate_cocomo_effort(esloc=20.0, em=1.2)
        self.assertGreater(effort, 0.0)

    def test_calculate_npv(self) -> None:
        """测试 NPV 计算"""
        npv = ReuseDecisionEngine.calculate_npv(
            initial_cost=100.0,
            annual_savings=50.0,
            annual_maintenance=10.0,
            discount_rate=0.08,
            years=5,
        )
        self.assertGreater(npv, 0.0)  # 正现金流应产生正 NPV

    def test_calculate_npv_negative(self) -> None:
        """测试亏损场景 NPV 为负"""
        npv = ReuseDecisionEngine.calculate_npv(
            initial_cost=500.0,
            annual_savings=10.0,
            annual_maintenance=5.0,
            years=3,
        )
        self.assertLess(npv, 0.0)

    def test_calculate_roi(self) -> None:
        """测试 ROI 计算"""
        roi = ReuseDecisionEngine.calculate_roi(
            initial_cost=100.0,
            total_savings=300.0,
            total_maintenance=50.0,
        )
        self.assertAlmostEqual(roi, 150.0)  # (300-50-100)/100 = 150%

    # -----------------------------------------------------------------------
    # 插件机制测试
    # -----------------------------------------------------------------------

    def test_plugin_registration(self) -> None:
        """测试插件注册和执行"""
        called = []

        def dummy_hook(arg1, arg2):
            called.append((arg1, arg2))
            return "ok"

        self.engine.plugins.register("pre_phase_eval", dummy_hook)
        asset = AssetProfile(asset_id="PLUGIN-001", name="插件测试")
        context = ContextProfile(name="测试上下文")
        self.engine.evaluate(asset, context)

        self.assertTrue(len(called) > 0)


class TestDataModels(unittest.TestCase):
    """数据模型基础测试"""

    def test_risk_item_creation(self) -> None:
        """测试风险项创建"""
        risk = RiskItem(
            risk_id="R-001",
            phase="阶段1",
            description="测试风险",
            severity="HIGH",
            mitigation="测试缓解",
        )
        self.assertEqual(risk.risk_id, "R-001")
        self.assertEqual(risk.owner, "未分配")  # 默认值

    def test_phase_result_creation(self) -> None:
        """测试阶段结果创建"""
        pr = PhaseResult(
            phase_id="P1",
            phase_name="测试阶段",
            status=DecisionStatus.PASS,
            score=85.0,
            weight=1.0,
        )
        self.assertEqual(pr.status, DecisionStatus.PASS)
        self.assertEqual(pr.score, 85.0)


# ---------------------------------------------------------------------------
# 自运行入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
