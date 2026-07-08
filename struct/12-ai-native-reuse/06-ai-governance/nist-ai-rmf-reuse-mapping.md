# NIST AI 风险管理框架与架构复用映射

> **版本**: 2026-07-08
> **定位**: AI 原生复用层 —— NIST AI RMF 及扩展 Profile 对 AI 组件复用的风险管理指导
> **对齐标准**: NIST AI RMF 1.0, NIST AI 600-1 (2024-07), NIST AI RMF Critical Infrastructure Profile (2026-04), ISO/IEC 42001
> **状态**: ✅ 已完成

---

## 目录

- [NIST AI 风险管理框架与架构复用映射](#nist-ai-风险管理框架与架构复用映射)
  - [目录](#目录)
  - [1. NIST AI RMF 体系概述](#1-nist-ai-rmf-体系概述)
    - [1.1 核心框架：AI RMF 1.0](#11-核心框架ai-rmf-10)
    - [1.2 扩展 Profile：AI 600-1](#12-扩展-profileai-600-1)
    - [1.3 扩展 Profile：Critical Infrastructure](#13-扩展-profilecritical-infrastructure)
  - [2. AI 组件复用的特殊风险](#2-ai-组件复用的特殊风险)
    - [2.1 风险分类矩阵](#21-风险分类矩阵)
    - [2.2 风险传递机制](#22-风险传递机制)
  - [3. AI RMF 映射到四层复用模型](#3-ai-rmf-映射到四层复用模型)
    - [3.1 业务层 — AI 能力复用的治理框架](#31-业务层--ai-能力复用的治理框架)
    - [3.2 应用层 — AI 服务/API 复用的风险映射](#32-应用层--ai-服务api-复用的风险映射)
    - [3.3 组件层 — AI 模型/框架/工具库复用的度量](#33-组件层--ai-模型框架工具库复用的度量)
    - [3.4 功能层 — AI 功能（MCP 工具）复用的管理](#34-功能层--ai-功能mcp-工具复用的管理)
  - [4. AI 组件复用的信任评估框架](#4-ai-组件复用的信任评估框架)
    - [4.1 三维信任模型](#41-三维信任模型)
    - [4.2 技术可信度评估（结合 Conformal Prediction）](#42-技术可信度评估结合-conformal-prediction)
    - [4.3 数据可信度评估](#43-数据可信度评估)
    - [4.4 供应链可信度评估](#44-供应链可信度评估)
    - [4.5 综合信任评分](#45-综合信任评分)
  - [5. 案例：AI 模型复用的风险管理实践](#5-案例ai-模型复用的风险管理实践)
    - [5.1 案例背景](#51-案例背景)
    - [5.2 AI RMF 映射评估](#52-ai-rmf-映射评估)
    - [5.3 信任评分计算](#53-信任评分计算)
  - [6. 正向示例：MCP 工具目录的 AI RMF 治理](#6-正向示例mcp-工具目录的-ai-rmf-治理)
  - [7. 反例：未评估即复用开源 Agent 导致合规事故](#7-反例未评估即复用开源-agent-导致合规事故)
  - [8. 权威来源](#8-权威来源)

---

## 概念定义

**AI 组件复用风险**：在架构中复用预训练模型、微调模型、AI 服务、Agent 框架或 MCP 工具时，因上游组件的缺陷、偏见、漏洞或合规问题向 downstream 系统传递的可能性。

**信任评估框架**：基于技术可信度、数据可信度与供应链可信度三个维度，对 AI 组件进行量化评分，以支持复用决策的结构化方法。

**NIST AI RMF 1.0**：美国国家标准与技术研究院发布的自愿性 AI 风险管理框架，包含 Govern、Map、Measure、Manage 四大功能。

## 1. NIST AI RMF 体系概述

### 1.1 核心框架：AI RMF 1.0

NIST AI Risk Management Framework (AI RMF) 1.0 于 **2023 年 1 月 26 日**发布，是一个自愿性的 AI 风险管理框架，包含四大核心功能：

| 功能 | 目标 | 与复用的关联 |
|:---|:---|:---|
| **Govern** (治理) | 建立组织级 AI 风险治理结构 | 定义 AI 组件复用的治理策略和责任 |
| **Map** (映射) | 识别 AI 系统的上下文和风险 | 识别复用 AI 组件的上下文和风险 |
| **Measure** (度量) | 评估和追踪 AI 风险指标 | 建立复用 AI 组件的质量和安全性度量 |
| **Manage** (管理) | 响应已识别的风险 | 实施复用 AI 组件的风险缓解措施 |

### 1.2 扩展 Profile：AI 600-1

NIST AI 600-1 (Generative AI Profile) 于 **2024 年 7 月 26 日**发布，专门针对生成式 AI 系统（LLM、Copilot、Agentic 系统）的风险扩展。核心新增风险包括：

- **幻觉 (Hallucination / Confabulation)**: 生成看似合理但实际错误的内容
- **数据泄露**: 训练数据或提示中的敏感信息泄露
- **有害内容生成**: 生成偏见、歧视或有害内容
- **供应链依赖**: 对基础模型、训练数据、推理框架的依赖
- **提示注入**: 通过精心设计的输入操纵模型行为

AI 600-1 将 12 类 GenAI 风险映射到 Govern、Map、Measure、Manage 四个功能，是构建 LLM/Agent 复用风险清单的直接依据。

### 1.3 扩展 Profile：Critical Infrastructure

NIST AI RMF Critical Infrastructure Profile 于 **2026 年 4 月 7 日**发布概念说明，针对 16 个关键基础设施部门（能源、医疗、金融、交通、通信等）的 AI 应用提供风险实践指导。

**关键要求**:

- 关键基础设施中的 AI 系统必须具备故障安全机制
- AI 组件变更必须经过影响评估
- 跨部门 AI 组件复用需满足最严格的部门合规要求

---

## 2. AI 组件复用的特殊风险

### 2.1 风险分类矩阵

| 风险类别 | 具体风险 | 复用场景 | 严重程度 |
|:---|:---|:---|:---:|
| **模型风险** | 幻觉、偏见、性能漂移 | 复用预训练模型 | 🔴 高 |
| **数据风险** | 训练数据污染、隐私泄露 | 复用训练数据集 | 🔴 高 |
| **框架风险** | 推理框架漏洞、供应链攻击 | 复用 PyTorch/TensorFlow 等 | 🟡 中 |
| **部署风险** | 提示注入、对抗攻击 | 复用 API 封装层 | 🟡 中 |
| **治理风险** | 合规缺失、责任不清 | 复用未经审计的 AI 组件 | 🟡 中 |
| **环境风险** | 碳足迹、资源消耗 | 复用大模型 | 🟢 低 |

### 2.2 风险传递机制

AI 组件的风险具有**级联传递特性**：

```
基础模型 (如 GPT-4, Llama 3)
    ↓ 风险传递
微调模型 (领域适配)
    ↓ 风险传递
应用层 AI 服务 (API 封装)
    ↓ 风险传递
终端用户应用
```

**复用决策启示**:

- 越靠近基础模型的复用，风险传递范围越大
- 每个复用层级都应进行独立的风险评估
- 不能仅依赖上游供应商的风险声明

---

## 3. AI RMF 映射到四层复用模型

### 3.1 业务层 — AI 能力复用的治理框架

**Govern 功能映射**:

- 建立 AI 组件复用治理委员会
- 制定 AI 复用策略（允许/限制/禁止的 AI 组件类型）
- 定义 AI 复用审批流程（特别针对关键基础设施场景）

**Map 功能映射**:

- 识别业务场景中 AI 组件的角色和影响范围
- 评估 AI 失效对业务连续性的影响
- 映射监管要求（EU AI Act、NIST、行业特定法规）

### 3.2 应用层 — AI 服务/API 复用的风险映射

**Measure 功能映射**:

- 建立 AI API 服务质量指标（延迟、可用性、准确率）
- 实施 AI API 安全测试（提示注入、越狱测试）
- 监控 AI API 的模型版本变更和性能漂移

**Manage 功能映射**:

- 实施 AI API 的访问控制和速率限制
- 建立 AI API 故障的降级策略
- 制定 AI API 供应商变更的应急响应计划

### 3.3 组件层 — AI 模型/框架/工具库复用的度量

**模型复用度量**:

| 度量项 | 方法 | 目标 |
|:---|:---|:---|
| 模型卡完整性 | 检查 Model Cards 是否包含训练数据、性能基准、限制 | 100% 关键模型 |
| 偏见检测 | 使用 Fairlearn/AIF360 进行公平性测试 | 偏差指标在可接受范围 |
| 鲁棒性测试 | 对抗样本测试、分布外检测 | 攻击成功率 <阈值 |
| 可解释性 | LIME/SHAP 分析关键决策 | 关键决策可解释 |

**框架复用度量**:

| 度量项 | 方法 | 目标 |
|:---|:---|:---|
| 漏洞扫描 | SCA 扫描框架依赖 | 无高危 CVE |
| 供应链溯源 | SLSA provenance | Build L2+ |
| 许可证合规 | FOSSA/Black Duck | 与策略兼容 |

### 3.4 功能层 — AI 功能（MCP 工具）复用的管理

**MCP 工具复用风险**:

- **工具功能误用**: AI Agent 错误调用工具或传递错误参数
- **工具权限过度**: 复用的 MCP 工具拥有超出必要范围的权限
- **工具版本漂移**: MCP 工具定义变更导致 Agent 行为异常

**管理措施**:

- 对复用的 MCP 工具进行功能测试和边界测试
- 实施最小权限原则（MCP 工具仅暴露必要操作）
- 建立 MCP 工具版本锁定和兼容性验证机制

---

## 4. AI 组件复用的信任评估框架

### 4.1 三维信任模型

```
                    ┌─────────────────┐
                    │   技术可信度     │
                    │ (Technical      │
                    │  Trustworthiness)│
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   模型可信度   │    │   数据可信度   │    │  供应链可信度  │
│  (Model Trust) │    │  (Data Trust) │    │ (Supply Trust) │
└───────────────┘    └───────────────┘    └───────────────┘
```

### 4.2 技术可信度评估（结合 Conformal Prediction）

| 评估维度 | 方法 | 工具/标准 |
|:---|:---|:---|
| 预测可靠性 | Conformal Prediction 覆盖率 | 本项目 `calibration-tool.py` |
| 性能稳定性 | 持续监控准确率/召回率/F1 | Prometheus + Grafana |
| 对抗鲁棒性 | 对抗样本测试 | Adversarial Robustness Toolbox |
| 公平性 | 统计公平性指标 | Fairlearn, AIF360 |

### 4.3 数据可信度评估

| 评估维度 | 方法 | 工具/标准 |
|:---|:---|:---|
| 数据来源 | 训练数据溯源 | Data Provenance 标准 |
| 数据质量 | 数据清洗和验证记录 | Great Expectations |
| 隐私合规 | 差分隐私评估 | Opacus, Google DP Library |
| 偏见检测 | 人口统计平等性测试 | AIF360 |

### 4.4 供应链可信度评估

| 评估维度 | 方法 | 工具/标准 |
|:---|:---|:---|
| 模型来源 | 模型签名验证 | Sigstore, C2PA |
| 框架安全 | SCA 扫描 | Snyk, Trivy |
| 构建可信 | SLSA provenance | SLSA Build L2+ |
| 许可证 | 许可证兼容性检查 | FOSSA, Black Duck |

### 4.5 综合信任评分

```
AI 组件复用信任评分 =
    w1 × 技术可信度(0-100) +
    w2 × 数据可信度(0-100) +
    w3 × 供应链可信度(0-100)

其中 w1 + w2 + w3 = 1.0

默认权重（可根据场景调整）:
- 通用场景: w1=0.4, w2=0.3, w3=0.3
- 关键基础设施: w1=0.3, w2=0.3, w3=0.4
- 研究/实验: w1=0.5, w2=0.3, w3=0.2
```

| 综合评分 | 信任等级 | 复用建议 |
|:---|:---|:---|
| 85-100 | 🟢 A 级 | 无条件批准 |
| 70-84 | 🟢 B 级 | 标准批准 |
| 55-69 | 🟡 C 级 | 条件批准 + 缓解计划 |
| 40-54 | 🟠 D 级 | 延迟复用 + 整改要求 |
| 0-39 | 🔴 E 级 | 拒绝复用 |

---

## 5. 案例：AI 模型复用的风险管理实践

### 5.1 案例背景

某医疗影像公司计划在其诊断辅助系统中复用开源深度学习模型 `CheXNet`（胸部 X 光疾病检测）。

### 5.2 AI RMF 映射评估

**Govern**:

- ✅ 建立 AI 伦理审查委员会
- ✅ 制定医疗 AI 复用策略（符合 FDA/CE 要求）
- ⚠️ 需补充关键基础设施 Profile 合规评估

**Map**:

- ✅ 识别模型用途：辅助诊断，非最终诊断
- ✅ 评估失效影响：误诊风险，需医生最终确认
- ✅ 映射监管要求：FDA 510(k) / CE MDR

**Measure**:

- ✅ 模型卡审查：包含训练数据（ChestX-ray14）、性能基准（AUC ~0.94）
- ⚠️ 偏见检测：需验证不同人群（性别、年龄、种族）的性能一致性
- ⚠️ 鲁棒性测试：需测试对抗噪声和分布外数据

**Manage**:

- ✅ 实施医生确认机制（人在回路）
- ✅ 建立模型性能持续监控
- ✅ 制定模型失效的降级策略

### 5.3 信任评分计算

| 维度 | 得分 | 权重 | 加权得分 |
|:---|:---:|:---:|:---:|
| 技术可信度 | 78 | 0.3 | 23.4 |
| 数据可信度 | 65 | 0.3 | 19.5 |
| 供应链可信度 | 70 | 0.4 | 28.0 |
| **综合评分** | — | — | **70.9** |

**决策**: B 级，标准批准，需补充偏见检测和鲁棒性测试。

---

## 正向示例：MCP 工具目录的 AI RMF 治理

某全球性科技公司建立 MCP 工具目录，并依据 NIST AI RMF 设计复用治理流程：

| RMF 功能 | 复用控制实践 |
|---------|-------------|
| **Govern** | 成立 AI 组件复用委员会；制定《MCP 工具准入策略》；所有工具必须通过安全与合规审查 |
| **Map** | 建立工具风险登记册；识别每个工具的数据访问范围、下游影响与监管映射 |
| **Measure** | 对工具进行功能测试、SBOM 扫描、CVE 检查；高风险工具需红队测试 |
| **Manage** | 实施最小权限 scope、版本锁定、运行时监控与熔断机制；发现风险后启动下架或整改 |

**效果**：工具复用率提升 60%，重复开发减少；高危安全事件归零；审计证据满足 SOC 2 与 ISO 42001 要求。

---

## 反例：未评估即复用开源 Agent 导致合规事故

**场景**：某金融科技团队为快速上线客户服务 Agent，直接复用 GitHub 上热门的开源 Agent 框架与预训练模型，未执行 AI RMF 评估。

**问题**：

1. **Map 缺失**：未识别该模型训练数据可能包含受版权保护内容，导致生成回答中出现未授权引用。
2. **Measure 缺失**：未进行偏见检测与提示注入测试；上线后发现模型对特定地区用户群体回答准确率显著偏低。
3. **Manage 缺失**：未建立模型版本锁定与监控；模型上游更新后行为漂移，生成违反监管要求的理财建议。

**后果**：监管调查、客户投诉、品牌受损，直接经济损失超过百万美元。

**避免建议**：

1. 所有 AI 组件复用前必须完成 AI RMF 四维评估（Govern/Map/Measure/Manage）。
2. 开源模型必须审查 Model Card、训练数据来源、许可证与已知限制。
3. 建立复用组件的信任评分与准入等级，D/E 级组件禁止上线。
4. 对生成式 AI 组件执行 AI 600-1 十二类风险检查清单。

---

## 交叉引用

- MCP 协议规范见 [`../01-mcp-protocol/mcp-2025-11-25-authoritative.md`](../01-mcp-protocol/mcp-2025-11-25-authoritative.md)
- A2A 协议规范见 [`../02-a2a-protocol/a2a-v1-authoritative.md`](../02-a2a-protocol/a2a-v1-authoritative.md)
- Agent 组合与不确定性组合见 [`../03-agentic-infrastructure/llm-agent-composition.md`](../03-agentic-infrastructure/llm-agent-composition.md)
- 概率契约与 SLA 见 [`../05-probabilistic-contracts/probabilistic-contract-framework.md`](../05-probabilistic-contracts/probabilistic-contract-framework.md)
- Conformal Prediction 应用见 [`../07-conformal-prediction/cp-formal-verification.md`](../07-conformal-prediction/cp-formal-verification.md)

## 分析与讨论

AI 组件复用的风险管理必须贯穿 Govern→Map→Measure→Manage 全周期，而非仅在采购时做一次评估。原因在于：

1. **风险级联**：基础模型的风险会传递到微调模型、API 封装层与终端应用。
2. **分布漂移**：训练/校准分布与部署分布的差异会放大幻觉、偏见与错误率。
3. **监管扩展**：EU AI Act、NIST AI 600-1、Critical Infrastructure Profile 对生成式 AI 与关键基础设施 AI 提出更严格要求。

因此，建议将 NIST AI RMF 评估嵌入 CI/CD 与 Agent Marketplace 准入流程，实现“评估即代码、信任可度量”。

## 8. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| NIST AI RMF 1.0 | <https://www.nist.gov/itl/ai-risk-management-framework> | 2026-07-08 |
| NIST AI RMF 1.0 PDF | <https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf> | 2026-07-08 |
| NIST AI 600-1 (GenAI Profile) PDF | <https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.600-1.pdf> | 2026-07-08 |
| NIST AI RMF Critical Infrastructure Profile Concept Note | <https://www.nist.gov/itl/ai-risk-management-framework> | 2026-07-08 |
| ISO/IEC 42001 (AI Management Systems) | <https://www.iso.org/standard/81230.html> | 2026-07-08 |
| Conformal Prediction (Vovk et al.) | <https://arxiv.org/abs/2107.07511> | 2026-07-08 |
| Model Cards (Mitchell et al.) | <https://arxiv.org/abs/1810.03993> | 2026-07-08 |
| OWASP Top 10 for Agentic Applications 2026 | <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/> | 2026-07-08 |

---

> 最后更新：2026-07-08
