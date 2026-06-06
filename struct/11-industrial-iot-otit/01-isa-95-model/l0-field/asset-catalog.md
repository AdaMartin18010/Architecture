# L0 现场层复用资产目录

> **版本**: 2026-06-06
> **层级**: ISA-95 Level 0 — 现场设备层 (Field Device Layer)
> **时间尺度**: 毫秒–秒 (ms–s)
> **管理域**: 物理过程与传感器/执行器域
> **对齐来源**: ANSI/ISA-95.00.01-2010 (IEC 62264-1), IEC 61131-3, IEC 61804, IO-Link Consortium

---

## 1. 层定义与复用范围

L0 现场层是 ISA-95 五层模型的最底层，直接面向物理生产过程。该层资产的核心复用价值在于：**设备描述的标准化**与**传感器/执行器配置模板化**。通过复用经认证的设备描述文件和参数模板，可在棕地( brownfield )扩容或绿地( greenfield )建设时，将工程调试周期缩短 30%–50%。

> **交叉引用**: 本层资产与 `struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md` 中定义的"价值流阶段间接口契约"直接对应——L0 层传感器数据是"订单到现金"价值流中"生产执行"阶段最原始的输入信号。

---

## 2. 资产分类表

| 序号 | 资产名称 | 描述 | 标准/规范 | 复用频率 | 成熟度 |
|-----|---------|------|----------|---------|--------|
| E1 | **IODD (IO-Link Device Description)** | IO-Link 设备的 XML 描述文件，包含标识数据、过程数据、参数集、诊断事件与菜单结构。支持 IO-Link 主站自动识别与参数化。 | IO-Link Specification V1.1.3+ (IO-Link Consortium) | 高 (每次新增同类传感器即复用) | 成熟 |
| E2 | **GSD/GSDML (Generic Station Description)** | Profinet/Profibus 设备的通用站描述文件（GSD 用于 DP/PA，GSDML 用于 PN）。定义模块配置、参数集、诊断位、IO 映射与 DAP (Device Access Point)。 | PI (Profibus & Profinet International), IEC 61784 | 高 (Profinet 生态标配) | 成熟 |
| E3 | **EDS (Electronic Data Sheet)** | EtherNet/IP 及 DeviceNet 设备的电子数据表，描述设备类别、参数对象、IO 汇编实例、显式/隐式报文连接。 | ODVA (Open DeviceNet Vendors Association), CIP Specification Vol. 1–3 | 高 (Rockwell/Omron 等生态核心) | 成熟 |
| E4 | **XDD / CDD (CANopen/DeviceNet)** | CANopen 设备的电子数据描述（EDS 扩展 XML 版 XDD）及 FDT 通用设备描述（CDD）。定义对象字典索引、PDO/SDO 映射、设备子协议。 | CiA (CAN in Automation) 301/402, IEC 61804 | 中 (食品饮料、包装机械常用) | 成熟 |
| E5 | **OPC UA DI 信息模型模板** | OPC UA Device Integration (DI) 规范的设备类型定义模板，包括 DeviceType、ConfigurableObjectType、FunctionalGroupType 的实例化模板。 | OPC Foundation: OPC 10000-100 (DI) | 高 (OPC UA 生态必选) | 成熟 |
| E6 | **PA-DIM Companion Specification** | 过程自动化设备信息模型 (Process Automation Device Information Model)，将 EDDL 语义映射到 OPC UA，统一温度/压力/流量/物位变送器的信息模型。 | OPC Foundation / FieldComm Group, PA-DIM V1.0+ | 中 (流程工业新建项目) | 发展中 |
| E7 | **传感器校准证书模板** | 包含校准日期、标准器溯源、测量不确定度、修正系数、环境条件的可复用 XML/JSON 模板，符合 ISO/IEC 17025 数据管理要求。 | ISO/IEC 17025:2017 | 中 (质量审计驱动复用) | 成熟 |
| E8 | **执行器安全关断配置模板** | 阀门/驱动器的失电安全位、行程时间、ESD (Emergency Shut-Down) 逻辑模板，集成 IEC 61508 SIL 等级参数。 | IEC 61508 / IEC 61511, ISA-84 | 低–中 (安全系统专用) | 成熟 |

---

## 3. 复用建议

### 3.1 设备描述文件的层内复用策略

1. **同类替换复用**: 当现场更换同型号传感器（如将 Endress+Hauser Prosonic 更换为同系列新型号），直接复用既有 IODD/GSDML 文件，仅需更新版本号与固件兼容性校验。
2. **族系模板继承**: 基于设备厂商的族系模板（如 Siemens SIRIUS 电机启动器族），通过参数差异表派生具体型号描述，避免从零创建。
3. **多协议桥接复用**: 通过 OPC UA DI + PA-DIM 将面向 L1 的 Profinet GSDML 语义自动转换为 OPC UA 信息模型，实现一份资产描述跨协议复用。

### 3.2 跨层复用接口

- **L0 → L1**: IODD/EDS/GSDML 被 PLC 工程工具（TIA Portal, RSLogix, Codesys）导入，自动生成过程映像变量与 UDT。详见 [L1 控制层复用资产目录](../l1-control/asset-catalog.md)。
- **L0 → L2/L3**: OPC UA DI / PA-DIM 信息模型可被 SCADA/MES 直接订阅，跳过传统 PLC 标签映射，减少一层数据转换。

### 3.3 形式化验证提示

> **交叉引用**: 安全关键执行器（如 ESD 阀门）的配置模板可引入 `struct/07-formal-verification/05-spark-ada/spark-ada-do333-industrial.md` 中的合同化思维：将失电安全位、行程超时、SIL 等级要求编码为设备描述文件中的形式化属性约束，在工程导入阶段即执行静态校验。

---

## 4. 权威来源

1. ANSI/ISA-95.00.01-2010 / IEC 62264-1:2013 — Enterprise-Control System Integration Part 1: Models and Terminology
2. IO-Link Consortium — IO-Link Interface and System Specification Version 1.1.3 (2021)
3. Profibus & Profinet International (PI) — GSDML Specification for Profinet IO
4. ODVA — CIP Specification Volume 1: Common Industrial Protocol, Edition 3.8
5. OPC Foundation — OPC Unified Architecture for Devices (DI), OPC 10000-100
6. OPC Foundation / FieldComm Group — PA-DIM Companion Specification (Process Automation Device Information Model)
7. IEC 61804 — Function blocks (FB) for process control and electronic device description language (EDDL)
8. IEC 61508-2:2010 — Functional safety of electrical/electronic/programmable electronic safety-related systems

---

> 最后更新: 2026-06-06
