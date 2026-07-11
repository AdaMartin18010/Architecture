# 学术/技术白皮书引用模板

> **项目**: Software Architecture Reuse Knowledge Base (SAR-KB)
> **版本**: 2026-06-10 v1.0
> **定位**: 为引用本知识体系的学术论文、技术白皮书、学位论文提供标准化摘要、BibTeX、论点、图表与术语引用块
> **适用范围**: 软件架构、软件复用、形式化方法、供应链安全、工业 IoT、AI 工程

---

## 目录

- [学术/技术白皮书引用模板](#学术技术白皮书引用模板)
  - [目录](#目录)
  - [1. 论文摘要模板](#1-论文摘要模板)
    - [1.1 中文摘要模板](#11-中文摘要模板)
    - [1.2 英文摘要模板](#12-英文摘要模板)
  - [2. 引用格式块（BibTeX）](#2-引用格式块bibtex)
    - [2.1 引用本项目整体](#21-引用本项目整体)
    - [2.2 引用全书框架大纲](#22-引用全书框架大纲)
    - [2.3 引用具体主题（按一级主题编号）](#23-引用具体主题按一级主题编号)
    - [2.4 引用公理-定理体系](#24-引用公理-定理体系)
    - [2.5 引用标准对齐矩阵](#25-引用标准对齐矩阵)
  - [3. 关键论点速查表](#3-关键论点速查表)
    - [3.1 元模型与标准对齐（01）](#31-元模型与标准对齐01)
    - [3.2 业务架构复用（02）](#32-业务架构复用02)
    - [3.3 应用架构复用（03）](#33-应用架构复用03)
    - [3.4 组件架构复用（04）](#34-组件架构复用04)
    - [3.5 功能架构复用（05）](#35-功能架构复用05)
    - [3.6 跨层复用治理（06）](#36-跨层复用治理06)
    - [3.7 形式化验证（07）](#37-形式化验证07)
    - [3.8 认知架构（08）](#38-认知架构08)
    - [3.9 价值量化（09）](#39-价值量化09)
    - [3.10 供应链安全（10）](#310-供应链安全10)
    - [3.11 工业 IoT / OT-IT 融合（11）](#311-工业-iot--ot-it-融合11)
    - [3.12 AI 原生复用（12）](#312-ai-原生复用12)
    - [3.13 新兴趋势（13）](#313-新兴趋势13)
  - [4. 图表引用索引](#4-图表引用索引)
    - [4.1 Mermaid 架构图](#41-mermaid-架构图)
    - [4.2 标准矩阵与映射表](#42-标准矩阵与映射表)
    - [4.3 公理-定理推理树](#43-公理-定理推理树)
    - [4.4 决策树与速查卡](#44-决策树与速查卡)
  - [5. 术语对照表](#5-术语对照表)
    - [5.1 核心概念](#51-核心概念)
    - [5.2 元模型与标准](#52-元模型与标准)
    - [5.3 复用层次与单元](#53-复用层次与单元)
    - [5.4 治理与度量](#54-治理与度量)
    - [5.5 形式化验证](#55-形式化验证)
    - [5.6 供应链安全](#56-供应链安全)
    - [5.7 工业 IoT / OT-IT](#57-工业-iot--ot-it)
    - [5.8 AI 原生与前沿](#58-ai-原生与前沿)
  - [补充说明：学术/技术白皮书引用模板](#补充说明学术技术白皮书引用模板)
  - [示例](#示例)
  - [反例](#反例)
  - [权威来源](#权威来源)

---

## 1. 论文摘要模板

### 1.1 中文摘要模板

> **适用场景**: 中文核心期刊、CCF 推荐会议/期刊、学位论文

**【研究背景】** 软件复用已从早期的子程序库演进至云原生组件、AI 功能协议（MCP/A2A）等多元形态，但缺乏覆盖业务→应用→组件→功能四层架构的统一知识体系。现有研究多聚焦单一层次或单一技术栈，跨层治理、形式化正确性保证与价值量化的系统整合尚属空白。

**【问题陈述】** 如何在 ISO/IEC/IEEE 420xx 标准族、TOGAF Standard 10、SLSA 1.2 等 30 余个国际标准的框架下，建立一套可验证、可度量、可治理的全栈软件架构复用方法论？特别是在 AI 原生功能复用引入概率性契约、工业 OT 场景要求确定性保证的双重张力下，复用的边界与条件如何形式化定义？

**【方法论】** 本文基于 Software Architecture Reuse Knowledge Base (SAR-KB) 的四层架构视角（业务架构→应用架构→组件架构→功能架构），提出：

1. **元模型层**：以 ISO/IEC/IEEE 42010:2022 为概念地基，整合 TOGAF Standard 10、ArchiMate 3.2、ISO/IEC 26550:2015 产品线工程模型，建立统一的复用术语体系与 20 条形式化公理；
2. **层次层**：逐层分析业务能力（FEA BRM）、云原生应用（CNCF/NIST SP 800-204）、组件接口契约（Design by Contract）、AI 功能协议（MCP 2025-11-25 / A2A v1.0.0）的复用机制与反模式；
3. **验证层**：运用 TLA+、Alloy、Coq/Isabelle、Rust 类型系统、SPARK/Ada 等形式化方法，构建从分布式协议到内存安全的多层次正确性保证框架；
4. **治理与量化层**：建立基于 ISO/IEC 26565:2026 的五级成熟度模型（26566 提供产品线纹理方法/工具能力支撑）、COCOMO II 2026 校准版的 ROI 计算模型，以及 NASA-TLX 适配版的认知负荷评估方法。

**【主要贡献】**

- 首次将 30 个国际标准纳入统一的复用元模型 v2.0，提供跨标准术语映射矩阵；
- 建立 20 条公理 + 35 条定理的推理树，覆盖元模型、存在性、结构性、过程性四个维度；
- 提出 AI 功能复用的概率契约框架（置信度函数 γ(x)）与 Conformal Prediction 校准方法；
- 覆盖工业 IoT/OT-IT 融合（ISA-95、OPC UA FX、IEC 61508）与软件供应链安全（SLSA 1.2、SBOM、零信任）两大垂直纵深。

**【结论】** 软件架构复用是一项跨越技术、经济、认知与安全的系统工程。四层架构视角与形式化验证的结合，为不同规模、不同安全等级的组织提供了可落地的复用决策框架。未来工作将聚焦于 WASM Component Model 的跨语言复用边界扩展与 AI 辅助复用决策的认知增强架构。

---

### 1.2 英文摘要模板

> **适用场景**: IEEE/ACM Transactions、ICSE、FSE、ESEC/FSE、TOGAF 相关会议、国际期刊

**Background.** Software reuse has evolved from subroutine libraries to cloud-native components and AI function protocols (MCP/A2A). Yet a unified knowledge system spanning Business → Application → Component → Function architecture layers remains absent. Existing research typically focuses on a single layer or technology stack, leaving cross-layer governance, formal correctness assurance, and value quantification as fragmented concerns.

**Problem.** How can a verifiable, measurable, and governable full-stack software architecture reuse methodology be established under the umbrella of 30+ international standards—including the ISO/IEC/IEEE 420xx family, TOGAF Standard 10, and SLSA? In particular, how can reuse boundaries be formalized under the dual tension of probabilistic AI-native function contracts and deterministic industrial OT constraints?

**Methodology.** This paper adopts the four-layer architectural perspective of the Software Architecture Reuse Knowledge Base (SAR-KB):

1. **Meta-model layer**: Uses ISO/IEC/IEEE 42010:2022 as the conceptual foundation, integrating TOGAF Standard 10, ArchiMate 3.2, and ISO/IEC 26550:2015 product-line engineering to establish a unified terminology system and 20 formal axioms;
2. **Layer-wise analysis**: Examines reuse mechanisms and anti-patterns for business capabilities (FEA BRM), cloud-native applications (CNCF / NIST SP 800-204), component interface contracts (Design by Contract), and AI function protocols (MCP 2025-11-25 / A2A v1.0.0);
3. **Formal verification**: Employs TLA+, Alloy, Coq/Isabelle, Rust type systems, and SPARK/Ada to construct a multi-level correctness assurance framework spanning distributed protocols to memory safety;
4. **Governance & quantification**: Proposes a five-level maturity model aligned with ISO/IEC 26565:2026 (26566 provides product line texture methods/tool capabilities), a COCOMO II 2026-calibrated ROI model, and a NASA-TLX-adapted cognitive load assessment method.

**Contributions.**

- First integration of 30 international standards into a unified reuse meta-model v2.0 with cross-standard terminology mapping matrices;
- An axiom-theorem inference tree comprising 20 axioms and 35 theorems across meta-model, existence, structure, and process dimensions;
- A probabilistic contract framework (confidence function γ(x)) for AI function reuse, combined with Conformal Prediction calibration;
- Deep vertical coverage of Industrial IoT/OT-IT convergence (ISA-95, OPC UA FX, IEC 61508) and software supply-chain security (SLSA 1.2, SBOM, zero-trust).

**Conclusion.** Software architecture reuse is a socio-technical system spanning technology, economics, cognition, and security. The combination of a four-layer architectural perspective with formal verification provides organizations of varying scales and safety-criticality levels with a actionable reuse decision framework. Future work will focus on extending the cross-language reuse boundary of the WASM Component Model and on cognitive-augmentation architectures for AI-assisted reuse decisions.

---

## 2. 引用格式块（BibTeX）

### 2.1 引用本项目整体

```bibtex
@misc{SARKB2026,
  title        = {Software Architecture Reuse Knowledge Base ({SAR-KB}):
                  A Four-Layer Framework for Cross-Layer Reuse Governance,
                  Formal Verification, and Value Quantification},
  author       = {{SAR-KB Consortium}},
  year         = {2026},
  version      = {2026-06-10},
  url          = {https://github.com/your-org/sar-kb},
  note         = {Structured knowledge base covering 13 primary topics,
                  30 international standards, 20 axioms, and 35 theorems.
                  Available at: \url{...}},
  howpublished = {\url{https://github.com/your-org/sar-kb}}
}
```

### 2.2 引用全书框架大纲

```bibtex
@book{SoftwareArchitectureReuse2026,
  title     = {软件工程架构复用视角},
  subtitle  = {Software Architecture Reuse: A Multi-Layer Engineering Perspective},
  author    = {{SAR-KB 写作集体}},
  year      = {2026},
  edition   = {Phase~6 预热版},
  note      = {12章 + 附录，约 326,000 字；覆盖 ISO 420xx、TOGAF 10、SLSA、MCP/A2A 等 30 个标准},
  publisher = {自出版 / 开源知识库},
  url       = {https://github.com/your-org/sar-kb}
}
```

### 2.3 引用具体主题（按一级主题编号）

```bibtex
@inbook{SARKB:MetaModel2026,
  title     = {元模型与标准对齐},
  booktitle = {软件工程架构复用视角},
  chapter   = {2},
  author    = {{SAR-KB Consortium}},
  year      = {2026},
  note      = {ISO/IEC/IEEE 42010:2022, TOGAF 10, ArchiMate 3.2, ISO 26550:2015.
               含 15 条形式化公理与 17 条定理。}
}

@inbook{SARKB:FormalVerification2026,
  title     = {形式化验证与复用正确性},
  booktitle = {软件工程架构复用视角},
  chapter   = {8},
  author    = {{SAR-KB Consortium}},
  year      = {2026},
  note      = {TLA+, Alloy, Coq, Isabelle, Rust, SPARK/Ada, B Method.
               含形式化验证投资回报率决策矩阵。}
}

@inbook{SARKB:SupplyChainSecurity2026,
  title     = {供应链安全工程},
  booktitle = {软件工程架构复用视角},
  chapter   = {10},
  author    = {{SAR-KB Consortium}},
  year      = {2026},
  note      = {SLSA 1.2, SBOM (SPDX 2.3 / CycloneDX 1.6 / SWID),
               NIST SSDF 1.2, 零信任纵深防御。}
}

@inbook{SARKB:AINative2026,
  title     = {AI 原生与前沿趋势},
  booktitle = {软件工程架构复用视角},
  chapter   = {12},
  author    = {{SAR-KB Consortium}},
  year      = {2026},
  note      = {MCP 2025-11-25, A2A v1.0.0, Conformal Prediction,
               WASM Component Model, Platform Engineering.}
}
```

### 2.4 引用公理-定理体系

```bibtex
@techreport{SARKB:AxiomTheorem2026,
  title       = {Axiom-Theorem Inference Tree for Software Architecture Reuse},
  author      = {{SAR-KB Formal Methods Group}},
  institution = {SAR-KB},
  year        = {2026},
  number      = {SAR-KB-FM-001},
  note        = {20 axioms (4 meta + 3 existence + 4 structural + 4 process
                 + 5 extended) and 35 derived theorems.
                 Source: struct/99-reference/glossary/axiom-theorem-tree.md}
}
```

### 2.5 引用标准对齐矩阵

```bibtex
@techreport{SARKB:AlignmentMatrix2026,
  title       = {Master Alignment Matrix: 30 International Standards for
                 Software Architecture Reuse},
  author      = {{SAR-KB Standards Group}},
  institution = {SAR-KB},
  year        = {2026},
  number      = {SAR-KB-STD-001},
  note        = {v2.0, 2026-06-10. Matrices A--F covering standard families,
                 topic coverage, terminology crosswalk, protocol applicability,
                 formal methods, and 2026 update tracking.}
}
```

---

## 3. 关键论点速查表

> **使用说明**: 以下论点可直接嵌入论文的 Related Work、Methodology 或 Discussion 章节。每个论点标注了推荐引用的 1–2 个权威来源（标准编号或经典文献），并给出了 SAR-KB 中的支撑文件路径。

### 3.1 元模型与标准对齐（01）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 01-1 | **架构-复用二元性**：架构的本质是约束的集合；复用的本质是约束的传递。 | ISO/IEC/IEEE 42010:2022; Bunge-Wand-Weber (BWW) 本体论 | `01-meta-model-standards/06-formal-axioms/axiom-system.md` |
| 01-2 | **可变性公理**：复用的本质是管理共性与变性的分离与绑定。 | ISO 26550:2015 产品线工程; DOLCE 本体论 | 同上 |
| 01-3 | **层次不可约性**：复用具有层次性（业务→应用→组件→功能），层次间不可约化。 | ISO 21838 Top-Level Ontologies | 同上 |
| 01-4 | **接口可替换性**：两个组件可互相替换，当且仅当它们的外部可观察行为在给定约束下等价。 | Liskov Substitution Principle; Design by Contract (Meyer, 1988) | 同上 |
| 01-5 | **组合性**：若组件 C₁ 和 C₂ 分别满足规约 S₁ 和 S₂，且接口兼容，则组合体满足 S₁∘S₂ 的弱化形式。 | Assume-Guarantee 推理; TLA+ Composition Theorem | 同上 |
| 01-6 | **治理复杂度定律**：复用规模 N 与治理复杂度 G 满足 G(N) = k·N·log(N)。 | 信息论; 网络理论 | 同上 |
| 01-7 | **TOGAF 10 与 ISO 42010 概念映射**：ABB/SBB → 架构模型，Enterprise Continuum → 复用资产库。 | TOGAF 10; ISO/IEC/IEEE 42010:2022 | `01-meta-model-standards/02-togaf-10-alignment/detailed-mapping.md` |

### 3.2 业务架构复用（02）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 02-1 | **业务能力原子性**：业务能力是可复用的最小业务语义单元，其边界由价值创造而非组织结构定义。 | TOGAF 10 Capability Mapping; FEA BRM 2.0 | `02-business-architecture-reuse/02-business-capability/fea-brm-togaf-mapping.md` |
| 02-2 | **价值流组合定理**：端到端价值流的可复用性等于其组成业务能力可复用性的加权乘积；短板效应决定整体上限。 | TOGAF 10; FEA BRM 2.0 | `02-business-architecture-reuse/03-value-stream/value-stream-composition.md` |
| 02-3 | **BPMN 2.0 复用元素**：Call Activity、Event Sub-Process、Message Flow 提供了可执行业务复用的标准化语法。 | OMG BPMN 2.0; DMN 1.5 | `02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-executable-cases.md` |

### 3.3 应用架构复用（03）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 03-1 | **云原生复用三元条件**：容器化 ∧ 声明式配置 ∧ 环境独立性是应用级复用的充要条件。 | CNCF; NIST SP 800-204 | `03-application-architecture-reuse/07-cloud-native-patterns/reusability-matrix-2026.md` |
| 03-2 | **微服务复用天花板**：微服务粒度越小复用率越高，但治理复杂度呈指数增长，存在最优粒度点。 | Conway's Law; 2024–2026 CNCF 调查报告 | 同上 |
| 03-3 | **数据-应用解耦定理**：数据架构与应用架构的复用独立当且仅当数据访问通过抽象数据服务实现。 | Data Mesh 原则; Hohpe & Woolf, *Enterprise Integration Patterns* | `03-application-architecture-reuse/05-data-architecture/data-mesh-data-product-reuse.md` |
| 03-4 | **模块化单体最优性**：在团队规模 N < 50 且部署频率 f < 1/天的约束下，模块化单体的总体复用成本低于微服务。 | 2024–2026 CNCF 调查报告; Spring Modulith 实践 | 同上 |

### 3.4 组件架构复用（04）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 04-1 | **接口契约完备性**：组件可复用性 ∝ 接口契约完备性（前置/后置条件、不变量、副作用），而非实现细节。 | Design by Contract (Meyer, 1988); Liskov Substitution Principle | `04-component-architecture-reuse/04-design-patterns/interface-design-patterns.md` |
| 04-2 | **传递依赖风险定理**：组件供应链风险随传递依赖树深度呈指数增长：Risk(C) ≥ Σ Risk(depᵢ) × α^depth。 | SLSA Framework; Sonatype 2025/2026 Supply Chain Reports | `04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md` |
| 04-3 | **六大语言生态差异**：JVM、Node.js、Rust、Go、Python、.NET 在包管理、Semver 实践、变性机制上呈现显著差异，直接影响复用成熟度。 | Semver 2.0; SPDX 2.3 | `04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md` |

### 3.5 功能架构复用（05）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 05-1 | **MCP Tool 复用等价性**：MCP Tool 的复用等价于其语义描述与模式约束在目标 LLM 上下文中的可传递性。 | MCP 2025-11-25 Specification | `05-functional-architecture-reuse/06-mcp-a2a-protocols/protocol-analysis.md` |
| 05-2 | **AI 功能非确定性定理**：AI 功能的可复用性受温度参数和模型版本漂移制约，复用契约必须包含确定性边界（如 P(正确性) ≥ 0.95）。 | MCP Specification; Conformal Prediction Theory | `05-functional-architecture-reuse/05-ai-llm-functions/llm-function-reuse-patterns.md` |
| 05-3 | **Temporal 工作流确定性复用**：工作流的可复用性等价于其确定性——相同 History 产生相同 Activity 调用序列。 | Temporal Documentation; Event Sourcing Theory | `05-functional-architecture-reuse/04-workflow-orchestration/temporal-reuse-patterns.md` |

### 3.6 跨层复用治理（06）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 06-1 | **治理必要性公理**：无治理的复用退化为克隆；无度量的治理退化为形式。 | ISO/IEC 26565:2026（产品线成熟度框架）; NASA RRL | `06-cross-layer-governance/01-process-governance/cross-layer-governance.md` |
| 06-2 | **五级成熟度模型**：整合 ISO/IEC 26565:2026 / RiSE / RCMM / NASA RRL 的五级复用成熟度评估框架。 | ISO/IEC 26565:2026; RiSE/RCMM 实证研究 | `06-cross-layer-governance/03-maturity-models/reuse-maturity-models-rcmm-rise.md` |
| 06-3 | **四级度量体系**：资产级（RRL）、项目级（复用率）、组织级（成熟度）、生态级（供应链健康度）。 | ISO/IEC 26565:2026（产品线成熟度框架）; NASA RRL | `06-cross-layer-governance/05-metrics-kpi/metrics-framework.md` |
| 06-4 | **跨层升级/降级决策矩阵**：何时将组件提升为应用服务？何时将业务服务降维为组件？需综合耦合度、发布频率与团队拓扑。 | Conway's Law; ISO/IEC/IEEE 42020:2019 | `06-cross-layer-governance/06-up-downgrade-matrix/` |

### 3.7 形式化验证（07）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 07-1 | **形式化信任传递公理**：若组件 C 通过形式化方法验证了性质 P，则任何合规使用 C 的系统继承 P 的正确性保证。 | Hoare Logic; Weakest Precondition Calculus | `07-formal-verification/01-tla-plus/case-library.md` |
| 07-2 | **TLA+ 分布式协议验证**：TLA+ 在分布式一致性协议（Raft、Paxos）与 MCP 能力协商中的规约案例库。 | Leslie Lamport, *The TLA+ Hyperbook* | 同上 |
| 07-3 | **Rust 类型系统形式化基础**：所有权、借用、生命周期与 Polonius/NLL 的形式语义，支撑内存安全 + 并发安全的编译期保证。 | MPI-SWS RustBelt (Jung et al., 2018); Rust Reference | `07-formal-verification/04-rust-type-system/formal-semantics.md` |
| 07-4 | **SPARK/Ada DO-333 工业实践**：飞行控制软件的形式化验证达到 SIL 4 / DO-178C 白金级。 | AdaCore SPARK Pro; DO-333 | `07-formal-verification/05-spark-ada/spark-ada-do333-industrial.md` |
| 07-5 | **B Method 精化链**：铁路信号系统（巴黎地铁 14 号线、纽约地铁 CBTC）的复用正确性传递。 | Clearsy Atelier B; *B-Book* (Abrial, 1996) | `07-formal-verification/06-b-method/event-b-railway-refinement.md` |

### 3.8 认知架构（08）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 08-1 | **认知负荷守恒公理**：复用资产的设计目标应是降低外在负荷、优化相关负荷，而非消除内在负荷。 | Sweller (1988) Cognitive Load Theory; NASA-TLX | `08-cognitive-architecture/03-cognitive-load-theory/quantitative-model.md` |
| 08-2 | **专家悖论定理**：专家复用决策时间更短但资产识别成本更高；新手决策时间更长且外在负荷占比更大。 | ACT-R 认知架构; Chi et al. (1981) Expert-Novice Studies | 同上 |
| 08-3 | **最优文档粒度定理**：存在最优粒度 g* 使总认知负荷最小：dCL_total/dg = 0。 | Information Foraging Theory (Pirolli & Card); NASA-TLX | 同上 |

### 3.9 价值量化（09）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 09-1 | **AAF < AAF_ECONOMIC_FLOOR（0.7，canonical [0.0, 1.0]） 阈值定理**：复用项目 ROI 为正的必要条件是改编调整因子 AAF < AAF_ECONOMIC_FLOOR（0.7，canonical [0.0, 1.0]）；AAF ≥ AAF_ECONOMIC_FLOOR（0.7） 时仅剩战略价值。 | COCOMO II Reuse Model (Boehm et al., USC); NASA RRL | `09-value-quantification/01-cocomo-ii-reuse/cocomo-2026-calibration.md` |
| 09-2 | **COCOMO II 2026 校准版**：ESLOC、AAF、RUSE 乘数的 AI 辅助开发适配。 | USC COCOMO II Model Definition Manual | 同上 |
| 09-3 | **复用 ROI 完整模型**：直接收益 + 间接收益 + 战略收益 + NPV。 | FinOps Framework; Real Options Theory | `09-value-quantification/02-roi-npv-models/roi-real-options-strategic-value.md` |

### 3.10 供应链安全（10）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 10-1 | **信任传递崩塌公理**：软件供应链中的信任是传递的，但传递链长度与信任度成指数反比；chain_length > 5 时 Trust ≈ 0。 | SLSA Framework; OpenSSF Supply Chain Security | `10-supply-chain-security/01-slsa-framework/slsa-reuse-boundaries.md` |
| 10-2 | **SLSA 1.2 四级框架**：L1（基础构建）→ L4（可复现 + 双因素审查）的复用安全边界。 | SLSA 1.2; OpenSSF | 同上 |
| 10-3 | **SBOM 完备性边界定理**：动态依赖、条件编译引入的依赖、运行时加载的插件无法在任何静态 SBOM 中完全捕获。 | SPDX 2.3; CycloneDX 1.6; NTIA SBOM Minimum Elements | `10-supply-chain-security/02-sbom-standards/sbom-reuse-security.md` |
| 10-4 | **零信任软件供应链架构**：5 层防御矩阵设计模板。 | NIST SSDF 1.2; NIST SP 800-161r1 | `10-supply-chain-security/05-zero-trust-supply-chain/zero-trust-template.md` |

### 3.11 工业 IoT / OT-IT 融合（11）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 11-1 | **OT 确定性不可协商公理**：工业 OT 组件复用必须以确定性为首要约束；牺牲确定性的复用策略在 OT 场景中不可接受。 | IEC 61508; ISA-95; OPC UA FX | `11-industrial-iot-otit/06-functional-safety/iec-61508/iec-61508-ed3-reuse.md` |
| 11-2 | **ISA-95 层独立性定理**：L3-L4（MES-ERP）标准化程度最高、复用成熟度最高；L0-L1（现场-控制）标准化程度最低、受设备绑定约束。 | IEC 62264; OPC UA Companion Specifications | `11-industrial-iot-otit/01-isa-95-model/isa-95-asset-catalog-deep-dive.md` |
| 11-3 | **OPC UA FX 协议层次**：C2C / C2D / D2D 的复用边界与 UADP 帧结构分析。 | OPC Foundation; IEC 62541-14 PubSub v1.05 | `11-industrial-iot-otit/02-opc-ua-fx/opc-ua-fx-reuse-hierarchy.md` |
| 11-4 | **AAS-OPC UA 数字孪生映射**：IEC 63278 元模型、子模型模板、OPC UA NodeSet 映射。 | IEC 63278; OPC Foundation | `11-industrial-iot-otit/05-digital-twin-aas/aas-opcua-mapping.md` |

### 3.12 AI 原生复用（12）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 12-1 | **MCP-A2A 互补性定理**：MCP 解决「Agent 如何调用功能」，A2A 解决「Agent 如何与其他 Agent 协作」；联合覆盖度大于简单相加。 | MCP 2025-11-25; A2A v1.0.0 Specification | `12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-deep-dive.md` |
| 12-2 | **概率契约框架**：AI 功能复用契约必须包含置信度函数 γ(x) ∈ [0,1]、校准方法与确定性边界声明。 | Conformal Prediction Theory; Vovk et al. (2005) | `12-ai-native-reuse/05-probabilistic-contracts/` |
| 12-3 | **校准上限定理**：当 LLM 输出分布与真实分布的 KL 散度 > ε 时，任何校准方法都无法使校准误差 < δ。 | Vovk, Gammerman, Shafer (2005) *Algorithmic Learning in a Random World* | `12-ai-native-reuse/07-conformal-prediction/cp-code-generation.md` |
| 12-4 | **模型漂移边界公理**：AI 功能复用有效性随时间指数衰减，衰减率与模型更新频率成反比。 | ML Model Monitoring Best Practices; MCP Specification | `12-ai-native-reuse/07-conformal-prediction/cp-code-generation.md` |

### 3.13 新兴趋势（13）

| # | 核心论点 | 权威来源 | SAR-KB 支撑文件 |
|---|---------|---------|----------------|
| 13-1 | **WASM 可移植性定理**：WASM 组件的跨平台复用边界等于其 WASI 接口的交集。 | W3C WebAssembly; Bytecode Alliance WASI 0.3 | `13-emerging-trends/03-webassembly-components/wasm-reuse-decision-tree.md` |
| 13-2 | **平台工程 ROI 定理**：当开发者数量 N > 50 时，内部开发者平台的投资回报率为正；ROI ∝ √N。 | CNCF Platform Engineering Maturity Model 2026 | `13-emerging-trends/01-platform-engineering/platform-maturity-model.md` |
| 13-3 | **技术融合公理**：当两种技术的成熟度都超过阈值 τ 时，其融合将产生新的复用范式。 | Gartner Hype Cycle; Technology Readiness Levels (TRL) | `13-emerging-trends/` |

---

## 4. 图表引用索引

> **使用说明**: 以下图表可直接以 Mermaid 源码、Markdown 表格或截图形式嵌入论文。引用时请标注来源文件名与 SAR-KB 路径。

### 4.1 Mermaid 架构图

| 图表名称 | 主题 | 文件名 | 说明 |
|---------|------|--------|------|
| **章节依赖关系图** | 全书结构 | `book-outline.md` (§4) | 五层依赖网络：基础层 → 核心四层 → 深度支撑 → 治理安全 → 垂直前沿 |
| **01 元模型标准族谱图** | 元模型 | `standard-family-tree.mmd` | ISO 420xx 族谱与 TOGAF/ArchiMate 的层次映射 |
| **02 业务架构复用模式图** | 业务架构 | `02-business-architecture-reuse.mmd` | 业务能力五层模型、价值流编排、BPMN/DMN 复用元素 |
| **03 应用架构复用模式图** | 应用架构 | `03-application-architecture-reuse.mmd` | 八种架构模式八维对比、服务网格通信抽象、Data Mesh 域导向 |
| **04 组件架构复用模式图** | 组件架构 | `04-component-architecture-reuse.mmd` | 组件四层模型、六大语言生态对比、依赖传递风险树 |
| **05 功能架构复用模式图** | 功能架构 | `05-functional-architecture-reuse.mmd` | MCP/A2A 协议栈互补、Temporal 工作流模式、AI 功能概率契约 |
| **06 跨层治理模式图** | 治理 | `06-cross-layer-governance.mmd` | 四级度量指标体系、FinOps 成本分摊、升级/降级决策矩阵 |
| **07 形式化验证方法图** | 形式化验证 | `07-formal-verification.mmd` | 工具 × 层次 × 成本决策矩阵、seL4/CompCert/铁路信号案例链 |
| **08 认知架构模型图** | 认知架构 | `08-cognitive-architecture.mmd` | ACT-R/BDI 认知模型、NASA-TLX 适配量表、专家-新手差异 |
| **09 价值量化模型图** | 价值量化 | `09-value-quantification.mmd` | COCOMO II 复用模型、ROI-NPV 计算流、盈亏平衡点分析 |
| **10 供应链安全架构图** | 供应链安全 | `10-supply-chain-security.mmd` | SLSA 四级框架、攻击案例链（Log4j/XZ Utils/3CX）、零信任 5 层矩阵 |
| **11 工业 IoT 复用架构图** | 工业 IoT | `11-industrial-iot-otit.mmd` | ISA-95 五层资产目录、OPC UA FX C2C/C2D/D2D、AAS-OPC UA 映射 |
| **12 AI 原生复用架构图** | AI 原生 | `12-ai-native-reuse.mmd` | MCP 能力协商、A2A Task 生命周期、Conformal Prediction 覆盖保证 |
| **13 新兴趋势技术雷达图** | 新兴趋势 | `13-emerging-trends.mmd` | 平台工程成熟度、WASM 跨语言决策树、模块化单体回归路径 |
| **概念映射总图** | 元模型 | `concept-mapping.mmd` | 跨标准核心概念映射（ISO 42010 ↔ TOGAF ↔ ArchiMate ↔ 26550） |

### 4.2 标准矩阵与映射表

| 图表名称 | 文件名 | 说明 |
|---------|--------|------|
| **矩阵 A：复用层次 × 标准族** | `master-alignment-matrix.md` (§矩阵 A) | 8 个层次 × 8 类标准（核心/辅助/框架/建模/质量/过程/协议/2026 新增） |
| **矩阵 B：标准 × 主题覆盖度** | `master-alignment-matrix.md` (§矩阵 B) | 27 个标准 × 8 个主题的五级覆盖度评分（★） |
| **矩阵 C-1：核心架构术语映射** | `master-alignment-matrix.md` (§矩阵 C) | 本体系概念 ↔ ISO 42010 ↔ TOGAF 10 ↔ ArchiMate 3.2 ↔ ISO 26550 ↔ ISA-95 |
| **矩阵 C-2：AI 原生协议术语映射** | `master-alignment-matrix.md` (§矩阵 C) | MCP 2025-11-25 ↔ A2A v1.0.0 ↔ 通用含义（Tool, Agent Card, Task, Sampling 等） |
| **矩阵 C-3：工业数字孪生术语映射** | `master-alignment-matrix.md` (§矩阵 C) | IEC 63278 (AAS) ↔ OPC UA FX ↔ WIT/WASM ↔ TSN（Submodel, GCL, UADP 等） |
| **矩阵 D：协议 × 应用场景** | `master-alignment-matrix.md` (§矩阵 D) | 8 个协议 × 6 类场景（业务编排/应用集成/组件复用/功能调用/工业通信/AI 协作） |
| **矩阵 E：形式化方法 × 验证目标** | `master-alignment-matrix.md` (§矩阵 E) | 9 种形式化方法 × 8 类验证目标（分布式协议/架构约束/定理证明/安全关键/铁路信号/内存安全/并发安全） |
| **矩阵 F：2026 标准更新追踪** | `master-alignment-matrix.md` (§矩阵 F) | 18 项标准的当前状态、预期更新、对体系影响 |

### 4.3 公理-定理推理树

| 图表名称 | 文件名 | 说明 |
|---------|--------|------|
| **公理-定理全体系依赖概览** | `axiom-theorem-tree.md` (§6.1) | 文本形式的依赖树：元公理 M.1-M.4 → 存在性/结构性/过程性公理 → 17 条定理 |
| **01 主题公理层次结构** | `axiom-theorem-tree.md` (§6.2) | 四层公理体系：元公理层 / 存在性公理层 / 结构性公理层 / 过程性公理层 |
| **关键路径（最深推导链）** | `axiom-theorem-tree.md` (§6.3) | 最深推导链长度 5：M.3 → S.4 → P.1 → P.2 → P.3 → Th.14 |
| **公理-定理完整依赖网络图** | `axiom-theorem-full-graph.mmd` | Mermaid 图形化全依赖网络（50 个节点） |
| **待证明猜想表** | `axiom-theorem-tree.md` (§7) | 5 个开放猜想：最优粒度、AI 辅助成熟度、形式化成本摩尔定律、WASM 覆盖度、供应链检测时间 |

### 4.4 决策树与速查卡

| 图表名称 | 文件名 | 说明 |
|---------|--------|------|
| **功能复用粒度-成本-收益决策树** | `05-functional-architecture-reuse/decision-tree-granularity-cost-roi.md` | 算法 → 函数 → 业务规则 → 工作流 → AI 功能的选型决策树 |
| **WASM 跨语言复用决策树** | `13-emerging-trends/03-webassembly-components/wasm-reuse-decision-tree.md` | 语言边界、WASI 接口交集、平台特定功能排除决策 |
| **复用决策快速参考卡** | `quick-reference-card.md` | 一页纸速查：四层架构关键问题、标准速查、反模式清单 |
| **跨层升级/降级决策矩阵** | `06-cross-layer-governance/06-up-downgrade-matrix/` | 组件↔应用↔业务服务的升级/降级条件与触发阈值 |
| **形式化验证投资回报率矩阵** | `07-formal-verification/09-comparative-matrices/` | 工具 × 层次 × 成本的三维选型决策支持 |

---

## 5. 术语对照表

> **使用说明**: 以下术语按主题分组，建议在中英文论文的 **Terminology / Nomenclature** 章节中引用。括号内标注了主要来源标准。

### 5.1 核心概念

| 英文术语 | 中文术语 | 来源标准 / 文献 |
|---------|---------|----------------|
| Software Architecture Reuse | 软件架构复用 | SAR-KB |
| Reuse Knowledge Base (SAR-KB) | 软件架构复用知识库 | SAR-KB |
| Four-Layer Architectural Perspective | 四层架构视角 | SAR-KB (基于 ISO 42010) |
| Business Architecture Reuse | 业务架构复用 | TOGAF 10; FEA BRM |
| Application Architecture Reuse | 应用架构复用 | ISO 42010; CNCF |
| Component Architecture Reuse | 组件架构复用 | IEEE 1517; ISO 26550 |
| Functional Architecture Reuse | 功能架构复用 | MCP 2025-11-25; IEEE 1517 |

### 5.2 元模型与标准

| 英文术语 | 中文术语 | 来源标准 / 文献 |
|---------|---------|----------------|
| Architecture Description (AD) | 架构描述 | ISO/IEC/IEEE 42010:2022 |
| Viewpoint / View / Model | 视点 / 视图 / 模型 | ISO/IEC/IEEE 42010:2022 |
| Correspondence Rule | 对应规则 / 接口契约 | ISO/IEC/IEEE 42010:2022 |
| Architecture Building Block (ABB) | 架构构建块 | TOGAF 10 |
| Solution Building Block (SBB) | 解决方案构建块 | TOGAF 10 |
| Enterprise Continuum | 企业连续体 / 复用资产库 | TOGAF 10 |
| Product Line Engineering (PLE) | 产品线工程 | ISO/IEC 26550:2015 |
| Domain Engineering / Application Engineering | 领域工程 / 应用工程 | ISO/IEC 26550:2015 |
| Commonality / Variability | 共性 / 变性 | ISO/IEC 26550:2015; DOLCE |
| Reusable Asset Specification (RAS) | 可复用资产规范 | OMG RAS v2.2 |

### 5.3 复用层次与单元

| 英文术语 | 中文术语 | 来源标准 / 文献 |
|---------|---------|----------------|
| Business Capability | 业务能力 | TOGAF 10; FEA BRM 2.0 |
| Value Stream | 价值流 | TOGAF 10; FEA |
| Data Product | 数据产品 | Data Mesh 原则 |
| Microservice | 微服务 | CNCF; NIST SP 800-204 |
| Modular Monolith | 模块化单体 | Spring Modulith; CNCF 2024–2026 |
| Service Mesh | 服务网格 | CNCF; Istio/Envoy |
| Component Contract / Interface Contract | 组件契约 / 接口契约 | Design by Contract (Meyer, 1988) |
| Design by Contract (DbC) | 契约式设计 | Meyer (1988) |
| Semantic Versioning (Semver) | 语义化版本控制 | Semver 2.0 |
| MCP Tool / Resource / Prompt / Sampling | MCP 工具 / 资源 / 提示 / 采样 | MCP 2025-11-25 |
| Agent Card | 智能体卡片 | A2A v1.0.0 |
| Skill / Task / Artifact / Part | 技能 / 任务 / 产物 / 片段 | A2A v1.0.0 |
| Temporal Workflow / Activity / Signal | Temporal 工作流 / 活动 / 信号 | Temporal Documentation |

### 5.4 治理与度量

| 英文术语 | 中文术语 | 来源标准 / 文献 |
|---------|---------|----------------|
| Cross-Layer Governance | 跨层复用治理 | ISO/IEC 26565:2026（产品线成熟度框架） |
| Reuse Maturity Model | 复用成熟度模型 | ISO/IEC 26565:2026; RiSE; RCMM |
| Reusability Requirement Level (RRL) | 复用需求等级 | NASA RRL |
| Reuse Rate / Reuse Ratio | 复用率 | NASA RRL; ISO 26565 |
| Adaptation Adjustment Factor (AAF) | 改编调整因子 | COCOMO II (Boehm et al.) |
| Equivalent Source Lines of Code (ESLOC) | 等价源代码行数 | COCOMO II |
| Return on Investment (ROI) of Reuse | 复用投资回报率 | COCOMO II; FinOps |
| Net Present Value (NPV) | 净现值 | 金融工程; Real Options Theory |
| Cognitive Load Theory (CLT) | 认知负荷理论 | Sweller (1988) |
| Intrinsic / Extraneous / Germane Cognitive Load | 内在 / 外在 / 相关认知负荷 | Sweller (1988); NASA-TLX |
| Center of Excellence (CoE) | 卓越中心 | 组织管理实践 |
| Internal Developer Platform (IDP) | 内部开发者平台 | CNCF Platform Engineering |
| Golden Path | 黄金路径 | CNCF Platform Engineering |

### 5.5 形式化验证

| 英文术语 | 中文术语 | 来源标准 / 文献 |
|---------|---------|----------------|
| Formal Verification | 形式化验证 | Hoare Logic; TLA+; Coq |
| Model Checking | 模型检测 | SPIN; NuSMV; TLA+ |
| Theorem Proving | 定理证明 | Coq; Isabelle/HOL |
| Constraint Solving | 约束求解 | Alloy Analyzer |
| Temporal Logic of Actions (TLA+) | 行为时序逻辑 | Leslie Lamport |
| Composition Theorem | 组合定理 | TLA+; Assume-Guarantee |
| Weakest Precondition Calculus | 最弱前置条件演算 | Dijkstra; Hoare Logic |
| Ownership / Borrowing / Lifetime | 所有权 / 借用 / 生命周期 | Rust Reference; RustBelt |
| Non-Lexical Lifetimes (NLL) | 非词法生命周期 | Rust Compiler; Polonius |
| SPARK / Ada | SPARK/Ada 形式化语言 | AdaCore; DO-333 |
| B Method / Event-B | B 方法 / Event-B | Abrial (1996); Atelier B |
| Refinement Chain | 精化链 | B Method; Event-B |
| Safety Integrity Level (SIL) | 安全完整性等级 | IEC 61508 |
| Automotive Safety Integrity Level (ASIL) | 汽车安全完整性等级 | ISO 26262 |
| Software Element out of Context (SEooC) | 独立于上下文的软件要素 | ISO 26262; IEC 61508 |
| Proven-in-Use | 使用验证 / 运行经验证明 | IEC 61508 Ed.3 |

### 5.6 供应链安全

| 英文术语 | 中文术语 | 来源标准 / 文献 |
|---------|---------|----------------|
| Supply Chain Security | 供应链安全 | SLSA; OpenSSF; NIST SSDF |
| Supply Chain Levels for Software Artifacts (SLSA) | 软件制品供应链等级 | SLSA 1.2; OpenSSF |
| Provenance | 来源证明 / 溯源 | SLSA; in-toto Attestation |
| Attestation | 证明 / 鉴证 | in-toto; Sigstore |
| Software Bill of Materials (SBOM) | 软件物料清单 | SPDX 2.3; CycloneDX 1.6; SWID |
| Transitive Dependency | 传递依赖 | 软件包管理实践 |
| Zero-Trust Architecture | 零信任架构 | NIST SP 800-207 |
| Software Supply Chain Attack | 软件供应链攻击 | NIST SP 800-161r1 |
| EU Cyber Resilience Act (CRA) | 欧盟网络韧性法案 | EU CRA (2024) |

### 5.7 工业 IoT / OT-IT

| 英文术语 | 中文术语 | 来源标准 / 文献 |
|---------|---------|----------------|
| Operational Technology (OT) | 运营技术 / 操作技术 | ISA-95; IEC 62264 |
| ISA-95 / IEC 62264 | 企业-控制系统集成标准 | ISA-95; IEC 62264 |
| OPC Unified Architecture (OPC UA) FX | OPC UA 现场级通信 | OPC Foundation; IEC 62541-14 |
| Client-to-Client (C2C) / Client-to-Device (C2D) / Device-to-Device (D2D) | 客户端到客户端 / 客户端到设备 / 设备到设备 | OPC UA FX 1.0 |
| UA Datagram Protocol (UADP) | UA 数据报协议 | OPC UA PubSub v1.05 |
| Time-Sensitive Networking (TSN) | 时间敏感网络 | IEEE 802.1; IEC/IEEE 60802 |
| Gate Control List (GCL) | 门控列表 | IEEE 802.1Qbv |
| Asset Administration Shell (AAS) | 资产管理壳 | IEC 63278 |
| Submodel / Submodel Template | 子模型 / 子模型模板 | IEC 63278 |
| Digital Twin | 数字孪生 | IEC 63278; RAMI 4.0 |
| PLCopen Motion Control | PLCopen 运动控制 | PLCopen Motion Part 4 |
| Functional Safety | 功能安全 | IEC 61508; ISO 26262 |
| Time-Sensitive Networking (TSN) Profile for Industrial Automation | 工业自动化 TSN 配置文件 | IEC/IEEE 60802 |

### 5.8 AI 原生与前沿

| 英文术语 | 中文术语 | 来源标准 / 文献 |
|---------|---------|----------------|
| Model Context Protocol (MCP) | 模型上下文协议 | MCP 2025-11-25 (LF Agentic AI Foundation) |
| Agent-to-Agent Protocol (A2A) | 智能体间协议 | A2A v1.0.0 (Google / LF) |
| Probabilistic Contract | 概率契约 | SAR-KB; Conformal Prediction |
| Confidence Function γ(x) | 置信度函数 | SAR-KB; Conformal Prediction |
| Conformal Prediction (CP) | 保形预测 / 共形预测 | Vovk et al. (2005) |
| Marginal Coverage Guarantee | 边际覆盖保证 | Conformal Prediction Theory |
| Model Drift | 模型漂移 | ML Monitoring; MCP Specification |
| Calibration Error | 校准误差 | Conformal Prediction; ML Theory |
| WebAssembly (WASM) Component Model | WebAssembly 组件模型 | W3C; Bytecode Alliance |
| WebAssembly Interface Types (WIT) | WebAssembly 接口类型 | Component Model 3.0 |
| WebAssembly System Interface (WASI) | WebAssembly 系统接口 | WASI 0.3 |
| Platform Engineering | 平台工程 | CNCF; Team Topologies |
| RegTech AI | 监管科技 AI | 金融科技前沿 |

---

> **维护规则**:
>
> 1. 每季度对照 `struct/99-reference/standards-index/master-alignment-matrix.md` 更新标准编号与状态；
> 2. 每新增一个公理/定理，需在「关键论点速查表」对应主题中补充条目；
> 3. 每新增一个可视化文件，需在「图表引用索引」中登记；
> 4. 术语变更需同步更新 `struct/99-reference/glossary/terminology-crosswalk.md`。
>
> **对齐验证**:
>
> - 本模板与 `struct/99-reference/book-outline.md` 12 章结构一致；
> - 公理/定理计数与 `struct/99-reference/glossary/axiom-theorem-tree.md` 2026-06-10 状态一致（20 公理 + 35 定理）；
> - 标准矩阵引用与 `struct/99-reference/standards-index/master-alignment-matrix.md` v2.0 一致；
> - 13 个一级主题与 `struct/README.md` 实际文件结构一致。
>
> 最后更新: 2026-06-10


---

## 补充说明：学术/技术白皮书引用模板

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
