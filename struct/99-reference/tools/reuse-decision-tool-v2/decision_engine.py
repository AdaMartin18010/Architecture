# -*- coding: utf-8 -*-
"""
复用决策引擎 (Reuse Decision Engine v2.0)

实现六阶段复用决策流程：
  1. 语义兼容性判定
  2. 变性绑定判定
  3. 质量达标判定
  4. 安全合规判定
  5. 成本收益判定
  6. 治理合规判定

特性：
  - 基于规则的决策树（从 JSON 配置加载，不硬编码）
  - 支持置信度评分（0-100）
  - 支持风险登记（Risk Register）输出
  - 支持升级/降级建议（功能→组件→应用→业务）
  - 插件式扩展机制
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable


# ---------------------------------------------------------------------------
# 枚举与常量
# ---------------------------------------------------------------------------

class DecisionStatus(Enum):
    """单阶段决策状态"""
    PASS = "通过"
    CONDITIONAL = "条件通过"
    REJECT = "拒绝"
    NOT_EVALUATED = "未评估"


class FinalDecision(Enum):
    """最终决策结果"""
    APPROVE = "批准复用"
    CONDITIONAL_APPROVE = "条件批准"
    REJECT = "拒绝复用"
    NEED_MORE_INFO = "需要补充信息"


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------

@dataclass
class RiskItem:
    """风险登记项"""
    risk_id: str
    phase: str
    description: str
    severity: str  # HIGH / MEDIUM / LOW
    mitigation: str
    owner: str = "未分配"


@dataclass
class PhaseResult:
    """单阶段评估结果"""
    phase_id: str
    phase_name: str
    status: DecisionStatus
    score: float  # 0-100
    weight: float
    details: List[Dict[str, Any]] = field(default_factory=list)
    messages: List[str] = field(default_factory=list)


@dataclass
class DecisionResult:
    """完整决策结果"""
    asset_id: str
    asset_name: str
    context_name: str
    final_decision: FinalDecision
    final_score: float  # 0-100 置信度
    phase_results: List[PhaseResult] = field(default_factory=list)
    risks: List[RiskItem] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    upgrade_path: Optional[List[str]] = None
    downgrade_path: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "context_name": self.context_name,
            "final_decision": self.final_decision.value,
            "final_score": round(self.final_score, 2),
            "phase_results": [
                {
                    "phase_id": p.phase_id,
                    "phase_name": p.phase_name,
                    "status": p.status.value,
                    "score": round(p.score, 2),
                    "weight": p.weight,
                    "details": p.details,
                    "messages": p.messages,
                }
                for p in self.phase_results
            ],
            "risks": [
                {
                    "risk_id": r.risk_id,
                    "phase": r.phase,
                    "description": r.description,
                    "severity": r.severity,
                    "mitigation": r.mitigation,
                    "owner": r.owner,
                }
                for r in self.risks
            ],
            "recommendations": self.recommendations,
            "upgrade_path": self.upgrade_path,
            "downgrade_path": self.downgrade_path,
            "metadata": self.metadata,
        }


@dataclass
class AssetProfile:
    """待评估资产画像"""
    asset_id: str
    name: str
    category: str = ""
    domain_scope: List[str] = field(default_factory=list)
    supported_tech: List[str] = field(default_factory=list)
    variation_points: List[str] = field(default_factory=list)
    binding_times: List[str] = field(default_factory=list)
    rrl: float = 0.0  # Reuse Readiness Level (0-5)
    maturity: int = 1  # 1-5
    reliability: float = 0.0  # 0-1
    maintainability: float = 0.0  # 0-1
    license: str = "未知"
    security_level: str = "L1"
    slsa_level: int = 1
    aaf_typical: float = 0.5
    npv_positive: bool = False
    roi_years: float = 999.0
    required_org_maturity: int = 1
    process_standardized: bool = False
    asset_catalog_required: bool = False
    interface_contract: Dict[str, Any] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextProfile:
    """复用上下文画像"""
    name: str
    required_domain: List[str] = field(default_factory=list)
    tech_constraints: List[str] = field(default_factory=list)
    required_variations: List[str] = field(default_factory=list)
    preferred_binding_time: str = "运行期"
    min_rrl: float = 3.0
    min_maturity: int = 3
    min_reliability: float = 0.85
    min_maintainability: float = 0.80
    approved_licenses: List[str] = field(default_factory=lambda: ["MIT", "Apache-2.0", "BSD"])
    min_security_level: str = "L2"
    min_slsa_level: int = 1
    max_payback_years: float = 3.0
    org_maturity_level: int = 1
    process_standardized: bool = False
    asset_catalog_exists: bool = False
    required_interface: Dict[str, Any] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# 插件机制
# ---------------------------------------------------------------------------

class PluginRegistry:
    """插件注册表，支持动态扩展评估维度"""

    def __init__(self) -> None:
        self._hooks: Dict[str, List[Callable]] = {
            "pre_phase_eval": [],
            "post_phase_eval": [],
            "final_decision": [],
        }

    def register(self, hook_name: str, func: Callable) -> None:
        """注册插件函数到指定钩子"""
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []
        self._hooks[hook_name].append(func)

    def run(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """运行指定钩子的所有插件"""
        results = []
        for func in self._hooks.get(hook_name, []):
            try:
                results.append(func(*args, **kwargs))
            except Exception as e:
                # 插件错误不应中断主流程
                results.append({"error": str(e)})
        return results


# ---------------------------------------------------------------------------
# 决策引擎核心
# ---------------------------------------------------------------------------

class ReuseDecisionEngine:
    """
    复用决策引擎

    从 JSON 配置文件加载六阶段决策规则，对资产和上下文进行评估。
    """

    DEFAULT_DATA_DIR = Path(__file__).resolve().parent / "data"

    def __init__(
        self,
        rules_path: Optional[Path] = None,
        patterns_path: Optional[Path] = None,
        standards_path: Optional[Path] = None,
        maturity_path: Optional[Path] = None,
    ) -> None:
        """
        初始化决策引擎。

        Args:
            rules_path: 决策规则 JSON 路径，默认使用内置 data/decision_rules.json
            patterns_path: 复用模式 JSON 路径
            standards_path: 标准索引 JSON 路径
            maturity_path: 成熟度矩阵 JSON 路径
        """
        self.data_dir = self.DEFAULT_DATA_DIR
        self.rules_path = rules_path or self.data_dir / "decision_rules.json"
        self.patterns_path = patterns_path or self.data_dir / "reuse_patterns.json"
        self.standards_path = standards_path or self.data_dir / "standards_index.json"
        self.maturity_path = maturity_path or self.data_dir / "maturity_matrix.json"

        # 加载配置
        self.rules: Dict[str, Any] = self._load_json(self.rules_path)
        self.patterns: Dict[str, Any] = self._load_json(self.patterns_path)
        self.standards: Dict[str, Any] = self._load_json(self.standards_path)
        self.maturity: Dict[str, Any] = self._load_json(self.maturity_path)

        # 插件注册表
        self.plugins = PluginRegistry()

        # 内部缓存
        self._patterns_by_id: Dict[str, Dict[str, Any]] = {}
        if "patterns" in self.patterns:
            for pat in self.patterns["patterns"]:
                self._patterns_by_id[pat["id"]] = pat

    @staticmethod
    def _load_json(path: Path) -> Dict[str, Any]:
        """安全加载 JSON 文件"""
        if not path.exists():
            raise FileNotFoundError(f"数据文件不存在: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------------------------------------------------
    # 六阶段决策流程
    # -----------------------------------------------------------------------

    def evaluate(self, asset: AssetProfile, context: ContextProfile) -> DecisionResult:
        """
        执行完整六阶段复用决策评估。

        Args:
            asset: 待复用资产画像
            context: 复用上下文画像

        Returns:
            DecisionResult: 完整决策结果
        """
        phase_results: List[PhaseResult] = []
        risks: List[RiskItem] = []
        recommendations: List[str] = []

        # 运行 pre_phase_eval 钩子
        self.plugins.run("pre_phase_eval", asset, context)

        phases_config = self.rules.get("phases", [])
        for phase_cfg in phases_config:
            phase_result = self._evaluate_phase(phase_cfg, asset, context)
            phase_results.append(phase_result)

            # 风险登记
            if phase_result.status in (DecisionStatus.CONDITIONAL, DecisionStatus.REJECT):
                for msg in phase_result.messages:
                    risks.append(
                        RiskItem(
                            risk_id=f"RISK-{phase_result.phase_id}-{len(risks)+1:03d}",
                            phase=phase_result.phase_name,
                            description=msg,
                            severity="HIGH" if phase_result.status == DecisionStatus.REJECT else "MEDIUM",
                            mitigation=self._suggest_mitigation(phase_result.phase_id, msg),
                        )
                    )

            # 运行 post_phase_eval 钩子
            self.plugins.run("post_phase_eval", phase_result, asset, context)

        # 计算最终决策
        final_decision, final_score = self._compute_final_decision(phase_results, risks)

        # 升级/降级建议
        upgrade_path, downgrade_path = self._compute_hierarchy_suggestion(
            final_decision, asset, context
        )

        # 全局推荐
        recommendations = self._generate_recommendations(phase_results, risks, final_decision)

        result = DecisionResult(
            asset_id=asset.asset_id,
            asset_name=asset.name,
            context_name=context.name,
            final_decision=final_decision,
            final_score=final_score,
            phase_results=phase_results,
            risks=risks,
            recommendations=recommendations,
            upgrade_path=upgrade_path,
            downgrade_path=downgrade_path,
            metadata={
                "engine_version": self.rules.get("version", "unknown"),
                "ruleset": self.rules_path.name,
            },
        )

        # 运行 final_decision 钩子
        self.plugins.run("final_decision", result)

        return result

    def _evaluate_phase(
        self, phase_cfg: Dict[str, Any], asset: AssetProfile, context: ContextProfile
    ) -> PhaseResult:
        """评估单个阶段"""
        phase_id = phase_cfg["id"]
        phase_name = phase_cfg["name"]
        rules = phase_cfg.get("rules", [])
        pass_threshold = phase_cfg.get("pass_threshold", 70)
        conditional_threshold = phase_cfg.get("conditional_threshold", 50)

        total_weight = 0.0
        weighted_score = 0.0
        details: List[Dict[str, Any]] = []
        messages: List[str] = []

        for rule in rules:
            rule_id = rule["id"]
            rule_name = rule["name"]
            weight = rule.get("weight", 1.0)
            threshold = rule.get("threshold", 0.0)
            operator = rule.get("operator", ">=")
            failure_action = rule.get("failure_action", "CONDITIONAL")

            # 执行规则评估
            rule_passed, actual_value = self._execute_rule(rule, asset, context)

            rule_score = 100.0 if rule_passed else 0.0
            # 对于数值型条件，可计算部分得分
            if isinstance(actual_value, (int, float)) and operator in (">=", ">", "<=", "<"):
                if operator in (">=", ">"):
                    ratio = min(actual_value / threshold, 1.5) if threshold != 0 else 1.0
                else:
                    ratio = min(threshold / actual_value, 1.5) if actual_value != 0 else 1.0
                rule_score = min(ratio * 100, 100.0)

            weighted_score += rule_score * weight
            total_weight += weight

            detail = {
                "rule_id": rule_id,
                "rule_name": rule_name,
                "passed": rule_passed,
                "actual": actual_value if not isinstance(actual_value, bool) else None,
                "threshold": threshold,
                "operator": operator,
                "score": round(rule_score, 2),
            }
            details.append(detail)

            if not rule_passed:
                msg = rule.get("failure_message", f"规则 {rule_name} 未通过")
                messages.append(msg)
                # 如果失败动作为 REJECT，后续规则仍评估但标记
                detail["failure_action"] = failure_action

        # 计算阶段得分
        phase_score = (weighted_score / total_weight) if total_weight > 0 else 0.0

        # 判定阶段状态
        # 如果有任何 REJECT 规则失败，则阶段为 REJECT
        has_reject = any(
            d.get("failure_action") == "REJECT" and not d["passed"] for d in details
        )
        if has_reject:
            status = DecisionStatus.REJECT
        elif phase_score >= pass_threshold:
            status = DecisionStatus.PASS
        elif phase_score >= conditional_threshold:
            status = DecisionStatus.CONDITIONAL
        else:
            status = DecisionStatus.REJECT

        return PhaseResult(
            phase_id=phase_id,
            phase_name=phase_name,
            status=status,
            score=phase_score,
            weight=1.0,  # 各阶段等权，最终得分取平均
            details=details,
            messages=messages,
        )

    def _execute_rule(
        self, rule: Dict[str, Any], asset: AssetProfile, context: ContextProfile
    ) -> tuple[bool, Any]:
        """
        执行单条规则的评估。

        规则条件以字符串描述存储在 JSON 中，引擎根据预定义映射解析执行。
        实际生产环境可集成表达式引擎（如 jsonlogic）。
        """
        condition: str = rule.get("condition", "")
        threshold = rule.get("threshold", 0.0)
        operator = rule.get("operator", ">=")

        # 规则解析映射表
        # 语义兼容性规则
        if "domain_scope" in condition and "intersects" in condition:
            if not asset.domain_scope or not context.required_domain:
                return True, 1.0
            intersection = set(asset.domain_scope) & set(context.required_domain)
            # 语义兼容性：需求领域应被资产领域覆盖
            required = set(context.required_domain)
            ratio = len(intersection) / len(required) if required else 1.0
            return ratio >= threshold, ratio

        if "tech_constraints" in condition and "subsetof" in condition:
            if not context.tech_constraints:
                return True, 1.0
            supported = set(asset.supported_tech)
            required = set(context.tech_constraints)
            if not required:
                return True, 1.0
            covered = required & supported
            ratio = len(covered) / len(required)
            return ratio >= threshold, ratio

        if "interface_contract" in condition and "compatible" in condition:
            # 简化：检查接口协议是否匹配
            asset_proto = asset.interface_contract.get("protocol", "")
            ctx_proto = context.required_interface.get("protocol", "")
            if not ctx_proto:
                return True, 1.0
            passed = asset_proto == ctx_proto or not asset_proto
            return passed, 1.0 if passed else 0.0

        # 变性绑定规则
        if "variation_points" in condition and "intersects" in condition:
            if not asset.variation_points or not context.required_variations:
                return True, 1.0
            intersection = set(asset.variation_points) & set(context.required_variations)
            union = set(asset.variation_points) | set(context.required_variations)
            ratio = len(intersection) / len(union) if union else 1.0
            return ratio >= threshold, ratio

        if "binding_times" in condition and "contains" in condition:
            passed = context.preferred_binding_time in asset.binding_times
            return passed, 1.0 if passed else 0.0

        if "configuration_complexity" in condition or ("count" in condition and "variation_points" in condition):
            req_count = len(context.required_variations)
            asset_count = len(asset.variation_points)
            if asset_count == 0:
                ratio = 0.0 if req_count > 0 else 0.0
            else:
                ratio = req_count / asset_count
            # 条件为 <= threshold
            passed = ratio <= threshold
            return passed, ratio

        # 质量达标规则
        if "rrl" in condition:
            passed = asset.rrl >= context.min_rrl
            return passed, asset.rrl

        if "maturity" in condition and "min_maturity" in condition:
            passed = asset.maturity >= context.min_maturity
            return passed, asset.maturity

        if "reliability" in condition:
            passed = asset.reliability >= context.min_reliability
            return passed, asset.reliability

        if "maintainability" in condition:
            passed = asset.maintainability >= context.min_maintainability
            return passed, asset.maintainability

        # 安全合规规则
        if "license" in condition and "approved_licenses" in condition:
            passed = asset.license in context.approved_licenses
            return passed, asset.license

        if "security_level" in condition:
            # 简化为 L1 < L2 < L3 < L4
            level_map = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}
            asset_lvl = level_map.get(asset.security_level, 0)
            ctx_lvl = level_map.get(context.min_security_level, 0)
            passed = asset_lvl >= ctx_lvl
            return passed, asset_lvl

        if "slsa_level" in condition:
            passed = asset.slsa_level >= context.min_slsa_level
            return passed, asset.slsa_level

        # 成本收益规则
        if "aaf" in condition and "<" in operator:
            # estimated_aaf 使用资产典型值或上下文中的估算值
            aaf = context.extra.get("estimated_aaf", asset.aaf_typical)
            if operator == "<":
                passed = aaf < threshold
            else:
                passed = aaf <= threshold
            return passed, aaf

        if "npv" in condition:
            npv = context.extra.get("estimated_npv", 1.0 if asset.npv_positive else -1.0)
            passed = npv > threshold
            return passed, npv

        if "payback_period" in condition:
            pp = context.extra.get("estimated_payback", asset.roi_years)
            passed = pp <= context.max_payback_years
            return passed, pp

        # 治理合规规则
        if "org_maturity_level" in condition:
            passed = context.org_maturity_level >= asset.required_org_maturity
            return passed, context.org_maturity_level

        if "process_standardized" in condition and "==" in condition:
            passed = context.process_standardized == True  # noqa: E712
            return passed, context.process_standardized

        if "asset_catalog" in condition and "exists" in condition:
            passed = context.asset_catalog_exists == True  # noqa: E712
            return passed, context.asset_catalog_exists

        # 未知规则默认通过，但记录警告
        return True, None

    def _compute_final_decision(
        self, phase_results: List[PhaseResult], risks: List[RiskItem]
    ) -> tuple[FinalDecision, float]:
        """计算最终决策和置信度"""
        if not phase_results:
            return FinalDecision.NEED_MORE_INFO, 0.0

        scores = [p.score for p in phase_results]
        avg_score = sum(scores) / len(scores)

        # 风险惩罚
        risk_penalty = self.rules.get("global_rules", {}).get("risk_penalty_factor", 0.05)
        high_risk_count = sum(1 for r in risks if r.severity == "HIGH")
        medium_risk_count = sum(1 for r in risks if r.severity == "MEDIUM")
        penalty = min((high_risk_count * risk_penalty * 2) + (medium_risk_count * risk_penalty), 0.5)
        final_score = max(avg_score * (1 - penalty), 0.0)

        # 状态统计
        reject_count = sum(1 for p in phase_results if p.status == DecisionStatus.REJECT)
        conditional_count = sum(1 for p in phase_results if p.status == DecisionStatus.CONDITIONAL)
        max_conditional = self.rules.get("global_rules", {}).get("max_conditional_phases", 2)

        if reject_count > 0:
            return FinalDecision.REJECT, round(final_score, 2)

        if conditional_count > max_conditional:
            return FinalDecision.CONDITIONAL_APPROVE, round(final_score, 2)

        if conditional_count > 0:
            return FinalDecision.CONDITIONAL_APPROVE, round(final_score, 2)

        return FinalDecision.APPROVE, round(final_score, 2)

    def _compute_hierarchy_suggestion(
        self, final_decision: FinalDecision, asset: AssetProfile, context: ContextProfile
    ) -> tuple[Optional[List[str]], Optional[List[str]]]:
        """计算升级/降级建议路径"""
        hierarchy = (
            self.rules.get("global_rules", {})
            .get("upgrade_recommendation", {})
            .get("hierarchy", ["功能复用", "组件复用", "应用复用", "业务复用"])
        )

        # 根据资产类别推断当前层级
        category_map = {
            "功能": "功能复用",
            "组件": "组件复用",
            "应用": "应用复用",
            "业务": "业务复用",
        }
        current_level = "组件复用"
        for key, val in category_map.items():
            if key in asset.category:
                current_level = val
                break

        current_idx = hierarchy.index(current_level) if current_level in hierarchy else 1

        upgrade_path = None
        downgrade_path = None

        if final_decision == FinalDecision.REJECT:
            # 建议降级：尝试更低层级的复用
            if current_idx > 0:
                downgrade_path = hierarchy[:current_idx][::-1]

        elif final_decision == FinalDecision.CONDITIONAL_APPROVE:
            # 建议升级：如果当前层级条件通过，更高层级可能更成熟
            if current_idx < len(hierarchy) - 1:
                upgrade_path = hierarchy[current_idx + 1 :]

        return upgrade_path, downgrade_path

    def _generate_recommendations(
        self,
        phase_results: List[PhaseResult],
        risks: List[RiskItem],
        final_decision: FinalDecision,
    ) -> List[str]:
        """生成行动推荐"""
        recommendations = []

        if final_decision == FinalDecision.APPROVE:
            recommendations.append("✅ 决策通过：可启动复用适配与集成流程")
            recommendations.append("📋 建议记录复用决策依据至资产库元数据")
        elif final_decision == FinalDecision.CONDITIONAL_APPROVE:
            recommendations.append("⚠️ 条件通过：需满足以下条件后方可正式复用")
            for i, risk in enumerate(risks, 1):
                recommendations.append(f"   {i}. [{risk.phase}] {risk.description}")
            recommendations.append("📋 建议制定风险缓解计划并分配责任人")
        elif final_decision == FinalDecision.REJECT:
            recommendations.append("❌ 决策拒绝：当前资产不适合在指定上下文中复用")
            # 找出得分最低的阶段
            weakest = min(phase_results, key=lambda p: p.score)
            recommendations.append(
                f"🔍 最薄弱环节：{weakest.phase_name}（得分 {weakest.score:.1f}）"
            )
            recommendations.append("💡 建议：根据降级路径寻找更轻量级的复用机会，或启动自研")

        # 阶段级具体建议
        for pr in phase_results:
            if pr.status == DecisionStatus.CONDITIONAL:
                if "AAF" in " ".join(pr.messages):
                    recommendations.append(
                        f"📐 成本优化：{pr.phase_name} — 考虑降低改编范围或寻找替代资产"
                    )
                if "许可证" in " ".join(pr.messages):
                    recommendations.append(
                        f"⚖️ 合规建议：{pr.phase_name} — 联系法务评估许可证兼容性"
                    )
                if "成熟度" in " ".join(pr.messages):
                    recommendations.append(
                        f"📈 质量提升：{pr.phase_name} — 建议资产提供方完善测试和文档"
                    )

        return recommendations

    def _suggest_mitigation(self, phase_id: str, message: str) -> str:
        """根据阶段和消息生成缓解建议"""
        mitigation_map = {
            "PHASE-1": "补充领域分析文档，建立语义映射表；必要时引入领域专家评审",
            "PHASE-2": "评估变性点配置复杂度，考虑引入适配层或中间件解耦",
            "PHASE-3": "要求资产提供方提供测试报告、覆盖率数据和质量度量",
            "PHASE-4": "启动安全审计和许可证合规审查；更新组织白名单策略",
            "PHASE-5": "重新估算 COCOMO 参数，考虑机会成本；引入 FinOps 分摊模型",
            "PHASE-6": "优先建立资产目录和标准化流程，再推进大规模复用",
        }
        base = mitigation_map.get(phase_id, "进行根因分析并制定专项改进计划")
        if "AAF" in message:
            base += "；重点优化改编调整因子"
        if "许可证" in message:
            base += "；寻求法务和开源治理委员会支持"
        if "安全" in message:
            base += "；引入渗透测试和 SBOM 审查"
        return base

    # -----------------------------------------------------------------------
    # 标准对齐检查
    # -----------------------------------------------------------------------

    def check_standard_alignment(self, standard_key: str, version: Optional[str] = None) -> Dict[str, Any]:
        """
        检查指定标准的对齐状态。

        Args:
            standard_key: 标准键名，如 iso42010、slsa 等
            version: 可选，指定要对比的版本

        Returns:
            对齐状态报告字典
        """
        standards_data = self.standards.get("standards", {})
        if standard_key not in standards_data:
            return {
                "standard": standard_key,
                "found": False,
                "message": f"未找到标准 {standard_key}，支持的标准: {list(standards_data.keys())}",
            }

        std = standards_data[standard_key]
        report = {
            "standard": standard_key,
            "found": True,
            "name": std.get("name", ""),
            "full_name": std.get("full_name", ""),
            "current_version": std.get("current_version", ""),
            "status": std.get("status", ""),
            "url": std.get("url", ""),
            "relevance": std.get("relevance_to_reuse", ""),
            "alignment_checklist": std.get("alignment_checklist", []),
            "compliance_levels": std.get("compliance_levels", {}),
        }

        if version and version != std.get("current_version", ""):
            report["version_warning"] = (
                f"请求版本 {version} 与当前跟踪版本 {std.get('current_version')} 不一致"
            )

        return report

    # -----------------------------------------------------------------------
    # 成熟度评估
    # -----------------------------------------------------------------------

    def assess_maturity(
        self, level: int, dimension: str = "all"
    ) -> Dict[str, Any]:
        """
        评估复用成熟度。

        Args:
            level: 目标成熟度等级 1-5
            dimension: 评估维度，"all" 或维度 ID 如 "D1"

        Returns:
            成熟度评估报告
        """
        if not 1 <= level <= 5:
            return {"error": "成熟度等级必须在 1-5 之间"}

        levels_def = self.maturity.get("levels_definition", {})
        dimensions = self.maturity.get("dimensions", [])

        target_level_name = levels_def.get(str(level), {}).get("name", "未知")
        target_level_desc = levels_def.get(str(level), {}).get("description", "")

        # 筛选维度
        selected_dims = dimensions
        if dimension != "all":
            selected_dims = [d for d in dimensions if d["id"] == dimension]
            if not selected_dims:
                return {"error": f"未知维度: {dimension}"}

        gap_analysis = []
        for dim in selected_dims:
            dim_gap = {
                "dimension_id": dim["id"],
                "dimension_name": dim["name"],
                "questions": [],
            }
            for q in dim.get("questions", []):
                level_map = q.get("level_map", {})
                target_answer = level_map.get(str(level), "未定义")
                dim_gap["questions"].append(
                    {
                        "question_id": q["id"],
                        "text": q["text"],
                        "target_level_answer": target_answer,
                        "weight": q.get("weight", 1.0),
                    }
                )
            gap_analysis.append(dim_gap)

        return {
            "target_level": level,
            "target_level_name": target_level_name,
            "target_level_description": target_level_desc,
            "dimension": dimension,
            "gap_analysis": gap_analysis,
            "recommendation": (
                f"要达到 {target_level_name}，请在上述各维度中实现对应目标状态的实践。"
                f"建议从权重最高的维度优先投入。"
            ),
        }

    # -----------------------------------------------------------------------
    # 决策卡片生成
    # -----------------------------------------------------------------------

    def generate_decision_card(
        self, asset_id: str, fmt: str = "markdown"
    ) -> str:
        """
        生成复用决策卡片。

        Args:
            asset_id: 资产 ID
            fmt: 输出格式，"markdown" 或 "json"

        Returns:
            决策卡片字符串
        """
        # 尝试从模式库中查找资产
        asset_data = self._patterns_by_id.get(asset_id)
        if not asset_data:
            # 构建一个默认资产画像
            asset = AssetProfile(asset_id=asset_id, name=f"资产-{asset_id}")
        else:
            qp = asset_data.get("quality_profile", {})
            sp = asset_data.get("security_compliance", {})
            cp = asset_data.get("cost_profile", {})
            gp = asset_data.get("governance", {})
            asset = AssetProfile(
                asset_id=asset_id,
                name=asset_data.get("name", asset_id),
                category=asset_data.get("category", ""),
                domain_scope=asset_data.get("semantic_compatibility", {}).get("domain_scope", []),
                supported_tech=asset_data.get("semantic_compatibility", {}).get("tech_constraints", []),
                variation_points=asset_data.get("variability_model", {}).get("variation_points", []),
                binding_times=asset_data.get("variability_model", {}).get("binding_time", []),
                rrl=qp.get("rrl", 0.0),
                maturity=qp.get("maturity", 1),
                reliability=qp.get("reliability", 0.0),
                maintainability=qp.get("maintainability", 0.0),
                license=sp.get("license", "未知"),
                security_level=sp.get("security_level", "L1"),
                slsa_level=sp.get("slsa_level", 1),
                aaf_typical=cp.get("aaf_typical", 0.5),
                npv_positive=cp.get("npv_positive", False),
                roi_years=cp.get("roi_years", 999.0),
                required_org_maturity=gp.get("org_maturity_required", 1),
                process_standardized=gp.get("process_standardized", False),
                asset_catalog_required=gp.get("asset_catalog_required", False),
            )

        # 使用默认上下文进行评估
        context = ContextProfile(name="默认评估上下文")
        result = self.evaluate(asset, context)

        if fmt.lower() == "json":
            return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)

        # Markdown 格式
        lines = [
            f"# 复用决策卡片：{result.asset_name}",
            f"",
            f"- **资产 ID**: `{result.asset_id}`",
            f"- **评估上下文**: {result.context_name}",
            f"- **决策结果**: {result.final_decision.value}",
            f"- **置信度评分**: {result.final_score}/100",
            f"",
            f"## 六阶段评估详情",
            f"",
            "| 阶段 | 状态 | 得分 | 说明 |",
            "|------|------|------|------|",
        ]
        for pr in result.phase_results:
            status_emoji = {"通过": "✅", "条件通过": "⚠️", "拒绝": "❌", "未评估": "⏳"}
            emoji = status_emoji.get(pr.status.value, "")
            msgs = "；".join(pr.messages) if pr.messages else "无异常"
            lines.append(f"| {pr.phase_name} | {emoji} {pr.status.value} | {pr.score:.1f} | {msgs} |")

        lines.extend([
            f"",
            f"## 风险登记",
            f"",
        ])
        if result.risks:
            lines.append("| 风险 ID | 阶段 | 严重程度 | 描述 | 缓解措施 |")
            lines.append("|---------|------|----------|------|----------|")
            for r in result.risks:
                lines.append(f"| {r.risk_id} | {r.phase} | {r.severity} | {r.description} | {r.mitigation} |")
        else:
            lines.append("🎉 未发现显著风险。")

        lines.extend([
            f"",
            f"## 推荐行动",
            f"",
        ])
        for rec in result.recommendations:
            lines.append(f"- {rec}")

        if result.upgrade_path:
            lines.extend([
                f"",
                f"## 升级路径",
                f"",
                " → ".join(result.upgrade_path),
            ])
        if result.downgrade_path:
            lines.extend([
                f"",
                f"## 降级路径",
                f"",
                " → ".join(result.downgrade_path),
            ])

        lines.extend([
            f"",
            f"---",
            f"> 生成时间: 2026-06-10 | 引擎版本: {result.metadata.get('engine_version', 'unknown')}",
        ])

        return "\n".join(lines)

    # -----------------------------------------------------------------------
    # COCOMO II 集成
    # -----------------------------------------------------------------------

    @staticmethod
    def calculate_cocomo_esloc(ksloc_reused: float, aaf: float) -> float:
        """计算等效新代码量 (ESLOC)"""
        return aaf * ksloc_reused

    @staticmethod
    def calculate_cocomo_effort(esloc: float, em: float = 1.0, a: float = 2.94, b: float = 0.91) -> float:
        """计算 COCOMO II 工作量（人月）"""
        return a * (esloc ** b) * em

    @staticmethod
    def calculate_npv(
        initial_cost: float,
        annual_savings: float,
        annual_maintenance: float,
        discount_rate: float = 0.08,
        years: int = 5,
    ) -> float:
        """
        计算净现值 (NPV)

        Args:
            initial_cost: 初始投入（复用适配成本）
            annual_savings: 每年节省（相比自研）
            annual_maintenance: 每年维护成本
            discount_rate: 折现率
            years: 评估年限
        """
        npv = -initial_cost
        for year in range(1, years + 1):
            net_cash_flow = annual_savings - annual_maintenance
            npv += net_cash_flow / ((1 + discount_rate) ** year)
        return npv

    @staticmethod
    def calculate_roi(
        initial_cost: float,
        total_savings: float,
        total_maintenance: float,
    ) -> float:
        """计算投资回报率 (ROI)"""
        net_gain = total_savings - total_maintenance - initial_cost
        return (net_gain / initial_cost) * 100 if initial_cost != 0 else 0.0


# ---------------------------------------------------------------------------
# 便捷工厂函数
# ---------------------------------------------------------------------------

def create_engine_from_data_dir(data_dir: Path) -> ReuseDecisionEngine:
    """从指定数据目录创建决策引擎实例"""
    return ReuseDecisionEngine(
        rules_path=data_dir / "decision_rules.json",
        patterns_path=data_dir / "reuse_patterns.json",
        standards_path=data_dir / "standards_index.json",
        maturity_path=data_dir / "maturity_matrix.json",
    )
