# 功能安全与工业 OT-IT 复用

> **版本**: 2026-07-09
> **定位**: 在工业 OT-IT 融合复用中确保功能安全证据的可追溯、可复用与可验证，覆盖 IEC 61508、ISO 26262、SOTIF、IEC 62443 的交叉约束。
> **对齐标准**: IEC 61508 Ed.3 (CDV/PRVC)、ISO 26262:2018、ISO 21448:2022 (SOTIF)、ISA/IEC 62443 系列

---

## 1. 概念定义

**功能安全（Functional Safety）** 是指电气/电子/可编程电子安全相关系统免受随机硬件故障与系统性故障导致的不可接受风险。在 OT-IT 复用场景中，功能安全证据（Safety Case、SEooC、Proven-in-Use）是跨项目复用的关键资产，但必须在目标系统的运行环境中重新验证假设覆盖性。

| 标准 | 应用领域 | 完整性等级 | 复用资产 |
|------|---------|-----------|---------|
| **IEC 61508** | 通用工业、过程、铁路等 | SIL 1–4 | 安全生命周期、TIL 工具资质、Route 2H PIU |
| **ISO 26262** | 道路车辆 | ASIL A–D | SEooC、安全手册、假设清单 |
| **ISO 21448 (SOTIF)** | 自动驾驶/ADAS | — | ODD、触发条件、性能局限评估 |
| **IEC 62443** | 工业控制系统网络安全 | SL/CL 1–4 | 安全区/管道、FR 1-7 控制要求 |

> **定理 FS.1** (Safety Evidence Reuse Invariance): 功能安全证据只能在满足其原始假设的运行环境中复用。任何假设的违反都会使证据失效，必须重新进行影响分析与验证。

---

## 2. 标准条款映射：IEC 61508 生命周期与软件复用

| IEC 61508 条款 | 内容 | 与软件复用的关系 |
|---------------|------|----------------|
| **Part 1, 7.4** | 安全生命周期管理 | 复用元素必须纳入目标项目的生命周期与配置管理 |
| **Part 2, 7.4.10** | Route 2H Proven-in-Use | 基于现场运行数据证明硬件故障率，需 χ² 置信区间 |
| **Part 3, 7.4.4** | 支持工具与编程语言 | Ed.2 T1/T2/T3 → Ed.3 TIL 0-4 工具资质 |
| **Part 3, Annex D** | 合规项安全手册 | 软件元素复用必须提供 Safety Manual |
| **IEC TR 61508-3-3:2025** | 面向对象软件 | C++ 等 OO 语言在安全关键软件中的论证方法 |
| **IEC TS 61508-3-1:2016** | SIL ≤ 2 软件复用 | 预存软件元素的复用路径 |

| IEC 61508 工具类别 | Ed.2 | Ed.3 TIL | 典型工具 | 项目治理要求 |
|:---|:---|:---:|:---|:---|
| **T1** | 仅生成无法引入错误的输出 | TIL 0 | 文档编辑器、版本控制 GUI | 配置管理 |
| **T2** | 支持 V&V，错误可被后续检查发现 | TIL 1–2 | 静态分析、单元测试框架 | 记录版本与配置 |
| **T3** | 用于开发/转换安全相关软件 | TIL 3–4 | 编译器、模型转换器、形式化验证器 | 必须执行工具资格，建立 TCF |

---

## 3. SEooC 与跨标准复用

**Safety Element out of Context（SEooC）** 是按 ISO 26262 开发的组件，在没有完整 item 级系统定义的情况下，基于合理假设进行开发。复用 SEooC 时，集成方必须验证：

1. **Assumptions of Use（AoU）**：预期 ASIL 分配、时序、诊断预算、安全状态
2. **Assumptions of Environment（AoE）**：接口、协议、电气限制、集成约束
3. **Safety Manual**：集成、配置和验证的权威指导

> ⚠️ **关键限制**：功能安全是 *item* 属性，非 element 属性。不能为 SEooC 构建独立安全案例。

| 来源标准 | 目标标准 | 复用前提 | 关键工作 |
|---------|---------|---------|---------|
| IEC 61508 | IEC 61511 | 设备认证为 "compliant item" | 提供安全手册、SIL 能力声明 |
| ISO 26262 | IEC 61508 (Ed.3) | 复杂传感器/计算平台跨域复用 | 映射 T&M 表、调整架构约束 |
| IEC 61508 | ISO 26262 | 通用组件进入汽车供应链 | 增加 S/E/C 分析、ASIL 分解 |
| DO-178C | IEC 61508 | 航空软件复用于工业 | 重新论证工具资格、调整生命周期 |

---

## 4. 正向示例

### 示例 1：SEooC 制动控制软件复用

某 Tier-1 供应商将经 ISO 26262 ASIL-D 认证的制动控制软件作为 SEooC 复用到多款车型。安全手册明确列出环境假设、集成约束与诊断覆盖要求；OEM 仅需验证这些假设在目标车型中的覆盖性，避免重复进行完整的 ASIL 开发。

### 示例 2：Proven-In-Use 阀门执行器

某过程工业最终元件供应商收集同型号 SIL 2 阀门执行器在现场累计 10⁸ 设备小时的运行数据，按 IEC 61508-2 7.4.10 与 IEC 61508-6 附录 D 的 χ² 置信区间方法推导危险未检测故障率，成功通过 Route 2H 论证。

### 示例 3：IEC 61508 Ed.3 工具资质映射

某安全 PLC 项目将经 DO-330 TQL-1 认证的静态分析工具通过跨标准合规分析映射到 IEC 61508 TIL 3 与 ISO 26262 TCL 3，显著减少重复资质工作量。

---

## 5. 反例 / 失败案例

### 反例 1：复用未经 SIL 评估的开源库

某医疗机器人团队将开源运动控制库直接复用到 SIL 2 安全功能，未评估其系统性能力、诊断覆盖率与工具资格。认证阶段无法证明需求追溯与测试完整性，项目被迫返工并推迟上市 9 个月。

### 反例 2：PIU 证据在固件更新后失效

某传感器厂商基于历史运行数据申请 Proven-In-Use 认可，但在审计期间发布了未纳入证据集的固件补丁，导致原有运行小时数据与新版本软件不可比，PIU 论证被评估员否决。

### 反例 3：安全-安全冲突

某企业将高 SIL 等级但低网络安全能力（SL 1 以下）的传统安全 PLC 复用到 modern 网络化架构中，未进行网络隔离。攻击者通过网络路径注入虚假安全状态信号，破坏了功能安全目标。

---

## 6. SIL-SL 联合评估框架

| 应用场景 | 建议的 SIL-SL 关系 | 说明 |
|---------|------------------|------|
| 高后果风险场景 | SIL = SL | 安全功能与网络安全防护强度对等 |
| 中后果风险场景 | SL ≥ SIL - 1 | 网络安全等级不低于功能安全等级减一 |
| 低后果风险场景 | SL ≥ 1 | 至少具备基础网络安全防护 |

> **定理 FS.2** (Safety-Security Coupling): 当网络攻击路径可能影响安全功能执行时，仅通过 SIL 认证不足以保证整体安全目标；必须联合评估 IEC 61508 / ISO 26262 与 IEC 62443。

---

## 7. 权威来源

> **权威来源**:
>
> - IEC 61508-3:2010 *Software safety requirements*: <https://standards.iteh.ai/catalog/standards/iec/f6570ef4-4785-4a0c-bc73-35d31a657dfb/iec-61508-3-2010> （核查日期：2026-07-09）
> - IEC 61508-6:2010 *Guidelines on the application of IEC 61508-2 and IEC 61508-3*: <https://standards.iteh.ai/catalog/standards/iec/e6145828-18e4-44ed-8aee-104e68bfbb85/iec-61508-6-2010> （核查日期：2026-07-09）
> - IEC TR 61508-3-3:2025 *Guidance on object-oriented software*: <https://webstore.iec.ch/en/publication/99554> （核查日期：2026-07-09）
> - ISO 26262:2018 *Road vehicles — Functional safety*: <https://www.iso.org/standard/68383.html> （核查日期：2026-07-09）
> - ISO 21448:2022 *Road vehicles — Safety of the intended functionality (SOTIF)*: <https://www.iso.org/standard/77490.html> （核查日期：2026-07-09）
> - ISA/IEC 62443 系列： <https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards> （核查日期：2026-07-09）

---

## 8. 交叉引用

- IEC 61508 / ISO 26262 / SOTIF 对齐： [`iec-61508-iso-26262-sotif-alignment.md`](./iec-61508-iso-26262-sotif-alignment.md)
- IEC 61508 Ed.3 复用： [`iec-61508/iec-61508-ed3-reuse.md`](./iec-61508/iec-61508-ed3-reuse.md)
- IEC 62443 工业网络安全复用： [`iec-62443-reuse-security.md`](./iec-62443-reuse-security.md)
- ISO 26262 SEooC 模板： [`iso26262-seooc-template.md`](./iso26262-seooc-template.md)

---

> 最后更新: 2026-07-09
