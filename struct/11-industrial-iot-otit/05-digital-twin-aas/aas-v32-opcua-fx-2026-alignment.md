# AAS v3.2 + OPC UA FX V1.00.03 + Digital Twin 权威对齐（2025‑2026）

> **定位**：工业架构复用体系中数字孪生与现场通信层的最新权威基准。
> **权威来源**：IDTA、OPC Foundation、IEC 63278、Eclipse BaSyx、Microsoft/Siemens W3C TD 融合声明。

---

## 1. 关键结论（TL;DR）

| 标准 | 最新版本 | 关键更新 |
|------|----------|----------|
| **AAS** | Part 1 v3.2 (2026‑03‑24) | 首个完全开源 HTML 规范；`idShort` 允许连字符；`DateTimeUtc` 统一；100+ Submodel Templates |
| **OPC UA FX** | V1.00.03 (2025‑07‑31) | 诊断能力增强；LLDP 信息建模；C2C 已量产，C2D/D2D 进入 Phase 2 试点 |
| **IEC 63278** | ‑1:2023 (EN 2024) | AAS 结构首份国际标准，赋予采购合同效力 |
| **Eclipse BaSyx** | v2.0.1 (2026‑04) | Python/Java/Go/TS 多语言 SDK；新增 `basyx-pdf-to-aas` (LLM 提取)、`aas-mcp` (MCP Server) |
| **DTDL** | v3/v4 (Azure IoT Operations) | Microsoft + Siemens 宣布与 W3C Thing Description 融合 |

---

## 2. AAS v3.2 深度更新

### 2.1 版本时间线

```text
2023        IEC 63278-1:2023 发布（AAS 结构国际标准）
2024-01     EN IEC 63278-1:2024 采纳
2025-03     AAS Part 1 v3.0.2 维护版
2025-05     AAS Part 1 v3.1 — 首个完全开源 HTML 规范
2026-03-24  AAS Part 1 v3.2 — 当前最新
```

### 2.2 v3.2 核心变更

| 变更类别 | 具体内容 |
|----------|----------|
| **数据类型** | `lastUpdate`、`timeStamp` 统一为 `DateTimeUtc`；`Identifier` 长度 2000→2048；`ContentType` 100→128 |
| **约束放松** | `Blob/contentType`、`File/contentType`、`Entity/entityType`、`RelationshipElement/first/second` 变为可选；`idShort` 允许连字符 |
| **新枚举** | `AasContainerSubmodelElements`、`AasNonContainerSubmodelElements`；`AssetKind/Role` 新增 |
| **语义修正** | `AASd-021` 指向 `Qualifier/type`（非 `valueType`）；`BlobType` 版本更新至 3.1 |
| **开源化** | v3.1 起完全在 GitHub 维护，PlantUML 图表，PDF + HTML 双格式 |

### 2.3 Submodel Templates（SMT）生态

截至 2026 年初，IDTA 已注册 **100+ Submodel Templates**，涵盖：

| SMT | ID | 复用场景 |
|-----|-----|----------|
| Digital Nameplate | IDTA-02006 | 资产身份标识 |
| Technical Data | IDTA-02002 | 技术参数手册 |
| Product Carbon Footprint | IDTA-02023 | ESG / CBAM 合规 |
| Digital Battery Passport | IDTA-02035 (7 parts) | EU 电池法规 |
| Handover Documentation | IDTA-02004 | 工程移交 |
| Software Nameplate | IDTA-020XX | 软件组件溯源 |
| MTP (Module Type Package) | IDTA-020XX | 过程工业模块复用 |

> **架构复用意义**：SMT 是 OT/IT 边界的可复用语义契约。一个电池护照 Submodel 可在 PLM 中创建、在 MES 中消费、在 ERP 中审计，通过标准化 REST API 跨越组织边界。

---

## 3. OPC UA FX V1.00.03

### 3.1 状态概览

| 维度 | 状态 |
|------|------|
| **版本** | OPC 10000-80~84 V1.00.03 |
| **发布日期** | 2025‑07‑31 |
| **C2C** | 已量产，多厂商互操作（Siemens、Beckhoff、B&R、Phoenix Contact） |
| **C2D** | Phase 2 (2024‑2027) 开发中，SPS 2025 嵌入式原型 |
| **D2D** | Phase 2 同批次，运动控制 / I/O / 仪表配置文件开发中 |

### 3.2 V1.00.03 新增

- 诊断能力增强（Conformance Units / Profiles）
- LLDP（Link Layer Discovery Protocol）信息建模
- 术语澄清与引用更新
- 向后兼容 V1.00.0x

### 3.3 UADP 帧结构速查

```text
UADP over UDP/IP    — 默认，实时且可路由
UADP over Layer 2   — 可选，无 IP 开销，最高性能
OPC UA Client/Server (TCP/IP) — 仅用于连接建立
```

---

## 4. AAS ↔ OPC UA NodeSet 映射现状

> **重要说明**：截至 2026 年中，**尚无单一发布的标准**专门规定 "AAS to OPC UA NodeSet 映射"。实际互操作依赖多条 converging 路径：

### 4.1 实现路径

| 路径 | 机制 | 状态 |
|------|------|------|
| **OPC UA Device Interface (IEC 62541-100)** | AAS 结构 ↔ UA Device Type 双向自动转换；Data Element → UA Variable；Service → UA Method | IDTA Plug-and-Produce 工作组验证 |
| **UAFX AutomationComponent** | Part 81 的 `AutomationComponent` 在概念上与 AAS Submodel 对齐 | 概念对齐，无自动映射工具 |
| **Companion Spec 引用** | AAS Submodel 语义标识符引用 OPC UA Companion Spec（Machinery、Robotics 等） | 工程实践中常见 |
| **AASX 嵌入** | AASX Package 将 OPC UA NodeSet XML 作为补充文件嵌入 | 离线工程工具链支持 |

### 4.2 运行时架构建议

```text
┌─────────────────────────────────────────────┐
│  IT 层：ERP / PLM / MES                     │
│  └── AAS REST API (Part 2)                  │
│       └── 语义层：Digital Nameplate、Carbon  │
│           Footprint、Bill of Material       │
├─────────────────────────────────────────────┤
│  网关层：AAS ↔ OPC UA 桥接                   │
│  └── AAS Server (BaSyx) + OPC UA Client     │
├─────────────────────────────────────────────┤
│  OT 层：PLC / DCS / 边缘设备                 │
│  └── OPC UA PubSub (UADP) — 实时过程数据     │
│      OPC UA FX C2C/C2D — 控制器协调          │
└─────────────────────────────────────────────┘
```

**核心原则**：AAS 承载“数字护照”和语义容器；OPC UA 承载实时变量流。二者互补，非替代。

---

## 5. DTDL vs AAS：架构复用选择

| 维度 | AAS (IDTA/IEC) | DTDL (Microsoft) |
|------|----------------|------------------|
| **标准层级** | 国际标准 (IEC 63278) | 企业规范 |
| **生态** | 欧洲制造 / 工业 4.0 / Catena-X | Azure IoT / 云原生 |
| **语义丰富度** | 高（生命周期、Submodel Template） | 中（telemetry/property/command） |
| **互操作** | REST API、AASX 包交换 | Azure Digital Twins Graph |
| **最新动向** | 100+ SMT、Digital Product Passport | 与 W3C Thing Description 融合 |

> **Microsoft + Siemens 声明（2024‑04）**：双方将 DTDL 与 W3C Thing Description 融合，作为数字孪生民主化的“自然下一步”。这意味着未来可能出现 W3C TD ↔ AAS 的桥接标准。

**复用建议**：

- 跨企业供应链、欧盟市场、需要 Digital Product Passport → **AAS**
- Azure 原生 IoT 平台、快速原型 → **DTDL / W3C TD**
- 长期策略 → 规划 **AAS-W3C TD 双语网关**

---

## 6. Eclipse BaSyx 生态最新

| 组件 | 版本 | 亮点 |
|------|------|------|
| **Python SDK** | v2.0.1 (2026‑04) | 实现 AAS Part 1 v3.0.1、Part 2 v3.0 |
| **Java Server SDK** | v2.0.0‑m08 | Maven: `org.eclipse.digitaltwin.basyx` |
| **Go Components** | 活跃 | 标准化 Server 组件 |
| **Web UI** | v2 (2025‑03) | 实时 AAS/Submodel 编辑器、Digital Nameplate V3 插件、Keycloak 集成 |
| **basyx-pdf-to-aas** | 2025‑09 | LLM 从 PDF 提取技术数据并导出 AAS |
| **aas-mcp** | 2025‑09 | **MCP Server for BaSyx** — AI Agent 可直接查询 AAS 仓库 |

> **aas-mcp 的复用意义**：MCP 2025-11-25 协议让 LLM Agent 能够通过标准化接口消费 AAS Submodel 数据，打通“工业数字孪生 ↔ AI 代理”的边界。

---

## 7. IEC 智能制造基础标准层

| 标准 | 内容 | 与 AAS 关系 |
|------|------|-------------|
| **IEC 63278-1:2023** | AAS 结构 | AAS 本体 |
| **IEC TR 63319** | 智能制造参考模型元建模分析 (SEMP) | 理论基础 |
| **IEC 63339** | 智能制造统一参考模型 | 跨域参考 |
| **IEC 63489** | 智能制造通用数据概念 | 数据语义基座 |

AAS 位于这些基础标准之上，作为工业资产的**具体数字孪生信封和 Submodel 机制**。

---

## 8. 复用架构实践建议

### 8.1 组件目录中的 AAS 资产

```text
组件目录 (Backstage / 内部 Catalog)
├── 软件组件
│   └── SBOM (CycloneDX) + SLSA provenance
├── 工业组件
│   └── AASX Package (Digital Nameplate + Technical Data)
│   └── OPC UA NodeSet (实时接口)
│   └── WIT Interface (Wasm 组件边界)
└── AI 模型
    └── ML-BOM (CycloneDX) + AAS Submodel (Software Nameplate)
```

### 8.2 分层映射

| 项目目录 | 工业数字孪生角色 |
|----------|------------------|
| `struct/04-component-architecture-reuse/` | AAS Submodel = 工业组件语义契约 |
| `struct/11-industrial-iot-otit/` | OPC UA FX = 现场实时通信；AAS = 数字护照 |
| `struct/10-supply-chain-security/` | AAS + SBOM + SLSA = 全链路溯源 |
| `struct/12-ai-native-reuse/` | aas-mcp = AI Agent 消费工业孪生数据 |

---

## 9. 权威来源

1. IDTA AAS Specifications: <https://industrialdigitaltwin.org/en/content-hub/specifications>
2. IDTA Submodel Templates: <https://industrialdigitaltwin.org/en/content-hub/submodels>
3. OPC Foundation UAFX: <https://reference.opcfoundation.org/>
4. IEC 63278-1: <https://webstore.iec.ch/publication/66912>
5. Eclipse BaSyx: <https://www.eclipse.org/basyx/>
6. Eclipse BaSyx GitHub: <https://github.com/eclipse-basyx>
7. Microsoft/Siemens DTDL-W3C Convergence: <https://press.siemens.com/global/en/pressrelease/siemens-and-microsoft-converge-digital-twin-definition-language-w3c-thing-description>
8. Schmidt et al. (2023) DTDL→AAS: <https://doi.org/10.3390/s23187742>

---

*文档生成时间：2026-06-06 · 对齐 AAS Part 1 v3.2 / OPC UA FX V1.00.03 / IEC 63278 / BaSyx v2.0.1*


---

## 补充说明：AAS v3.2 + OPC UA FX V1.00.03 + Digital Twin 权威对齐（2025‑2026）

## 概念定义

**定义**：工业 IoT/OT-IT 复用是在制造、能源、交通等运营技术（OT）与信息技术（IT）融合场景中，复用 ISA-95 层级模型、OPC UA 信息模型、功能安全组件与数字孪生资产。

## 示例

**示例**：汽车工厂将 ISA-95 L0-L4 资产目录映射到 IEC 63278 资产管理壳（AAS），通过 OPC UA FX 实现现场设备与 MES/ERP 的即插即用复用。

## 反例

**反例**：将 IT 系统直接补丁策略套用到 PLC 产线，未考虑实时性约束与功能安全认证，导致停机与安全事故。

## 分析

**分析**：OT-IT 复用需要在实时性、安全性与 IT 敏捷性之间取得平衡，标准信息模型是打破竖井的关键。
