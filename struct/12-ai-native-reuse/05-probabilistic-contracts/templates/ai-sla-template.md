# AI 功能服务等级协议（SLA）模板

> **用途**：将概率契约转换为可对外承诺或内部治理的服务等级目标。
> **版本**：2026-06-12

---

## 1. 服务概述

| 项目 | 内容 |
|------|------|
| 服务名称 | `{service_name}` |
| 服务描述 | `{service_description}` |
| 契约 ID | `{contract_id}` |
| 责任团队 | `{owner_team}` |
| 生效日期 | `{effective_date}` |
| 复核周期 | `{review_cycle}`（建议每 7–30 天复核一次） |

---

## 2. 服务等级目标（SLO）

| SLO 项 | 目标值 | 测量方法 | 观测窗口 |
|--------|--------|----------|----------|
| 正确率（Correctness） | `≥ {correctness_rate}` | 人工/规则/验证器判定输出正确 | 1 天 / 7 天 / 30 天 |
| 可用性（Availability） | `≥ {availability}` | 服务成功响应比例 | 30 天 |
| 延迟 P99（Latency） | `≤ {latency_p99_ms} ms` | 端到端调用耗时 | 1 天 |
| 低置信度比例（Low Confidence Rate） | `≤ {low_confidence_rate}` | `γ(x) < θ_hitl` 的调用占比 | 7 天 |
| 人在回路比例（Human-in-the-Loop Rate） | `≤ {human_in_the_loop_rate}` | 触发人工复核的调用占比 | 7 天 |
| 校准误差 ECE | `≤ {max_ece}` | 按置信度分桶计算 | 7 天 |

---

## 3. 概率契约参数

| 参数 | 设定值 | 说明 |
|------|--------|------|
| 模型版本 | `{model_version}` | 版本变更需重新校准 |
| Temperature | `{temperature}` | 关键任务建议 ≤ 0.2 |
| Top-p | `{top_p}` | 与 temperature 联合约束 |
| 目标覆盖率 `1 − α` | `{target_coverage}` | 由 Conformal Prediction 保证 |
| 置信度基线 `γ_base` | `{base_gamma}` | 综合复杂度与熟悉度后调整 |

---

## 4. 违约阈值

### 4.1 硬阈值（Hard Breach）

```text
触发条件：empirical_correctness < correctness_rate − {hard_delta}
```

| 触发动作 | 责任方 | 恢复时间目标（RTO） |
|----------|--------|---------------------|
| 立即熔断 / 拒绝复用 | 平台团队 | 15 分钟 |
| 切换至备用模型或人工兜底 | 值班工程师 | 30 分钟 |
| 生成事故报告并归档 | SRE | 24 小时 |

### 4.2 软阈值（Soft Breach）

```text
触发条件：correctness_rate − {soft_delta} ≤ empirical_correctness < correctness_rate − {hard_delta}
```

| 触发动作 | 责任方 | 处理时限 |
|----------|--------|----------|
| 增加一致性检查或重新采样 | 模型团队 | 1 小时 |
| 降低置信度并扩大人在回路范围 | 产品团队 | 4 小时 |
| 纳入下次校准周期重点观察 | 数据团队 | 7 天 |

### 4.3 人在回路阈值

```text
触发条件：γ(x) < {human_in_the_loop_threshold} 或 prediction_set = {0, 1}
```

| 动作 | 说明 |
|------|------|
| 强制人工复核 | 输出在上线或提交前必须经过人工确认 |
| 记录复核结果 | 用于下一轮校准与模型改进 |
| 动态调整 θ | 每月根据 C_review / C_error 重新计算 |

---

## 5. 错误预算

```text
月度错误预算 = (1 − correctness_rate) × 月度总调用量
            = {error_budget} × {monthly_volume}
```

错误预算消耗达以下比例时触发治理动作：

| 消耗比例 | 动作 |
|----------|------|
| 50% | 发送预警通知 |
| 75% | 冻结非紧急功能发布 |
| 100% | 启动熔断或降级策略 |

---

## 6. 补偿与问责

| 违约级别 | 条件 | 补偿/问责 |
|----------|------|-----------|
| 轻微 | 单日内 SLO 未达成但仍在错误预算内 | 记录事件，无需补偿 |
| 中等 | 连续 3 日未达成或单月错误预算超支 | 服务积分/延迟修复承诺 |
| 严重 | 硬阈值触发导致生产事故 | 事故复盘 + 改进计划 |

---

## 7. 复核与更新

| 触发条件 | 动作 |
|----------|------|
| 模型版本升级 | 7 天内重新校准并更新 SLO 基线 |
| 输入分布显著漂移 | 触发漂移检测流程，必要时重新校准 |
| 季度复盘 | 评审 SLO 达成率、错误预算消耗、违约记录 |

---

## 8. 附录

### 8.1 术语

- **SLO（Service Level Objective）**：服务等级目标，量化服务应达到的质量水平。
- **SLA（Service Level Agreement）**：服务等级协议，包含违约条件与补偿条款。
- **ECE（Expected Calibration Error）**：期望校准误差，衡量置信度与实际准确率的对齐程度。
- **HitL（Human-in-the-Loop）**：人在回路，低置信度或不确定输出的人工复核机制。

### 8.2 参考文档

- 概率契约框架：`probabilistic-contract-framework.md`
- 校准工具：`calibration-tool.py`
- 监控指标：`monitoring-metrics.md`


---

## 补充说明：AI 功能服务等级协议（SLA）模板

## 示例

**示例**：某 LLM 分类服务承诺 P(准确率>0.92)≥0.95，使用 conformal prediction 计算预测集，并在运行时监控漂移触发重新校准。

## 反例

**反例**：将 LLM 输出直接接入关键业务规则而无置信度边界，错误分类导致合规罚款。

## 权威来源

> **权威来源**:
>
> - [Conformal Prediction](https://arxiv.org/abs/2107.07511)
> - [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25)
> - 核查日期：2026-07-07

## 分析

**分析**：概率契约将非确定性转化为可度量的风险边界，是 AI 服务等级协议的核心。
