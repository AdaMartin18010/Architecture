# AI 辅助复用决策系统：原型设计

> **版本**: 2026-06-08
> **定位**: P2-T8 交付物——AI 辅助复用决策系统的最小可行原型（PoC）设计，将 RAG + LLM 作为开发者复用决策的认知增强层
> **对齐**: ISO/IEC 26566:2026（产品线纹理 product line texture 方法/工具能力）、ACT-R (CMU)、NASA-TLX、RAG 最佳实践、Human-AI Teaming
> **状态**: 草案，待 PoC 验证

---

## 目录

- [AI 辅助复用决策系统：原型设计](#ai-辅助复用决策系统原型设计)
  - [目录](#目录)
  - [1. 概念定义](#1-概念定义)
  - [2. 系统架构设计](#2-系统架构设计)
    - [2.1 RAG 流水线](#21-rag-流水线)
    - [2.2 知识库构成](#22-知识库构成)
    - [2.3 LLM 角色](#23-llm-角色)
  - [3. 认知增强机制](#3-认知增强机制)
    - [3.0 AI 认知增强设计原则](#30-ai-认知增强设计原则)
    - [3.1 降低开发者认知负荷（NASA-TLX 适配）](#31-降低开发者认知负荷nasa-tlx-适配)
    - [3.2 信息分层呈现](#32-信息分层呈现)
    - [3.3 交互模式](#33-交互模式)
  - [3. 原型架构图](#3-原型架构图)
  - [4. PoC 设计](#4-poc-设计)
    - [4.1 最小可行原型的技术栈](#41-最小可行原型的技术栈)
    - [4.2 第一阶段范围](#42-第一阶段范围)
    - [4.3 评估指标](#43-评估指标)
  - [5. 与认知架构理论的对接](#5-与认知架构理论的对接)
    - [5.1 ACT-R 模式匹配在系统中的作用](#51-act-r-模式匹配在系统中的作用)
    - [5.2 BDI 模型与 LLM 推理的映射](#52-bdi-模型与-llm-推理的映射)
    - [5.3 专家 vs 新手的差异化信息呈现](#53-专家-vs-新手的差异化信息呈现)
  - [7. 正向示例](#7-正向示例)
    - [7.1 正向示例：上下文感知的组件推荐](#71-正向示例上下文感知的组件推荐)
  - [8. 反例 / 反模式](#8-反例--反模式)
    - [8.1 反例：过度代理导致配置漂移](#81-反例过度代理导致配置漂移)
  - [9. 权威来源](#9-权威来源)
    - [交叉引用](#交叉引用)
  - [10. 参考](#10-参考)

## 1. 概念定义

**定义**：AI 辅助复用决策系统（AI-Assisted Reuse Decision System）是一种以 RAG + LLM 为核心、面向软件复用场景的人机协同认知增强工具。它通过理解开发者当前上下文，从知识库中检索相关资产与决策证据，生成可解释、可验证的复用建议，最终由人类开发者确认后执行。

**核心目标**：

```text
优化目标:
  min(CL_extraneous)  —— 降低外在负荷（搜索、理解、适配的摩擦）
  max(CL_germane)     —— 提升相关负荷（促进深度学习和模式识别）
  CL_intrinsic ≈ const —— 不改变内在负荷（任务固有复杂性）
```

## 2. 系统架构设计

### 2.1 RAG 流水线

系统将复用决策支持建模为四阶段 RAG 流水线：

```mermaid
flowchart LR
    A[开发者查询] --> B[查询理解<br/>意图识别+实体提取]
    B --> C[知识库索引<br/>向量+结构化+图谱]
    C --> D[混合检索<br/>Dense+Sparse+Metadata]
    D --> E[重排序<br/>Cross-Encoder+LTR]
    E --> F[上下文组装<br/>Top-K 文档+案例+公理]
    F --> G[LLM 生成<br/>CoT 推理+结构化输出]
    G --> H[输出生成<br/>建议+置信度+来源]
    H --> I[人类确认<br/>采纳/修改/拒绝]
    I --> J[反馈回写<br/>优化索引与排序]
```

| 阶段 | 功能 | 关键技术 |
|------|------|---------|
| **索引** | 将复用资产文档、规范、案例转化为可检索的向量与结构化表示 | Markdown 分块、CodeBERT 嵌入、元数据标签 |
| **检索** | 根据查询语义召回候选知识片段 | HNSW 向量搜索 + BM25 关键词混合检索 |
| **重排序** | 对初筛结果按业务相关性精排 | Cross-Encoder（如 bge-reranker）+ 团队使用历史权重 |
| **生成** | 基于检索上下文生成决策建议 | LLM + Chain-of-Thought 提示工程 + JSON Schema 约束 |

### 2.2 知识库构成

知识库是 RAG 系统的核心资产，由四类知识源构成：

| 知识类型 | 内容示例 | 更新策略 |
|---------|---------|---------|
| **复用资产文档** | 组件 README、API 文档、接口契约、SBOM | 每日同步内部目录 |
| **标准规范** | ISO/IEC 26566（产品线纹理）条款、组织架构原则、技术雷达 | 版本化快照 |
| **历史决策案例** | ADR（架构决策记录）、复用评审纪要、成功/失败复盘 | 事件驱动追加 |
| **公理-定理体系** | 复用质量公理、适配成本定理、风险传递引理（见 `07-formal-verification`） | 形式化验证后发布 |

### 2.3 LLM 角色

LLM 不替代人类决策，而是作为**认知卸载代理**承担三类任务：

- **决策建议生成**：基于检索上下文，输出“推荐 / 有条件使用 / 不推荐”的结构化建议
- **权衡分析**：对多个候选组件进行多维度对比（功能、性能、安全、成本），生成雷达图与文字分析
- **风险预警**：自动识别许可证冲突、CVE、版本兼容性陷阱，并引用知识库中的历史失败案例

---

## 3. 认知增强机制

### 3.0 AI 认知增强设计原则

基于 Human-AI Teaming 研究（Amershi et al., 2019; NIST AI RMF, 2023）与本原型定位，AI 辅助复用系统应遵循以下设计原则：

| 原则 | 说明 | 在本系统中的体现 |
|------|------|----------------|
| **人类主导** | AI 提供建议，最终决策权在人类 | 所有推荐附带置信度与来源，需人类确认后执行 |
| **适时适量** | 在正确时机提供恰当粒度信息 | 渐进式披露四层输出，避免信息过载 |
| **可解释性** | 推荐必须有理由与证据链 | 引用 ADR、CVE、历史案例与代码示例 |
| **可纠正性** | 支持人类快速修正 AI 输出 |  thumbs up/down、自由文本反馈、一键回滚 |
| **能力边界透明** | 明确声明 AI 不擅长的场景 | 无匹配时明确建议自研，而非编造推荐 |
| **持续学习** | 从人类反馈中改进 | 隐式与显式反馈共同优化检索与排序 |
| **责任归属清晰** | 人类对最终决策负责 | 高风险集成保留人类 veto |

### 3.1 降低开发者认知负荷（NASA-TLX 适配）

本设计直接对接 [`03-cognitive-load-theory/quantitative-model.md`](../03-cognitive-load-theory/quantitative-model.md) 中的 NASA-TLX 适配版量表，目标是将复用决策的**外在负荷（CL_extraneous）降低 30% 以上**。

| NASA-TLX 维度 | 系统增强策略 | 预期降幅 |
|--------------|-------------|---------|
| 心智需求 | 自动生成一句话摘要与关键参数速览 | −25% |
| 搜索效率 | 语义检索替代关键词试错，Top-5 精准召回 | −40% |
| 文档清晰度 | 结构化输出：摘要→参数→分析→来源 | −30% |
| 挫败感 | 对无匹配场景给出明确自研建议，避免信息困境 | −20% |

系统内置轻量级 NASA-TLX 微问卷（每次决策后 30 秒填写），用于持续校准推荐策略。

### 3.2 信息分层呈现

遵循**渐进式披露（Progressive Disclosure）**原则，将输出组织为四层：

```text
Layer 1: 摘要（1句话）
  └── "推荐使用 auth-jwt-rs256，预计节省 2 小时，风险等级：低"

Layer 2: 关键参数（5-7 个结构化字段）
  └── 功能匹配度、技术质量、经济价值、风险等级、战略契合、置信度、来源

Layer 3: 详细分析（多段落 + 对比表）
  └── 候选对比、适配代码片段、依赖冲突分析、历史案例引用

Layer 4: 原始来源（可追溯链接）
  └── 组件文档、ADR、CVE 数据库、公理-定理证明
```

开发者可按需展开，避免工作记忆超载。

### 3.3 交互模式

系统支持三种人机协同交互模式：

| 模式 | 适用场景 | 交互特征 |
|------|---------|---------|
| **问答式（Q&A）** | 开发者有明确疑问 | 自然语言提问 → 结构化回答，支持追问 |
| **对比式（Compare）** | 多候选难以取舍 | 并排对比矩阵 + 雷达图 + LLM 生成的权衡分析 |
| **向导式（Wizard）** | 新手或复杂决策 | 分步引导：需求澄清 → 候选筛选 → 风险评估 → 集成建议 |

---

## 3. 原型架构图

```mermaid
flowchart TB
    subgraph Input["开发者输入层"]
        Q1[自然语言查询]
        Q2[代码上下文]
        Q3[约束条件]
    end

    subgraph Retrieval["知识检索层"]
        R1[查询解析<br/>意图识别]
        R2[向量数据库<br/>ChromaDB / HNSW]
        R3[关键词检索<br/>BM25]
        R4[混合融合<br/>RRF 重排序]
    end

    subgraph Reasoning["LLM 推理层"]
        L1[提示工程<br/>角色+约束+示例]
        L2[思维链 CoT<br/>逐步推理]
        L3[结构化输出<br/>JSON Schema]
    end

    subgraph Output["输出生成层"]
        O1[决策建议<br/>推荐/条件/拒绝]
        O2[置信度评分<br/>Conformal Prediction]
        O3[参考来源<br/>可追溯引用]
    end

    Q1 --> R1
    Q2 --> R1
    Q3 --> R1
    R1 --> R2
    R1 --> R3
    R2 --> R4
    R3 --> R4
    R4 --> L1
    L1 --> L2
    L2 --> L3
    L3 --> O1
    L3 --> O2
    L3 --> O3
```

---

## 4. PoC 设计

### 4.1 最小可行原型的技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| **后端** | Python 3.11+ | 生态成熟，RAG 库丰富 |
| **编排** | LangChain / LlamaIndex | RAG 流水线标准化，支持自定义检索器 |
| **向量数据库** | ChromaDB | 嵌入式部署、轻量、支持元数据过滤 |
| **嵌入模型** | text-embedding-3-large / BGE | 代码与文档语义理解强 |
| **LLM** | OpenAI API (GPT-4o) / Claude 3.5 Sonnet | 长上下文、结构化输出稳定 |
| **前端** | Streamlit | 快速构建交互式原型，支持对话与可视化 |
| **评估** | RAGAS | 检索准确率与答案相关性自动评估 |

### 4.2 第一阶段范围

PoC 第一阶段**仅覆盖 `04-component-architecture-reuse` 的决策支持**，具体包括：

- 组件目录语义检索（内部库 + 精选开源组件）
- 组件对比与适配建议生成
- 基于历史 ADR 的风险预警

明确排除：业务流程架构复用、跨层治理规则自动执行、形式化验证集成（后续阶段引入）。

### 4.3 评估指标

| 指标 | 基线 | 目标 | 测量方法 |
|------|------|------|---------|
| **决策时间缩短率** | 传统手动搜索+评估 | ≥ 30% | A/B 测试，记录从查询到决策的时间 |
| **复用采纳率提升** | 当前组织复用采纳率 | ≥ 15% | 追踪开发者实际集成推荐组件的比例 |
| **开发者满意度** | N/A | ≥ 4.0/5.0 | NASA-TLX 适配版 + 系统可用性量表 (SUS) |
| **检索准确率@5** | N/A | ≥ 0.80 | 人工标注 Top-5 结果的相关性 |

---

## 5. 与认知架构理论的对接

### 5.1 ACT-R 模式匹配在系统中的作用

ACT-R（Carnegie Mellon）认为专家与新手的核心差异在于**程序性记忆的编译程度**：专家通过大量实践将陈述性知识编译为自动触发的产生式规则（Anderson et al., 2004）。

在本系统中，ACT-R 模式匹配被映射为两层机制：

- **扩散激活（Spreading Activation）**：向量检索的语义相似度计算模拟了人类陈述性记忆的激活扩散。查询向量与资产向量的余弦相似度对应于记忆块的基础激活值（Base-Level Activation）。
- **产生式规则复用**：系统将历史成功复用案例编码为“IF 需求模式 X THEN 推荐资产 Y”的伪规则，通过 RAG 注入 LLM 上下文，加速新手开发者的模式识别过程。

### 5.2 BDI 模型与 LLM 推理的映射

BDI（Belief-Desire-Intention）模型为 LLM 的推理过程提供了可解释的认知框架（Rao & Georgeff, 1995）：

| BDI 元素 | 系统映射 | LLM 推理环节 |
|---------|---------|-------------|
| **Belief（信念）** | RAG 检索到的知识片段（资产文档、案例、规范） | 上下文注入，约束幻觉 |
| **Desire（愿望）** | 开发者的功能需求 + NFR 约束（性能、安全、合规） | 查询理解与意图识别 |
| **Intention（意图）** | LLM 生成的推荐行动 + 人类确认后的执行承诺 | 结构化输出：推荐 + 理由 + 适配方案 |

LLM 的 CoT 推理可视为 BDI 的**实用推理（Practical Reasoning）**过程：基于当前信念更新候选集合，过滤生成意图集合，最终输出行动计划。

### 5.3 专家 vs 新手的差异化信息呈现

依据 ACT-R 的新手-专家模型，系统采用自适应信息呈现策略：

| 维度 | 新手开发者 | 专家开发者 |
|------|-----------|-----------|
| **默认展开层级** | Layer 1→2（摘要+关键参数） | Layer 1（仅摘要），可快捷深入 Layer 4 |
| **交互模式默认** | 向导式（Wizard） | 问答式（Q&A） |
| **解释深度** | 详细：包含概念解释、代码示例、常见错误 | 精简：仅参数、对比、来源链接 |
| **推荐策略** | 优先推荐内部成熟组件，降低不确定性 | 允许探索前沿/实验性组件，提供风险声明 |
| **认知负荷预算** | 严格约束：NASA-TLX 总分 ≤ 50 | 宽松约束：NASA-TLX 总分 ≤ 70 |

---

## 7. 正向示例

### 7.1 正向示例：上下文感知的组件推荐

**示例**：某电商平台的 IDE 插件在开发者编写订单退款逻辑时，自动识别上下文并推荐内部 `refund-orchestrator` 组件。推荐结果按四层呈现：

- **Layer 1**："推荐使用 refund-orchestrator，预计节省 3 小时，风险等级：中"
- **Layer 2**：功能匹配度 92%、技术债务评分 B、历史采用率 78%
- **Layer 3**：调用示例、与现有支付服务的依赖关系、已知 CVE 清单
- **Layer 4**：ADR 链接、组件文档、历史失败案例

开发者在 5 分钟内完成评估并集成，NASA-TLX 评分从基线 68 降至 42，复用采纳率提升 28%。

## 8. 反例 / 反模式

### 8.1 反例：过度代理导致配置漂移

**反例**：某运维团队将生产环境的服务发现配置迁移完全交给 AI Agent 执行，未设置人类确认点与回滚机制。Agent 在 RAG 检索时引用了已废弃的 Consul 模板，并将变更自动推送到 200+ 服务实例，导致服务发现异常 47 分钟。事后审计发现：

- Agent 的置信度阈值设置过低（0.3）
- 知识库更新延迟 72 小时
- 缺少人类 veto 与变更前预览

**教训**：AI 在复用与集成场景中必须保留人类最终决策权，高风险操作需设置强制确认、回滚点和可解释证据链。

## 9. 权威来源

> **权威来源**:
>
> - [ACT-R Cognitive Architecture](https://act-r.psy.cmu.edu) — Carnegie Mellon University
> - [BDI Agent Architecture - Michael Georgeff](https://www.cs.ox.ac.uk/people/michael.georgeff/) — University of Oxford
> - [Cognitive Load Theory - ScienceDirect Topics](https://www.sciencedirect.com/topics/psychology/cognitive-load-theory)
> - [NASA Task Load Index (TLX)](https://www.nasa.gov/human-systems-integration-division/nasa-task-load-index-tlx/)
> - [Guidelines for Human-AI Interaction - Amershi et al., CHI 2019](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
> - [NIST AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
> - [MCP Specification](https://modelcontextprotocol.io)
> - [A2A Protocol](https://a2aprotocol.org)
> - 核查日期：2026-07-09

### 交叉引用

- 与 [开发者复用决策的认知负荷量化模型](../03-cognitive-load-theory/quantitative-model.md) 配合：可用该模型评估引入 AI 助手前后的 CL_reuse 变化。
- 与 [认知负荷理论与架构复用](../03-cognitive-load-theory/cognitive-load-theory.md) 关联：认知增强机制应遵循 CLT 的三维负荷管理原则。
- 与 [知识图谱与架构复用](../06-knowledge-graphs/knowledge-graph-reuse.md) 关联：KG 可作为 RAG 系统的结构化检索层。

## 10. 参考

- Anderson, J.R. et al. (2004). "An Integrated Theory of the Mind". *Psychological Review*.
- Hart, S.G. & Staveland, L.E. (1988). "Development of NASA-TLX (Task Load Index)". *Advances in Psychology*.
- Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks". *NeurIPS*.
- Rao, A.S. & Georgeff, M.P. (1995). "BDI Agents: From Theory to Practice". *ICMAS*.
- Sweller, J. (2011). Cognitive Load Theory. *Psychology of Learning and Motivation*, 55, 37–76.
- Amershi, S. et al. (2019). "Guidelines for Human-AI Interaction". *Proceedings of CHI 2019*.
- NIST (2023). "Artificial Intelligence Risk Management Framework 1.0".
- Xu, W., & Gao, Z. (2024). "Applying HCAI in Developing Effective Human-AI Teaming". *Interactions*, 31(1), 32–37.

---

*最后更新: 2026-07-09 · P2-T8 认知增强原型设计（对齐 Human-AI Teaming 与知识图谱）*


---
