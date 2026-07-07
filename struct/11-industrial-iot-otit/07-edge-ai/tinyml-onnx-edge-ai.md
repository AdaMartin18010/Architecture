# 边缘 AI 与 TinyML 模型复用
>
> 版本: 2026-06-06
> 对齐来源: arXiv TinyNav/ICCPS 2026, GitHub 生态, TensorFlow Lite Micro, ONNX Runtime, STM32Cube.AI

## 1. 技术谱系与定义

| 术语 | 定义 | 典型算力 |
|-----|------|---------|
| **TinyML** | 在微控制器（MCU, < 1MB RAM）上运行的机器学习 | < 1 mW, Cortex-M |
| **Edge AI** | 在边缘设备（SoC, NPU, GPU）上运行的 AI 推理 | 1–30 W, ARM A 系列 / NPU |
| **Embedded ML** | 嵌入式系统中的 ML 工作负载统称 | 涵盖 TinyML 到 Edge AI |

## 2. 模型复用技术栈

### 2.1 训练→优化→部署流水线

```text
PyTorch/TensorFlow 训练
    ↓
模型转换（ONNX / TFLite）
    ↓
量化优化（INT8 / 混合精度 / 剪枝 / 知识蒸馏）
    ↓
目标运行时（TFLite Micro / ONNX Runtime / STM32Cube.AI）
    ↓
边缘部署（MCU / SoC / FPGA）
```

### 2.2 关键运行时与框架

| 运行时 | 定位 | 支持硬件 | 复用特性 |
|-------|------|---------|---------|
| **TensorFlow Lite Micro** | 微控制器推理 | Cortex-M, ESP32, RISC-V | 解释器 < 20KB, 模型序列化复用 |
| **ONNX Runtime** | 跨平台推理 | ARM, x86, WASM, RISC-V | 统一 ONNX 格式跨语言/跨设备 |
| **CMSIS-NN** | ARM 内核优化 | Cortex-M4/M7/M55 | 算子库复用，INT8 加速 |
| **ESP-NN** | Espressif 芯片优化 | ESP32-S3 等 | 针对 ESP 的 NN 函数复用 |
| **STM32Cube.AI** | ST 生态集成 | STM32 全系列 | 自动代码生成，模型验证工具链 |
| **frugally-deep** | 嵌入式 C++ Keras | 任意 C++ 平台 | 头文件库，Keras 模型直接加载 |
| **TinyChatEngine** | 设备端 LLM | 高端 MCU / 边缘 SoC | 量化 LLM 推理复用 |

## 3. 模型优化技术（复用前的必要步骤）

### 3.1 量化（Quantization）

| 量化类型 | 精度影响 | 适用场景 |
|---------|---------|---------|
| 训练后量化（PTQ）INT8 | 1–3% 精度损失 | 快速部署、校准集充足 |
| 量化感知训练（QAT）INT8 | < 1% 损失 | 高要求视觉/语音任务 |
| 2-bit 极端量化 | 显著损失 | 极简对话/分类（如 Z80-μLM） |

### 3.2 知识蒸馏（Knowledge Distillation）

- 大型教师模型 → 小型学生模型
- 保留教师模型的"暗知识"（软标签）
- 适合跨设备族复用：同一教师蒸馏出多个规模的学生模型

### 3.3 网络架构搜索（NAS）与 Once-For-All

- **Once-For-All (OFA)**：训练一次，通过弹性深度/宽度/分辨率派生多个子网络
- **MCUNet 系列**：针对 MCU 的内存高效推理（Patch-based Inference）
- **复用价值**：避免为每种目标设备重新训练

## 4. 边缘 AI 复用模式

### 4.1 模型仓库与版本管理

```text
Model Registry
├── Base Model (FP32)
├── Quantized Variants
│   ├── INT8 (Cortex-M4)
│   ├── INT8 (Cortex-M7 + DSP)
│   └── FP16 (Cortex-A + NPU)
├── Distilled Variants
│   ├── Small (< 100KB)
│   └── Medium (< 500KB)
└── Metadata
    ├── 数据血缘
    ├── 校准集信息
    ├── 验证指标
    └── 目标硬件兼容性矩阵
```

### 4.2 跨硬件复用策略

| 策略 | 实现方式 | 限制 |
|-----|---------|------|
| ONNX 通用格式 | 单次导出，多运行时加载 | 算子支持度差异 |
| 中间表示分层 | 高 IR → 后端优化器 → 目标代码 | 需要厂商工具链 |
| 容器化 WASM | wasmCloud / WasmEdge 运行 | 性能开销 |
| 联邦推理 | 边缘预处理 + 云端精推理 | 网络依赖 |

### 4.3 CubeSat / 航天案例（ICCPS 2026）

TinyML 增强立方星任务能力：

- **星载推理**：在资源受限的星载计算机上执行图像分类/异常检测
- **模型复用**：地面训练的模型经 INT8 量化后部署到太空级 MCU
- **挑战**：辐射导致的软错误、极端温度、严格功耗预算

## 5. 与功能安全的交叉

### 5.1 ISO 26262 第三版 (Ed.3) 对 ML 的预期要求

> 注：ISO 26262 当前有效版本为 2018。第三版新工作项已于 2026 初注册，目标发布 ~2029，以下内容基于已公开的工作范围。

- **数据质量验证**：训练数据标注准确性、覆盖度、偏见分析
- **模型训练安全**：超参数版本控制、可复现训练
- **部署监控**：运行时置信度监控、OOD（分布外）检测

### 5.2 感知层安全机制

| 机制 | 目的 |
|-----|------|
| 对抗样本训练 | 提高鲁棒性 |
| 模型冗余 | 传统算法 + ML 算法对比输出 |
| 置信度阈值监控 | 低置信度时触发降级 |
| 规则算法兜底 | ML 偏离规则时切换安全模式 |

## 6. 工业 IoT 场景映射

| ISA-95 层级 | 边缘 AI 应用 | 典型模型类型 |
|------------|-------------|-------------|
| L0 现场 | 振动异常检测（TinyML） | 1D-CNN / LSTM 分类器 |
| L1 控制 | 视觉质检（Edge AI） | MobileNet / EfficientNet |
| L2  supervisory | 预测性维护 | 时间序列预测 |
| L3 MES | 生产排程优化 | 强化学习策略 |
| L4 ERP | 需求预测 | 大规模时序模型 |

## 7. 参考索引

- TensorFlow Lite Micro: [github.com/tensorflow/tflite-micro](https://github.com/tensorflow/tflite-micro)
- ONNX Runtime: [onnx.ai](https://onnx.ai)
- CMSIS-NN: ARM-software/CMSIS-NN
- STM32Cube.AI: [st.com/stm32cubeai](https://stm32ai.st.com)
- TinyML 社区: [tinyml.org](https://tinyml.org)
- ArXiv: "TinyNav: End-to-End TinyML for Real-Time Autonomous Navigation on Microcontrollers" (2026)
- ArXiv: "TinyML Enhances CubeSat Mission Capabilities" (ICCPS 2026)
- Han et al. (2026): "Tiny machine learning (tinyml): research trends and future application opportunities"


---

## 补充章节
## 反例

**反例**：将 IT 系统直接补丁策略套用到 PLC 产线，未考虑实时性约束与功能安全认证，导致停机与安全事故。

## 权威来源

> **权威来源**:
>
> - [ISA-95 / IEC 62264](https://www.isa.org/standards-and-publications/isa-standards/isa-95)
> - [OPC Foundation](https://opcfoundation.org)
> - [IEC 61508](https://webstore.iec.ch/publication/66912)
> - [IEC 63278 AAS](https://iec.ch/dyn/www/f?p=103:38:0::::FSP_ORG_ID:1363)
> - 核查日期：2026-07-07

## 分析

**分析**：OT-IT 复用需要在实时性、安全性与 IT 敏捷性之间取得平衡，标准信息模型是打破竖井的关键。