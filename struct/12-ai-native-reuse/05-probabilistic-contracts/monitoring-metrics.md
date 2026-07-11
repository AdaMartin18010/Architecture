# 概率契约运行时监控指标

> **定位**：定义 AI 功能复用概率契约在运行时应当采集、告警与可视化的核心指标。
> **版本**：2026-06-12

---

## 1. 指标总览

| 指标名 | 类型 | 标签 | 说明 |
|--------|------|------|------|
| `ai_contract_coverage` | Gauge | `contract_id`, `model_version`, `temperature`, `top_p` | 经验覆盖率，目标 `≥ 1 − α` |
| `ai_contract_calibration_error_ece` | Gauge | `contract_id`, `model_version`, `bin_strategy` | 期望校准误差（ECE） |
| `ai_contract_brier_score` | Gauge | `contract_id`, `model_version` | Brier Score |
| `ai_contract_prediction_set_size` | Histogram / Summary | `contract_id`, `model_version` | 预测集合大小（1/2/不确定） |
| `ai_contract_model_drift_ks_stat` | Gauge | `contract_id`, `baseline_version`, `current_version` | KS 统计量 |
| `ai_contract_model_drift_p_value` | Gauge | `contract_id`, `baseline_version`, `current_version` | KS 检验 p-value |
| `ai_contract_low_confidence_rate` | Gauge | `contract_id`, `model_version` | 低置信度调用比例 |
| `ai_contract_human_in_the_loop_rate` | Gauge | `contract_id`, `model_version` | 触发人在回路的比例 |
| `ai_contract_total_invocations` | Counter | `contract_id`, `model_version`, `result` | 总调用次数（按结果分面） |
| `ai_contract_latency_seconds` | Histogram / Summary | `contract_id`, `model_version` | 端到端调用耗时 |

---

## 2. 指标详细定义

### 2.1 contract_coverage

```text
ai_contract_coverage = 正确调用数 / 总调用数
```

在观测窗口内，模型输出正确的调用占比。应与概率契约中的 `γ(x)` 对齐。

**告警规则示例**：

```yaml
alert: ContractCoverageBreach
expr: ai_contract_coverage < 0.90
for: 5m
labels:
  severity: critical
annotations:
  summary: "AI contract {{ $labels.contract_id }} coverage below SLO"
```

### 2.2 calibration_error_ece

```text
ECE = Σ_{b=1}^{B} (n_b / N) |acc(b) − conf(b)|
```

按预测概率等宽分桶（默认 10 桶），计算每个桶内平均预测分数与实际准确率的加权绝对偏差。

**告警规则示例**：

```yaml
alert: HighCalibrationError
expr: ai_contract_calibration_error_ece > 0.05
for: 10m
labels:
  severity: warning
annotations:
  summary: "AI contract {{ $labels.contract_id }} ECE too high"
```

### 2.3 brier_score

```text
Brier = (1 / N) Σ_{i=1}^{N} (p_i − y_i)^2
```

综合衡量概率预测准确性的评分，取值范围 `[0, 1]`，越小越好。

### 2.4 prediction_set_size

记录每次调用生成的 Conformal 预测集合大小：

- `1`：接受（`[1]`）或拒绝（`[0]`）
- `2`：不确定（`[0, 1]`）

可进一步细分为：

```text
ai_contract_prediction_set_size{decision="accept"}
ai_contract_prediction_set_size{decision="reject"}
ai_contract_prediction_set_size{decision="uncertain"}
```

### 2.5 model_drift_ks_stat / model_drift_p_value

使用 Kolmogorov-Smirnov 检验比较基线模型与新模型的非一致性分数分布：

```text
ai_contract_model_drift_ks_stat = D_statistic
ai_contract_model_drift_p_value = p_value
```

**告警规则示例**：

```yaml
alert: ModelDriftDetected
expr: ai_contract_model_drift_p_value < 0.05
for: 5m
labels:
  severity: warning
annotations:
  summary: "Model drift detected for {{ $labels.contract_id }}"
```

### 2.6 low_confidence_rate

```text
low_confidence_rate = 满足 γ(x) < θ_hitl 的调用数 / 总调用数
```

反映系统对输入不确定性的比例。持续升高可能意味着输入分布漂移或模型能力下降。

### 2.7 human_in_the_loop_rate

```text
human_in_the_loop_rate = 触发人工复核的调用数 / 总调用数
```

衡量人在回路机制的实际负载，用于评估运营成本与审查资源配置。

---

## 3. Prometheus Metrics 示例

以下为一个完整的 Prometheus 指标导出示例（Python + `prometheus_client`）：

```python
from prometheus_client import Counter, Gauge, Histogram, generate_latest

CONTRACT_LABELS = ["contract_id", "model_version", "temperature", "top_p"]

contract_coverage = Gauge(
    "ai_contract_coverage",
    "Empirical coverage of the probabilistic contract",
    CONTRACT_LABELS,
)

calibration_error_ece = Gauge(
    "ai_contract_calibration_error_ece",
    "Expected Calibration Error",
    ["contract_id", "model_version", "bin_strategy"],
)

brier_score = Gauge(
    "ai_contract_brier_score",
    "Brier score of the model confidence",
    ["contract_id", "model_version"],
)

prediction_set_size = Histogram(
    "ai_contract_prediction_set_size",
    "Size of the conformal prediction set",
    ["contract_id", "model_version", "decision"],
    buckets=[1, 2],
)

model_drift_ks_stat = Gauge(
    "ai_contract_model_drift_ks_stat",
    "KS statistic for model drift detection",
    ["contract_id", "baseline_version", "current_version"],
)

model_drift_p_value = Gauge(
    "ai_contract_model_drift_p_value",
    "KS test p-value for model drift detection",
    ["contract_id", "baseline_version", "current_version"],
)

low_confidence_rate = Gauge(
    "ai_contract_low_confidence_rate",
    "Rate of low-confidence invocations",
    ["contract_id", "model_version"],
)

human_in_the_loop_rate = Gauge(
    "ai_contract_human_in_the_loop_rate",
    "Rate of human-in-the-loop triggers",
    ["contract_id", "model_version"],
)

total_invocations = Counter(
    "ai_contract_total_invocations",
    "Total number of contract invocations",
    ["contract_id", "model_version", "result"],
)

latency_seconds = Histogram(
    "ai_contract_latency_seconds",
    "End-to-end invocation latency",
    ["contract_id", "model_version"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)
```

---

## 4. Grafana 面板配置片段

以下提供一个 Grafana Dashboard JSON 片段，可直接导入或嵌入现有看板。

### 4.1 覆盖率与校准误差

```json
{
  "id": null,
  "title": "AI Contract Coverage & Calibration",
  "type": "timeseries",
  "targets": [
    {
      "expr": "ai_contract_coverage{contract_id=~\"$contract_id\"}",
      "legendFormat": "Coverage - {{ contract_id }}",
      "refId": "A"
    },
    {
      "expr": "1 - ai_contract_calibration_error_ece{contract_id=~\"$contract_id\"}",
      "legendFormat": "1 - ECE - {{ contract_id }}",
      "refId": "B"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percentunit",
      "min": 0,
      "max": 1,
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "color": "red", "value": 0 },
          { "color": "yellow", "value": 0.85 },
          { "color": "green", "value": 0.95 }
        ]
      }
    }
  }
}
```

### 4.2 预测集合分布

```json
{
  "id": null,
  "title": "Prediction Set Distribution",
  "type": "piechart",
  "targets": [
    {
      "expr": "sum by (decision) (ai_contract_prediction_set_size_bucket{contract_id=~\"$contract_id\"})",
      "refId": "A"
    }
  ],
  "options": {
    "legend": { "displayMode": "list", "placement": "right" }
  }
}
```

### 4.3 人在回路与低置信度

```json
{
  "id": null,
  "title": "Human-in-the-Loop & Low Confidence",
  "type": "timeseries",
  "targets": [
    {
      "expr": "ai_contract_human_in_the_loop_rate{contract_id=~\"$contract_id\"}",
      "legendFormat": "HitL Rate - {{ contract_id }}",
      "refId": "A"
    },
    {
      "expr": "ai_contract_low_confidence_rate{contract_id=~\"$contract_id\"}",
      "legendFormat": "Low Conf Rate - {{ contract_id }}",
      "refId": "B"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percentunit",
      "min": 0,
      "max": 1
    }
  }
}
```

### 4.4 模型漂移

```json
{
  "id": null,
  "title": "Model Drift (KS)",
  "type": "timeseries",
  "targets": [
    {
      "expr": "ai_contract_model_drift_ks_stat{contract_id=~\"$contract_id\"}",
      "legendFormat": "KS Stat - {{ contract_id }}",
      "refId": "A"
    },
    {
      "expr": "ai_contract_model_drift_p_value{contract_id=~\"$contract_id\"}",
      "legendFormat": "p-value - {{ contract_id }}",
      "refId": "B"
    }
  ]
}
```

---

## 5. 告警汇总建议

| 告警名 | 表达式 | 严重度 | 升级策略 |
|--------|--------|--------|----------|
| ContractHardBreach | `coverage < γ − δ_hard` | critical | 立即熔断并通知值班 |
| ContractSoftBreach | `γ − δ_soft ≤ coverage < γ − δ_hard` | warning | 记录并通知模型团队 |
| HighCalibrationError | `ece > 0.05` | warning | 纳入校准周期 |
| ModelDrift | `drift_p_value < 0.05` | warning | 触发重新校准 |
| HighHitLRate | `hitl_rate > 0.30` | info | 评估成本与模型能力 |
| HighLatency | `latency_p99 > threshold` | warning | 扩容或优化链路 |

---

## 6. 与概率契约框架的对应关系

| 监控指标 | 框架元素 |
|----------|----------|
| `ai_contract_coverage` | 契约满足条件 `P(correct) ≥ γ(x)` |
| `ai_contract_calibration_error_ece` | 校准质量、定理 AI.1 Calibration Ceiling |
| `ai_contract_prediction_set_size` | Conformal Prediction 集合 `C(x)` |
| `ai_contract_model_drift_ks_stat` | 公理 12.1 Model Drift Bound |
| `ai_contract_low_confidence_rate` | 置信度函数 `γ(x)` |
| `ai_contract_human_in_the_loop_rate` | 定理 AI.2 Human-in-the-Loop Optimality |


---

## 补充说明：概率契约运行时监控指标

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