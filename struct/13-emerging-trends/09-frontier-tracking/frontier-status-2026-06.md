# Phase D 前沿跟踪文档

- **版本**: 2026-06-10
- **定位**: 软件架构复用框架——新兴标准与技术动态跟踪
- **核查日期**: 2026-06-10
- **状态**: 🔍 跟踪中

---

## 目录

- [Phase D 前沿跟踪文档](#phase-d-前沿跟踪文档)
  - [目录](#目录)
  - [1. MCP (Model Context Protocol) 下一版本动态跟踪](#1-mcp-model-context-protocol-下一版本动态跟踪)
    - [1.1 当前稳定版本](#11-当前稳定版本)
    - [1.2 未来版本预期](#12-未来版本预期)
    - [1.3 权威来源](#13-权威来源)
    - [1.4 社区讨论方向](#14-社区讨论方向)
      - [1.4.1 流式传输增强（Streaming Enhancements）](#141-流式传输增强streaming-enhancements)
      - [1.4.2 权限模型细化（Fine-grained Authorization）](#142-权限模型细化fine-grained-authorization)
      - [1.4.3 多模态上下文（Multimodal Context）](#143-多模态上下文multimodal-context)
      - [1.4.4 A2A 互操作（Agent-to-Agent Interoperability）](#144-a2a-互操作agent-to-agent-interoperability)
    - [1.5 对本项目的影响评估](#15-对本项目的影响评估)
  - [2. WASI 1.0 进展跟踪](#2-wasi-10-进展跟踪)
    - [2.1 当前状态概览](#21-当前状态概览)
    - [2.2 WASI 0.3 提案阶段详情](#22-wasi-03-提案阶段详情)
    - [2.3 权威来源](#23-权威来源)
    - [2.4 wasm-pkg-tools 替代 Warg 的最新状态](#24-wasm-pkg-tools-替代-warg-的最新状态)
      - [2.4.1 背景](#241-背景)
      - [2.4.2 wasm-pkg-tools 现状](#242-wasm-pkg-tools-现状)
      - [2.4.3 关键特性](#243-关键特性)
      - [2.4.4 对 WASM 组件复用的意义](#244-对-wasm-组件复用的意义)
    - [2.5 对本项目的影响评估](#25-对本项目的影响评估)
  - [3. ArchiMate 4.0 状态更新](#3-archimate-40-状态更新)
    - [3.1 当前状态](#31-当前状态)
    - [3.2 本项目处理策略](#32-本项目处理策略)
    - [3.3 权威来源](#33-权威来源)
    - [3.4 对本项目的影响评估](#34-对本项目的影响评估)
  - [4. ISO 新标准发布跟踪](#4-iso-新标准发布跟踪)
    - [4.1 ISO/IEC 12207:2026](#41-isoiec-122072026)
    - [4.2 ISO/IEC AWI 42030](#42-isoiec-awi-42030)
    - [4.3 ISO/IEC 25040:2024](#43-isoiec-250402024)
    - [4.4 ISO/IEC 26550:2015](#44-isoiec-265502015)
    - [4.5 ISO/IEC 5338（AI 系统生命周期）](#45-isoiec-5338ai-系统生命周期)
    - [4.6 ISO/IEC 42001（AI 管理体系）](#46-isoiec-42001ai-管理体系)
    - [4.7 标准跟踪汇总表](#47-标准跟踪汇总表)
  - [5. AI-native 架构前沿](#5-ai-native-架构前沿)
    - [5.1 Agentic Governance 标准萌芽](#51-agentic-governance-标准萌芽)
      - [5.1.1 组织动态](#511-组织动态)
      - [5.1.2 萌芽方向](#512-萌芽方向)
      - [5.1.3 权威来源](#513-权威来源)
    - [5.2 Conformal Prediction 在软件复用中的新兴应用](#52-conformal-prediction-在软件复用中的新兴应用)
      - [5.2.1 技术概述](#521-技术概述)
      - [5.2.2 在软件复用中的应用场景](#522-在软件复用中的应用场景)
      - [5.2.3 权威来源](#523-权威来源)
    - [5.3 LLM 驱动的架构复用辅助工具](#53-llm-驱动的架构复用辅助工具)
      - [5.3.1 当前工具生态](#531-当前工具生态)
      - [5.3.2 新兴趋势](#532-新兴趋势)
      - [5.3.3 权威来源](#533-权威来源)
  - [6. 供应链安全前沿](#6-供应链安全前沿)
    - [6.1 EU CRA 2024/2847 执行时间表](#61-eu-cra-20242847-执行时间表)
      - [6.1.1 法规概述](#611-法规概述)
      - [6.1.2 关键时间节点](#612-关键时间节点)
      - [6.1.3 对软件复用的具体影响](#613-对软件复用的具体影响)
      - [6.1.4 权威来源](#614-权威来源)
    - [6.2 OpenSSF Scorecard 新版本动态](#62-openssf-scorecard-新版本动态)
    - [6.3 SLSA 1.2 后续版本规划](#63-slsa-12-后续版本规划)
  - [7. 工业物联网前沿](#7-工业物联网前沿)
    - [7.1 IEC 62443 系列更新](#71-iec-62443-系列更新)
      - [7.1.1 IEC 62443-4-2:2025](#711-iec-62443-4-22025)
      - [7.1.2 系列全貌](#712-系列全貌)
    - [7.2 OPC UA FX 成熟度](#72-opc-ua-fx-成熟度)
    - [7.3 AAS v3.1 预期发布时间](#73-aas-v31-预期发布时间)
  - [需要关注的事件日历](#需要关注的事件日历)
    - [2026 年下半年](#2026-年下半年)
    - [2027 年](#2027-年)
    - [持续跟踪项（无固定日期）](#持续跟踪项无固定日期)
  - [文档元数据](#文档元数据)

---

## 1. MCP (Model Context Protocol) 下一版本动态跟踪

### 1.1 当前稳定版本

| 属性 | 详情 |
|------|------|
| **版本号** | MCP 2025-11-25 |
| **发布日期** | 2025-11-25 |
| **状态** | 稳定版（已在本项目 Phase B 中确认并引用） |
| **核心特性** | 工具定义协议、资源管理、提示模板、采样机制 |

本项目已在多个模块中引用了 MCP 2025-11-25 规范，作为 AI 辅助架构复用的工具级互操作协议基准。

### 1.2 未来版本预期

| 属性 | 详情 |
|------|------|
| **版本号** | MCP 2026-07-28（预期 RC） |
| **预期发布时间** | 2026-07-28 |
| **状态** | 🟡 预期 RC（Release Candidate） |
| **备注** | 目前 Anthropic 尚未发布官方 RC，该日期基于社区共识与路线图推断 |

> ⚠️ **重要提示**: 2026-07-28 当前标注为"预期 RC"，非已确认的正式发布日期。需持续跟踪 Anthropic 官方公告以获取最终确认。

### 1.3 权威来源

- **Anthropic 官方工程博客**: <https://www.anthropic.com/engineering>
- **MCP 官方规范仓库**: <https://github.com/modelcontextprotocol/specification>
- **社区讨论区**: <https://github.com/modelcontextprotocol/specification/discussions>

**核查日期**: 2026-06-10

**来源可靠性评估**: Anthropic 官方渠道为最高优先级；GitHub 讨论区为社区声音参考，需交叉验证。

### 1.4 社区讨论方向

#### 1.4.1 流式传输增强（Streaming Enhancements）

当前 MCP 的传输层主要基于 stdio 与 HTTP/SSE。社区正在积极讨论以下增强方向：

- **双向流式通信**: 从当前的服务器→客户端单向流，扩展为全双工流式通道
- **分块响应协议**: 支持大型资源（如代码库、文档集）的分块传输与渐进式渲染
- **WebSocket 传输支持**: 在 HTTP/SSE 之外增加 WebSocket 作为可选传输层，降低长连接开销
- **流控与背压机制**: 定义标准的流量控制原语，防止内存溢出与网络拥塞

**对复用决策的影响**: 流式传输标准化后，AI 辅助架构设计工具可实时处理大型架构文档，工具级复用的响应延迟将显著降低。

#### 1.4.2 权限模型细化（Fine-grained Authorization）

当前 MCP 的权限模型较为粗粒度，社区正推动以下细化方向：

- **基于角色的访问控制（RBAC）**: 为不同工具调用方定义角色（如"只读审计者"、"架构修改者"）
- **资源级权限**: 支持对单个资源实例（如特定 API 端点、数据库表）设置独立权限
- **动态权限委托**: 允许运行时临时授权，支持工作流中的权限升降级
- **OAuth 2.0 / OIDC 集成**: 与标准身份协议对齐，便于企业集成

**对复用决策的影响**: 权限模型细化后，多团队共享 MCP 工具库时的安全边界将更加清晰，跨组织工具复用的合规门槛降低。

#### 1.4.3 多模态上下文（Multimodal Context）

随着多模态大模型（如 Claude 4、GPT-5o）的普及，社区呼吁扩展 MCP 以支持非文本上下文：

- **图像资源类型**: 允许传输架构图、UI 设计稿、流程图作为上下文
- **结构化数据嵌入**: 支持 JSON Schema、UML XMI、ArchiMate Exchange Format 等机器可读格式
- **音频/视频上下文（长期）**: 为会议记录、演示视频等提供标准化的上下文传递机制

**对复用决策的影响**: 多模态上下文支持将使架构复用不再局限于文本描述，架构师可直接将设计图纸、模型文件作为复用上下文输入 AI 辅助工具。

#### 1.4.4 A2A 互操作（Agent-to-Agent Interoperability）

A2A（Agent-to-Agent）协议由 Google 主导，与 MCP 形成互补关系。社区讨论焦点包括：

- **MCP ↔ A2A 网关**: 设计桥接协议，使 MCP 工具可被 A2A Agent 调用
- **统一能力发现**: 在两种协议间共享服务发现与能力描述机制
- **任务委托标准**: 定义跨协议的任务分解与结果回传语义

**对复用决策的影响**: A2A 互操作实现后，基于 MCP 的架构复用工具可无缝接入更广泛的 Agent 生态，复用范围从单工具扩展至多 Agent 协作网络。

### 1.5 对本项目的影响评估

| 影响维度 | 评估 | 优先级 |
|----------|------|--------|
| **工具定义标准化** | MCP 工具定义协议成为事实标准后，工具级复用将大规模增加 | 🔴 高 |
| **AI 辅助架构设计** | 流式传输与多模态支持将提升 AI 辅助设计工具的用户体验 | 🟡 中 |
| **跨组织复用** | 权限模型细化降低共享工具库的安全合规门槛 | 🟡 中 |
| **生态扩展** | A2A 互操作扩展复用范围至多 Agent 协作场景 | 🟢 低（长期） |

**建议行动**:

1. 在 Phase E 中预留 MCP 2026-07-28 的兼容性升级路径
2. 关注 2026-07 前后 Anthropic 官方公告，确认 RC 实际发布时间
3. 评估现有 MCP 工具定义是否需要针对流式传输增强进行重构

---

## 2. WASI 1.0 进展跟踪

### 2.1 当前状态概览

| 里程碑 | 版本 | 状态 | 时间线 |
|--------|------|------|--------|
| WASI Preview 1 | 0.1 | ✅ 已发布 | 2022 |
| WASI Preview 2 | 0.2 | ✅ 已发布 | 2024-01 |
| WASI 0.3 | 0.3 | 🟡 提案阶段 | 2025-2026 |
| **WASI 1.0** | **1.0** | 🔵 **预期 late 2026 / early 2027** | **2026H2 - 2027H1** |

### 2.2 WASI 0.3 提案阶段详情

WASI 0.3 目前处于 WebAssembly 标准流程的"提案阶段（Proposal Phase）"，核心工作项包括：

- **组件模型完善**: 稳定 Component Model 的导入/导出接口规范
- **异步支持**: 引入基于 future/stream 的异步 I/O 原语
- **改进的错误处理**: 标准化错误码体系，提升跨平台一致性
- **性能优化**: 减少宿主调用开销，提升 WASI 接口的执行效率

### 2.3 权威来源

- **Bytecode Alliance 官方博客**: <https://bytecodealliance.org/articles>
- **WASI 提案仓库**: <https://github.com/WebAssembly/WASI>
- **组件模型规范**: <https://github.com/WebAssembly/component-model>
- **W3C WebAssembly 工作组**: <https://www.w3.org/groups/wg/wasm/>

**核查日期**: 2026-06-10

**来源可靠性评估**: Bytecode Alliance 与 W3C WebAssembly 工作组为最高权威来源；GitHub 仓库 issues/PR 反映最新技术动向。

### 2.4 wasm-pkg-tools 替代 Warg 的最新状态

#### 2.4.1 背景

Warg（WebAssembly Registry）曾是 Bytecode Alliance 力推的 WASM 组件包管理协议与参考实现。然而，社区反馈 Warg 的复杂度过高，且与现有包管理生态（npm、Cargo、PyPI）的集成成本较大。

#### 2.4.2 wasm-pkg-tools 现状

| 属性 | 详情 |
|------|------|
| **项目仓库** | <https://github.com/bytecodealliance/wasm-pkg-tools> |
| **定位** | WASM 组件的轻量级包管理工具链 |
| **当前状态** | 🟢 积极开发中，已成为 Bytecode Alliance 推荐方案 |
| **核心组件** | `wasm-pkg-client`（客户端）、`wasm-pkg-loader`（加载器）、`wkg`（CLI 工具） |

#### 2.4.3 关键特性

- **OCI Registry 兼容**: 支持将 WASM 组件存储于任何 OCI 兼容的容器镜像仓库
- **多语言绑定生成**: 根据 WIT（Wasm Interface Types）接口自动生成宿主语言绑定
- **语义版本管理**: 遵循 SemVer 2.0 规范进行组件版本控制
- **与 wasmCloud 集成**: 原生支持 wasmCloud 应用平台的组件分发

#### 2.4.4 对 WASM 组件复用的意义

wasm-pkg-tools 的成熟标志着 WASM 组件生态从"协议定义期"进入"工具落地期"：

- 开发者可像管理 Docker 镜像一样管理 WASM 组件
- 企业私有仓库（Harbor、Artifactory）可直接复用于 WASM 组件存储
- 组件发现与依赖解析的自动化程度大幅提升

### 2.5 对本项目的影响评估

| 影响维度 | 评估 | 优先级 |
|----------|------|--------|
| **跨平台组件可移植性** | WASI 1.0 标准化系统接口后，WASM 组件复用将突破宿主环境限制 | 🔴 高 |
| **包管理生态** | wasm-pkg-tools 成熟使 WASM 组件分发机制与现有 DevOps 流程对齐 | 🔴 高 |
| **组件市场** | OCI Registry 兼容催生 WASM 组件的公共/私有市场，复用发现成本降低 | 🟡 中 |
| **安全沙箱** | WASI 能力模型（Capability-based）为复用组件提供天然安全边界 | 🟡 中 |

**建议行动**:

1. 在架构复用框架的"组件层"增加 WASM + WASI 作为一等复用载体
2. 跟踪 wasm-pkg-tools 1.0 发布，评估集成至本项目工具链的可行性
3. 关注 WASI 0.3 → 1.0 的过渡窗口，预留接口兼容性层

---

## 3. ArchiMate 4.0 状态更新

### 3.1 当前状态

| 属性 | 详情 |
|------|------|
| **标准名称** | ArchiMate 4.0 |
| **发布机构** | The Open Group |
| **当前状态** | ✅ **已正式发布（2026-04-27）** |
| **官方版本** | ArchiMate 4.0（Document C260, April 2026），与 ArchiMate 3.2 向后兼容 |
| **关键变更** | 引入 Common Domain、行为元素跨层统一、关系 Multiplicity、简化元模型 |
| **预期方向** | 增强对数字化转型、敏捷架构、AI 系统的建模支持 |

### 3.2 本项目处理策略

**已采取的措施**:

- ✅ The Open Group 已于 2026-04-27 正式发布 ArchiMate 4 Specification
- ✅ 本项目已同步更新所有 ArchiMate 4.0 引用状态为“已正式发布”
- ✅ 在 `01-meta-model-standards/04-archimate-4/archimate-iso-mapping.md` 中补充 4.0 关键变更映射
- ✅ 保留 ArchiMate 3.2 作为向后兼容的引用版本

**待执行行动**:

- 持续跟踪工具厂商对 ArchiMate 4.0 的支持进展
- 在下一季度审查时更新概念映射表中的 4.0 特有元素（如 Common Domain、Multiplicity）

### 3.3 权威来源

- **The Open Group ArchiMate 4 发布新闻稿**: <https://www.opengroup.org/The-Open-Group-Announces-ArchiMate%C2%AE-4-Specification>
- **The Open Group ArchiMate Forum**: <https://www.opengroup.org/archimate-forum>
- **ArchiMate 3.2 规范**: <https://pubs.opengroup.org/architecture/archimate32-doc/>
- **The Open Group 标准发布日历**: <https://www.opengroup.org/standards>

**核查日期**: 2026-06-10

**来源可靠性评估**: The Open Group 官方网站与 ArchiMate Forum 为唯一权威来源；第三方博客/论坛信息需谨慎采信。

### 3.4 对本项目的影响评估

| 影响维度 | 评估 | 优先级 |
|----------|------|--------|
| **元模型一致性** | ArchiMate 4.0 引入 Common Domain 等新概念，映射表已更新 | ✅ 已处理 |
| **工具链兼容性** | 主流建模工具（Visual Paradigm 等）已提供 4.0 支持 | 🟡 中 |
| **标准合规性** | 同时引用 ArchiMate 4.0 与 3.2，确保向后兼容 | ✅ 已处理 |

**建议行动**:

1. 订阅 The Open Group ArchiMate Forum 邮件列表，跟踪 4.0 后续澄清与认证更新
2. 在下一季度审查时评估是否需要将默认引用版本从 3.2 迁移到 4.0
3. 基于已发布的 ArchiMate 4.0 规范更新元模型映射表和概念对照表

---

## 4. ISO 新标准发布跟踪

### 4.1 ISO/IEC 12207:2026

| 属性 | 详情 |
|------|------|
| **标准名称** | ISO/IEC/IEEE 12207:2026 — Systems and software engineering — Software life cycle processes |
| **前一版本** | ISO/IEC/IEEE 12207:2017 |
| **当前状态** | ✅ **已发布（2026-04-29）** |
| **关键更新** | 澄清技术过程、改进风险管理与配置管理、扩展敏捷方法、新增 MBSSE 附录 |
| **跟踪说明** | 已取代 2017 版；本项目所有 12207 引用应逐步迁移至 2026 版 |

**权威来源**: <https://www.iso.org/standard/90219.html>

**对本项目的影响**: 12207:2026 将更新软件生命周期过程框架，本项目"复用过程模型"需与之对齐。

### 4.2 ISO/IEC AWI 42030

| 属性 | 详情 |
|------|------|
| **标准名称** | ISO/IEC AWI 42030 — Software and systems engineering — Architecture evaluation |
| **定位** | 架构描述评估框架 |
| **当前状态** | 🟡 **AWI 阶段，仍在制定中** |
| **预期内容** | 软件与系统架构的评估方法、指标、过程框架 |

**现行版**: <https://www.iso.org/standard/73436.html>（ISO/IEC/IEEE 42030:2019）
**AWI 修订项目**: <https://www.iso.org/standard/93814.html>

**对本项目的影响**: 若 42030 正式发布，本项目"架构复用评估"模块可直接引用该标准作为评估框架基准，替代当前自定义评估模型。

### 4.3 ISO/IEC 25040:2024

| 属性 | 详情 |
|------|------|
| **标准名称** | ISO/IEC 25040:2024 — Systems and software Quality Requirements and Evaluation (SQuaRE) — Quality evaluation framework |
| **Phase B 状态** | 已完成跟踪，确认已发布 |
| **当前状态** | ✅ **已发布并生效** |
| **更新情况** | 截至 2026-06-10，无后续修订版 |

**权威来源**: <https://www.iso.org/standard/83467.html>

**对本项目的影响**: 已在 Phase B 完成引用，当前版本无需更新。

### 4.4 ISO/IEC 26550:2015

| 属性 | 详情 |
|------|------|
| **标准名称** | ISO/IEC 26550:2015 — Software and systems engineering — Methods and tools for model-driven product lines |
| **定位** | 产品线工程方法学与工具 |
| **当前状态** | ✅ **已发布（2015）** |
| **核心内容** | 产品线工程参考模型、领域工程与应用工程、可变性管理 |

**权威来源**: <https://www.iso.org/standard/69529.html>

**对本项目的影响**: 26550:2015 的产品线工程方法与"大规模软件复用"高度相关，建议在 Phase E 中增加对该标准的引用与映射。

### 4.5 ISO/IEC 5338（AI 系统生命周期）

| 属性 | 详情 |
|------|------|
| **标准名称** | ISO/IEC 5338:2023 — Information technology — Artificial intelligence — AI system life cycle processes |
| **定位** | AI 系统生命周期过程标准 |
| **当前状态** | ✅ **已发布（2023）** |
| **与 12207 关系** | 作为 ISO/IEC/IEEE 12207:2026 的 AI 领域专用扩展 |
| **对本项目的影响** | AI-native 架构复用工具的生命周期过程需与此标准对齐 |

**权威来源**: <https://www.iso.org/standard/81118.html>

**对本项目的影响**: AI-native 架构复用工具的生命周期过程需与此标准对齐，特别是在 AI 模型版本管理、训练数据治理、模型退役等阶段。

### 4.6 ISO/IEC 42001（AI 管理体系）

| 属性 | 详情 |
|------|------|
| **标准名称** | ISO/IEC 42001:2023 — Information technology — Artificial intelligence — Management system |
| **定位** | AI 管理体系认证标准（类似 ISO 9001 的 AI 专用版） |
| **当前状态** | ✅ **已发布（2023），当前版本有效** |
| **更新预期** | 暂无 42001:2026 或 2027 修订版的公开信息 |

**权威来源**: <https://www.iso.org/standard/81230.html>

**对本项目的影响**: 若本项目涉及的 AI 辅助架构复用工具用于合规场景，需参考 42001 建立 AI 管理体系。

### 4.7 标准跟踪汇总表

| 标准编号 | 标准名称 | Phase A/B 状态 | 当前状态 | 优先级 |
|----------|----------|----------------|----------|--------|
| ISO/IEC 12207:2026 | 软件生命周期过程 | 已发布（2026-04-29） | ✅ 已发布 | 🔴 高 |
| ISO/IEC AWI 42030 | 架构评估 | — | 🟡 AWI 阶段 | 🟡 中 |
| ISO/IEC 25040:2024 | 质量评估框架 | 已发布（Phase B） | ✅ 已发布 | ✅ 已处理 |
| ISO/IEC 26550:2015 | 产品线工程 | — | ✅ 已发布 | ✅ 已处理 |
| ISO/IEC 5338:2023 | AI 系统生命周期 | — | ✅ 已发布 | 🟡 中 |
| ISO/IEC 42001:2023 | AI 管理体系 | — | ✅ 已发布 | 🟢 低 |

---

## 5. AI-native 架构前沿

### 5.1 Agentic Governance 标准萌芽

#### 5.1.1 组织动态

随着 AI Agent 在企业架构中的渗透，治理需求日益迫切。以下组织正在推动 Agentic Governance 相关标准：

- **CAA（Conformant AI Alliance）**: 推动 AI Agent 的可解释性与合规性框架
- **IEEE P2874**: 正在制定"自主系统伦理治理"标准
- **OASIS**: 探讨 AI Agent 互操作与治理的标准化路径
- **LF AI & Data**: 开源 AI 治理工具链与最佳实践

#### 5.1.2 萌芽方向

| 方向 | 描述 | 成熟度 |
|------|------|--------|
| **Agent 身份与溯源** | 为每个 AI Agent 分配可验证的数字身份 | 早期提案 |
| **决策审计链** | 记录 Agent 决策过程的不可篡改日志 | 概念验证 |
| **人类在环（HITL）标准** | 定义何时必须引入人类审批的阈值与流程 | 早期草案 |
| **多 Agent 冲突消解** | 当多个 Agent 决策冲突时的仲裁机制 | 研究阶段 |

#### 5.1.3 权威来源

- **CAA 官网**: <https://www.conformant-ai.org（示例> URL，需持续跟踪实际组织动态）
- **IEEE SA**: <https://standards.ieee.org/>
- **LF AI & Data**: <https://lfaidata.foundation/>

**对本项目的影响**: Agentic Governance 标准成熟后，AI 辅助架构复用工具需内置治理审计能力，确保复用建议的可追溯与可解释。

### 5.2 Conformal Prediction 在软件复用中的新兴应用

#### 5.2.1 技术概述

Conformal Prediction（共形预测）是一种基于统计学习理论的框架，可为机器学习模型的预测提供**有限样本下的有效置信度保证**。其核心特性包括：

- **覆盖率保证**: 在任意数据分布下，预测集的真实覆盖概率不低于预设置信水平
- **无分布假设**: 不依赖数据分布的先验知识
- **校准灵活性**: 可与任意底层模型（LLM、传统 ML）结合

#### 5.2.2 在软件复用中的应用场景

| 场景 | 应用方式 | 预期效果 |
|------|----------|----------|
| **组件适配风险预测** | 预测"组件 A 适配至系统 B"的成功概率区间 | 降低复用失败风险 |
| **架构决策置信度** | 为 AI 推荐的架构方案提供统计置信集 | 增强架构师信任度 |
| **复用投资回报估计** | 预测复用带来的成本节约区间 | 支撑量化决策 |
| **缺陷传播预测** | 预测复用组件引入缺陷的概率分布 | 提升质量预判能力 |

#### 5.2.3 权威来源

- **Vovk, Gammerman, Shafer 经典著作**: "Algorithmic Learning in a Random World"
- **Angelopoulos & Bates 综述**: "A Gentle Introduction to Conformal Prediction"
- **arXiv 最新论文**: <https://arxiv.org/search/?query=conformal+prediction+software+engineering>

**对本项目的影响**: Conformal Prediction 为 AI 辅助架构复用引入了**统计严谨性**，建议在 Phase E 中评估将其集成至复用推荐引擎的可行性。

### 5.3 LLM 驱动的架构复用辅助工具

#### 5.3.1 当前工具生态

| 工具/平台 | 功能定位 | 与复用的关系 |
|-----------|----------|--------------|
| **GitHub Copilot** | 代码生成与补全 | 代码片段级复用辅助 |
| **Sourcegraph Cody** | 代码库理解与查询 | 组件发现与知识复用 |
| **JetBrains AI** | IDE 内 AI 辅助 | 设计模式推荐 |
| **ArchGPT（概念）** | 架构设计专用 LLM | 架构模式复用 |
| **Structurizr + AI** | C4 模型 + LLM 扩展 | 架构描述复用与生成 |

#### 5.3.2 新兴趋势

- **RAG 架构知识库**: 将企业架构文档、设计决策记录（ADR）注入 LLM 上下文，实现组织级架构知识复用
- **架构差异分析**: LLM 自动比较目标系统与候选复用组件的架构差异，生成适配建议
- **模式挖掘**: 从现有代码库中自动提取可复用架构模式

#### 5.3.3 权威来源

- **Microsoft Research**: "Large Language Models for Software Engineering: A Systematic Review"
- **arXiv cs.SE**: <https://arxiv.org/list/cs.SE/recent>
- **ACM TOSEM**: <https://dl.acm.org/journal/tosem>

**对本项目的影响**: LLM 驱动的复用辅助工具正在快速成熟，建议本项目在 Phase E 中明确与这些工具的集成策略，而非从零构建。

---

## 6. 供应链安全前沿

### 6.1 EU CRA 2024/2847 执行时间表

#### 6.1.1 法规概述

EU Cyber Resilience Act（CRA，网络弹性法案）法规编号 2024/2847，是欧盟针对数字产品网络安全的首部横向立法，直接影响含软件产品的设计、开发与维护。

#### 6.1.2 关键时间节点

| 日期 | 事件 | 状态 | 对本项目的影响 |
|------|------|------|----------------|
| **2024-12-10** | CRA 正式生效 | ✅ 已生效 | 法规约束力开始形成 |
| **2026-09-11** | **漏洞报告义务生效** | 🔴 **即将到来** | 复用组件的漏洞披露流程必须合规 |
| **2027-12-11** | **完全合规 deadline** | 🟡 未来里程碑 | 所有在售产品必须符合 CRA 要求 |

#### 6.1.3 对软件复用的具体影响

- **SBOM 强制要求**: 复用组件必须附带机器可读的 SBOM（Software Bill of Materials）
- **漏洞快速修复**: 发现漏洞后须在合理时间内修复（Class I: 21 天；Class II: 90 天）
- **安全更新承诺**: 产品投放市场后须保证 5 年安全更新支持
- **第三方组件责任**: 集成第三方组件的厂商对最终产品安全负全责

#### 6.1.4 权威来源

- **EUR-Lex 官方文本**: <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847>
- **ENISA CRA 指南**: <https://www.enisa.europa.eu/topics/cyber-regulation/cyber-resilience-act>
- **EU Commission CRA 页面**: <https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act>

**核查日期**: 2026-06-10

### 6.2 OpenSSF Scorecard 新版本动态

| 属性 | 详情 |
|------|------|
| **项目** | OpenSSF Scorecard |
| **当前版本** | v5.x（持续迭代中） |
| **功能演进** | 新增供应链完整性检查、SLSA  provenance 验证、依赖项风险评估 |
| **集成趋势** | GitHub Action、GitLab CI、容器镜像扫描的默认集成 |

**权威来源**: <https://github.com/ossf/scorecard>

**对本项目的影响**: 建议将 OpenSSF Scorecard 作为复用组件的安全评分基准，在组件入库时自动执行扫描。

### 6.3 SLSA 1.2 后续版本规划

| 属性 | 详情 |
|------|------|
| **当前版本** | SLSA 1.2（Supply-chain Levels for Software Artifacts） |
| **发布机构** | OpenSSF |
| **后续规划** | SLSA 2.0 正在社区讨论中，可能引入更细粒度的 provenance 验证与构建环境证明 |
| **关键方向** | .hermetic builds（封闭构建）、可重现构建（Reproducible Builds）的标准化 |

**权威来源**: <https://slsa.dev/>

**对本项目的影响**: SLSA 等级可作为复用组件的信任度指标，高 SLSA 等级组件优先推荐复用。

---

## 7. 工业物联网前沿

### 7.1 IEC 62443 系列更新

#### 7.1.1 IEC 62443-4-2:2025

| 属性 | 详情 |
|------|------|
| **标准名称** | IEC 62443-4-2:2019 — Security for industrial automation and control systems — Technical security requirements for IACS components |
| **定位** | 工业自动化控制系统组件的技术安全要求 |
| **当前状态** | ✅ **已发布（2019）** |
| **更新要点** | 组件技术安全要求（SL-1 至 SL-4）；2025 年发布的 IEC TS 62443-6-2 为评估方法论 |

> **勘误说明（2026-06-12）**: 此前本项目误将 IEC 62443-4-2 标注为 2025 版。经权威来源复核，IEC 62443-4-2 现行版为 **2019**；2025 年发布的是 **IEC TS 62443-6-2:2025**（评估方法论）。

#### 7.1.2 系列全貌

| 部分 | 内容 | 状态 |
|------|------|------|
| IEC 62443-1-1 | 术语、概念与模型 | 已发布 |
| IEC 62443-2-1 | 安全程序要求（资产所有者） | 已发布 |
| IEC 62443-2-4 | 服务提供商安全程序 | 已发布 |
| IEC 62443-3-2 | 系统级安全要求 | 已发布 |
| IEC 62443-3-3 | 系统安全等级与要求 | 已发布 |
| IEC 62443-4-1 | 产品安全开发生命周期 | 已发布 |
| **IEC 62443-4-2** | **组件技术安全要求** | **✅ 已发布（2019）** |
| IEC 62443-4-3 | 产品安全测试 | 制定中 |

**权威来源**: <https://webstore.iec.ch/searchform&q=62443>

**对本项目的影响**: 工业场景下的软件架构复用必须满足 IEC 62443-4-2 的安全等级要求（SL-1 至 SL-4），建议在工业物联网复用指南中明确引用。

### 7.2 OPC UA FX 成熟度

| 属性 | 详情 |
|------|------|
| **全称** | OPC UA Field Exchange（OPC UA FX） |
| **定位** | 现场设备级的 OPC UA 通信规范，支持确定性实时通信 |
| **当前状态** | 🟡 **已发布（1.0），生态正在成熟中** |
| **核心特性** |  publisher/subscriber 模型、TSN（Time-Sensitive Networking）集成、确定性延迟 |

**权威来源**: <https://opcfoundation.org/about/opc-technologies/opc-ua/>

**对本项目的影响**: OPC UA FX 的成熟使工业现场设备可作为标准化服务被上层架构复用，推动"现场即服务（Field as a Service）"架构模式。

### 7.3 AAS v3.1 预期发布时间

| 属性 | 详情 |
|------|------|
| **全称** | Asset Administration Shell（资产管理壳）v3.1 |
| **标准机构** | IEC 63278 / IDTA（Industrial Digital Twin Association） |
| **当前版本** | AAS v3.0（已发布） |
| **预期版本** | **AAS v3.1** |
| **预期发布时间** | 🟡 **2026 年末至 2027 年初** |
| **预期更新** | 增强与子模型模板、语义互操作、数字孪生联邦化的支持 |

**权威来源**: <https://industrialdigitaltwin.org/> | <https://www.iec.ch/dyn/www/f?p=103:38:0::::FSP_ORG_ID:1366>

**对本项目的影响**: AAS 是工业数字孪生的核心标准化接口，AAS v3.1 的发布将直接影响工业架构复用的"数字孪生驱动复用"模式。

---

## 需要关注的事件日历

### 2026 年下半年

| 日期 | 事件 | 来源 | 优先级 |
|------|------|------|--------|
| **2026-07-28** | **MCP 2026-07-28 预期 RC 发布** | Anthropic | 🔴 高 |
| **2026-09-11** | **EU CRA 漏洞报告义务生效** | EU 2024/2847 | 🔴 高 |
| 2026-09 | ISO/IEC JTC 1/SC 7 工作会议（跟踪 12207:2026 行业采用与澄清） | ISO | 🟢 低 |
| 2026-10 | WebAssembly CG/WG 秋季会议（WASI 0.3 进展） | W3C | 🟡 中 |
| 2026-11 | The Open Group 季度会议（ArchiMate 4.0 动态） | The Open Group | 🟡 中 |
| 2026-12 | IDTA 年度大会（AAS v3.1 路线图更新） | IDTA | 🟡 中 |
| 2026-12 | OpenSSF 年终总结（SLSA 2.0 规划） | OpenSSF | 🟢 低 |

### 2027 年

| 日期 | 事件 | 来源 | 优先级 |
|------|------|------|--------|
| 2027-01 | ISO/IEC/IEEE 12207:2026 已在 2026-04-29 发布；跟踪行业采用情况 | ISO | 🟡 中 |
| 2027-03 | Bytecode Alliance 峰会（WASI 1.0 路线图） | Bytecode Alliance | 🔴 高 |
| 2027-06 | MCP 2026-07-28 正式版预期稳定窗口 | Anthropic | 🟡 中 |
| 2027-09 | AAS v3.1 可能发布 | IDTA / IEC | 🟡 中 |
| **2027-12-11** | **EU CRA 完全合规 deadline** | EU 2024/2847 | 🔴 高 |

### 持续跟踪项（无固定日期）

| 事项 | 跟踪频率 | 来源 | 优先级 |
|------|----------|------|--------|
| ISO/IEC AWI 42030 状态更新 | 每季度核查 | ISO | 🟡 中 |
| ISO/IEC 5338:2023 采用情况 | 每季度核查 | ISO | 🟢 低 |
| wasm-pkg-tools 1.0 发布 | 每月核查 | GitHub | 🔴 高 |
| OpenSSF Scorecard v6 | 每季度核查 | GitHub | 🟢 低 |
| ArchiMate 4.0 工具与认证更新 | 每季度核查 | The Open Group | 🟡 中 |
| Agentic Governance 标准草案 | 每半年核查 | IEEE / CAA / OASIS | 🟢 低 |
| Conformal Prediction SE 应用论文 | 每季度核查 | arXiv / ACM / IEEE | 🟢 低 |

---

## 文档元数据

| 属性 | 值 |
|------|-----|
| **文档编号** | struct/13-emerging-trends/09-frontier-tracking/frontier-status-2026-06 |
| **版本** | 2026-06-10 |
| **维护责任** | Phase D 前沿跟踪小组 |
| **下次全面审查** | 2026-09-10（季度审查） |
| **关联文档** | book-outline-v2.md、Phase A/B/C 各跟踪文档 |
| **变更记录** | 新建文档——整合 MCP、WASI、ArchiMate、ISO、AI-native、供应链安全、工业物联网七大前沿领域跟踪 |

---

*本文档为动态跟踪文件，信息有效期至下次全面审查。所有 URL 与状态均为 2026-06-10 核查时的快照，实际状态可能随时间变化。*
