# 概率契约校准工具 (Probabilistic Contract Calibration)

本目录包含基于 **Split Conformal Prediction** 的 AI 功能复用概率契约校准工具，为 LLM 生成代码、工具调用及功能输出提供可证明的统计保证。

## 理论基础

- **边际覆盖保证**：在 calibration 与 test 数据可交换的前提下，

  ```text
  P(y ∈ C(x)) ≥ 1 − α
  ```

  即真实标签落在预测集合中的概率不低于 `1−α`。
- **非一致性分数**（Nonconformity Score）：对正确样本取 `1−p`，对错误样本取 `p`，其中 `p` 为模型输出的预测分数。

## 文件说明

| 文件 | 说明 |
|---|---|
| `calibration-tool.py` | 核心校准脚本，支持 calibrate / predict / drift / report 四个子命令 |
| `example_calibration.csv` | 示例校准数据（模型 v1.0，含真实标签） |
| `example_drift.csv` | 示例漂移数据（模型 v1.1，用于与基线比较） |
| `example_new_inputs.csv` | 示例待预测数据（可用于 predict 子命令） |

## 环境要求

- Python 3.10+
- `numpy`
- `scipy`

```bash
pip install numpy scipy
```

## 数据格式

CSV 文件需包含以下列：

```csv
sample_id,prediction_score,true_label,temperature,top_p,model_version
task-001,0.920,1,0.7,0.90,llm-v1.0
```

- `prediction_score`：模型对输出正确性的预测概率（0~1）
- `true_label`：人工评估结果，`1` 表示正确，`0` 表示错误
- `temperature`：采样温度，需在 `[0, 2]` 范围内
- `top_p`：核采样参数，需在 `[0, 1]` 范围内

## CLI 用法

### 1. calibrate — 校准阈值

```bash
python calibration-tool.py calibrate --data example_calibration.csv --alpha 0.05
```

输出示例：

```
在 α=0.050 水平下，预测集合覆盖率为 95.0%；经验校准覆盖率 95.8%；conformal 阈值 q=0.3124
平均预测集合大小: 1.23
```

### 2. predict — 生成预测集合

```bash
python calibration-tool.py predict \
  --data example_calibration.csv \
  --input example_new_inputs.csv \
  --alpha 0.05
```

输出中的预测集合含义：

- `[1]`：接受（模型输出满足概率契约）
- `[0]`：拒绝（不满足契约）
- `[0, 1]`：不确定（需人工复核）

### 3. drift — 检测模型版本漂移

```bash
python calibration-tool.py drift \
  --baseline example_calibration.csv \
  --new example_drift.csv \
  --alpha 0.05
```

使用 **Kolmogorov-Smirnov 检验**比较两版本模型在同一测试集上的非一致性分数分布。若 `p-value < 0.05`，则触发漂移警报并建议重新校准。

### 4. report — 生成校准报告

```bash
python calibration-tool.py report --data example_calibration.csv --alpha 0.05
```

输出 JSON 格式的完整报告，包含契约边界声明、平均预测集合大小、温度/Top-p 统计及分数分布。

## 边界声明格式

工具统一输出如下形式的概率契约边界声明：

> 在 α=0.050 水平下，预测集合覆盖率为 95.0%；经验校准覆盖率 95.8%；conformal 阈值 q=0.3124

该声明可直接嵌入架构治理文档或 SLA 中，作为 AI 功能复用的量化信任边界。
