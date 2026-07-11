# Event-B 与 B Method：铁路信号系统的精化复用
>
> 版本: 2026-06-06
> 对齐来源: Atelier B / CLEARSY、Rodin Platform、CENELEC EN 50128、Abrial (2010)、Michael Butler 讲义

## 1. B Method 与 Event-B 体系

### 1.1 历史演进

| 阶段 | 时间 | 特征 |
|-----|------|------|
| B Method | 1990s– | 软件开发形式化方法，集合论+逻辑，Atelier B / B-Toolkit |
| Event-B | 2004– | 系统行为建模，更灵活的精化概念，Rodin 平台 |

### 1.2 核心工具链

| 工具 | 类型 | 工业应用 |
|-----|------|---------|
| **Atelier B** | 商业工具（CLEARSY, FR） | 铁路行业主导，SIL4 认证平台 |
| **Rodin Platform** | 开源 Eclipse 插件 | Event-B 建模、证明、动画 |
| **ProB** | 模型检验器 | Rodin 插件，LTL 属性检验 |
| **B-Toolkit** | 历史工具（B-Core, UK） | 早期 B Method 项目 |

### 1.3 工业采用

- **铁路联锁**：Alstom、Systerel、Thales、CLEARSY
- **智能电网**：Selex、Critical Software
- **核能/国防**：AWE（原子武器机构）、航空项目

## 2. Event-B 建模基础

### 2.1 两大构造

| 构造 | 角色 | 内容 |
|-----|------|------|
| **Context（上下文）** | 静态部分 | 载体集、常量、公理、定理 |
| **Machine（机器）** | 动态部分 | 状态变量、守卫事件（Guarded Events）|

### 2.2 关键机制

- **精化（Refinement）**：从抽象规格逐步细化到具体设计
  - 数据精化：抽象变量替换为具体变量（需 Gluing Invariant）
  - 行为精化：事件原子性分解（Atomicity Decomposition）
- **上下文扩展（Context Extension）**：继承并增强静态知识
- **证明义务（Proof Obligations）**：
  - 不变量保持（INV）
  - 守卫加强（GRD）
  - 动作模拟（SIM）
  - 自然数变体（NAT）/ 变体递减（VAR）

### 2.3 证明统计示例

典型教学案例（课程管理系统）证明分布：

| 构造 | 证明义务 | 自动(%) | 手动(%) |
|-----|---------|--------|--------|
| Contexts | 3 | 100% | 0% |
| 抽象 Machine (m0) | 11 | 73% | 27% |
| 第一次精化 (m1) | 14 | 93% | 7% |
| 数据精化 (m2) | 29 | 90% | 10% |
| **总计** | **57** | **88%** | **12%** |

> 数据精化产生约 50% 的证明义务，但自动化率仍保持高位。

## 3. 铁路信号系统案例

### 3.1 CENELEC EN 50128 与形式化方法

EN 50128（铁路领域软件安全标准）推荐使用形式化方法，尤其是 SIL 1–4 的软件架构设计和组件设计。

### 3.2 ERTMS/ETCS 建模

```
步骤 1：图形建模（UML Profile）
    ├── 安全铁路元模型（Safety Railway Meta-model）
    └── UML 类图扩展安全概念

步骤 2：模型转换
    ├── Event-B 元模型（B Method 扩展）
    └── UML → Event-B 自动模型转换

步骤 3：Event-B 生成与形式验证
    ├── 模型检验（ProB）
    └── 动画验证（Animation）
```

### 3.3 精化链在铁路中的应用

- **功能关注（Functional Concern）**：顶层 Machine 表示系统主功能，可精化为不同具体设计；所有精化机器均为潜在替代方案。
- **行为关注（Behavioural Concern）**：通过变体（Variant）和水平不变量（Horizontal Invariant）链接同一系统的不同替代实现。

### 3.4 模型分解技术

铁路信号系统模型庞大复杂，Event-B 提供多种分解策略：

1. **共享变量分解**（Shared Variable Decomposition）
2. **共享事件分解**（Shared Event Decomposition）
3. **外部事件分解**（External Event Decomposition）

**复用价值**：分解后的子模型可独立精化，提升模块化与可维护性。

## 4. CLEARSY Safety Platform

### 4.1 原生 B 能力的安全平台

- **SIL4 认证**（Certifer 9594/0262）
- **关键特性**：将软件变量与代表物理实体及其时序演化的变量结合
- **证明直达系统属性**：避免复杂形式化软件需求正确性的难题

### 4.2 示例：列车定位系统

- **证明目标**：计算的位置区间始终包含列车的实际位置
- **方法**：B 模型中同时包含软件变量和物理世界变量，利用平台保证的实时性约束完成证明

## 5. 复用模式

### 5.1 精化模式库

| 模式 | 描述 | 复用场景 |
|-----|------|---------|
| 抽象引入模式 | 从非形式需求到抽象 Machine | 新项目启动模板 |
| 数据精化模式 | 集合→函数→数组的逐步替换 | 内存优化设计 |
| 事件拆分模式 | 一个抽象事件→多个具体事件 | 并发行为建模 |
| 守卫加强模式 | 逐步添加安全守卫 | 安全关键系统 |

### 5.2 证明复用

- **证明库（Proof Libraries）**：Rodin 的易扩展架构支持插件化证明器
- **模式匹配证明**：相似结构的证明义务自动匹配已有证明

### 5.3 跨项目模型元素复用

- **Context 扩展链**：基础数学理论 → 领域特定公理 → 项目特定常量
- **Machine 复用**：已验证的通信协议 Machine 作为新系统的子组件

## 6. Event-B 与 LTL

- 传统 Event-B 验证聚焦于**安全属性**（Safety）："坏事永远不会发生"
- **活性属性**（Liveness）需借助 LTL 和 ProB 模型检验
- **挑战**：LTL 属性一般不被精化保持，需发展保持 LTL 的精化变体

## 7. 参考索引

- Abrial, J.-R.: "Modeling in Event-B: System and Software Engineering" (2010)
- Abrial, J.-R.: "The B-Book: Assigning Programs to Meanings" (1996)
- CENELEC EN 50128:2011 "Railway applications — Communication, signalling and processing systems"
- Rodin Platform: [event-b.org](https://wiki.event-b.org/index.php/Main_Page)
- Atelier B: [atelierb.eu](https://www.atelierb.eu)
- CLEARSY Safety Platform 资料
- Butler, M.: "Modelling and verification with Event-B" (SETSS 2016 讲义)
- Sabatier, D.: CLEARSY 铁路形式证明项目 (2016)


---

## 补充说明：Event-B 与 B Method：铁路信号系统的精化复用

## 概念定义

**定义**：B Method 与 Event-B 是基于集合论与精化演算的形式化方法，通过从抽象规约逐步精化到可执行代码，并证明每步精化保持规约性质。

## 反例

**反例**：某地铁项目复用上一代联锁代码但未重建精化链，新增功能破坏了“敌对进路互锁”不变式，导致信号冲突风险。

## 权威来源

> **权威来源**:
>
> - [Event-B](https://wiki.event-b.org/index.php/Main_Page)
> - [Atelier B](https://www.atelierb.eu/en/)
> - 核查日期：2026-07-07
