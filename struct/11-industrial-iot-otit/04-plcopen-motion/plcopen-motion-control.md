# PLCopen Motion Control 与功能块复用
>
> 版本: 2026-06-06
> 对齐来源: PLCopen.org 官方规范、IEC 61131-3 Ed3、IEC 61508/62061 功能安全

## 1. 规范体系与版本

| 规范部分 | 版本状态 | 核心内容 |
|---------|---------|---------|
| Part 1 & 2 | v2.0 合并版 | 单轴/多轴运动控制基础功能块 |
| Part 3 | 现行 | 用户指南与工程实例 |
| Part 4 | 2025 发布 | 协调运动（Coordinated Motion），机器人控制集成 |
| Part 5 | 现行 | 回零（Homing）过程标准 |
| Part 6 | 现行 | 流体动力扩展 |
| Safety | 现行 | 安全功能块，符合 IEC 61508 / IEC 62061 |

## 2. 状态机（State Machine）—— 复用语义基础

PLCopen 运动控制以**轴状态机**为核心语义模型。
任意时刻轴处于且仅处于一个状态，功能块调用触发状态转移。

### 2.1 八状态定义

```text
Disabled ──MC_Power──→ StandStill
StandStill ──MC_Home──→ Homing ──Done──→ StandStill
StandStill ──MC_Move*──→ Discrete Motion / Continuous Motion
StandStill ──MC_Stop──→ Stopping ──Done──→ StandStill
AnyState ──Error──→ ErrorStop ──MC_Reset──→ StandStill
Continuous Motion ──MC_CamIn/GearIn──→ Synchronized Motion
```

| 状态 | 语义 |
|-----|------|
| **Disabled** | 初始状态；伺服未使能，轴不受 FB 控制 |
| **StandStill** | 伺服已使能，无运动命令；所有运动起点 |
| **Homing** | 正在执行回零程序 |
| **Discrete Motion** | 执行点到点定位（绝对/相对） |
| **Continuous Motion** | 执行速度模式或力矩模式 |
| **Synchronized Motion** | 作为从轴跟随主轴（电子凸轮/齿轮/相位） |
| **Stopping** | 正在执行停止斜坡；期间 Execute 保持 TRUE |
| **ErrorStop** | 错误触发急停；仅接受 MC_Reset / MC_Power |

### 2.2 状态转移规则（复用保证）

- **顺序执行原则**：即使 PLC 支持真正并行处理，运动命令在状态机层面仍为顺序生效。
- **立即性（Immediately）**：状态改变在发出对应命令后立即反映；实际响应时间取决于系统实现。
- **异常优先级**：ErrorStop 为最高优先级状态，任何状态下检测到轴错误均强制转入。

## 3. 功能块分类与复用接口

### 3.1 管理型功能块（Administrative FBs）

| 功能块 | 作用 | 复用场景 |
|-------|------|---------|
| `MC_Power` | 伺服使能/关闭 | 所有轴的启停标准化 |
| `MC_Reset` | 清除轴错误 | 故障恢复流程复用 |
| `MC_ReadStatus` | 读取轴状态字 | 诊断面板/HMI 复用 |
| `MC_ReadActualPosition` | 读取实际位置 | 闭环监控复用 |
| `MC_ReadParameter` / `MC_WriteParameter` | 参数读写 | 调试与维护工具 |

### 3.2 单轴运动功能块

| 功能块 | 运动类型 | 关键输入 |
|-------|---------|---------|
| `MC_MoveAbsolute` | 绝对定位 | Position, Velocity, Acceleration, Deceleration |
| `MC_MoveRelative` | 相对定位 | Distance, ... |
| `MC_MoveAdditive` | 叠加定位 | Distance, 在当前目标上累加 |
| `MC_MoveVelocity` | 速度模式 | Velocity, Direction |
| `MC_MoveSuperimposed` | 叠加运动 | 主运动之上的微调 |
| `MC_Home` | 回零 | 支持 Part 5 定义的多模式回零 |
| `MC_Stop` | 受控停止 | Deceleration, Jerk |
| `MC_TorqueControl` | 力矩控制 | Torque, TorqueRamp |

### 3.3 多轴协调功能块

| 功能块 | 协调模式 | 复用价值 |
|-------|---------|---------|
| `MC_CamIn` / `MC_CamOut` | 电子凸轮 | 包装、印刷、飞剪曲线复用 |
| `MC_GearIn` / `MC_GearOut` | 电子齿轮 | 同步传动比复用 |
| `MC_Phasing` | 相位偏移 | 套准（Register）控制 |

### 3.4 Part 4 — 协调运动与机器人（2025 发布）

PLCopen Part 4 将 PLC、机器人和运动控制整合到统一编程环境：

- **运动组（Motion Group）**：定义多轴组合，当组内任一轴故障时，控制器可生成正确的组级错误响应。
- **运动组状态机**：独立的状态机管理整组轴的协调行为。
- **运动学变换（Kinematic Transformations）**：标准化 SCARA、Delta 等常见构型；允许用户自定义逆运动学。
- **统一控制**：从单一 PLC 型系统编程控制完整机器，消除传统 PLC↔机器人控制器间的通信延迟。

## 4. 安全功能块（Safety FBs）

### 4.1 安全层与应用层分离

PLCopen Safety 采用**双通道架构**：

- **安全层（Safety Layer）**：IEC 61508 / IEC 62061 SIL 认证，受约束语言子集。
- **应用层（Application Layer）**：标准 IEC 61131-3，非安全相关。

### 4.2 三级通用状态图

每个安全功能块内部定义为三级状态机：

1. **未激活（Not Active）**
2. **安全状态（Safe State）**
3. **激活（Active）**

### 4.3 标准化安全功能（Safe Motion）

2017 年发布的 Safe Motion 将 **17 个安全运动功能**映射到工业网络：

| 功能类别 | 示例 | 安全机制 |
|---------|------|---------|
| 安全停止 | SOS, STO, SS1, SS2 | 按 IEC 61800-5-2 安全停机曲线 |
| 安全速度 | SLS, SSM, SSR | 速度监控与限制 |
| 安全位置 | SLP, SCA | 范围与方向监控 |
| 安全制动 | SBT, SBC | 制动测试与控制 |

接口标准化为 `SF_SafetyRequest` + 统一命名约定，实现跨厂商安全运动功能复用。

## 5. 复用优势与工程实践

### 5.1 跨平台移植

- **硬件无关性**：应用层代码不依赖特定驱动或网络架构。
- **厂商独立性**：同一套 PLCopen 应用可在不同品牌 PLC 间移植（需保持功能块接口兼容）。
- **投资保护**：机器制造商的软件投资不受硬件迭代影响。

### 5.2 培训与维护成本

- 统一状态机语义降低跨项目学习曲线。
- 诊断代码标准化（如 X336 = "FB 在 Continuous Motion 状态不允许"）。

### 5.3 认证效率

- 使用经安全认证的 PLCopen 兼容开发工具，可简化机械安全认证流程。
- 安全功能块的高抽象级别隐藏实现细节，减少用户侧认证范围。

## 6. 与 ISA-95 的层级映射

| ISA-95 层级 | PLCopen 应用 | 典型功能块 |
|------------|-------------|-----------|
| L0 现场设备 | 伺服驱动器 | `MC_Power`, `MC_ReadActualPosition` |
| L1 控制 | PLC 运动控制 | `MC_MoveAbsolute`, `MC_Home` |
| L2  supervisory | 产线协调 | `MC_CamIn`, `MC_GearIn`, Motion Group |
| L3 MES | 订单驱动换型 | 凸轮表切换 (`MC_CamTblSelect`) |

## 7. 参考索引

- [PLCopen Motion Control Part 1 & 2 v2.0](https://www.plcopen.org)
- [PLCopen Safety Part 1 — Safety Function Blocks](https://www.plcopen.org)
- IEC 61131-3:2013 Ed3 (Programming Languages)
- IEC 61508-3:2010 / IEC 62061:2021 (Functional Safety)
- IEC 61800-5-2:2016 (Safe Torque Off / Safe Stop)


---

## 补充说明：PLCopen Motion Control 与功能块复用

## 示例

**示例**：汽车工厂将 ISA-95 L0-L4 资产目录映射到 IEC 63278 资产管理壳（AAS），通过 OPC UA FX 实现现场设备与 MES/ERP 的即插即用复用。

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
