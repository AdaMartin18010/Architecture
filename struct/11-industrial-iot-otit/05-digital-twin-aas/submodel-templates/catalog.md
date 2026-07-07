# AAS 子模型模板清单

> **版本**: 2026-06-06
> **对齐来源**: IDTA (Industrial Digital Twin Association) Submodel Registry, IEC 63278-1:2023, IEC 63365:2024
> **定位**: 覆盖 IDTA 已发布子模型模板的精简目录，突出复用价值与工程选型指南

---

## 1. 子模型模板概述

AAS 子模型模板（Submodel Template, SMT）是数字孪生语义互操作的关键复用单元。
每个模板定义了特定应用场景下的数据结构、语义标识和验证规则。
遵循标准模板可确保：

- **跨厂商数据交换**: 不同厂商工具对同一子模型的解析结果一致
- **生命周期数据贯通**: 设计、采购、运维阶段使用统一的语义框架
- **合规性自动化**: 直接支持欧盟数字产品护照（DPP）等法规要求

---

## 2. 标准子模型模板详表

### 2.1 基础标识类

#### IDTA-02006: Nameplate（铭牌）

| 属性 | 内容 |
|------|------|
| **版本** | 2.0 |
| **标准来源** | IDTA-02006-2-0, 基于 ZVEI 数字铭牌倡议 |
| **用途** | 提供设备的法定铭牌信息，支持数字产品护照（DPP）合规 |
| **核心属性** | `ManufacturerName`, `ManufacturerProductDesignation`, `SerialNumber`, `YearOfConstruction`, `Markings` (CE, UL 等认证标志) |
| **复用频率** | ⭐⭐⭐⭐⭐ (所有物理资产必须) |
| **典型应用** | 资产识别、合规检查、备件订购、供应链管理 |

```text
语义标识示例:
  ManufacturerName → 0173-1#02-AAO677#002 (ECLASS)
  SerialNumber → 0173-1#02-AAM556#002 (ECLASS)
```

#### IDTA-02003: Technical Data（技术数据）

| 属性 | 内容 |
|------|------|
| **版本** | 1.2 |
| **标准来源** | IDTA-02003-1-2 |
| **用途** | 标准化的设备技术规格描述，支持工程选型和系统集成 |
| **核心属性** | `GeneralInformation` (制造商信息), `ProductClassifications` (ECLASS/IEC CDD 分类), `TechnicalProperties` (电气/机械/环境参数), `FurtherInformation` (有效期、文档引用) |
| **复用频率** | ⭐⭐⭐⭐⭐ (所有物理资产强烈推荐) |
| **典型应用** | 设备选型、CAD/CAE 集成、能耗仿真、数字线程 |

#### IDTA-02007: Identification（标识）

| 属性 | 内容 |
|------|------|
| **版本** | 1.0 |
| **标准来源** | IDTA-02007-1-0 |
| **用途** | 管理资产的多重标识符，支持全生命周期追踪追溯 |
| **核心属性** | `GlobalAssetId` (全局资产 ID), `LocalId` (本地标识), `Barcode`, `RFID`, `QRCode`, `IPAddress` |
| **复用频率** | ⭐⭐⭐⭐☆ |
| **典型应用** | 库存管理、资产追踪、维护历史关联 |

#### IDTA-02002: Contact Information（联系信息）

| 属性 | 内容 |
|------|------|
| **版本** | 1.0 |
| **标准来源** | IDTA-02002-1-0 |
| **用途** | 记录与资产相关的组织/人员联系信息 |
| **核心属性** | `RoleOfContactPerson`, `NationalCode`, `Language`, `TimeZone`, `Street`, `City`, `State`, `Zipcode`, `Email`, `Url`, `Phone` |
| **复用频率** | ⭐⭐⭐⭐☆ |
| **典型应用** | 供应商管理、服务请求、紧急联系人、合规审计 |

---

### 2.2 文档与生命周期类

#### IDTA-02008: Handover Documentation（移交文档）

| 属性 | 内容 |
|------|------|
| **版本** | 1.0 |
| **标准来源** | IDTA-02008-1-0 |
| **用途** | 标准化工厂验收测试（FAT）和现场验收测试（SAT）的文档移交 |
| **核心属性** | `Documents` (手册、证书、测试报告), `Languages`, `DocumentClassifications` (安全、操作、维护), `ApprovalStatus` |
| **复用频率** | ⭐⭐⭐⭐☆ |
| **典型应用** | FAT/SAT、运维交接、审计追踪、知识管理 |

#### IDTA-02012: Service Notifications（服务通知）

| 属性 | 内容 |
|------|------|
| **版本** | 1.0 |
| **标准来源** | IDTA-02012-1-0 |
| **用途** | 记录服务事件和通知，支持与 CMMS（计算机化维护管理系统）集成 |
| **核心属性** | `ServiceCategory`, `ServiceStatus`, `FaultDescription`, `ServiceDate`, `Technician`, `ServiceReport`, `SparePartsUsed` |
| **复用频率** | ⭐⭐⭐☆☆ |
| **典型应用** | 售后服务、维护工单、故障分析、供应商绩效评估 |

#### IDTA-02014: Maintenance（维护）

| 属性 | 内容 |
|------|------|
| **版本** | 1.0 (草案) |
| **标准来源** | IDTA-02014-1-0 |
| **用途** | 维护计划、维护记录、维护工单的语义化描述 |
| **核心属性** | `MaintenanceSchedule` (计划类型、周期), `MaintenanceRecord` (实际执行日期、工时、结果), `RequiredSpareParts`, `MaintenanceInterval` |
| **复用频率** | ⭐⭐⭐⭐☆ |
| **典型应用** | 预测性维护、CMMS 集成、维护成本分析、设备可用性计算 |

---

### 2.3 环境与可持续性类

#### IDTA-02016: Carbon Footprint（碳足迹）

| 属性 | 内容 |
|------|------|
| **版本** | 1.0 |
| **标准来源** | IDTA-02016-1-0, 对齐 GHG Protocol |
| **用途** | 提供资产或产品的碳足迹数据，支持 ESG 报告和欧盟数字产品护照 |
| **核心属性** | `PCF` (Product Carbon Footprint), `Scope1Emissions`, `Scope2Emissions`, `Scope3Emissions`, `ReferenceYear`, `VerificationStatus` |
| **复用频率** | ⭐⭐⭐⭐☆ (ESG/DPP 驱动快速增长) |
| **典型应用** | ESG 报告、产品护照、供应链碳核算、绿色采购 |

#### IDTA-02017: Material（材料）

| 属性 | 内容 |
|------|------|
| **版本** | 1.0 |
| **标准来源** | IDTA-02017-1-0, 对齐 IMDS |
| **用途** | 材料成分声明和可回收性信息 |
| **核心属性** | `MaterialComposition`, `SubstanceOfConcern`, `RecyclabilityRate`, `IMDSReference`, `REACHCompliance` |
| **复用频率** | ⭐⭐⭐☆☆ |
| **典型应用** | 环保合规、循环经济、报废处理、材料溯源 |

---

### 2.4 数据与接口类

#### IDTA-02022: Time Series Data（时序数据）

| 属性 | 内容 |
|------|------|
| **版本** | 1.1 |
| **标准来源** | IDTA-02022-1-1 |
| **用途** | 时间序列数据的标准化描述，支持传感器数据、历史数据库集成 |
| **核心属性** | `SamplingRate`, `Unit`, `DataType`, `StorageLocation`, `LinkedSegment` (外部数据源端点), `InternalSegment` (AAS 内嵌数据), `RecordMetadata` |
| **复用频率** | ⭐⭐⭐⭐☆ |
| **典型应用** | 状态监测、预测性维护、能耗分析、质量追溯 |

```
时序数据三种存储模式:
  - InternalSegment: 数据直接存储在 AAS 子模型中（小量数据）
  - LinkedSegment: 通过 URL/端点引用外部时序数据库（InfluxDB, TimescaleDB）
  - ExternalSegment: 数据文件嵌入 AASX 包（CSV, Parquet）
```

#### IDTA-02026: Provision of 3D Models（3D 模型提供）

| 属性 | 内容 |
|------|------|
| **版本** | 1.0 |
| **标准来源** | IDTA-02026-1-0 |
| **用途** | 3D 几何模型的标准化引用，支持数字孪生可视化 |
| **核心属性** | `ModelFormat` (STEP, glTF, OBJ), `LevelOfDetail` (LOD), `CoordinateSystem`, `Unit`, `FileReference`, `PreviewImage` |
| **复用频率** | ⭐⭐⭐☆☆ |
| **典型应用** | 数字孪生可视化、VR/AR 维护指导、碰撞检测、装配仿真 |

---

### 2.5 安全与合规类

#### IDTA-02025: Functional Safety（功能安全）

| 属性 | 内容 |
|------|------|
| **版本** | 1.0 |
| **标准来源** | IDTA-02025-1-0, 对齐 IEC 61508 / IEC 62061 |
| **用途** | 安全相关参数的标准化描述，支持 TÜV 认证和功能安全评估 |
| **核心属性** | `SafetyIntegrityLevel` (SIL), `PerformanceLevel` (PL), `PFH` (每小时危险失效概率), `PFD` (按需失效概率), `SafetyManualReference`, `ProofTestInterval` |
| **复用频率** | ⭐⭐⭐☆☆ (安全关键行业高优先级) |
| **典型应用** | 功能安全评估、TÜV 认证、安全回路设计、风险评估 |

---

### 2.6 行业特定类（高复用价值）

#### IDTA-02021: Sizing of Power Drive Trains（电力传动系统选型）

| 属性 | 内容 |
|------|------|
| **版本** | 1.1 |
| **标准来源** | IDTA-02021-1-1 |
| **用途** | 驱动系统（电机+变频器+齿轮箱）选型信息的标准化交换 |
| **核心属性** | `DriveData`, `MotorData`, `GearboxData`, `TransformerData`, `MechanicalLoadData` (转动惯量、负载扭矩曲线), `OperatingCycles` |
| **复用频率** | ⭐⭐⭐⭐☆ (驱动行业高复用) |
| **典型应用** | 驱动选型工具、数字工程、供应商报价、能效优化 |

#### IDTA-02017-1: Asset Interface Description（资产接口描述）

| 属性 | 内容 |
|------|------|
| **版本** | 1.0 |
| **标准来源** | IDTA-02017-1-0 |
| **用途** | 描述资产接口（OPC UA, MQTT, Modbus, HTTP 等），支持自动连接建立 |
| **核心属性** | `EndpointMetadata` (URL, 安全策略), `ProtocolInformation` (协议版本、序列化格式), `ExternalDescriptor` (OPC UA NodeSet 引用), `Authentication` |
| **复用频率** | ⭐⭐⭐⭐☆ (工业 4.0 互联互通核心) |
| **典型应用** | 自动配置、即插即用、设备集成、边缘网关配置 |

---

## 3. 子模型模板选择矩阵

### 3.1 按资产类型推荐

| 资产类型 | 必备子模型 | 推荐子模型 | 可选子模型 |
|---------|----------|----------|----------|
| **旋转机械** (泵、风机、压缩机) | Nameplate, Technical Data | Time Series, Maintenance | Carbon Footprint, 3D Models |
| **电气设备** (变压器、开关柜) | Nameplate, Technical Data | Maintenance, Circuit Breaker | Cybersecurity, Functional Safety |
| **伺服驱动系统** | Nameplate, Technical Data | Sizing of Power Drive Trains | Time Series, Maintenance |
| **控制阀** | Nameplate, Technical Data | Process Instrumentation, Maintenance | 3D Models |
| **工业机器人** | Nameplate, Technical Data | Software, Maintenance | Functional Safety, 3D Models |
| **软件组件** | Identification, Software Nameplate | Documentation | Cybersecurity |
| **产线/工位** | Nameplate, Technical Data | Asset Interface Description, Contact Information | Time Series, Maintenance |

### 3.2 按生命周期阶段推荐

| 阶段 | 核心子模型 | 目标 |
|------|----------|------|
| **设计与采购** | Nameplate + Technical Data + Sizing of Power Drive Trains + Carbon Footprint | 工程选型、供应商评估 |
| **制造与交付** | Nameplate + Handover Documentation + Contact Information + 3D Models | FAT/SAT、文档移交 |
| **安装与调试** | Asset Interface Description + Functional Safety + Handover Documentation | 自动配置、安全认证 |
| **运营** | Time Series + Maintenance + Service Notifications + Energy Monitoring | 状态监测、预测维护 |
| **退役** | Material + Carbon Footprint + Handover Documentation | 环保处置、循环经济 |

---

## 4. 与数字产品护照 (DPP) 的映射

欧盟数字产品护照 (Digital Product Passport, DPP) 要求的 AAS 子模型组合：

| DPP 数据类别 | 对应 AAS 子模型模板 | 法规来源 |
|-------------|-------------------|---------|
| 产品标识 | Identification + Nameplate | ESPR (EU) 2024/1781 |
| 合规信息 | Handover Documentation (证书部分) | CE 标志法规 |
| 可持续性 | Carbon Footprint + Material | EU Taxonomy, CSRD |
| 供应链 | Hierarchical Structures enabling BOM + Contact Information | Supply Chain Due Diligence |
| 使用说明 | Provided Documentation for Operation | 产品安全法规 |
| 维护历史 | Maintenance + Service Notifications | 行业最佳实践 |

---

## 5. 语义标识体系

每个子模型模板元素通过 `semanticId` 关联到工业数据字典：

| 前缀 | 来源 | 说明 | 示例 |
|-----|------|------|------|
| `0173-1#...` | ECLASS | 工业分类标准属性 | `0173-1#02-AAO677#002` (ManufacturerName) |
| `0112/2///61360_4#...` | IEC CDD | IEC 公共数据字典 | `0112/2///61360_4#AAF276#001` |
| `https://admin-shell.io/...` | IDTA | AAS 特定语义标识 | `https://admin-shell.io/idta/TimeSeries/1/1` |

---

## 6. 子模型模板复用价值评估

| 评估维度 | 权重 | 评估方法 |
|---------|------|---------|
| **行业采纳率** | 35% | IDTA Registry 下载量、GitHub 引用数 |
| **标准成熟度** | 25% | 版本号、审查状态（Published/In Review/Draft） |
| **工具支持度** | 20% | AASX Package Explorer、BaSyx、Siemens Polarion 等工具的内置模板 |
| **法规强制性** | 15% | DPP、ESPR、REACH 等法规的明确要求 |
| **跨行业适用性** | 5% | 离散制造、流程工业、能源电力的通用程度 |

---

## 7. 参考索引

- IDTA Submodel Registry: <https://github.com/admin-shell-io/submodel-templates>
- IDTA-01001-3-0: *Details of the Asset Administration Shell Part 1 — Metamodel*
- IDTA-01002-3-0: *Details of the Asset Administration Shell Part 2 — APIs*
- IEC 63278-1:2023: *Asset Administration Shell structure*
- IEC 63365:2024: *Generic Submodels and Specifications*
- IEC 61360: *IEC Common Data Dictionary (CDD)*
- ECLASS: <https://www.eclass.eu>
- EU Digital Product Passport: ESPR Regulation (EU) 2024/1781
- [Industrial Digital Twin Association](https://industrialdigitaltwin.org/en)


---

## 补充章节
## 概念定义

**定义**：工业 IoT/OT-IT 复用是在制造、能源、交通等运营技术（OT）与信息技术（IT）融合场景中，复用 ISA-95 层级模型、OPC UA 信息模型、功能安全组件与数字孪生资产。

## 示例

**示例**：汽车工厂将 ISA-95 L0-L4 资产目录映射到 IEC 63278 资产管理壳（AAS），通过 OPC UA FX 实现现场设备与 MES/ERP 的即插即用复用。

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