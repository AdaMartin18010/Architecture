# IEC 63278 AAS 系列标准路线图

> **版本**: 2026-06-06
> **权威来源**: IEC Webstore, IDTA Specifications, Industrial Digital Twin Association
> **定位**: 对齐 IEC 63278 AAS 系列标准的最新发布状态和发展路线图

---

## 1. IEC 63278 系列概览

IEC 63278 定义了工业应用中资产管理壳（Asset Administration Shell, AAS）的国际标准。该系列分为 5 个部分：

| 部分 | 标题 | 状态 | 发布/预计时间 |
|------|------|------|--------------|
| **IEC 63278-1** | Asset Administration Shell structure（AAS 结构） | ✅ 已发布 | 2023-12-14 |
| **IEC 63278-2** | Information meta model（信息元模型） | 🔄 开发中 | 预计 2025-2026 |
| **IEC 63278-3** | Security provisions for Asset Administration Shells（安全规定） | 🔄 开发中 | 预计 2024-2025 |
| **IEC 63278-4** | Use cases and modelling examples（用例和建模示例） | 🔄 开发中 | 预计 2025 |
| **IEC 63278-5** | Interfaces（接口） | 📝 预研 | 预计 2026 |

---

## 2. IEC 63278-1:2023（已发布）

### 范围

定义 AAS 的标准化数字表示结构。AAS 提供对信息和服务的统一访问。

### 适用范围

- 任何类型的工业过程（离散制造、连续过程、批处理、混合生产）
- 任何应用工业过程测量、控制和自动化的工业领域
- 资产生命周期的各个阶段（从概念到报废处理）
- 物理、数字或无形的资产实体

### 核心定义

> **Asset（资产）**: 物理、数字或无形的实体，对企业具有价值。
> **Asset Administration Shell（AAS）**: 资产的标准化数字表示，提供对信息和服务的统一访问。

### AAS 结构核心元素

```text
Asset Administration Shell
├── Identification（标识）
│   └── id: 全局唯一标识符（字符串）
├── AssetInformation（资产信息）
│   ├── assetKind: Type / Instance / NotApplicable
│   ├── globalAssetId: 全局资产 ID
│   └── specificAssetIds: 特定资产 ID 列表
├── Submodels（子模型）
│   ├── idShort: 短标识
│   ├── identification: 全局标识
│   ├── semanticId: 语义标识（推荐）
│   └── submodelElements: 子模型元素
└── Extensions（扩展）
```

---

## 3. IDTA-01001-3-0 元模型（与 IEC 63278-2 对齐）

IDTA（Industrial Digital Twin Association）发布的元模型规范与 IEC 63278-2 同步开发。

### 3.0 版主要变更

| 变更项 | 说明 |
|--------|------|
| **SubmodelElementCollection 拆分** | 拆分为 SubmodelElementList（有序）和 SubmodelElementCollection（无序） |
| **Reference 重构** | 添加 referredSemanticId，移除 Local/Parent 属性 |
| **Identifier 简化** | idType 从 Identifier 移除，ID 现为纯字符串 |
| **idShort 可选化** | Referable 的 idShort 变为可选 |
| **语义 ID 推荐化** | SubmodelElement 的 semanticId 不再强制，但强烈推荐 |
| **Supplemental Semantic IDs** | 新增辅助语义 ID |
| **Asset 概念修订** | 移除 Asset 类，改为 AssetInformation；移除 billOfMaterial |
| **字符串类型规范化** | 大量 string 属性替换为带长度限制的类型 |
| **EventElement 标记为 Experimental** | 事件相关类标记为实验性 |
| **ConceptDictionaries 移除** | 不再支持 |
| **Views 移除** | 不再支持 |

---

## 4. AAS 子模型模板生态

IDTA 维护的子模型模板清单（2026 状态）：

| 模板 ID | 模板名称 | 状态 |
|---------|---------|------|
| IDTA-02002 | Contact Information | ✅ 已发布 |
| IDTA-02003 | Technical Data | ✅ 已发布 |
| IDTA-02006 | Nameplate | ✅ 已发布 |
| IDTA-02007 | Identification | ✅ 已发布 |
| IDTA-02008 | Handover Documentation | ✅ 已发布 |
| IDTA-02022 | Time Series Data | ✅ 已发布 |
| IDTA-02023 | Carbon Footprint | ✅ 已发布 |
| IDTA-02024 | Provision of 3D Models | 开发中 |
| IDTA-02025 | Functional Safety | 开发中 |

---

## 5. IEC 63278-3: 安全规定

### 范围

定义 AAS 的安全要求，包括：

- 身份验证与授权
- 数据完整性与机密性
- 访问控制
- 安全通信
- 与 IEC 62443 工业控制系统安全系列的协调

### 关键安全原则

1. **Defense in Depth**: 多层安全控制
2. **Security by Design**: 安全内建于 AAS 设计
3. **Least Privilege**: 最小权限原则
4. **Secure Defaults**: 默认安全配置

---

## 6. IEC 63278-5: 接口

### 规划中的接口类型

| 接口类型 | 用途 |
|---------|------|
| **REST/HTTP API** | 与 IT 系统集成 |
| **OPC UA** | 与 OT 系统集成 |
| **MQTT** | 物联网场景 |
| **AASX Package** | 离线数据交换 |

### OPC UA 映射

IEC 63278-5 将标准化 AAS 到 OPC UA 的映射规则：

| AAS 元素 | OPC UA 对应 |
|---------|------------|
| AssetAdministrationShell | Object / Folder |
| Submodel | ObjectType / Folder |
| Property | Variable |
| Operation | Method |
| EventElement | EventType |
| Entity | Object |
| RelationshipElement | Reference |

---

## 7. AASX 包文件格式

AASX（AAS Package）是基于 OPC（Open Packaging Convention, ECMA-376）的 ZIP 文件格式：

```text
AASX Package (.aasx)
├── [Content_Types].xml
├── _rels/.rels
├── aasx/                     ← AAS 数据（JSON/XML）
│   └── asset-administration-shell.aas.json
├── attachments/              ← 附件（PDF、图纸、手册）
│   ├── datasheet.pdf
│   └── drawing.dwg
└── [other related files]
```

---

## 8. 与数字产品护照 (DPP) 的关系

AAS 是欧盟数字产品护照（Digital Product Passport, DPP）的技术基础之一：

- DPP 需要标准化的产品信息交换
- AAS 子模型模板可以作为 DPP 的数据结构基础
- AASX 包格式可以作为 DPP 的数据载体
- IEC 63278 与欧盟可持续产品生态设计法规（ESPR）对齐

---

## 9. 复用策略建议

| 层次 | 复用资产 | 建议 |
|------|---------|------|
| **元模型层** | IEC 63278-1 / IDTA-01001 | 严格遵循，避免自定义扩展 |
| **子模型模板层** | IDTA-020xx 模板 | 优先使用标准模板，减少自定义 |
| **接口层** | OPC UA / REST API | 按场景选择，确保互操作性 |
| **实现层** | Eclipse BaSyx, AASX Package Explorer | 使用成熟开源实现 |

---

## 10. 关键定理

> **定理 I.AAS.3** (AAS Standard Conformance): 严格遵循 IEC 63278 和 IDTA 规范的 AAS 实现，具有最高的跨厂商互操作性。任何自定义扩展都会降低复用范围。
> **定理 I.AAS.4** (Submodel Template Network Effect): AAS 子模型模板的价值与行业内采用该模板的厂商数量成正比。采用率越高，互操作成本越低。

---

> 最后更新: 2026-06-06
> 权威来源:
>
> - <https://webstore.iec.ch/en/publication/65628> (IEC 63278-1:2023)
> - <https://industrialdigitaltwin.org/> (IDTA)
> - <https://www.iec.ch/dyn/www/f?p=103:38:0::::FSP_ORG_ID:1363>
