# 复用决策报告：{{ asset_name }}

> **报告类型**: 六阶段复用决策评估
> **生成引擎**: 复用决策引擎 v{{ engine_version }}
> **生成时间**: {{ generation_time }}

---

## 基本信息

| 属性 | 值 |
|------|-----|
| 资产 ID | `{{ asset_id }}` |
| 资产名称 | {{ asset_name }} |
| 评估上下文 | {{ context_name }} |
| 最终决策 | **{{ final_decision }}** |
| 置信度评分 | {{ final_score }}/100 |

---

## 执行摘要

{% if final_decision == "批准复用" %}
✅ **建议批准复用**。该资产在六阶段评估中表现良好，风险可控，符合组织复用策略。
{% elif final_decision == "条件批准" %}
⚠️ **条件批准复用**。该资产基本满足复用要求，但存在需要关注的风险项。建议在满足以下条件后正式复用：
{% for risk in risks %}

- [ ] **{{ risk.phase }}**: {{ risk.description }} — {{ risk.mitigation }}
{% endfor %}
{% else %}
❌ **建议拒绝复用**。该资产在当前上下文中不适合复用，主要问题包括：
{% for phase in phase_results %}
{% if phase.status == "拒绝" %}
- **{{ phase.phase_name }}**: {{ phase.messages | join("；") }}
{% endif %}
{% endfor %}
{% endif %}

---

## 六阶段评估详情

### 评估矩阵

| 阶段 | 状态 | 得分 | 权重 | 关键信息 |
|------|------|------|------|----------|
{% for phase in phase_results %}
| {{ phase.phase_name }} | {{ phase.status }} | {{ phase.score | round(1) }} | {{ phase.weight }} | {{ phase.messages | join("；") or "—" }} |
{% endfor %}

### 阶段规则明细

{% for phase in phase_results %}

#### {{ phase.phase_id }} — {{ phase.phase_name }} ({{ phase.status }}, 得分: {{ phase.score | round(1) }})

{% for detail in phase.details %}

- **{{ detail.rule_name }}** (`{{ detail.rule_id }}`)
  - 结果: {% if detail.passed %}✅ 通过{% else %}❌ 未通过{% endif %}
  - 实际值: `{{ detail.actual }}`
  - 阈值: `{{ detail.threshold }} {{ detail.operator }}`
  - 规则得分: {{ detail.score | round(1) }}
{% endfor %}

{% endfor %}

---

## 风险登记 (Risk Register)

{% if risks %}

| 风险 ID | 阶段 | 严重程度 | 描述 | 缓解措施 | 责任人 |
|---------|------|----------|------|----------|--------|
{% for risk in risks %}
| {{ risk.risk_id }} | {{ risk.phase }} | {{ risk.severity }} | {{ risk.description }} | {{ risk.mitigation }} | {{ risk.owner }} |
{% endfor %}
{% else %}
🎉 本次评估未发现显著风险项。
{% endif %}

---

## 推荐行动

{% for rec in recommendations %}
{{ loop.index }}. {{ rec }}
{% endfor %}

---

## 复用层级建议

{% if upgrade_path %}

### ⬆️ 升级路径

当前资产可考虑向更高层级复用演进：

```
{{ upgrade_path | join(" → ") }}
```

{% endif %}

{% if downgrade_path %}

### ⬇️ 降级路径

若当前层级复用受阻，可考虑更轻量级的复用方式：

```
{{ downgrade_path | join(" → ") }}
```

{% endif %}

---

## 附录

### A. 术语说明

- **RRL**: Reuse Readiness Level，复用准备度 (0-5)
- **AAF**: Adaptation Adjustment Factor，改编调整因子 (0-1)
- **NPV**: Net Present Value，净现值
- **SLSA**: Supply-chain Levels for Software Artifacts
- **MCP**: Model Context Protocol

### B. 参考标准

- ISO/IEC/IEEE 42010:2022 — Architecture description
- ISO/IEC 25010:2023 — SQuaRE Quality Models
- ISO/IEC 26566:2026 — Reuse Maturity Assessment
- NASA Reuse Readiness Levels (RRL)

### C. 报告元数据

| 属性 | 值 |
|------|-----|
| 规则集文件 | {{ ruleset }} |
| 引擎版本 | {{ engine_version }} |
| 评估资产数 | 1 |
| 评估阶段数 | 6 |

---

> **声明**: 本报告由复用决策引擎自动生成，仅供决策参考。最终复用决策应结合团队专业判断和实际项目约束。


---

## 补充说明：复用决策报告：{{ asset_name }}

## 示例

**示例**：维护 authoritative-sources.md 登记所有 ISO/IEC、IEEE、NIST、CNCF 来源 URL 与核查日期，确保全书引用可验证。

## 反例

**反例**：参考层链接长期不更新，术语表与正文定义冲突，读者无法确认内容准确性与时效性。

## 权威来源

> **权威来源**:
>
> - [ISO](https://www.iso.org)
> - [IEEE Standards](https://standards.ieee.org)
> - [NIST](https://www.nist.gov)
> - [CNCF](https://www.cncf.io)
> - 核查日期：2026-07-07

## 分析

**分析**：参考层的价值不在于内容本身，而在于建立知识之间的信任锚点；必须随标准演进定期审计与更新。
