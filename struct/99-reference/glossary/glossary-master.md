
## B

### Business Capability (业务能力)

- **定义**: 企业为达成特定结果而具备的稳定能力，通常独立于组织、流程、技术与实现，用于描述"企业能做什么"。
- **属性**:
  - 结果导向（Outcome-oriented）
  - 相对稳定（不随项目频繁变化）
  - 可分层（Level 1–5 能力树）
  - 可映射到价值流、应用服务与组件
- **关系**:
  - 上位：业务架构复用单元
  - 映射：TOGAF Capability Map、FEA BRM、BIAN Service Landscape
  - 实现：应用服务、业务过程、组织单元
- **解释**: 以业务能力为粒度进行复用，可在组织变革、并购或 IT 现代化时保持业务语义的连续性。
- **示例**: "客户开户"作为一个业务能力，在零售银行、私人银行、企业银行中可能有不同实现，但核心能力定义相同。
- **反例**: 将业务能力与具体部门或 IT 系统一一绑定，导致能力图随组织调整而频繁重写。
- **权威来源**:
  - [TOGAF® Standard, 10th Edition](https://www.opengroup.org/togaf) — The Open Group
  - [BIAN Service Landscape](https://bian.org/servicelandscape/) — BIAN
  - 核查日期：2026-07-07

### Business Process (业务流程)

- **定义**: 为达成特定业务目标而执行的一组相互关联、结构化的活动，通常具有明确的输入、输出、触发事件与参与者。
- **属性**:
  - 活动序列与顺序/并行关系
  - 明确的触发事件与完成条件
  - 涉及角色、数据与业务规则
  - 可建模（BPMN）、可执行（BPMN Engine + DMN）
- **关系**:
  - 上位：业务架构行为元素
  - 实现：BPMN 2.0、DMN 1.5
  - 复用：流程片段、流程模板、决策服务
- **解释**: 业务流程复用关注"如何做"的标准化；通过 BPMN/DMN 可将流程逻辑与实现平台解耦。
- **示例**: 将"贷款审批流程"建模为可复用 BPMN 模板，各子公司根据当地法规配置变性点（如额度阈值、审批层级）。
- **反例**: 将流程硬编码在单体应用中，未使用 BPMN 建模，导致流程调整需要重新发布整个系统。
- **权威来源**:
  - [BPMN 2.0 Specification](https://www.omg.org/spec/BPMN/) — OMG
  - [DMN 1.5 Specification](https://www.omg.org/spec/DMN/) — OMG
  - 核查日期：2026-07-07

---

## C

### Component (组件)

- **定义**: 系统中具有明确接口、可独立部署、可替换的软件单元，是组件级复用的基本对象。在本知识体系中，组件是架构约束在模块层的载体。
- **属性**:
  - 接口契约明确
  - 实现封装
  - 可独立版本化与部署
  - 多实例复用
- **关系**:
  - 上位：组件架构复用单元
  - 实现：JAR、NuGet、npm、crate、WASM component
  - 依赖：接口契约、依赖管理、版本策略
- **解释**: 组件复用将软件生产从编码转变为集成与组装；组件模型决定了复用的粒度与互操作方式。
- **示例**: 一个独立的"支付网关组件"通过标准支付接口被电商、订阅、 donation 三个系统复用。
- **反例**: 将高度耦合业务逻辑的代码包发布为"组件"，调用方被迫引入大量无关依赖，复用成本高于自研。
- **权威来源**:
  - [Component-based software engineering](https://en.wikipedia.org/wiki/Component-based_software_engineering) — Wikipedia
  - [Software Components: Only the Giants Survive](https://dl.acm.org/doi/10.1145/1238844.1238850) — Brad Cox, ACM
  - 核查日期：2026-07-07

### Component Model (组件模型)

- **定义**: 对组件本质特征及组件间关系的抽象描述，包括接口规范、生命周期、部署形态、交互机制与组合规则。
- **属性**:
  - 接口定义语言（IDL）
  - 生命周期状态（开发、发布、部署、退役）
  - 组合与装配机制
  - 平台/语言绑定
- **关系**:
  - 实例：CORBA、EJB、COM+、OSGi、WASM Component Model
  - 影响：语言生态、依赖管理、版本策略
- **解释**: 组件模型是组件复用的"语法"；不同模型在跨语言、跨平台、运行时隔离等方面有本质差异。
- **示例**: WebAssembly Component Model 使用 WIT（Wasm Interface Types）定义组件接口，支持跨语言组合与沙箱隔离。
- **反例**: 在需要高隔离的安全关键场景中选用无进程边界的轻量级组件模型，导致故障传播不可控。
- **权威来源**:
  - [WebAssembly Component Model](https://component-model.bytecodealliance.org/) — Bytecode Alliance
  - [OMG CORBA Component Model](https://www.omg.org/spec/CCM/) — OMG
  - 核查日期：2026-07-07

### Conformal Prediction (共形预测)

- **定义**: 一种非参数统计框架，为机器学习模型预测提供有限样本下的覆盖保证（coverage guarantee），输出预测集合而非单点预测。
- **属性**:
  - 覆盖保证：在可交换性假设下保证真实标签落入预测集合的概率
  - 非交换性校正（adaptive conformal inference）
  - 可与任意黑盒模型结合
  - 预测集合大小反映不确定性
- **关系**:
  - 应用：AI 原生复用中的概率契约
  - 互补：贝叶斯方法、蒙特卡洛 dropout
  - 依赖：校准数据集、非一致性分数（nonconformity score）
- **解释**: 在 AI 组件复用中，传统点预测无法量化风险；Conformal Prediction 为"AI 功能复用"提供可证明的不确定性边界。
- **示例**: 一个医学影像 AI 组件使用 Conformal Prediction 输出"良性/可疑/恶性"集合，确保 95% 覆盖率，医生据此决定是否需要活检。
- **反例**: 在未验证数据分布漂移的情况下直接应用共形预测，导致覆盖保证失效。
- **权威来源**:
  - [Algorithmic Learning in a Random World](https://link.springer.com/book/10.1007/978-3-031-06649-8) — Vovk, Gammerman, Shafer
  - [Conformal Prediction: A Gentle Introduction](https://arxiv.org/abs/2107.07511) — Angelopoulos & Bates
  - 核查日期：2026-07-07

### Correspondence (对应关系)

- **定义**: ISO/IEC/IEEE 42010:2022 中用于建立并保持架构视图、模型、元素之间一致性的关系及其验证方法。
- **属性**:
  - 可表达视图间映射
  - 可附带规则/方法验证一致性
  - 是 AD 完整性的核心证据
  - 可追溯至利益相关者关注点
- **关系**:
  - 属于：Architecture Description
  - 关联：View、Model、Architecture View Component
- **解释**: 复用往往涉及多视图（业务、应用、组件、功能）；Correspondence 保证这些视图之间不存在矛盾。
- **示例**: 在安全视图中标识的"认证服务"对应到应用视图中的"AuthService"组件，两者通过对应关系绑定。
- **反例**: 多个视图中使用同名但不同义的"服务"概念，未建立对应关系，导致架构评审时无法发现冲突。
- **权威来源**:
  - [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74296.html) — ISO
  - 核查日期：2026-07-07

---

## D

### Digital Twin (数字孪生)

- **定义**: 物理实体或系统的虚拟表示，通过实时数据同步、模型与仿真支持监控、分析、预测与优化。
- **属性**:
  - 与物理实体的连接（实时/准实时）
  - 多尺度（组件级、系统级、生态系统级）
  - 支持仿真与预测
  - 可复用模型与数据
- **关系**:
  - 实现：AAS、OPC UA、IoT 平台
  - 映射：ISA-95 L0–L4、CAD/PLM
  - 应用：工业 4.0、智慧城市、能源网络
- **解释**: 数字孪生使工业资产的能力、状态与历史可在软件中复用，支撑跨生命周期的决策。
- **示例**: 风力发电机的数字孪生整合 SCADA 数据、气象模型与疲劳模型，预测叶片维护窗口。
- **反例**: 仅建立 3D 可视化模型而无实时数据连接与仿真能力，称其为"数字孪生"。
- **权威来源**:
  - [Digital Twin](https://en.wikipedia.org/wiki/Digital_twin) — Wikipedia
  - [IEC 63278 AAS](https://webstore.iec.ch/publication/66912) — IEC
  - 核查日期：2026-07-07

---

## E

### EDA (Event-Driven Architecture, 事件驱动架构)

- **定义**: 一种以事件为核心进行组件间通信与协作的架构风格；组件通过发布、订阅、处理事件来解耦时间与空间依赖。
- **属性**:
  - 异步、解耦
  - 事件作为一等公民
  - 可扩展性与弹性
  - 支持 CQRS、事件溯源、流处理
- **关系**:
  - 互补：微服务、Serverless、消息队列
  - 实现：Kafka、RabbitMQ、EventBridge、NATS
  - 模式：Pub/Sub、Event Sourcing、CQRS
- **解释**: EDA 通过事件抽象使复用单元之间无需知道彼此存在，从而降低集成耦合。
- **示例**: 电商平台使用 Kafka 事件流：订单创建 → 库存扣减 → 物流调度 → 通知服务，各服务独立演进。
- **反例**: 在需要强一致性的财务转账场景中强制使用纯事件驱动，导致最终一致性与补偿逻辑复杂化。
- **权威来源**:
  - [Event-driven architecture](https://en.wikipedia.org/wiki/Event-driven_architecture) — Wikipedia
  - [Building Event-Driven Microservices](https://www.oreilly.com/library/view/building-event-driven-microservices/9781492057888/) — O'Reilly
  - 核查日期：2026-07-07

---

## F

### FaaS (Function as a Service)

- **定义**: 云计算服务模型，开发者上传函数代码，由平台按需执行、自动扩缩容并按调用计费；是功能架构复用的重要载体。
- **属性**:
  - 事件触发
  - 无服务器运维（Serverless）
  - 短生命周期执行
  - 自动弹性伸缩
- **关系**:
  - 上位：Serverless 计算
  - 实现：AWS Lambda、Azure Functions、Google Cloud Functions
  - 复用：函数模板、事件函数库
- **解释**: FaaS 将复用粒度细化到函数级，适合事件处理、ETL、API 后端等场景，但需关注冷启动与供应商锁定。
- **示例**: 将"图片缩略图生成"实现为 FaaS 函数，多个上传入口（Web、App、第三方）通过事件触发复用。
- **反例**: 将长时间运行、有状态的业务流程拆分为大量 FaaS 函数，导致编排复杂、状态管理困难。
- **权威来源**:
  - [Serverless computing](https://en.wikipedia.org/wiki/Serverless_computing) — Wikipedia
  - [CNCF Serverless Whitepaper v2](https://github.com/cncf/wg-serverless/blob/master/whitepapers/serverless-overview/README.md) — CNCF
  - 核查日期：2026-07-07

### Formal Verification (形式化验证)

- **定义**: 使用数学方法严格证明系统或其规约满足特定性质（如安全性、活性、不变量）的技术集合，包括模型检测、定理证明、类型系统验证等。
- **属性**:
  - 数学严谨性
  - 可穷举状态空间（模型检测）或构造证明（定理证明）
  - 成本高、需要专业知识
  - 适用于安全关键与高价值系统
- **关系**:
  - 方法：TLA+、Alloy、Coq、Isabelle、SPARK/Ada、Rust 类型系统
  - 标准：DO-178C/DO-333、IEC 61508、ISO 26262
  - 应用：安全关键组件复用
- **解释**: 形式化验证为复用组件提供"可证明正确"的信任基础，是供应链安全与功能安全的重要支撑。
- **示例**: 使用 TLA+ 验证分布式锁服务在分区容忍下的安全性，确保多个复用方不会同时获得锁。
- **反例**: 对快速迭代、需求不稳定的业务系统强行使用完整形式化验证，导致验证成本超过其价值。
- **权威来源**:
  - [Formal methods](https://en.wikipedia.org/wiki/Formal_methods) — Wikipedia
  - [Specifying Systems](https://lamport.azurewebsites.net/tla/book.html) — Leslie Lamport
  - 核查日期：2026-07-07

---

## I

### IDP (Internal Developer Platform)

- **定义**: 企业为开发团队提供的自助式内部平台，整合工具、流程、标准与可复用资产（Golden Path、模板、服务目录），降低认知负荷并提高交付效率。
- **属性**:
  - 自助服务（Self-service）
  - Golden Path 标准化
  - 软件目录（Software Catalog）
  - 可观测性与治理集成
- **关系**:
  - 上位：平台工程
  - 实现：Backstage、Port、Cortex、Spotify Golden Path
  - 对齐：CNCF Platform Engineering Maturity Model
- **解释**: IDP 是复用资产的"消费层"；没有良好的 IDP，可复用资产难以被开发者发现与使用。
- **示例**: 某公司通过 Backstage 提供"创建新微服务"Golden Path，自动配置 CI/CD、监控、安全扫描与依赖基线。
- **反例**: IDP 仅作为工具门户，未整合可复用资产与治理策略，开发者仍需手动寻找与申请资源。
- **权威来源**:
  - [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/) — CNCF
  - [Platform Engineering Maturity Model](https://tag-app-delivery.cncf.io/blog/maturity-model/) — CNCF
  - 核查日期：2026-07-07

### Interface Contract (接口契约)

- **定义**: 组件之间交互的显式约定，包括接口签名、前置条件、后置条件、不变量、异常语义、版本策略与质量属性（SLA）。
- **属性**:
  - 语法（签名、数据类型）
  - 语义（行为、状态、约束）
  - 质量（延迟、可用性、安全）
  - 版本兼容性规则
- **关系**:
  - 属于：组件架构
  - 实现：OpenAPI、gRPC protobuf、WIT、Design-by-Contract
  - 影响：依赖管理、版本策略
- **解释**: 接口契约是组件复用的"法律"；契约越清晰，复用越安全；契约越隐式，集成风险越高。
- **示例**: 一个组件接口声明"前置条件：用户已认证；后置条件：返回订单列表；不变量：订单状态机仅在允许转移间变化"。
- **反例**: 接口仅返回 200/500，未定义错误码语义与重试策略，调用方在不同场景下行为不一致。
- **权威来源**:
  - [Design by Contract](https://en.wikipedia.org/wiki/Design_by_contract) — Wikipedia
  - [Bertrand Meyer, Object-Oriented Software Construction](https://bertrandmeyer.com/OOSC/) — Prentice Hall
  - 核查日期：2026-07-07

### ISA-95

- **定义**: 国际标准 IEC 62264，定义企业级系统（ERP/MES）与控制系统（SCADA/PLC/DCS）之间的集成模型，通常以 L0–L4 层次模型表示。
- **属性**:
  - L0 物理过程 → L1 感知/执行 → L2 监控 → L3 制造运营 → L4 企业业务
  - 明确层级职责与信息流
  - 支持互操作与复用
  - 与 AAS、OPC UA 映射
- **关系**:
  - 上位：工业自动化参考模型
  - 映射：IEC 63278 AAS、OPC UA、IEC 61508
  - 应用：智能制造、工业 4.0
- **解释**: ISA-95 为工业软件复用提供了清晰的层次边界；跨层复用必须尊重 L0–L4 的实时性与安全要求。
- **示例**: MES（L3）将生产订单下发到产线控制系统（L2），PLC（L1）执行并反馈设备状态（L0）。
- **反例**: 将 ERP（L4）直接控制机器人（L1），绕过 MES/SCADA 的调度与安全约束，导致实时性与安全失控。
- **权威来源**:
  - [IEC 62264 / ISA-95](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95) — ISA
  - [AWS Industrial IoT Architecture Patterns - ISA-95 Mapping](https://docs.aws.amazon.com/whitepapers/latest/industrial-iot-architecture-patterns/mapping-to-the-isa-95-model.html) — AWS
  - 核查日期：2026-07-07

---

## M

### MCP (Model Context Protocol)

- **定义**: 由 Anthropic 发起、后捐给 Linux Foundation Agentic AI Foundation 的开放协议，用于标准化 LLM/Agent 与外部工具、数据源、资源之间的上下文交互。
- **属性**:
  - Server-Client 架构
  - 三类原语：Tools、Resources、Prompts
  - 支持 stdio、Streamable HTTP、OAuth 2.1
  - 2025-11-25 为当前稳定版
- **关系**:
  - 互补：A2A（Agent 间）、ANP、ACP
  - 依赖：JSON-RPC、OAuth 2.1、JSON Schema
  - 安全：OWASP MCP Top 10、Authorization spec
- **解释**: MCP 使 AI Agent 能够以统一方式复用外部能力，避免每个工具都写一次集成代码。
- **示例**: 一个代码助手通过 MCP 连接到 GitHub、Jira、内部文档库，动态获取上下文并执行搜索、创建 Issue 等工具。
- **反例**: 将 MCP Server 暴露给不受信任的客户端而未实施授权与输入校验，导致工具投毒（tool poisoning）攻击。
- **权威来源**:
  - [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2025-11-25) — MCP
  - [MCP Authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) — MCP
  - 核查日期：2026-07-07

### Microservices (微服务)

- **定义**: 一种将应用构建为围绕业务能力组织的小型、自治服务的架构风格；每个服务独立部署、独立扩展，通过轻量级机制通信。
- **属性**:
  - 围绕业务能力组织
  - 去中心化治理
  - 独立部署与扩展
  - 容错设计
  - 基础设施自动化
- **关系**:
  - 演进：单体 → SOA → 微服务 → 模块化单体
  - 实现：容器、Kubernetes、服务网格
  - 复用：服务目录、API 网关、Sidecar
- **解释**: 微服务通过服务边界实现应用级复用；但服务粒度过细会导致分布式复杂性。
- **示例**: 电商平台将用户、订单、库存、支付拆分为独立微服务，各团队可独立发布。
- **反例**: 将本可共享数据库表的两服务强行拆分，却通过同步 HTTP 频繁调用并共享数据库，形成"分布式单体"。
- **权威来源**:
  - [Microservices](https://martinfowler.com/articles/microservices.html) — Martin Fowler
  - [Microservices](https://en.wikipedia.org/wiki/Microservices) — Wikipedia
  - 核查日期：2026-07-07

### Model Kind (模型种类)

- **定义**: ISO/IEC/IEEE 42010:2022 中定义的一类建模约定，包括其符号、语法、语义与规则，用于创建特定类型的架构模型。
- **属性**:
  - 约定语言/符号
  - 语法与语义规则
  - 适用于特定关注点
  - 可在一个 Viewpoint 中使用多个 Model Kind
- **关系**:
  - 属于：Architecture Description
  - 被使用：Viewpoint
  - 实例：UML 类图、ArchiMate 应用协作图、BPMN 流程图
- **解释**: 模型种类规定了"如何画"以及"画什么"；复用架构描述时，必须理解其采用的 Model Kind。
- **示例**: "安全性视图"使用威胁模型（STRIDE）与攻击树两种 Model Kind 来表达不同安全关注点。
- **反例**: 将 UML 部署图与网络拓扑图混用而不说明 Model Kind，导致同一符号在不同图中含义不同。
- **权威来源**:
  - [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74296.html) — ISO
  - 核查日期：2026-07-07

---

## O

### OPC UA (OPC Unified Architecture)

- **定义**: 工业自动化领域跨平台的机器对机器通信协议与信息模型标准，支持语义化数据建模、安全通信与复杂数据结构。
- **属性**:
  - 语义信息模型（Object/Variable/Method）
  - 客户端-服务器与发布-订阅两种通信模式
  - 内置安全机制（证书、加密、签名）
  - OPC UA FX 扩展支持现场级确定性通信
- **关系**:
  - 上位：工业互操作协议
  - 映射：ISA-95、IEC 63278 AAS、IEC 62541
  - 扩展：OPC UA FX、PubSub、TSN 集成
- **解释**: OPC UA 使工业设备的能力与数据能够以标准化语义被复用，是 OT-IT 融合的关键协议。
- **示例**: 不同厂商的机器人通过 OPC UA 暴露统一的状态变量与操作方法，MES 无需针对每款机器人编写适配器。
- **反例**: 仅使用 OPC UA 的传输层而未建立统一信息模型，导致不同厂商数据语义不一致。
- **权威来源**:
  - [OPC Unified Architecture](https://en.wikipedia.org/wiki/OPC_Unified_Architecture) — Wikipedia
  - [OPC UA Specification](https://opcfoundation.org/about/opc-technologies/opc-ua/) — OPC Foundation
  - 核查日期：2026-07-07

---

## P

### Platform Engineering (平台工程)

- **定义**: 构建并维护内部开发者平台（IDP）的学科与实践，通过自助服务、标准化路径与可复用能力提高软件开发效率与一致性。
- **属性**:
  - 产品化内部平台
  - Golden Path 与模板
  - 开发者体验优先
  - 平台即产品（Platform as a Product）
- **关系**:
  - 实现：IDP、Backstage、Portal
  - 对齐：DevOps、SRE、Cloud Native
  - 评估：CNCF Platform Engineering Maturity Model
- **解释**: 平台工程将基础设施、安全、可观测性等能力产品化，使开发团队能够专注于业务逻辑。
- **示例**: 平台团队提供"部署到 Kubernetes"Golden Path，封装 Helm Chart、CI/CD、监控、安全扫描，开发者只需填写业务参数。
- **反例**: 平台团队单方面决定所有技术栈，不提供自助服务，导致开发者绕过平台形成"影子 IT"。
- **权威来源**:
  - [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/) — CNCF
  - [Team Topologies](https://teamtopologies.com/) — Matthew Skelton, Manuel Pais
  - 核查日期：2026-07-07

### Product Line Engineering (PLE, 产品线工程)

- **定义**: 通过系统化复用一组核心资产（core assets）来开发一组相关产品的软件工程方法，强调共性（commonality）与变性（variability）的管理。
- **属性**:
  - 领域工程 + 应用工程 + 管理
  - 特征模型（Feature Model）描述变性
  - 核心资产库
  - 绑定时间与变性点
- **关系**:
  - 标准：ISO/IEC 26550、ISO/IEC 26565（产品线成熟度框架）、ISO/IEC 26566（产品线纹理）
  - 方法：FODA、FeatureIDE、Pure::Variants
  - 应用：汽车、航空、工业自动化、移动设备
- **解释**: PLE 是系统化复用的高级形式；通过特征模型可在产品族内高效派生多个变体。
- **示例**: 汽车厂商使用同一平台开发轿车、SUV、卡车，通过特征模型选择动力系统、车身、内饰等变体。
- **反例**: 未明确定义变性点与绑定时间，导致各产品分支独立维护，复用收益被抵消。
- **权威来源**:
  - [ISO/IEC 26550:2015](https://www.iso.org/standard/69529.html) — ISO
  - [ISO/IEC 26565:2026](https://www.iso.org/standard/81436.html) — ISO 产品线成熟度框架
  - [ISO/IEC 26566:2026](https://www.iso.org/standard/81437.html) — ISO 产品线纹理
  - 核查日期：2026-07-07

### Probabilistic Contract (概率契约)

- **定义**: 为 AI/不确定系统定义的契约，允许行为以概率形式满足规范（如"在 95% 的情况下响应延迟 < 200ms"），通常结合共形预测或统计验证。
- **属性**:
  - 概率化前置/后置条件
  - 可校准的置信水平
  - 覆盖保证与风险边界
  - 非确定性行为的显式量化
- **关系**:
  - 扩展：传统 Design-by-Contract
  - 方法：Conformal Prediction、统计模型检测
  - 应用：AI 功能复用、自动驾驶、医疗 AI
- **解释**: 传统契约无法表达 AI 的不确定性；概率契约将"软承诺"转化为可验证、可治理的约束。
- **示例**: 一个推荐系统承诺"推荐集合包含用户感兴趣项的概率 ≥ 90%"，并通过共形预测验证。
- **反例**: 将概率契约当作普通 SLA 使用，忽视其统计假设与校准要求，导致合规风险。
- **权威来源**:
  - [Conformal Prediction for Reliable Machine Learning](https://arxiv.org/abs/2107.07511) — Angelopoulos & Bates
  - [Probabilistic Contracts](https://doi.org/10.1145/3544548.3580835) — 相关 ACM 论文
  - 核查日期：2026-07-07

---

## R

### Reuse (复用)

- **定义**: 在多个上下文、系统或项目中使用已有软件资产（代码、设计、模式、服务、架构、知识）的过程；本知识体系进一步将复用定义为**约束的传递**。
- **属性**:
  - 基于可复用资产
  - 管理共性与变性
  - 需要上下文适配
  - 存在成本-收益阈值
- **关系**:
  - 元公理：M.1 Architecture-Reuse Duality
  - 层次：业务复用、应用复用、组件复用、功能复用
  - 治理：成熟度模型、度量、FinOps
- **解释**: 复用不是复制粘贴；成功的复用需要在通用性与特异性之间取得平衡，并通过治理机制维护。
- **示例**: 将组织级认证服务复用于 20 个业务系统，避免重复开发并保证安全策略一致。
- **反例**: 将高度耦合的代码片段复制到多个项目，未剥离业务专属逻辑，导致后续变更需要在多处同步修改。
- **权威来源**:
  - [Software reuse](https://en.wikipedia.org/wiki/Code_reuse) — Wikipedia
  - [IEEE 1517-2010](https://standards.ieee.org/standard/1517-2010.html) — IEEE
  - 核查日期：2026-07-07

### Reusable Asset (可复用资产)

- **定义**: 在特定上下文中被设计、文档化并治理，能够在多个系统、项目或组织中重复使用的软件工程制品；其边界由显式契约、稳定接口与可验证质量属性共同定义。
- **属性**:
  - 稳定性（变更频率低于使用频率）
  - 通用性（适用于 ≥2 个上下文）
  - 封装性（内部实现对使用者不可见）
  - 可发现性（目录、元数据、标签）
  - 可验证质量（测试、证明、评分）
- **关系**:
  - 存在公理：E.1 Reuse Asset Existence
  - 形式：组件、服务、API、模板、模式、架构、知识包
  - 治理：RAS、SBOM、SLSA
- **解释**: 可复用资产是复用的基本单元；资产质量直接决定复用的成功率。
- **示例**: 一个提供 OAuth 2.1 接口、SLA 保证与审计日志的组织级认证服务。
- **反例**: 未经测试、无文档、无版本号的内部脚本被多个团队复用，导致故障频发。
- **权威来源**:
  - [OMG RAS v2.2](https://www.omg.org/spec/RAS/) — OMG
  - [ISO/IEC 26550:2015](https://www.iso.org/standard/69529.html) — ISO
  - 核查日期：2026-07-07

### ROI (Return on Investment, 投资回报率)

- **定义**: 衡量复用投资经济价值的指标，通常比较复用成本（学习、适配、集成、治理）与自研成本及长期收益。
- **属性**:
  - 可量化成本与收益
  - 考虑时间价值（NPV、IRR）
  - 包含战略价值（实物期权）
  - 受复用次数与规模影响
- **关系**:
  - 方法：COCOMO II、NPV、Real Options
  - 应用：复用决策、平台投资、资产退役
  - 扩展：碳排价值（SCI）、合规价值
- **解释**: 复用并非总是经济最优；ROI 分析帮助组织在"自研 vs 复用 vs 购买"之间做出理性决策。
- **示例**: 某公司通过 COCOMO II 估算自研认证模块需 800 人时，复用现有服务需 200 人时，预计 5 个项目即可收回投资。
- **反例**: 仅计算初始开发成本，忽视长期维护、治理与机会成本，导致低估复用总成本。
- **权威来源**:
  - [COCOMO II Model Definition Manual](http://csse.usc.edu/csse/research/COCOMOII/cocomo2000.0.pdf) — USC
  - [Real Options](https://en.wikipedia.org/wiki/Real_options_valuation) — Wikipedia
  - 核查日期：2026-07-07

---

## S

### SBOM (Software Bill of Materials)

- **定义**: 软件组件及其依赖的清单，通常包括名称、版本、供应商、许可证、哈希值与漏洞信息；是供应链透明度的基础。
- **属性**:
  - 机器可读（SPDX、CycloneDX、SWID）
  - 层级依赖关系
  - 与漏洞数据（VEX）关联
  - 生成、分发与验证流程
- **关系**:
  - 互补：SLSA、Sigstore、GUAC
  - 标准：SPDX 2.3、CycloneDX 1.6
  - 法规：EU CRA、US EO 14028
- **解释**: 没有 SBOM，组织无法快速判断自身是否受某个供应链漏洞影响；SBOM 是复用资产治理的"成分表"。
- **示例**: 某产品发布时附带 SPDX SBOM，当 Log4Shell 爆发时，安全团队 30 分钟内定位受影响实例。
- **反例**: SBOM 仅在手写文档中维护，与实际构建产物不一致，导致漏洞响应基于过时信息。
- **权威来源**:
  - [SPDX Specification](https://spdx.dev/specifications/) — Linux Foundation
  - [CycloneDX Specification](https://cyclonedx.org/specification/overview/) — OWASP
  - 核查日期：2026-07-07

### Serverless

- **定义**: 一种云计算执行模型，云提供商动态管理计算资源，开发者无需关心服务器运维；通常与 FaaS 结合使用，但也包含托管数据库、消息队列等 BaaS 服务。
- **属性**:
  - 无服务器运维
  - 事件驱动
  - 自动弹性
  - 按使用付费
  - 供应商特定服务
- **关系**:
  - 实现：FaaS + BaaS
  - 复用：函数模板、事件源连接器
  - 风险：供应商锁定、冷启动、可观测性
- **解释**: Serverless 将复用粒度进一步细化到函数与托管服务，适合事件驱动、可变负载场景。
- **示例**: 使用 AWS Lambda + API Gateway + DynamoDB 构建无服务器 API，自动扩缩容。
- **反例**: 将需要长期运行、有状态的复杂工作流全部用 FaaS 实现，导致编排复杂、调试困难。
- **权威来源**:
  - [Serverless computing](https://en.wikipedia.org/wiki/Serverless_computing) — Wikipedia
  - [CNCF Serverless Whitepaper v2](https://github.com/cncf/wg-serverless/blob/master/whitepapers/serverless-overview/README.md) — CNCF
  - 核查日期：2026-07-07

### Service Mesh (服务网格)

- **定义**: 专门处理服务间通信的基础设施层，通过 Sidecar 代理为微服务提供流量管理、安全、可观测性等横切能力。
- **属性**:
  - 独立于应用代码
  - 提供 mTLS、熔断、重试、限流
  - 统一可观测性
  - 支持多集群/多租户
- **关系**:
  - 实现：Istio、Linkerd、Consul Connect
  - 互补：Kubernetes、Gateway API
  - 复用：通信模式、安全策略、流量规则
- **解释**: 服务网格将微服务通信的共性问题下沉到基础设施，使应用开发者专注于业务逻辑。
- **示例**: 使用 Istio 为所有微服务自动启用 mTLS、指标收集与熔断策略，无需修改服务代码。
- **反例**: 在仅有少量服务且流量简单的系统中引入服务网格，增加运维复杂度而未获得实质收益。
- **权威来源**:
  - [Service mesh](https://en.wikipedia.org/wiki/Service_mesh) — Wikipedia
  - [CNCF Service Mesh Whitepaper](https://github.com/cncf/wg-service-mesh) — CNCF
  - 核查日期：2026-07-07

### SLSA (Supply-chain Levels for Software Artifacts)

- **定义**: 由 OpenSSF 维护的框架，定义递增的软件供应链完整性要求，防止篡改并提升构建、来源与依赖的可信度；当前版本 1.2 包含 Build Track 与 Source Track。
- **属性**:
  - Build Track L1–L3（来源证明、托管构建、加固平台）
  - Source Track L1–L3（版本控制、托管审查、双人审查）
  - 基于 in-toto attestation
  - 与 SBOM、Sigstore、VEX 协同
- **关系**:
  - 互补：NIST SSDF、OWASP SCVS、EU CRA
  - 实现：Sigstore/cosign、GitHub Actions、SLSA generators
  - 映射：NIST SP 800-218
- **解释**: SLSA 为复用外部组件提供信任等级；等级越高，对组件来源与构建过程的保证越强。
- **示例**: 开源项目使用 GitHub Actions + SLSA generator 生成 L3 provenance attestation，用户可验证软件包未被篡改。
- **反例**: 宣称达到 SLSA L3 却将签名密钥存储在 CI 配置中，用户可访问密钥导致隔离要求失效。
- **权威来源**:
  - [SLSA Specification v1.2](https://slsa.dev/spec/v1.2/) — OpenSSF
  - [OpenSSF Secure Open Source Software Vision Brief 2025](https://openssf.org/wp-content/uploads/2025/02/OpenSSF_2025_Vision_Brief.pdf) — OpenSSF
  - 核查日期：2026-07-07

### Stakeholder (利益相关者)

- **定义**: 对系统或其架构有利益、关注或影响的个人、群体或组织；其关注点驱动架构视图的创建（ISO/IEC/IEEE 42010:2022）。
- **属性**:
  - 有明确的关注点（Concern）
  - 可能是内部或外部
  - 可映射到特定视图/视点
  - 关注点的优先级可冲突
- **关系**:
  - 驱动：Architecture View、Viewpoint
  - 属于：Architecture Description
  - 示例：最终用户、架构师、安全官、运维、审计、监管者
- **解释**: 复用决策往往涉及多利益相关者；不理解其关注点，无法设计出被接受的复用方案。
- **示例**: 安全团队关注数据隔离，财务团队关注成本分摊，开发团队关注易用性；三者需要不同视图表达。
- **反例**: 架构描述未识别安全审计人员为利益相关者，导致复用方案未考虑合规要求。
- **权威来源**:
  - [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74296.html) — ISO
  - 核查日期：2026-07-07

---

## T

### TLA+

- **定义**: 由 Leslie Lamport 开发的规约语言，基于时序逻辑动作（Temporal Logic of Actions），用于形式化描述并发与分布式系统。
- **属性**:
  - 状态、动作、不变量、活性
  - 模型检测器 TLC
  - 证明器 TLAPS
  - 适合并发、分布式算法
- **关系**:
  - 应用：形式化验证
  - 互补：Alloy（结构建模）、Coq/Isabelle（定理证明）
  - 教材：《Specifying Systems》
- **解释**: TLA+ 帮助架构师在复用并发/分布式组件前验证其行为是否满足安全与活性要求。
- **示例**: 使用 TLA+ 验证分布式数据库的复制协议在分区容忍下保持线性一致性。
- **反例**: 对简单顺序逻辑使用 TLA+，学习曲线与验证收益不匹配。
- **权威来源**:
  - [Specifying Systems](https://lamport.azurewebsites.net/tla/book.html) — Leslie Lamport
  - [TLA+ Home Page](https://lamport.azurewebsites.net/tla/tla.html) — Leslie Lamport
  - 核查日期：2026-07-07

### TOGAF

- **定义**: The Open Group 维护的企业架构开发方法框架，提供 ADM（Architecture Development Method）、架构内容元模型、能力框架与参考模型。
- **属性**:
  - ADM 周期性方法
  - 架构内容框架（元模型、分类、目录）
  - 企业连续体（Enterprise Continuum）
  - 架构能力与治理
- **关系**:
  - 对齐：ArchiMate、ISO 42010
  - 应用：业务架构、应用架构、技术架构
  - 版本：TOGAF Standard, 10th Edition
- **解释**: TOGAF 为组织级复用提供方法框架；企业连续体帮助组织识别可复用的架构资产。
- **示例**: 企业使用 TOGAF ADM 定义未来状态架构，并通过架构存储库识别可复用的共享服务。
- **反例**: 机械执行 TOGAF ADM 所有阶段而不考虑组织规模与敏捷需求，导致流程过重。
- **权威来源**:
  - [TOGAF® Standard, 10th Edition](https://www.opengroup.org/togaf) — The Open Group
  - 核查日期：2026-07-07

---

## V

### Value Stream (价值流)

- **定义**: 为向客户交付价值而执行的一系列端到端活动，通常跨越多个业务能力与组织边界；价值流复用关注价值创造步骤的标准化。
- **属性**:
  - 端到端客户价值导向
  - 跨部门/跨系统
  - 可识别价值增值与非增值步骤
  - 可映射到业务能力、流程与应用服务
- **关系**:
  - 上位：业务架构行为元素
  - 对齐：TOGAF、ITIL、Lean
  - 实现：BPMN、工作流编排
- **解释**: 价值流帮助组织从"部门视角"转向"客户价值视角"，识别复用机会与瓶颈。
- **示例**: "订单到收款"价值流包含销售、信用检查、发货、开票、收款等步骤，可识别哪些步骤可跨产品线复用。
- **反例**: 将价值流画得过于粗略，未与业务能力、应用服务建立映射，无法指导复用设计。
- **权威来源**:
  - [Value stream](https://en.wikipedia.org/wiki/Value_stream) — Wikipedia
  - [Value Stream Management](https://www.scaledagileframework.com/value-streams/) — SAFe
  - 核查日期：2026-07-07

### Variation Point (变性点)

- **定义**: 软件资产族中允许不同产品或上下文进行差异化实现的位置；是管理共性与变性的关键机制。
- **属性**:
  - 明确标识可变位置
  - 有绑定时间（编译时、部署时、运行时）
  - 有绑定规则/约束
  - 与特征模型关联
- **关系**:
  - 核心：可变性管理
  - 方法：特征模型、配置管理、插件机制
  - 应用：产品线工程、框架、可配置组件
- **解释**: 没有变性管理的复用是克隆；变性点使同一资产能够适应不同上下文而不过度复杂化。
- **示例**: 汽车信息娱乐系统的 UI 主题、语言、法规支持作为变性点，通过配置文件在不同市场绑定。
- **反例**: 将每个客户定制都实现为新的变性点而不加约束，导致组合爆炸与测试不可行。
- **权威来源**:
  - [ISO/IEC 26550:2015](https://www.iso.org/standard/69529.html) — ISO
  - [Feature-Oriented Domain Analysis (FODA)](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=11231) — SEI
  - 核查日期：2026-07-07

### Viewpoint (视点)

- **定义**: 用于创建、解释和使用架构视图的约定集合，包括关注点、受众、模型种类与分析技术（ISO/IEC/IEEE 42010:2022）。
- **属性**:
  - 针对特定利益相关者关注点
  - 定义视图应包含的模型种类
  - 规定符号、约定与分析规则
  - 可复用（标准化视点库）
- **关系**:
  - 产生：View
  - 属于：Architecture Description
  - 对齐：ISO 42010 Viewpoint、Kruchten 4+1、C4
- **解释**: 视点是架构描述的"镜头"；不同视点让不同利益相关者看到与自身相关的架构方面。
- **示例**: "性能视点"关注响应时间、吞吐量、资源使用，使用性能模型与瓶颈分析技术。
- **反例**: 一个视图混合了安全、性能与业务逻辑三种关注点，未采用不同视点，导致沟通效率低下。
- **权威来源**:
  - [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74296.html) — ISO
  - 核查日期：2026-07-07

---

## W

### WASM Component Model (WebAssembly Component Model)

- **定义**: WebAssembly 的组件模型扩展，允许使用 WIT（Wasm Interface Types）定义语言无关的组件接口，支持跨语言组合与沙箱化部署。
- **属性**:
  - 语言无关接口（WIT）
  - 基于能力的安全模型
  - 可组合性（组件可嵌套组合）
  - 与 WASI 配合提供系统接口
- **关系**:
  - 上位：组件模型
  - 运行时：Wasmtime、WasmEdge、WAMR
  - 语言：Rust、C/C++、Go、Python、.NET
- **解释**: WASM Component Model 有潜力成为跨语言、跨平台的通用组件复用基础设施。
- **示例**: 使用 Rust 编写的图像处理组件通过 WIT 接口被 Python Web 应用复用，无需重新实现。
- **反例**: 在需要原生性能与直接硬件访问的场景中强制使用 WASM，忽略虚拟化开销与接口限制。
- **权威来源**:
  - [WebAssembly Component Model](https://component-model.bytecodealliance.org/) — Bytecode Alliance
  - [WASI Preview 2](https://wasi.dev/) — WASI
  - 核查日期：2026-07-07

---

## 附录：术语索引表

| 术语 | 首字母 | 所属主题 | 交叉引用 |
|---|---|---|---|
| A2A | A | 12-AI 原生复用 | MCP、Agent |
| AAS | A | 11-工业 IoT | OPC UA、ISA-95、Digital Twin |
| API | A | 05-功能架构复用 | REST、gRPC、GraphQL |
| ArchiMate | A | 01-元模型 | TOGAF、ISO 42010 |
| Architecture | A | 01-元模型 | AD、Viewpoint、View |
| Architecture Description | A | 01-元模型 | ADL、ADF、Model Kind |
| Business Capability | B | 02-业务架构 | TOGAF、FEA BRM |
| Business Process | B | 02-业务架构 | BPMN、DMN |
| Component | C | 04-组件架构 | Interface Contract、Component Model |
| Component Model | C | 04-组件架构 | WASM、CORBA、OSGi |
| Conformal Prediction | C | 12-AI 原生复用 | Probabilistic Contract |
| Correspondence | C | 01-元模型 | View、Model Kind |
| Digital Twin | D | 11-工业 IoT | AAS、OPC UA |
| EDA | E | 03-应用架构 | Kafka、CQRS |
| FaaS | F | 05-功能架构 | Serverless、Lambda |
| Formal Verification | F | 07-形式化验证 | TLA+、Alloy、Coq |
| IDP | I | 13-新兴趋势 | Platform Engineering、Backstage |
| Interface Contract | I | 04-组件架构 | Design-by-Contract |
| ISA-95 | I | 11-工业 IoT | AAS、OPC UA |
| MCP | M | 12-AI 原生复用 | A2A、Tool、Resource |
| Microservices | M | 03-应用架构 | Service Mesh、API Gateway |
| Model Kind | M | 01-元模型 | Viewpoint、AD |
| OPC UA | O | 11-工业 IoT | AAS、ISA-95 |
| Platform Engineering | P | 13-新兴趋势 | IDP、Golden Path |
| Product Line Engineering | P | 01-元模型/02-业务 | ISO 26550、Feature Model |
| Probabilistic Contract | P | 12-AI 原生复用 | Conformal Prediction |
| Reuse | R | 01-元模型 | Reusable Asset、PLE |
| Reusable Asset | R | 01-元模型 | RAS、SLSA |
| ROI | R | 09-价值量化 | COCOMO II、NPV |
| SBOM | S | 10-供应链安全 | SLSA、SPDX、CycloneDX |
| Serverless | S | 03-应用架构 | FaaS、BaaS |
| Service Mesh | S | 03-应用架构 | Istio、Linkerd |
| SLSA | S | 10-供应链安全 | SBOM、Sigstore |
| Stakeholder | S | 01-元模型 | Concern、Viewpoint |
| TLA+ | T | 07-形式化验证 | TLC、TLAPS |
| TOGAF | T | 01-元模型 | ADM、ArchiMate |
| Value Stream | V | 02-业务架构 | BPMN、Capability |
| Variation Point | V | 01-元模型/04-组件 | Feature Model |
| Viewpoint | V | 01-元模型 | View、Stakeholder |
| WASM Component Model | W | 13-新兴趋势 | WIT、WASI |
