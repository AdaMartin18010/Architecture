# 国际标准对齐多维总矩阵

> **版本**: 2026-06-10 v2.0
> **定位**: 全体系的国际标准、框架、建模语言、质量度量、过程标准的交叉映射总表
> **维护**: 每季度对照 ISO/OMG/IEEE 官网更新一次

---

## 矩阵 A：复用层次 × 标准族

| 复用层次 | 核心标准 | 辅助标准 | 架构框架 | 建模语言 | 质量度量 | 过程标准 | 协议/接口 | 2026 新增 |
|----------|----------|----------|----------|----------|----------|----------|-----------|-----------|
| **元模型** | ISO/IEC/IEEE 42010:2022 | ISO/IEC/IEEE 24765, ISO/IEC/IEEE 15288, **OMG RAS**, **FAIR4RS**, **IEEE 1517** | TOGAF 10, Zachman | ArchiMate 3.2+ | ISO 25010:2023 | ISO/IEC/IEEE 42020 | N/A | DIS 42024/42042 |
| **业务** | FEA BRM 2.0 | ISO/IEC/IEEE 15288, BPMN 2.0 | TOGAF Phase B | ArchiMate Business, BPMN | ISO 25010 | 42020 | REST/GraphQL | DMN 1.5, ArchiMate 3.2 |
| **应用** | FEA ARM/SRM | ISO/IEC 26550, C4 | TOGAF Phase C/D | ArchiMate Application | ISO 25010 | 42020/1517 | gRPC/REST/Gateway API | Service Mesh, WASM, TOSCA v2.0, OASIS TOSCA v2.0 |
| **组件** | ISO 26566:2026（产品线纹理方法/工具能力） | IEEE 1517, C4, OWASP SCVS | arc42, C4 | UML Component | NASA RRL | 42020/12207 | FFI/WIT/Bindgen | WASM Component Model 3.0, WASI 0.3 Preview, SBOM |
| **功能** | IEEE 1517 | ISO 25010, COCOMO II | Serverless, Temporal | 代码/流程图/决策表/BPMN | 复用率/覆盖率 | 12207/15504 | MCP/A2A/DMN | **MCP 2025-11-25**, A2A v1.0, DMN 1.5 |
| **治理** | ISO/IEC 26565:2026（产品线成熟度框架） | RiSE/RCMM, FinOps, CMMI | TOGAF ADM | 成熟度模型 | ISO/IEC 26564:2022 | 42030 | OPA/Gatekeeper | Agentic Governance, Cloud Unit Economics |
| **安全** | SLSA 1.2 | NIST SSDF 1.2, OWASP SCVS | 零信任架构 | 攻击树、威胁模型 | CVSS/EPSS | ISO 27034, EU CRA | Sigstore/cosign | SLSA Multi-Track, Agentic AI Security |
| **工业** | ISA-95 / IEC 62264 | **IEC 61508 Ed.3** (CDV 投票完成，RVC 2026-05-15；IEC 官方预测发布 2026-07), **ISO 26262 Ed.3** (~2029) | RAMI 4.0 | UML, IEC 63278 AAS, PLCopen | SIL/ASIL | IEC 61508 lifecycle | OPC UA FX, TSN, Safe Motion | OPC UA FX 1.0 (Parts 80–84), TinyML, Edge AI, UADP |

> **更新说明**:
> 经权威核实，MCP 当前稳定版为 **2025-11-25**（2025-12-09 捐给 Linux Foundation Agentic AI Foundation）；**2026-07-28** 为官方 Release Candidate（2026-05-29 发布），最终版预计 2026-07-28，本矩阵统一以稳定版 2025-11-25 为基线。
> 新增 **OMG RAS v2.2**、**FAIR4RS**、**ISO/IEC/IEEE 1517:2010** 三个元模型层标准对齐。
> A2A 当前稳定版为 v1.0（Google Cloud Next 2026 发布）。WASM Component Model 跟踪 WASI 0.3 preview（2026 初）和 1.0 目标（2026 末/2027 初）。
> 工业层 UADP 作为 OPC UA FX 底层传输独立标注。
> [1](https://modelcontextprotocol.io/specification/2025-11-25)
> [2](https://a2a-protocol.org/latest/)
> [3](https://webassembly.org)
> [4](https://opcfoundation.org)

---

## 矩阵 B：标准 × 主题覆盖度

| 标准/框架 | 元模型 | 业务 | 应用 | 组件 | 功能 | 治理 | 安全 | 工业 |
|-----------|--------|------|------|------|------|------|------|------|
| **ISO 42010:2022** | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★☆☆☆ |
| **TOGAF 10** | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★☆☆☆ | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ |
| **ArchiMate 3.2+** | ★★★☆☆ | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★★☆☆ |
| **ISO 26550:2015** | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★★☆☆ |
| **ISO 26566:2026**（产品线纹理） | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★★★ | ☆☆☆☆☆ | ★★☆☆☆ |
| **IEEE 1517** | ★★☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ | ☆☆☆☆☆ | ★★☆☆☆ |
| **FEA 2.0** | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ☆☆☆☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ |
| **BPMN 2.0** | ★★☆☆☆ | ★★★★★ | ★★★☆☆ | ☆☆☆☆☆ | ★★★★☆ | ★★☆☆☆ | ☆☆☆☆☆ | ★★★☆☆ |
| **DMN 1.5** | ★★☆☆☆ | ★★★★☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★★★★ | ★★☆☆☆ | ☆☆☆☆☆ | ★★☆☆☆ |
| **SLSA 1.2** | ☆☆☆☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| **ISA-95 / IEC 62264** | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★★★ |
| **IEC 61508** | ★★☆☆☆ | ☆☆☆☆☆ | ★★☆☆☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★★ |
| **MCP 2025-11-25** | ★★☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ |
| **A2A v1.0.0** | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★☆☆☆ |
| **OPC UA FX 1.0** | ★★☆☆☆ | ☆☆☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★★☆ | ★★★★★ |
| **WASM Component Model** | ★★★☆☆ | ☆☆☆☆☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ★★★★☆ | ★★☆☆☆ |
| **OMG RAS v2.2** | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ☆☆☆☆☆ |
| **FAIR4RS** | ★★★☆☆ | ☆☆☆☆☆ | ★★☆☆☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ★★☆☆☆ |
| **ISO/IEC/IEEE 42020:2019** | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | ★★★★★ | ☆☆☆☆☆ | ★★☆☆☆ |
| **ISO 42030:2019** | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | ★★☆☆☆ | ☆☆☆☆☆ | ★★★★★ | ☆☆☆☆☆ | ★★☆☆☆ |
| **ISO 25040:2024** | ★★★☆☆ | ☆☆☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★★★★ | ☆☆☆☆☆ | ☆☆☆☆☆ |
| **ISO/IEC/IEEE 12207:2026** | ★★☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★☆☆☆ |
| **ISO 33000 (SPICE)** | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | ★★★★★ | ☆☆☆☆☆ | ★★☆☆☆ |
| **NIST SP 800-204** | ☆☆☆☆☆ | ☆☆☆☆☆ | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★☆☆☆ | ★★★★☆ | ☆☆☆☆☆ |
| **IEC 62443** | ★★☆☆☆ | ☆☆☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | ★★★★★ |
| **ISO/IEC 21838** | ★★★★★ | ☆☆☆☆☆ | ★★☆☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ |
| **OMG SysML v2** | ★★★☆☆ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★☆☆☆ | ☆☆☆☆☆ | ★★★☆☆ |
| **W3C WASM Core** | ★★★☆☆ | ☆☆☆☆☆ | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | ★★☆☆☆ |
| **The Open Group O-PAS** | ★★☆☆☆ | ☆☆☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★★☆ | ★★★★★ |

> **评分依据**:
> MCP 与 A2A 在功能层均为 ★★★★★（协议设计目标即为功能级 AI 复用）；
> A2A 在应用层评分高于 MCP（Agent Card 支持服务化发现与编排），在治理层因 Signed Agent Cards 与多租户支持评分 ★★★★☆；
> OPC UA FX 工业层 ★★★★★（现场层通信基线）；WASM Component Model 组件层 ★★★★★（跨语言组件封装）。
> 评分与 `axiom-theorem-tree.md` 中定理 5.1（Tool Reuse Equivalence）、定理 AI.2（MCP-A2A Complementarity）、公理 I.1（OT Determinism）对齐。

---

## 矩阵 C：术语映射（跨标准概念对齐）

### 表 C-1：核心架构术语

| 本体系概念 | ISO 42010:2022 | TOGAF 10 | ArchiMate 3.2+ | ISO 26550:2015 | ISA-95 |
|-----------|---------------|----------|----------------|----------------|--------|
| **架构描述** | Architecture Description (AD) | Architecture Repository / ADM 产物 | Architecture View / Model | Product Line Asset Documentation | Operations Definition |
| **视点** | Viewpoint | Architecture Viewpoint | Viewpoint | Stakeholder Concern View | Functional Hierarchy |
| **视图** | View | Architecture View | View | Architecture Description View | Operations Schedule |
| **复用单元** | Model (in Model Library) | Building Block (ABB/SBB) | Element / Building Block | Domain Asset / Core Asset | Segment / Resource |
| **共性/变性** | Concern / Viewpoint customization | Architecture Continuum variability | Element specialization | Commonality / Variability | Product Segment / Master Recipe |
| **接口契约** | Correspondence Rule | Interface Catalog | Relationship / Serving | Asset Interface | Exchange Framework |
| **生命周期** | Architecture Description lifecycle | ADM Cycle | Architecture Development Cycle | Domain Engineering + Application Engineering | Operations Lifecycle |

### 表 C-2：AI 原生协议术语映射

| 本体系概念 | MCP 2025-11-25 | A2A v1.0 | 通用含义 / 跨标准说明 |
|-----------|-------------------|-----------|----------------------|
| **MCP Tool** | Tool (Schema + Implementation, optional Icons) | Skill | 可被 LLM/Agent 调用的具体功能单元；A2A 中通过 Skill 字段声明，MCP 中通过 `tools/list` 与 `tools/call` 暴露；2025-11-25 支持 icons |
| **Agent Card** | — (Host-Client-Server 模型) | Agent Card (Signed JSON) | 智能体能力广告与信任锚；A2A 的核心发现机制，MCP 中无对等概念（能力通过运行时协商） |
| **Capability** | Capability (Negotiation) | Capability (Advertisement) | 声明可执行的操作集合；MCP 强调运行时协商，A2A 强调预发布目录 |
| **Resource** | Resource (URI + MIME + ttlMs) | Artifact (Part 数组) | 可被访问的数据/内容；MCP 强调缓存复用，A2A 强调结果的结构化交付 |
| **Prompt** | Prompt Template | Message Part | 与 LLM 交互的单元；MCP 提供可复用提示模板，A2A 将提示作为消息的一部分 |
| **Task** | Task (working/input_required/completed/failed/cancelled, SEP-1686) | Task (Lifecycle) | A2A 的有状态工作委托单元；MCP 2025-11-25 新增 Tasks 能力，支持异步轮询和结果获取 |
| **Sampling** | Sampling (反向模型调用) | — | MCP 特有：Server 请求 Client 的本地模型进行轻量推理 |

### 表 C-3：工业数字孪生与组件接口术语映射

| 本体系概念 | IEC 63278 (AAS) | OPC UA FX / Part 14 | WIT / WASM | TSN / IEEE 802.1 |
|-----------|-----------------|---------------------|------------|------------------|
| **AAS Submodel** | Submodel | ObjectType / Folder | — | 资产的管理壳子模型；AAS 中语义定义，OPC UA 中映射为对象类型 |
| **WIT Interface** | — | — | Interface (WIT IDL) | WebAssembly Interface Types：跨语言组件的契约层，等价于 AAS 的 Asset Interface 或 OPC UA 的 Method Signature |
| **GCL** | — | — | — | Gate Control List (IEEE 802.1Qbv)：TSN 门控调度表；配置交换机出端口 8 个队列的开/关时序 |
| **UADP** | — | UA Datagram Protocol (Part 14) | — | OPC UA PubSub 的紧凑二进制传输映射；C2C/C2D/D2D 三种模式通过头字段启用组合区分 |
| **Property** | Property | Variable | record field | Tag / Attribute：属性/变量在三个标准中的对应 |
| **Operation** | Operation | Method | func | 可调用操作；WIT 的 `func` 映射到 OPC UA Method 和 AAS Operation |
| **AASX Package** | AASX (XML/ZIP) | — | — | 离线数据交换格式；与 WASM 的 WAT/WASM 二进制制品类似，均为跨平台可分发单元 |

> **一致性校验**: 表 C-2 与 `terminology-crosswalk.md` 中 "AI Native Terminology" 章节对齐；表 C-3 与 `terminology-crosswalk.md` 中 "Industrial Standards Crosswalk" 及 "TSN 标准映射" 对齐。新增 18 个术语映射条目（Tool, Agent Card, Capability, Resource, Prompt, Task, Sampling, AAS Submodel, WIT Interface, GCL, UADP, Property, Operation, AASX Package 及跨标准释义）。

---

## 矩阵 D：协议/接口 × 应用场景

> **新增矩阵**（2026-06-28）: 覆盖主要协议和接口标准在六类典型场景中的适用性评估

| 协议/接口 | 业务编排 | 应用集成 | 组件复用 | 功能调用 | 工业通信 | AI 协作 |
|-----------|:--------:|:--------:|:--------:|:--------:|:--------:|:-------:|
| **MCP 2025-11-25** | ★☆☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★★ | ☆☆☆☆☆ | ★★★★☆ |
| **A2A v1.0.0** | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | ☆☆☆☆☆ | ★★★★★ |
| **OPC UA FX** | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★★★ | ☆☆☆☆☆ |
| **TSN** | ☆☆☆☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ | ★★☆☆☆ | ★★★★★ | ☆☆☆☆☆ |
| **gRPC** | ★★★☆☆ | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ |
| **REST/HTTP** | ★★★★☆ | ★★★★★ | ★★☆☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ |
| **WIT/WASM** | ★★☆☆☆ | ★★☆☆☆ | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ |
| **DMN 1.5** | ★★★★★ | ★★★☆☆ | ☆☆☆☆☆ | ★★★★★ | ★★☆☆☆ | ★★☆☆☆ |

| 协议/接口 | 业务编排说明 | 应用集成说明 | 组件复用说明 | 功能调用说明 | 工业通信说明 | AI 协作说明 |
|-----------|-------------|-------------|-------------|-------------|-------------|------------|
| **MCP** | 无状态协议，不适合长流程编排 | Streamable HTTP 可穿透网关 | WIT 风格接口可嵌入 WASM | 函数级 Tool Call 为设计核心 | 无实时/确定性保证 | 工具发现与调用是 Agent 基础能力 |
| **A2A** | Task 生命周期天然支持工作流编排 | Agent Card 支持服务目录集成 | Agent 可封装为可复用服务 | Skill 调用粒度适中 | 无工业实时特性 | Agent-to-Agent 协作是协议首要目标 |
| **OPC UA FX** | C2C 支持产线级协调 | C2C 跨控制器数据交换 | C2D/D2D 支持驱动级组件复用 | Method Call 支持功能调用 | UADP + TSN 实现确定性通信 | 无原生 AI 语义 |
| **TSN** | 非应用层协议 | 需配合 OPC UA/gPTP 使用 | 需配合上层协议 | 802.1Qbv 时隙分配 | 工业以太网确定性传输基座 | 非应用层协议 |
| **gRPC** | 可配合 Temporal/Cadence 编排 | HTTP/2 + ProtoBuf 为云原生标准 | 需 sidecar 或进程边界 | 强类型 stub 支持功能调用 | 无确定性调度 | 流式调用支持大模型 Token 流 |
| **REST** | BPMN/DMN 编排引擎首选 | 最广泛的互操作基线 | 松耦合，不适合细粒度组件 | 资源导向，非函数导向 | 无实时保证 | 简单但无原生流式/推送 |
| **WIT/WASM** | 需编排引擎封装 | WIT 接口跨语言互操作 | Component Model 3.0 为跨语言复用设计 | Canonical ABI 支持零拷贝调用 | WASI 尚未覆盖 TSN 原生接口 | 沙箱隔离适合不可信插件 |
| **DMN** | 决策表直接表达业务规则 | 可部署为决策服务 (KIE/Drools) | 决策逻辑封装为可复用组件 | 决策服务即功能调用 | 过程工业报警/联锁逻辑 | 可作为 Agent 的确定性规则层 |

> **架构建议**: 工业现场优先 OPC UA FX + TSN；云原生应用集成优先 gRPC/REST；AI Agent 协作采用 MCP（工具层）+ A2A（协作层）互补；业务规则复用采用 DMN；跨语言组件复用采用 WIT/WASM。

---

## 矩阵 E：形式化方法 × 验证目标

> **新增矩阵**（2026-06-28）: 覆盖主流形式化方法在七类验证目标中的适用性与工具成熟度

| 形式化方法 | 分布式协议 | 架构约束 | 定理证明 | 安全关键软件 | 铁路信号 | 内存安全 | 并发安全 |
|-----------|:----------:|:--------:|:--------:|:------------:|:--------:|:--------:|:--------:|
| **TLA+** | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ | ☆☆☆☆☆ | ★★★★★ |
| **Alloy** | ★★★☆☆ | ★★★★★ | ★★☆☆☆ | ★★☆☆☆ | ★★☆☆☆ | ☆☆☆☆☆ | ★★★☆☆ |
| **Coq** | ★★★☆☆ | ★★☆☆☆ | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ |
| **Isabelle** | ★★★☆☆ | ★★☆☆☆ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| **SPARK/Ada** | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ |
| **B Method** | ★★☆☆☆ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★☆☆ |
| **Rust 类型系统** | ★★☆☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★★★ | ★★★★★ |
| **Kani** | ★★☆☆☆ | ★★☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★★★ | ★★★★★ |
| **Miri** | ☆☆☆☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ | ★★☆☆☆ | ☆☆☆☆☆ | ★★★★★ | ★★★★☆ |

| 形式化方法 | 工具成熟度 | 学习曲线 | 代表工具/项目 | 典型应用场景 |
|-----------|:----------:|:--------:|---------------|-------------|
| **TLA+** | ★★★★☆ | 中 | TLC, TLAPS, Apalache | 分布式一致性协议（Raft, Paxos）、MCP 能力协商、A2A Task 状态机、OPC UA FX Connection Manager |
| **Alloy** | ★★★★☆ | 低–中 | Alloy Analyzer, Alloy* | 组件依赖无环性、架构视图一致性、MCP Tool 能力依赖图验证 |
| **Coq** | ★★★★★ | 高 | CoqIDE, VST, CompCert, Iris | 操作系统内核正确性（seL4）、编译器验证（CompCert）、RustBelt (Iris) |
| **Isabelle** | ★★★★★ | 高 | Isabelle/HOL, Archive of Formal Proofs | 密码学协议、铁路信号（ERTMS）、数学定理证明 |
| **SPARK/Ada** | ★★★★★ | 中高 | SPARK Pro, GNATprove, CodePeer | 航空电子（Airbus A380）、航天器软件、SIL 4 级功能安全 |
| **B Method** | ★★★★☆ | 高 | Atelier B, B4free, ProB | 铁路信号系统（巴黎地铁 14 号线, 纽约地铁 CBTC）、核电仪控 |
| **Rust 类型系统** | ★★★★★ | 中 | rustc, Polonius, cargo | 系统编程、嵌入式、浏览器引擎（Servo/Firefox）、WASM 运行时 |
| **Kani** | ★★★☆☆ | 中 | kani-verifier (AWS) | Rust unsafe 边界验证、并发原语模型检测、WASM 运行时组件 |
| **Miri** | ★★★★☆ | 低–中 | miri (Rust 官方) | Rust UB 行为检测、数据竞争发现、内存泄漏诊断 |

> **选型指南**:
>
> - **分布式协议 + 并发安全** → TLA+（时序逻辑）或 Rust 类型系统（编译期保证）
> - **高安全等级（SIL 4 / 铁路信号）** → SPARK/Ada 或 B Method（有成熟认证链）
> - **内存安全 + 现代系统语言** → Rust 类型系统 + Kani/Miri 组合验证
> - **架构约束快速验证** → Alloy（约束求解，小范围实例化）
> - **定理证明 + 程序正确性** → Coq/Isabelle（深证明，高成本）

---

## 矩阵 F：2026 标准更新追踪

> **原矩阵 D**，现顺延为矩阵 F，保留历史追踪功能并更新状态

| 标准 | 当前状态 | 预期更新 | 对体系的影响 | 跟踪责任人 |
|------|---------|---------|-------------|-----------|
| ISO/IEC/IEEE DIS 42024 | 草案 | 预计 2026–2027 发布 | 元模型层定义需更新 | TBD |
| ISO/IEC/IEEE DIS 42042 | 草案 | 预计 2026–2027 发布 | 参考架构规范补充 | TBD |
| **ArchiMate 4.0** | **[已正式发布（2026-04-27，Document C260）](https://www.opengroup.org/archimate-licensed-downloads)** | **正式发布内容包含 Common Domain + Business/Application/Technology + Motivation/Implementation；与 3.2 向后兼容** | 已更新对应映射文档 | TBD |
| **MCP 2025-11-25** | **已发布** | **后续修订由 Linux Foundation Agentic AI Foundation 治理；跟踪 12 个月废弃窗口** | **功能层 AI 协议基线：Tasks、Icons、Sampling with Tools、Elicitation URL、OAuth 增强** | TBD |
| **A2A v1.0.0** | **已发布 (Cloud Next 2026-04)** | **v1.1 预计 2026 H2** | **Agent 安全签名增强、多租户、gRPC 绑定** | TBD |
| **OPC UA FX 1.0** | **Parts 80–84 发布** | **C2D/D2D 完善中** | **工业现场层复用：UADP 极简头、GCL 时隙对齐** | TBD |
| SLSA 2.0 | 讨论中 | 预计 2027 | 供应链安全框架升级 | TBD |
| **WASI 1.0** | **预期 2026 底–2027 初** | **WASI 0.3.0 已正式发布 (2026-06-11，Wasmtime 43+/jco 支持)** | **WASM 跨平台组件复用：原生 async I/O、stream/future 类型** | TBD |
| PLCopen Motion Part 4 | 2025 发布 | Coordinated Motion 完善 | 机器人-PLC 统一控制 | TBD |
| **ISO 26262 Ed.3** | **修订中（2023 秋启动，委员会内部草案阶段）** | **SDV 区域架构、OTA 安全案例、AI/ML 资质、Safety Manual 升格为规范性工作产品、Part 3 更名；业内预计 ~2027-10 发布** | 汽车软件 SEooC 复用 | TBD |
| **IEC 61508 Ed.3** | **CDV 投票完成（RVC 2026-05-15，65A/1231~1234/RVC）；IEC 官方 Fcst. Publ. Date 2026-07；TÜV 等认证机构 2026-06 起已可按 61508-3:2026 执行认证** | **TIL 0–4 工具资质、OO 软件 TR 61508-3-3、与 ISO 26262 对齐** | 功能安全跨域复用 | TBD |
| OASIS TOSCA v2.0 | 2025-09 OASIS 标准 | IoT/边缘/过程自动化扩展 | 应用拓扑跨域编排 | TBD |
| Gateway API / GAMMA | 稳定 / SIG Network | 替代 Ingress 与服务网格 API | K8s 原生流量管理复用 | TBD |
| DMN 1.5 | 2024 OMG 发布 | 与 BPMN 深度集成 | 业务决策服务化复用 | TBD |
| NIST SP 800-161r1 | 现行 | 供应链风险管理 | 开源组件安全治理 | TBD |
| NIST SP 800-204 系列 | 2025 更新 | DevSecOps + 供应链集成 | 微服务安全架构复用 | TBD |

> **本轮更新重点**: MCP 官方当前稳定版为 **2025-11-25**（Anthropic 于 2025-12-09 捐给 Linux Foundation Agentic AI Foundation）；2026-07-28 为官方 RC（2026-05-29 发布），最终版尚未发布，本矩阵以稳定版 2025-11-25 为基线；A2A v1.0（Google / Linux Foundation）已 GA；OPC UA FX Parts 80–84 已发布，C2D 进入多厂商试点阶段；WASM Component Model 与 WASI 0.3 使 WASM 从实验走向生产基线。

---

## 使用说明

1. **设计时**: 查阅"矩阵 A"确定当前设计层次应使用的标准组合
2. **概念转换时**: 查阅"矩阵 C"进行跨标准术语翻译
3. **协议选型时**: 查阅"矩阵 D"确定协议与目标场景的匹配度
4. **形式化验证选型时**: 查阅"矩阵 E"确定方法、目标与工具链的组合
5. **年度审查时**: 查阅"矩阵 F"更新标准状态
6. **评估时**: 查阅"矩阵 B"确定某标准在目标主题中的适用度

---

## 权威来源引用

> 以下来源用于验证本文件中的标准编号、状态及技术细节：

1. **[MCP 2025-11-25]** Anthropic / Linux Foundation Agentic AI Foundation, *Model Context Protocol Specification*, 2025-11-25. <https://modelcontextprotocol.io/specification/2025-11-25> — 验证 MCP 协议状态、Tasks、Sampling、OAuth 安全模型。
2. **[A2A v1.0.1]** Google / Linux Foundation, *Agent-to-Agent Protocol Specification*, v1.0.0 2026-03-12 GA / v1.0.1 2026-05-26（当前最新）. <https://a2a-protocol.org/latest/> — 验证 Agent Card、Task Lifecycle、gRPC 绑定、Signed Agent Cards。
3. **[W3C WebAssembly 3.0 / Component Model]** W3C WebAssembly Community Group, *WebAssembly 3.0*, 2025-09; Bytecode Alliance, *Component Model* & WASI Roadmap. <https://webassembly.org> — 验证 WASM Component Model 3.0 发布状态、WIT 接口定义、WASI 0.3 async I/O。
4. **[OPC UA FX Parts 80–84]** OPC Foundation, *OPC Unified Architecture – Field Level Communications (FX)*, Parts 80–84, 2024–2026; IEC 62541-14 PubSub v1.05. <https://opcfoundation.org> — 验证 OPC UA FX 1.0 状态、UADP 帧结构、C2C/C2D/D2D 模式差异。
5. **[IEEE 802.1Qbv-2021 / IEC/IEEE 60802]** IEEE, *Standard for Local and Metropolitan Area Networks–Bridges and Bridged Networks–Amendment 25: Enhancements for Scheduled Traffic*, 2021; IEC/IEEE 60802 TSN Profile for Industrial Automation (Draft, 2025) — 验证 GCL（Gate Control List）参数、TSN 工业配置文件。
6. **[ISO/IEC 26566:2026]** ISO/IEC, *Software and systems engineering — Methods and tools for product line texture*, 2026 — 验证产品线纹理方法/工具能力状态。
7. **[TLA+ / TLA+ Hyperbook]** Leslie Lamport, *The TLA+ Hyperbook*, Microsoft Research. <https://lamport.azurewebsites.net/tla/tla.html> — 验证 TLA+ 在分布式协议与并发安全验证中的定位。
8. **[SPARK Pro / AdaCore]** AdaCore, *SPARK Pro*, <https://www.adacore.com/about-spark> — 验证 SPARK/Ada 在安全关键软件（DO-178C / SIL 4）中的工具成熟度。
9. **[B Method / Atelier B]** Clearsy, *Atelier B*, <https://www.atelierb.eu> — 验证 B Method 在铁路信号系统形式化精化链中的应用。
10. **[Coq / Inria]** Inria, *The Coq Proof Assistant*, <https://coq.inria.fr> — 验证 Coq 在定理证明与程序验证（CompCert, seL4, Iris/RustBelt）中的成熟度。

---

> 最后更新: 2026-06-28
> 更新责任人: 专业写作代理（6 月第 4 周全面更新）
> 下次计划更新: 2026-09-30（Q3 季度审查）
