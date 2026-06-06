# ISA-95 资产目录深度清单
>
> 版本: 2026-06-06
> 对齐来源: ANSI/ISA-95.00.01-2010 (IEC 62264-1), ISA-95.00.02-2018 (IEC 62264-2), ISA-95.00.03-2013 (IEC 62264-3), MESA International, OMAC PackML State Model

## 1. ISA-95 五层模型资产分类

### 1.1 层级定义与资产范围

| 层级 | 名称 | 时间尺度 | 典型资产 | 管理域 |
|-----|------|---------|---------|--------|
| **L0** | 现场设备 (Field) | 毫秒–秒 | 传感器、执行器、驱动器 | 物理过程 |
| **L1** | 基本控制 (Control) | 秒–分 | PLC、DCS 控制器、RTU、CNC | 过程控制 |
| **L2** | 监控层 (Supervisory) | 分–小时 | SCADA、HMI、批处理管理器 | 区域监控 |
| **L3** | 制造运营 (MES) | 小时–天 | MES 系统、质量管理系统、WMS | 工厂运营 |
| **L4** | 企业层 (Enterprise) | 天–月 | ERP、PLM、CRM、SCM | 业务管理 |

### 1.2 L0 现场设备资产类型

| 资产类别 | 子类型 | 关键属性 | 语义模型 |
|---------|--------|---------|---------|
| **温度传感器** | RTD、热电偶、红外 | 量程、精度、响应时间、IEC 60584/60751 类型 | OPC UA DI 规范 |
| **压力传感器** | 压阻、电容、压电 | 量程、过载能力、介质兼容性 | OPC UA DI |
| **流量传感器** | 电磁、超声、科里奥利、涡街 | 口径、精度、雷诺数范围 | OPC UA DI |
| **物位传感器** | 雷达、超声、电容、导波雷达 | 量程、介电常数要求 | OPC UA DI |
| **分析仪表** | pH、电导率、溶解氧、气相色谱 | 校准周期、试剂需求、测量原理 | 特定厂商 EDDL |
| **执行器** | 电动、气动、液压阀门 | 行程时间、扭矩/推力、失电安全位 | OPC UA DI |
| **变频器 (VFD)** | 矢量控制、直接转矩控制 | 功率范围、载波频率、EMC 等级 | OPC UA DI |
| **电机** | 感应电机、伺服电机、步进电机 | 额定功率、转速、转矩曲线、效率等级 | IEC 61800-7 (Drive Profile) |

### 1.3 L1 控制器资产类型

| 资产类别 | 子类型 | 关键属性 | 编程标准 |
|---------|--------|---------|---------|
| **PLC** | 紧凑型、模块化、安全 PLC (SIL 3) | I/O 点数、扫描周期、冗余配置 | IEC 61131-3 |
| **DCS 控制器** | 过程控制器、混合控制器 | 控制回路数、算法块库、冗余 | IEC 61499 (分布式) |
| **CNC** | 铣床、车床、加工中心 | 轴数、插补精度、G-code 支持 | ISO 6983 / DIN 66025 |
| **运动控制器** | 单轴、多轴、机器人控制器 | 轴数、同步精度、PLCopen MC 支持 | PLCopen Motion Control |
| **机器人控制器** | 六轴、SCARA、协作机器人 | 负载、臂展、重复精度、安全等级 | ISO 10218 / ISO/TS 15066 |
| **RTU** | 远程终端单元 | 通信协议、I/O 容量、环境等级 | IEC 60870-5-101/104 |

### 1.4 L2 监控层资产类型

| 资产类别 | 功能 | 集成接口 | 数据流 |
|---------|------|---------|--------|
| **SCADA** | 实时数据采集、报警、历史趋势 | OPC UA / OPC Classic / DNP3 | L1 → L2 → L3 |
| **HMI/操作站** | 操作员界面、配方管理、报表 | 直接 PLC 连接 / OPC | L1 ↔ 操作员 |
| **批处理管理器** | ISA-88 批处理执行、电子批记录 | ISA-88 S88 接口 | L2 ↔ L3 |
| **历史数据库** | 时间序列数据存储、压缩 | OPC HDA / MQTT / REST | L1/L2 → 存储 |
| **报警管理系统** | 报警优先级、抑制、泛滥管理 | OPC A&E / ISA-18.2 | L1 → 操作员 |

### 1.5 L3 MES 资产类型

| 资产类别 | ISA-95 活动 | 功能模块 | 与 L4 集成 |
|---------|------------|---------|-----------|
| **生产调度** | 详细排程 | 订单分配、资源优化、甘特图 | ERP 工单 |
| **生产跟踪** | 分派生产、收集生产数据 | WIP 跟踪、在制品状态、良率 | ERP 完工报告 |
| **质量管理** | 收集测试数据、分析质量 | SPC、CAPA、不合格品管理 | PLM 规格 |
| **维护管理** | 设备维护、收集维护数据 | CMMS、预测性维护、备件 | ERP 资产模块 |
| **物料管理** | 管理物料、管理库存 | 批次追踪、库位管理、盘点 | ERP 库存 |
| **人员管理** | 管理人力资源 | 技能矩阵、考勤、培训记录 | HR 系统 |
| **文档管理** | 管理文档 | 电子工作指令、SOP 版本控制 | PLM 文档 |

## 2. ISA-95 资源模型（Resource Model）

### 2.1 四类资源

| 资源类型 | 定义 | 示例 | 复用模式 |
|---------|------|------|---------|
| **人员 (Personnel)** | 执行工作的人员 | 操作员、维护技师、质检员 | 技能矩阵模板、资质证书复用 |
| **设备 (Equipment)** | 执行工作的物理资产 | 机床、反应釜、测试台 | 设备模板、OEE 指标库 |
| **物料 (Material)** | 被加工或消耗的实体 | 原料、在制品、成品、耗材 | 物料主数据、BOM 模板 |
| **过程段 (Process Segment)** | 能力定义（做什么、需要什么资源）| 装配工序、测试流程、包装规范 | 过程段模板库、能力目录 |

### 2.2 设备能力属性清单

```
Equipment Capability
├── Identification
│   ├── EquipmentID (全局唯一)
│   ├── EquipmentClass (设备类别，如 "CNC_Lathe_3Axis")
│   └── EquipmentLevel (Unit / Cell / Line / Site)
├── Operational Capability
│   ├── ProductionRate (单位时间产量)
│   ├── SetupTime (换型时间)
│   ├── CycleTime (节拍时间)
│   ├── Availability (可用性，OEE 组成)
│   ├── Performance (性能率，OEE 组成)
│   └── QualityRate (质量率，OEE 组成)
├── Physical Capability
│   ├── Dimensions (L×W×H，工作空间)
│   ├── WeightCapacity (最大负载)
│   ├── PowerRequirement (功耗)
│   └── EnvironmentalRequirements (温度、湿度、洁净度)
├── Control Capability
│   ├── SupportedProtocols (OPC UA, MQTT, Profinet, EtherCAT)
│   ├── ProgramStorageCapacity (程序存储容量)
│   └── DataCollectionFrequency (数据采集频率)
└── Maintenance Capability
    ├── MTBF (平均故障间隔)
    ├── MTTR (平均修复时间)
    ├── MaintenanceSchedule (预防性维护周期)
    └── SparePartsList (关键备件清单)
```

## 3. ISA-95 与 AAS 的映射

| ISA-95 概念 | AAS 对应 | 子模型模板 |
|------------|---------|-----------|
| Equipment | Asset (AssetKind = Instance) | Technical Data, Nameplate, Identification |
| EquipmentClass | Asset (AssetKind = Type) | Technical Data, Nameplate |
| Personnel | Asset (无形资产) | Contact Information, Qualifications |
| MaterialLot | Asset (Instance) | Identification, Carbon Footprint |
| ProcessSegment | Submodel (能力描述) | Custom Submodel |
| ProductionSchedule | Submodel (计划数据) | Time Series Data |
| MaintenanceRecord | Submodel (维护历史) | Handover Documentation |

## 4. OMAC PackML 状态机与 ISA-95 集成

### 4.1 PackML 单元模式状态

| 状态 | 说明 | ISA-95 活动映射 |
|-----|------|----------------|
| **Idle** | 等待命令 | 生产分派前 |
| **Starting** | 启动序列 | 资源分配 |
| **Execute** | 正常运行 | 执行生产 |
| **Completing** | 完成序列 | 收集生产数据 |
| **Complete** | 完成 | 生产跟踪更新 |
| **Resetting** | 复位 | 准备下一批次 |
| **Holding/Held** | 保持 | 异常处理 |
| **Unholding** | 解除保持 | 恢复执行 |
| **Suspending/Suspended** | 暂停 | 物料等待 |
| **Unsuspending** | 解除暂停 | 恢复执行 |
| **Stopping/Stopped** | 停止 | 安全停机 |
| **Aborting/Aborted** | 中止 | 紧急停机 |
| **Clearing** | 清除故障 | 维护介入 |

### 4.2 PackML 模式（Modes）

| 模式 | 用途 | 安全等级 |
|-----|------|---------|
| **Production** | 正常生产 | 最高安全约束 |
| **Maintenance** | 维护/调试 | 旁路部分安全互锁 |
| **Manual** | 手动操作 | 操作员直接控制 |
| **Recipe** | 配方管理 | 验证模式 |
| **User 1-4** | 厂商自定义 | 按需求定义 |

## 5. 语义模型与接口标准

### 5.1 设备描述技术对比

| 技术 | 标准化组织 | 用途 | 状态 |
|-----|-----------|------|------|
| **EDDL (Electronic Device Description Language)** | IEC 61804 | 现场设备参数描述 | 成熟，广泛使用 |
| **FDT/DTM (Field Device Tool)** | FDT Group | 设备参数化与诊断 | 成熟，向 FDT 3.0 演进 |
| **OPC UA DI (Device Integration)** | OPC Foundation | OPC UA 设备信息模型 | 主流，与 AAS 集成 |
| **PA-DIM (Process Automation Device Information Model)** | OPC Foundation / FieldComm | 过程自动化统一信息模型 | 开发中，对标 EDDL |
| **AAS 子模型模板** | IDTA | 资产标准化数字表示 | 发展中，生态建设 |

### 5.2 ISA-95 B2MML（Business To Manufacturing Markup Language）

- XML Schema 实现 ISA-95 数据交换
- 覆盖：人员、设备、物料、过程段、生产能力、生产调度、生产绩效
- 与 SOAP/Web Services 集成
- 现代替代：REST/JSON + OPC UA + AAS

## 6. 资产目录复用策略

### 6.1 模板化复用

| 模板层级 | 复用单元 | 实现方式 |
|---------|---------|---------|
| **设备类别模板** | 同类设备的通用属性集 | AAS 子模型模板 (IDTA-02003 Technical Data) |
| **OEE 指标模板** | 设备效率计算标准 | ISA-95 绩效数据 + PackML 计数器 |
| **维护策略模板** | 预防性/预测性维护规则 | ISA-95 维护请求 + AAS 维护子模型 |
| **技能矩阵模板** | 人员资质要求 | ISA-95 人员能力 + 培训记录子模型 |

### 6.2 跨层引用链

```
L4 ERP
├── 物料主数据 (Material Master)
└── 工单 (Work Order)
    ↓ B2MML / REST / AAS
L3 MES
├── 生产调度 (Production Schedule)
├── 设备 OEE 实时计算
└── 质量批次追踪
    ↓ OPC UA / MQTT
L2 SCADA
├── 报警管理 (ISA-18.2)
├── 历史数据 (Time Series)
└── 配方管理 (ISA-88)
    ↓ OPC UA / Profinet / EtherCAT
L1 PLC
├── 控制逻辑 (IEC 61131-3)
├── 运动控制 (PLCopen)
└── 安全逻辑 (SIL 3)
    ↓ I/O 信号
L0 传感器/执行器
├── 模拟量 (4-20mA, 0-10V)
└── 数字量 (24V DC)
```

## 7. 参考索引

- ANSI/ISA-95.00.01-2010 / IEC 62264-1:2013 — Enterprise-Control System Integration Part 1: Models and Terminology
- ANSI/ISA-95.00.02-2018 / IEC 62264-2 — Part 2: Object Model Attributes
- ANSI/ISA-95.00.03-2013 / IEC 62264-3 — Part 3: Activity Models of Manufacturing Operations Management
- IEC 62264-4:2015 — Part 4: Object Model Attributes for Manufacturing Operations Management
- ISA-88 / IEC 61512 — Batch Control
- ISA-18.2 / IEC 62682 — Management of Alarm Systems
- OMAC PackML — State Model and Tag Naming
- IEC 61804 — EDDL
- OPC UA DI — Device Integration Model
- PA-DIM — Process Automation Device Information Model
