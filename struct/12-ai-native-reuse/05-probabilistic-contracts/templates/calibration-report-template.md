# 概率契约校准报告模板

> **报告 ID**：`{report_id}`
> **生成时间**：`{generated_at}`
> **契约 ID**：`{contract_id}`
> **模型版本**：`{model_version}`

---

## 1. 数据摘要

| 指标 | 数值 |
|------|------|
| 校准样本量 | `{calibration_size}` |
| 目标错误率 α | `{alpha}` |
| 目标覆盖率 `1 − α` | `{target_coverage}` |
| 正例比例（正确样本） | `{positive_rate}` |
| 平均预测分数 | `{mean_prediction_score}` |
| 平均温度 | `{avg_temperature}` |
| 平均 Top-p | `{avg_top_p}` |
| 模型版本分布 | `{model_versions}` |

---

## 2. 校准结果

### 2.1 Conformal 边界

```text
{contract_boundary}
```

| 指标 | 数值 |
|------|------|
| Conformal 阈值 q | `{q}` |
| 经验覆盖率 | `{empirical_coverage}` |
| 平均预测集合大小 | `{avg_prediction_set_size}` |

### 2.2 校准质量指标

| 指标 | 数值 | 说明 |
|------|------|------|
| ECE（Expected Calibration Error） | `{ece}` | 期望校准误差，越小越好 |
| Brier Score | `{brier_score}` | 概率预测综合误差，越小越好 |
| Brier 分解 - 可靠性 | `{brier_reliability}` | 校准曲线与对角线的偏离 |
| Brier 分解 - 分辨率 | `{brier_resolution}` | 区分不同类别的能力 |
| Brier 分解 - 不确定性 | `{brier_uncertainty}` | 数据本身的随机性 |

---

## 3. Reliability Diagram 数据

以下按预测概率等宽分桶，展示每个桶内的平均预测分数与实际准确率：

| Bin 区间 | 样本数 | 平均预测分数 | 实际准确率 | 置信度-准确率偏差 |
|----------|--------|--------------|------------|-------------------|
| `{bin_1}` | `{count_1}` | `{avg_conf_1}` | `{acc_1}` | `{gap_1}` |
| `{bin_2}` | `{count_2}` | `{avg_conf_2}` | `{acc_2}` | `{gap_2}` |
| ... | ... | ... | ... | ... |

> 理想情况下，所有行的“置信度-准确率偏差”应接近 0，即平均预测分数 ≈ 实际准确率。

---

## 4. 分层校准（可选）

按 `{stratify_by}` 分层后的校准结果：

| 分层值 | 样本量 | ECE | Brier Score | 经验覆盖率 | 推荐 q |
|--------|--------|-----|-------------|------------|--------|
| `{stratum_1}` | `{n_1}` | `{ece_1}` | `{brier_1}` | `{cov_1}` | `{q_1}` |
| `{stratum_2}` | `{n_2}` | `{ece_2}` | `{brier_2}` | `{cov_2}` | `{q_2}` |
| ... | ... | ... | ... | ... | ... |

---

## 5. 覆盖率分析

| 指标 | 数值 |
|------|------|
| 预测集合为 `[1]`（接受）的样本比例 | `{accept_rate}` |
| 预测集合为 `[0]`（拒绝）的样本比例 | `{reject_rate}` |
| 预测集合为 `[0, 1]`（不确定）的样本比例 | `{uncertain_rate}` |
| 人在回路触发比例 | `{human_in_loop_rate}` |

---

## 6. 推荐阈值

基于本次校准数据，推荐以下运行时阈值：

| 阈值类型 | 推荐值 | 依据 |
|----------|--------|------|
| 置信度基线 γ_base | `{recommended_gamma_base}` | 目标覆盖率与 ECE 平衡 |
| 人在回路阈值 θ_hitl | `{recommended_hitl_threshold}` | `C_review / C_error` 或不确定性区间比例 |
| 硬违约阈值 δ_hard | `{recommended_hard_delta}` | 生产关键路径容忍度 |
| 软违约阈值 δ_soft | `{recommended_soft_delta}` | 非关键路径容忍度 |
| 推荐 temperature | `{recommended_temperature}` | 确定性需求 |
| 推荐 top_p | `{recommended_top_p}` | 确定性需求 |

---

## 7. 结论与建议

### 7.1 结论

```text
{conclusion_summary}
```

### 7.2 后续行动

| 优先级 | 行动项 | 负责人 | 截止日期 |
|--------|--------|--------|----------|
| P0 | 将校准阈值 q 写入契约 YAML | 平台工程师 | `{due_date_1}` |
| P1 | 部署运行时监控面板 | SRE | `{due_date_2}` |
| P2 | 按推荐阈值配置告警规则 | 值班工程师 | `{due_date_3}` |
| P2 | 纳入下一次再校准周期 | 数据科学家 | `{due_date_4}` |

---

## 8. 附录

### 8.1 指标计算公式

**ECE（等宽分桶，默认 10 桶）**：

```text
ECE = Σ_{b=1}^{B} (n_b / N) |acc(b) − conf(b)|
```

**Brier Score**：

```text
Brier = (1 / N) Σ_{i=1}^{N} (p_i − y_i)^2
```

**可靠性分解**：

```text
Brier = Reliability − Resolution + Uncertainty
```

### 8.2 参考文档

- 概率契约框架：`probabilistic-contract-framework.md`
- 校准工具 CLI：`calibration-tool.py`
- SLA 模板：`templates/ai-sla-template.md`


---

## 补充说明：概率契约校准报告模板

## 概念定义

**定义**：AI 原生复用是在大模型与 Agent 系统中，通过 MCP（Model Context Protocol）、A2A（Agent-to-Agent Protocol）与概率契约，将提示模板、RAG 管道、工具与 Agent 技能封装为可组合、可治理的资产。

## 示例

**示例**：企业构建 MCP 工具目录，把数据库查询、代码检索、文档解析发布为标准工具；客服 Agent 与运维 Agent 按统一协议调用，避免各自封装重复能力。

## 反例

**反例**：各团队在不同 Agent 中硬编码相同 Prompt 与 API 调用，无版本管理与输出契约，导致行为不一致、成本失控且难以审计。

## 权威来源

> **权威来源**:
>
> - [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25)
> - [A2A Protocol](https://google.github.io/A2A)
> - [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/)
> - 核查日期：2026-07-07