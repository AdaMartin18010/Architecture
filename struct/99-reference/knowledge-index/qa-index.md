# 软件架构复用知识体系问答索引 (QA Index)

> **版本**: 2026-06-10
> **覆盖范围**: `struct/` 下 13 个主题，50+ 问答对
> **构建方式**: 基于文件实际标题与核心章节提取

---

## 使用说明

1. **快速检索**: 使用 `Ctrl+F`（或 `Cmd+F`）在当前页面搜索关键词，如 `TLA+`、`SLSA`、`ISA-95`、`ROI`、`MCP`。
2. **问题格式**: 每个主题下以 `Q:` 开头的问题可直接复制到搜索引擎或对话系统中。
3. **答案指向**: `A:` 后的文件路径均为相对 `struct/` 的相对路径，可直接在仓库中定位。
4. **主题优先级**: 标有 ⭐ 的主题为深度覆盖区域（形式化验证、供应链安全、AI 原生复用、工业 IoT、价值量化）。

---

## 主题分类

### 01 元模型与标准对齐

- **Q: ISO/IEC/IEEE 42010:2022 的视点(Viewpoint)为什么是架构复用的基本单元？**
  - A: 视点定义了描述一类关注点的约定，一旦标准化，所有项目可基于相同视点生成视图，降低架构描述成本并保证跨项目结构一致性。详见 `01-meta-model-standards/01-iso-420xx-family/iso-42010-2022.md` §1–§2。

- **Q: 软件复用的定义在 ISO/IEC 26550:2015 中如何界定？**
  - A: ISO/IEC 26550:2015 定义产品线工程参考模型，采用"领域工程 + 应用工程"双轨制，将复用从项目级提升到组织级资产库管理。详见 `01-meta-model-standards/03-iso-26550-ple/ple-iso-integration.md`。

- **Q: OMG RAS v2.2 定义了可复用资产的哪四个核心 facet？**
  - A: Classification（分类）、Solution（解决方案）、Usage（使用描述）、RelatedAssets（相关资产）。详见 `01-meta-model-standards/07-omg-ras/ras-alignment.md`。

- **Q: TOGAF Standard 10 的 ABB/SBB 与 ISO/IEC/IEEE 42010:2022 如何映射？**
  - A: TOGAF Standard 10 的架构构建块（ABB）和解决方案构建块（SBB）可映射到 ISO/IEC/IEEE 42010:2022 的架构描述元模型中的模型种类与对应规则。详见 `01-meta-model-standards/02-togaf-10-alignment/detailed-mapping.md`。

- **Q: FAIR4RS 原则如何指导软件资产的可持续复用？**
  - A: FAIR4RS 要求软件资产具备可发现(Findable)、可访问(Accessible)、可互操作(Interoperable)、可重用(Reusable)属性，是研究软件长期治理的基准。详见 `01-meta-model-standards/08-fair4rs/fair4rs-alignment.md`。

---

### 02 业务架构复用

- **Q: 业务能力复用的最小语义单元是什么？**
  - A: 业务能力（Business Capability），其边界由"价值创造"而非"组织结构"定义。公理 2.1 指出能力原子性是业务复用的基础。详见 `02-business-architecture-reuse/README.md`。

- **Q: BPMN 2.0 与 DMN 1.5 在复用层次上如何分工？**
  - A: BPMN 负责可执行流程的编排复用，DMN 负责业务规则与决策逻辑的独立复用；两者结合可实现"流程驱动 + 规则驱动"的混合架构。详见 `02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md`。

- **Q: FEA BRM 与 TOGAF Capability Map 的交叉映射关系是什么？**
  - A: FEA BRM（联邦企业架构业务参考模型）的五层业务线结构与 TOGAF Phase B 的业务能力映射存在层级对应关系，可用于跨组织业务语义对齐。详见 `02-business-architecture-reuse/02-business-capability/fea-brm-togaf-mapping.md`。

---

### 03 应用架构复用

- **Q: 数据架构与应用架构的复用独立条件是什么？**
  - A: 定理 3.2 指出，独立当且仅当数据访问通过**抽象数据服务**而非**直接存储耦合**实现。详见 `03-application-architecture-reuse/README.md`。

- **Q: 2026 云原生架构模式复用性矩阵覆盖了哪些模式？**
  - A: 覆盖单体、模块化单体、SOA、微服务、微前端、Serverless、服务网格、EDA、模块化宏服务等模式的复用性、复杂度和适用场景对比。详见 `03-application-architecture-reuse/07-cloud-native-patterns/reusability-matrix-2026.md`。

- **Q: Data Mesh 的域导向复用核心理念是什么？**
  - A: 数据作为产品由域团队自治拥有，通过标准化接口和联邦治理实现跨域数据复用，而非集中式数据仓库。详见 `03-application-architecture-reuse/05-data-architecture/data-mesh-data-product-reuse.md`。

- **Q: 服务网格（Istio/Envoy/Cilium）的通信模式复用包括哪些？**
  - A: 包括 mTLS、流量镜像、金丝雀发布、熔断、重试、超时等可复用通信策略。详见 `03-application-architecture-reuse/08-service-mesh/service-mesh-communication-patterns.md`。

---

### 04 组件架构复用

- **Q: 组件的可复用性取决于什么而非实现细节？**
  - A: 接口契约的完备性（前置条件、后置条件、不变量、副作用声明）。公理 4.1 明确指出接口契约完备性是复用性的决定因素。详见 `04-component-architecture-reuse/README.md`。

- **Q: 2026 年六大语言生态复用成熟度对比涵盖哪些语言？**
  - A: JVM、Node.js、Rust、Go、Python、.NET、WebAssembly。对比矩阵覆盖包管理、依赖解析、供应链安全原生支持等维度。详见 `04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md`。

- **Q: 开源供应链复用的分层防御策略是什么？**
  - A: 四层防御：代理注册表(L1–L2)、审批工作流(L2–L3)、Lockfile+哈希(L3)、Vendoring(L4)。详见 `04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md`。

---

### 05 功能架构复用

- **Q: MCP (Model Context Protocol) 的四层能力原语是什么？**
  - A: tools（函数复用）、resources（数据复用）、prompts（提示模板复用）、sampling（推理复用）。详见 `05-functional-architecture-reuse/06-mcp-a2a-protocols/mcp-tool-design.md` 及 `12-ai-native-reuse/01-mcp-protocol/mcp-2026-deep-dive.md`。

- **Q: A2A 与 MCP 的根本区分是什么？**
  - A: MCP 是垂直协议（Agent ↔ Tool，无状态结构化调用），A2A 是水平协议（Agent ↔ Agent，有状态多轮任务委托）。详见 `12-ai-native-reuse/02-a2a-protocol/a2a-v1-deep-dive.md` §5.1。

- **Q: Temporal 工作流复用的核心模式有哪些？**
  - A: 包括工作流即代码、子工作流复用、活动(Activity)复用、Saga 补偿模式、定时任务复用等。详见 `05-functional-architecture-reuse/04-workflow-orchestration/temporal-reuse-patterns.md`。

- **Q: AI 功能复用为什么必须包含确定性边界？**
  - A: 定理 5.2 指出，AI 功能受温度参数和模型版本漂移制约，其复用契约必须声明概率边界（如 "P(正确性) ≥ 0.95"）。详见 `05-functional-architecture-reuse/README.md`。

---

### 06 跨层治理

- **Q: 复用成熟度五级模型的最高级是什么？**
  - A: Level 5: 优化 (Optimizing)。模型整合 ISO/IEC 26565:2026（产品线成熟度框架）/ 26566:2026（产品线纹理方法）、RiSE、RCMM、NASA RRL。详见 `06-cross-layer-governance/03-maturity-models/reuse-maturity-models-rcmm-rise.md`。

- **Q: FinOps 跨层复用成本模型包含哪三类成本？**
  - A: 直接成本、间接成本、风险成本；按使用量/团队/项目/层级进行分摊。详见 `06-cross-layer-governance/04-finops-cost/finops-unit-economics-2026.md`。

- **Q: 跨层复用升级/降级决策矩阵的核心依据是什么？**
  - A: 基于业务价值、技术债务、团队成熟度、合规要求四维度评估。详见 `06-cross-layer-governance/06-up-downgrade-matrix/upgrade-downgrade-matrix.md`。

- **Q: 无治理的复用会退化为什么？**
  - A: 克隆（Copy-Paste）。公理 6.1 指出："无治理的复用退化为克隆；无度量的治理退化为形式。"详见 `06-cross-layer-governance/README.md`。

---

### 07 形式化验证 ⭐

- **Q: TLA+ 与 Alloy 在验证层次上有何分工？**
  - A: TLA+ 用于**模型层时序行为验证**（分布式协议、状态机活性/安全性），Alloy 用于**规约层结构约束求解**（架构依赖、权限模型、类型一致性）。详见 `07-formal-verification/README.md`。

- **Q: TLA+ 案例库 T07 验证了什么协议？**
  - A: MCP Server 能力协商协议，验证核心安全不变量（Active 状态必须有共同能力）和活性（协商最终收敛）。详见 `07-formal-verification/01-tla-plus/mcp-capability-negotiation.md`。

- **Q: TLA+ 案例库还覆盖了哪些工业案例？**
  - A: 分布式支付服务（T06）、A2A Task 生命周期（T08）、PLCopen 运动控制（T10）。详见 `07-formal-verification/01-tla-plus/case-library.md`。

- **Q: Alloy 的 CapabilityClosure 约束形式化了什么安全原则？**
  - A: 形式化 MCP 安全模型中的"能力委托"原则（最小权限）：被调用工具的能力必须是调用者 Server 已声明能力的子集。详见 `07-formal-verification/02-alloy/mcp-tool-graph.md` §3。

- **Q: Alloy 的 AcyclicToolCalls 约束防止什么风险？**
  - A: 防止工具调用图中的循环依赖，避免协议层死锁、上下文膨胀和错误雪崩。详见 `07-formal-verification/02-alloy/mcp-tool-graph.md` §3。

- **Q: Coq 与 Isabelle/HOL 在可复用组件验证上的典型应用是什么？**
  - A: Coq 用于验证插入排序正确性和有界计数器状态不变量；Isabelle 用于验证插入排序和旋转门状态机。详见 `07-formal-verification/03-coq-isabelle/README.md`。

- **Q: Rust 类型系统如何保证内存安全？**
  - A: 通过所有权（唯一性+转移性+作用域绑定）、借用（读写互斥）和生命周期（偏序约束）三大机制，在编译期排除 use-after-free、double-free、dangling pointers 和 data races。详见 `07-formal-verification/04-rust-type-system/formal-semantics.md`。

- **Q: Cargo 依赖解析的数学基础是什么？**
  - A: 基于 SAT 求解的 NP 完全问题；实际使用 PubGrub 算法，采用统一版本策略（依赖图中每个包仅一个版本）。详见 `07-formal-verification/04-rust-type-system/cargo-sat-resolution.md`。

- **Q: SPARK Ada 与 Rust 在航空电子领域的认证路径有何差异？**
  - A: SPARK Ada 拥有完整的 DO-178C/DO-333 FAA/EASA 认证路径和工具资格（TQL-1）；Rust 目前尚无航空级 DO-178C 认证路径，但内存安全保证已通过 RustBelt (Iris) 形式化证明。详见 `07-formal-verification/09-comparative-matrices/spark-ada-vs-rust-verification-matrix.md`。

- **Q: B Method / Event-B 在铁路信号系统中的典型应用是什么？**
  - A: 通过三层精化（M0 进路安全 → M1 区段道岔 → M2 信号联锁）对铁路信号系统进行形式化精化链验证。详见 `07-formal-verification/06-b-method/railway-signaling-refinement.md`。

- **Q: 形式化验证的信任传递公理 F.1 内容是什么？**
  - A: 若组件 C 通过形式化方法验证了性质 P，则任何使用 C 的系统继承 P 的正确性保证，前提是 C 的使用方式不违反 C 的前置条件。详见 `07-formal-verification/README.md`。

- **Q: TLA+ 规约中不变量与活性的设计原则是什么？**
  - A: 每个案例至少包含结构性不变量（状态变量合法范围）和语义性不变量（业务安全性质），以及至少一个 leads-to (`~>`) 形式的活性性质。详见 `07-formal-verification/01-tla-plus/case-library.md` §3。

---

### 08 认知架构

- **Q: ACT-R 认知架构如何解释开发者的复用意图？**
  - A: ACT-R 将复用意图表征为陈述性记忆（已知组件库）与产生式规则（模式匹配触发复用行为）的交互过程。详见 `08-cognitive-architecture/01-act-r-model/act-r-cognitive-reuse.md`。

- **Q: 认知负荷理论中复用资产的设计目标是什么？**
  - A: 降低外在负荷（无关信息）和优化相关负荷（促进图式构建），而非消除内在负荷（任务固有复杂度）。公理 C.1 指出开发者认知资源有限。详见 `08-cognitive-architecture/03-cognitive-load-theory/cognitive-load-theory.md`。

- **Q: BDI 模型如何描述开发者对复用资产的认知状态？**
  - A: Belief（对组件能力和质量的信念）、Desire（复用以降低工作量的意愿）、Intention（实际执行复用决策的意图）。详见 `08-cognitive-architecture/02-bdi-model/bdi-agent-reuse.md`。

---

### 09 价值量化 ⭐

- **Q: COCOMO II 复用模型的核心方程是什么？**
  - A: `ESLOC = ASLOC × (1 - AT/100) × AAM`，其中 ESLOC 为等价新代码行，ASLOC 为需适配的代码行，AAM 为适配调整因子。详见 `09-value-quantification/01-cocomo-ii-reuse/cocomo-ii-reuse-model-deep-dive.md` §2。

- **Q: AAM（适配调整因子）的计算公式是什么？**
  - A: `AAM = [AA + AAF × (1 + 0.02 × SU × UNFM)] / 100`（AAF ≤ 50）；AAF 由设计修改(DM)、代码修改(CM)、集成修改(IM)加权计算。详见 `09-value-quantification/01-cocomo-ii-reuse/cocomo-ii-reuse-model-deep-dive.md` §2.2。

- **Q: AAF 的阈值对复用 ROI 有什么决定性影响？**
  - A: 定理 V.1 指出，复用 ROI 为正的必要条件是 AAF < AAF_ECONOMIC_FLOOR（0.7，canonical [0.0, 1.0]）；若 AAF ≥ AAF_ECONOMIC_FLOOR（0.7），直接经济价值消失，仅剩战略价值。详见 `09-value-quantification/02-roi-npv-models/roi-framework.md` §3。

- **Q: COCOMO II 2026 校准版适配了哪些现代开发模式？**
  - A: 适配 AI 辅助开发、Serverless、低代码平台，并将功能点扩展至故事点/对象点、依赖复杂度等新规模度量。详见 `09-value-quantification/01-cocomo-ii-reuse/cocomo-2026-calibration.md`。

- **Q: 复用 ROI 的直接收益、间接收益、战略收益分别包括什么？**
  - A: 直接收益 = 开发时间节约 + 缺陷减少 + 维护成本节约；间接收益 = 上市时间加速 + 技能杠杆 + 一致性提升；战略收益 = 生态系统建设 + 组织能力积累 + 合规优势。详见 `09-value-quantification/02-roi-npv-models/roi-framework.md` §1。

- **Q: 复用盈亏平衡点 N* 的计算公式是什么？**
  - A: `N* = C_initial / (S_build - S_reuse)`，若预计使用次数 N < N*，则不值得投资于复用。详见 `09-value-quantification/02-roi-npv-models/roi-framework.md` §3。

- **Q: RUSE（ Required Reuse）成本驱动器在 COCOMO II 中的影响是什么？**
  - A: RUSE 评级从 Nominal 到 Extra High 对应工作量乘数 1.00 → 1.24，量化"为跨组织复用而额外投入的设计与文档成本"。详见 `09-value-quantification/01-cocomo-ii-reuse/cocomo-ii-reuse-model-deep-dive.md` §4.2。

---

### 10 供应链安全 ⭐

- **Q: SLSA 1.2 Multi-Track 架构包含哪三个正式轨道？**
  - A: Build Track（构建轨道）、Source Track（源码轨道）、Build Environment Track（构建环境轨道）。详见 `10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md` §1.2。

- **Q: SLSA Build Track L1/L2/L3 的核心目标分别是什么？**
  - A: L1 = 自动化生成 Provenance（可追溯）；L2 = 托管构建 + 签名 Provenance（防构建后篡改）；L3 = 隔离/密封/临时构建 + 非伪造性 Provenance（防构建中篡改）。详见 `10-supply-chain-security/01-slsa-framework/slsa-reuse-boundaries.md` §2 及 `slsa-1-2-multi-track.md` §2。

- **Q: 系统有效 SLSA 等级如何由依赖组件决定？**
  - A: 定理 S.RB.2：系统有效等级为 `min(L₁, L₂, ..., Lₙ)`，即最短板决定整体等级。详见 `10-supply-chain-security/01-slsa-framework/slsa-reuse-boundaries.md` §4。

- **Q: SBOM 三种主流格式 SPDX / CycloneDX / SWID 的适用场景差异？**
  - A: SPDX 适用于许可证合规与法律咨询（ISO/IEC 5962）；CycloneDX 适用于安全漏洞管理与 DevSecOps；SWID 适用于软件资产盘点与 ITAM（NIST 对齐）。详见 `10-supply-chain-security/02-sbom-standards/sbom-comparison.md`。

- **Q: 零信任软件供应链的五个验证点是什么？**
  - A: 源代码验证、依赖验证、构建验证、制品验证、部署验证。公理 ZT.1 要求对每一个环节都进行验证。详见 `10-supply-chain-security/05-zero-trust-supply-chain/zero-trust-principles.md` §2。

- **Q: XZ Utils 后门的攻击路径属于哪类供应链攻击？**
  - A: 上游代码植入（3.5）：通过社交工程获取维护者信任 → 在测试文件中植入后门 → 通过 glibc hook 激活。详见 `10-supply-chain-security/03-attack-vectors/attack-tree.md` §3.5。

- **Q: SolarWinds 事件属于哪类供应链攻击？**
  - A: 构建系统篡改（3.2）：攻击者入侵 CI/CD 流水线，在构建阶段注入后门，最终被正常签名分发，影响 18,000+ 组织。详见 `10-supply-chain-security/03-attack-vectors/attack-tree.md` §3.2。

- **Q: Sigstore/cosign keyless signing 如何消除长期密钥管理风险？**
  - A: 通过 OIDC 联邦身份将短期签名密钥绑定至 CI 身份，无需长期保管签名密钥，配合 Rekor 透明日志提供非否认性证明。详见 `10-supply-chain-security/01-slsa-framework/slsa-reuse-boundaries.md` §3.2 升级路径。

- **Q: 供应链攻击树的 AND/OR 节点语义是什么？**
  - A: OR 节点表示攻击者只需成功一条路径；AND 节点表示必须同时满足所有子条件；叶节点为原子级攻击手段。详见 `10-supply-chain-security/03-attack-vectors/attack-tree.md` §1。

---

### 11 工业 IoT / OT-IT 融合 ⭐

- **Q: ISA-95 五层模型从 L0 到 L4 分别代表什么？**
  - A: L0 现场设备（毫秒–秒）、L1 基本控制（秒–分）、L2 监控层（分–小时）、L3 制造运营/MES（小时–天）、L4 企业层（天–月）。详见 `11-industrial-iot-otit/01-isa-95-model/isa-95-asset-catalog-deep-dive.md` §1.1。

- **Q: OPC UA FX 的四层复用模型是什么？**
  - A: Level 1 物理硬件复用（标准以太网/TSN 交换机）、Level 2 通信协议复用（TSN 配置模板/UADP 协议栈）、Level 3 信息模型复用（Companion Specifications）、Level 4 应用逻辑复用（C2C/C2D/D2D 配置模板）。详见 `11-industrial-iot-otit/02-opc-ua-fx/opc-ua-fx-reuse-hierarchy.md` §2。

- **Q: OPC UA FX 中 C2C / C2D / D2D 的周期范围分别是多少？**
  - A: C2C（Controller-to-Controller）10–100 ms；C2D（Controller-to-Device）500 μs–10 ms；D2D（Device-to-Device）250 μs–1 ms。详见 `11-industrial-iot-otit/02-opc-ua-fx/opc-ua-fx-reuse-hierarchy.md` §3。

- **Q: AAS 子模型模板(SMT)在架构复用中的意义是什么？**
  - A: SMT 是 OT/IT 边界的可复用语义契约，一个子模型（如 Digital Nameplate、Product Carbon Footprint）可在 PLM 中创建、在 MES 中消费、在 ERP 中审计，跨越组织边界复用。详见 `11-industrial-iot-otit/05-digital-twin-aas/aas-v32-opcua-fx-2026-alignment.md` §2.3。

- **Q: IEC 61508 Ed.3 与 Ed.2 在工具资质上的关键变化是什么？**
  - A: Ed.2 使用静态 T1/T2/T3 分类；Ed.3 改为基于风险的 TI/TD 分析 → TIL 0–4（类似 ISO 26262 TCL）。详见 `11-industrial-iot-otit/06-functional-safety/iec-61508-iso-26262-sotif-alignment.md` §2.2。

- **Q: SEooC（Safety Element out of Context）的核心交付物是什么？**
  - A: Assumptions of Use (AoU)、Assumptions of Environment (AoE)、Safety Requirements Specification、Safety Analyses、Safety Manual。详见 `11-industrial-iot-otit/06-functional-safety/iec-61508-iso-26262-sotif-alignment.md` §4。

- **Q: PLCopen 运动控制功能块的跨厂商复用机制是什么？**
  - A: 通过标准化功能块接口（如 MC_Power、MC_MoveAbsolute）实现跨厂商控制逻辑复用，基于 IEC 61131-3 和 PLCopen Motion Control 规范。详见 `11-industrial-iot-otit/04-plcopen-motion/function-block-interfaces.md`。

- **Q: TSN GCL 周期一致性定理的内容是什么？**
  - A: 定理 TSN.1 指出，若网络中有 N 个设备参与时间触发通信，则所有设备的 GCL 周期 T 必须满足 `T = k × T_base`（k ∈ ℕ⁺），且时钟同步精度 `|BaseTimeᵢ - BaseTimeⱼ| < ε`（通常 < 1 μs）。详见 `11-industrial-iot-otit/02-opc-ua-fx/opc-ua-fx-reuse-hierarchy.md` §6。

- **Q: 棕地工厂中协议网关的架构定位是什么？**
  - A: 定理 FX.2（Gateway Eternity）指出：在棕地工厂中，协议网关不是临时过渡措施，而是**永久性架构组件**。声称"最终消除网关"的架构愿景违背工业现实。详见 `11-industrial-iot-otit/02-opc-ua-fx/opc-ua-fx-reuse-hierarchy.md` §5。

---

### 12 AI 原生复用 ⭐

- **Q: MCP 2025-11-25 与 2026-07-28 RC 在传输模型上的核心差异？**
  - A: 2025-11-25 为有状态会话（Stateful）+ initialize/initialized 握手；2026-07-28 RC 演进为无状态核心（Stateless），移除握手，每请求自包含，支持负载均衡和自动扩缩容。详见 `12-ai-native-reuse/01-mcp-protocol/mcp-2026-deep-dive.md` §1。

- **Q: A2A 的 Agent Card 发布位置是什么？**
  - A: 发布于 `/.well-known/agent-card.json`（RFC 8615），包含能力发现、技能列表、认证方案等元数据。详见 `12-ai-native-reuse/02-a2a-protocol/a2a-v1-deep-dive.md` §3.1。

- **Q: A2A 任务生命周期状态机包含哪些状态？**
  - A: submitted → working → [input-required | auth-required] → completed；可分支至 rejected / failed / canceled。详见 `12-ai-native-reuse/02-a2a-protocol/a2a-v1-deep-dive.md` §3.2。

- **Q: A2A 与 MCP 的生产最佳实践组合模式是什么？**
  - A: A2A Client Agent 将复杂任务委托给 A2A Server Agent；Server Agent **内部使用 MCP** 与其工具、API 和数据源交互。将 Agent 简单包装为 MCP tool 是本质上的限制。详见 `12-ai-native-reuse/02-a2a-protocol/a2a-v1-deep-dive.md` §5.3。

- **Q: 概率契约框架中的置信度函数 γ(x) 取值范围是什么？**
  - A: γ(x) ∈ [0, 1]，用于量化 AI 功能输出的可信度，需结合温度参数、Top-p、模型版本漂移进行校准。详见 `12-ai-native-reuse/05-probabilistic-contracts/README.md`。

- **Q: Conformal Prediction 的边际覆盖保证公式是什么？**
  - A: `P(y ∈ C(x)) ≥ 1 − α`，即在 α 显著性水平下，真实标签落在预测集合中的概率不低于 `1−α`。详见 `12-ai-native-reuse/05-probabilistic-contracts/README.md` 及 `05-conformal-prediction/cp-code-generation.md`。

- **Q: 定理 AI.1 (Calibration Ceiling) 的核心结论是什么？**
  - A: 当 LLM 输出分布与真实分布的 KL 散度 > ε 时，任何校准方法都无法使校准误差 < δ，即置信度校准存在理论上限。详见 `12-ai-native-reuse/README.md`。

---

### 13 新兴趋势

- **Q: 平台工程被 Gartner 预测在 2026 年的大型组织采用率是多少？**
  - A: 80% 的大型组织将建立平台团队，内部开发者平台（IDP）作为复用的组织化载体。详见 `13-emerging-trends/01-platform-engineering/platform-engineering-cncf-2026.md`。

- **Q: WebAssembly Component Model 的接口类型标准是什么？**
  - A: WIT（Wasm Interface Types），支持跨语言、跨运行时的组件复用，WASI 0.3 为最新运行时接口标准。详见 `13-emerging-trends/03-webassembly-components/wasm-component-model-2026.md`。

- **Q: 模块化单体的适用边界是什么？**
  - A: 团队 < 50 人，部署频率 < 1 天/次；可通过 Spring Modulith / OSGi / JPMS 实现渐进式拆分。详见 `13-emerging-trends/02-modular-monolith/modular-monolith-reuse.md`。

---

## 附录：快速检索标签

| 关键词 | 相关主题 | 问答对编号范围 |
|--------|---------|---------------|
| TLA+ | 07 | Q1–Q5 (07节) |
| Alloy | 07 | Q4–Q5 (07节) |
| Coq / Isabelle | 07 | Q6 (07节) |
| Rust / Cargo | 07, 04, 13 | Q7–Q8 (07节) |
| SPARK Ada | 07 | Q9 (07节) |
| SLSA | 10 | Q1–Q3 (10节) |
| SBOM | 10 | Q4 (10节) |
| Sigstore / cosign | 10 | Q8 (10节) |
| ISA-95 | 11 | Q1 (11节) |
| OPC UA FX | 11 | Q2–Q3 (11节) |
| AAS / 数字孪生 | 11 | Q4 (11节) |
| SEooC | 11 | Q6 (11节) |
| MCP | 05, 12 | Q1 (05节), Q1–Q2 (12节) |
| A2A | 05, 12 | Q2 (05节), Q2–Q4 (12节) |
| Conformal Prediction | 12 | Q6 (12节) |
| COCOMO II | 09 | Q1–Q3, Q7 (09节) |
| ROI / NPV | 09 | Q3, Q5–Q6 (09节) |
| ISO 42010 | 01 | Q1, Q3 (01节) |
| 成熟度模型 | 06 | Q1 (06节) |

---

> **维护说明**: 本索引随 `struct/` 内容迭代持续更新。新增问答对时应保持"问题 + 1–2 句简要答案 + 相对路径"的格式一致性。


---

## 补充说明：软件架构复用知识体系问答索引 (QA Index)

## 概念定义

**定义**：参考层是结构化知识体系的“地图”，汇总权威来源、术语表、标准索引、课程对标与审计报告，为各主题提供可追溯的引用与一致性校验。

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