# L1 控制层复用资产目录

> **版本**: 2026-06-06
> **层级**: ISA-95 Level 1 — 基本控制层 (Basic Control Layer)
> **时间尺度**: 秒–分 (s–min)
> **管理域**: 过程控制与逻辑执行域
> **对齐来源**: IEC 61131-3 Ed3.0, PLCopen Motion Control Part 1+2 V2.0, IEC 61499, ISA-95.00.03-2013

---

## 1. 层定义与复用范围

L1 控制层是 ISA-95 中直接执行物理过程控制的层级，核心资产为 **PLC/DCS 程序单元**。
本层复用的关键在于：将经过现场验证的算法封装为可移植的 **功能块 (Function Block, FB)**、**用户数据类型 (UDT)** 与控制策略模板，实现"一次开发、多机型部署"。
PLCopen 运动控制库的成功实践表明，标准化 FB 可将跨厂商移植成本降低 40% 以上。

> **交叉引用**: L1 控制逻辑是 `struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md` 中"价值流阶段间接口契约"的技术实现载体——控制 FB 的输入/输出接口即构成了 L1↔L0、L1↔L2 的物理接口契约。

---

## 2. 资产分类表

| 序号 | 资产名称 | 描述 | 标准/规范 | 复用频率 | 成熟度 |
|-----|---------|------|----------|---------|--------|
| C1 | **通用 PID 控制功能块** | 支持增量式/位置式 PID、抗积分饱和、前馈补偿、自动/手动无扰切换的标准功能块。可直接复用于温度、压力、流量等单回路控制。 | IEC 61131-3 Ed3.0 (FB 语言), ISA-5.1 | 极高 (几乎每个控制项目) | 成熟 |
| C2 | **PLCopen 运动控制 FB 库** | 单轴/多轴运动控制标准功能块族：MC_Power, MC_MoveAbsolute, MC_MoveRelative, MC_GearIn, MC_CamIn, MC_Home 等。抽象 AXIS_REF 数据类型实现硬件无关。 | PLCopen Motion Control Part 1 & 2 V2.0 | 高 (离散制造、包装、机器人) | 成熟 |
| C3 | **设备 UDT (用户数据类型) 模板** | 面向电机、阀门、变频器等设备对象的标准化结构化数据类型，包含 Command (命令字)、Status (状态字)、Fault (故障码)、Param (参数集)。 | IEC 61131-3 (STRUCT), OOP 扩展 (Ed3.0) | 极高 (工程标准化基础) | 成熟 |
| C4 | **顺序控制顺序功能图 (SFC) 模板** | 基于 IEC 61131-3 SFC 的步序控制模板，包含 Init/Run/Hold/Abort/Complete 标准步及转移条件骨架，适用于批次与离散顺序控制。 | IEC 61131-3 (SFC 语言), ISA-88 / IEC 61512 | 高 (批次反应釜、灌装线) | 成熟 |
| C5 | **安全关断逻辑 FB (Safety FB)** | 符合 IEC 62061 / ISO 13849-1 的安全功能块，实现双通道急停、安全门监控、光幕消隐、安全速度监控。可直接复用于 SIL3/PL e 等级系统。 | IEC 62061:2021, ISO 13849-1:2023, IEC 61131-3 | 中 (安全项目必用) | 成熟 |
| C6 | **通信协议封装 FB** | 将 OPC UA Client/Server、MQTT Publisher、Modbus TCP/RTU Master、EtherNet/IP Adapter 等协议栈封装为标准化 FB，隐藏协议细节，暴露统一数据接口。 | OPC Foundation, OASIS MQTT, IEC 61131-3 | 高 (IIoT 与 OT-IT 融合) | 成熟 |
| C7 | **批次单元过程控制模板 (Unit Procedure)** | 基于 ISA-88 物理模型与过程模型的 Unit 级控制模板，包含 Equipment Phase、Operation、Unit Procedure 三层调用结构，支持配方参数动态绑定。 | ISA-88 / IEC 61512-1, IEC 61131-3 | 中 (制药、化工批次控制) | 成熟 |
| C8 | **振动/温度异常检测算法块** | 集成边缘预处理功能的控制算法 FB，实现 FFT 特征提取、阈值比较、简单统计过程控制 (SPC) 规则，用于泵/风机/轴承的预测性维护前端。 | ISO 17359 (Condition Monitoring), IEC 61131-3 | 中 (预测性维护项目) | 发展中 |

---

## 3. 复用建议

### 3.1 功能块库的多项目复用

1. **建立企业级 FB 库**: 将 C1–C8 按行业场景（流程、离散、混合）组织为层级化库，纳入版本控制（Git + PLC 工程工具导出格式），并配套自动化回归测试。
2. **AXIS_REF 抽象策略**: 运动控制项目优先采用 PLCopen 标准 AXIS_REF 抽象。更换伺服驱动器厂商时，仅需重新映射底层伺服接口，上层应用 FB（MC_MoveAbsolute 等）完全复用。
3. **UDT 跨层映射**: UDT 模板应同时生成 OPC UA 信息模型与 MES 数据契约，实现 L1 程序变量 → L2 SCADA 标签 → L3 MES 属性的自动映射，消除人工重复配置。

### 3.2 跨层复用接口

- **L1 ↔ L0**: UDT 模板与设备描述文件（IODD/EDS/GSDML）自动绑定，实现传感器物理通道到程序变量的零配置映射。详见 [L0 现场层复用资产目录](../l0-field/asset-catalog.md)。
- **L1 → L2**: 通过 OPC UA 服务器 FB 或 MQTT Publisher FB，将 UDT 实例直接发布为 L2 可订阅的信息模型节点。
- **L1 ← L3**: 通过 OPC UA Client FB 或 MQTT Subscriber FB，接收 L3 MES 下发的配方参数与工单指令。

### 3.3 形式化验证提示

> **交叉引用**: 安全关断逻辑 FB (C5) 与运动控制状态机 (C2) 属于高完整性控制资产。建议引入 `struct/07-formal-verification/05-spark-ada/spark-ada-do333-industrial.md` 中 DO-333 的**演绎验证**思想，对 FB 的 Pre/Post 条件进行形式化规约；对于状态机行为，可参考 `struct/07-formal-verification/06-b-method/event-b-railway-refinement.md` 中的 **Event-B 精化方法**，从抽象状态机逐步精化到 PLC 扫描周期级实现。

---

## 4. 权威来源

1. IEC 61131-3:2013 — Programmable controllers – Part 3: Programming languages (Ed3.0 含 OOP 扩展)
2. PLCopen — Motion Control Specification Part 1 & 2, Version 2.0 (2019)
3. PLCopen — Technical Paper: PLCopen Function Blocks for Motion Control (<www.plcopen.org>)
4. IEC 61499-1 / -2 — Function blocks for industrial-process measurement and control systems
5. ISA-88 / IEC 61512-1:2013 — Batch Control Part 1: Models and Terminology
6. IEC 62061:2021 — Safety of machinery: Functional safety of electrical control systems
7. ISO 13849-1:2023 — Safety of machinery: Safety-related parts of control systems
8. ANSI/ISA-95.00.03-2013 / IEC 62264-3 — Activity Models of Manufacturing Operations Management

---

> 最后更新: 2026-06-06


---

## 补充章节

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