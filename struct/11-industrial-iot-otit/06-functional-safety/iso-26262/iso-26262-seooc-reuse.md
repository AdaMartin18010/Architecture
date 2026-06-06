# ISO 26262 SEooC 与软件组件复用
>
> 版本: 2026-06-06
> 对齐来源: Tuxera Whitepaper (2023), MDH Publication (Safety Contracts), ISO 26262:2018 / :2025 草案

## 1. 核心概念：SEooC（Safety Element out of Context）

### 1.1 定义

SEooC 是为**跨上下文复用**而开发的安全元素。它：

- **不能**单独建立安全案例（Safety Case），因为功能安全是整车级 Item 的属性，而非元素属性。
- 必须清晰定义其功能、开发步骤和目标环境，以便集成商将其整合到目标系统的安全案例中。

> ISO 26262-2:2018, 4.5.7: "The ISO 26262 series of standards, as a whole, cannot be applied to an element developed as a SEooC because functional safety is not an element property."

### 1.2 软件 SEooC 的四种创建方法

| 方法 | 新建开发 | 有变更复用 | 无变更复用 | 关键要求 |
|-----|---------|-----------|-----------|---------|
| **组件资格认证** | 否 | 否 | 是 | 提供安全分析报告、假设验证 |
| **Proven-In-Use 论证** | 否 | 可能 | 是 | 足够运行历史、故障统计、配置控制 |
| **原 ISO 26262 项目组件** | 否 | 是 | 否 | 完整开发证据包、 tailoring |
| **按 ISO 26262-6 为复用开发** | 是 | 是 | 是 | 假设驱动开发、完整生命周期 |

## 2. 按 ISO 26262-6 构建软件 SEooC

### 2.1 假设驱动的开发流程

由于 SEooC 脱离具体车辆上下文开发，必须在概念和系统设计阶段做出**假设**：

1. **功能假设**：SEooC 的用途与功能
2. **运行模式与状态**：包含配置参数的运行模式
3. **法规与标准要求**：适用的法律、法规和标准
4. **运行与环境约束**：温度、振动、EMC 等
5. **接口定义**：输入/输出、数据类型、时序
6. **危害分析结果**：已知危害、ASIL 等级、安全目标

### 2.2 软件级产品开发（V 模型）

```
软件安全需求 (SSR)
    ↓
软件架构设计 —— ASIL 等级隔离、安全机制嵌入
    ↓
软件单元设计与实现 —— MISRA C:2023 / AUTOSAR C++14
    ↓
软件集成与验证 —— 单元测试、集成测试、HIL 仿真
    ↓
嵌入式软件测试 —— 故障注入、边界条件
```

### 2.3 软件架构安全设计原则

- **模块化与隔离**：遵循"ASIL 等级隔离"原则（如 ASIL D 模块与 QM 模块的内存隔离）
- **安全机制嵌入**：
  - Watchdog（监控推理超时）
  - CRC 校验（通信完整性）
  - 软件冗余（决策算法双版本对比）
  - 看门狗与监控器

### 2.4 支持过程

| 过程 | SEooC 特定要求 |
|-----|---------------|
| 安全需求规格与管理 | 假设必须文档化并可追溯 |
| 配置管理 | 基线化所有假设与接口 |
| 变更管理 | 假设变更影响分析 |
| 验证 | 假设验证计划独立于集成验证 |
| 文档 | 安全手册（Safety Manual）为交付物核心 |
| 工具置信度 | T2/T3 工具需资格认证 |

## 3. 安全合同（Safety Contracts）驱动的复用

### 3.1 概念

安全合同是 SEooC 开发方与集成方之间的**形式化接口约定**，捕获：

- **保证（Guarantees）**：SEooC 承诺在满足假设条件下提供的安全属性
- **假设（Assumptions）**：SEooC 对宿主系统的环境要求

### 3.2 元模型

```
SEooC Component
├── Safety Contract
│   ├── Functional Assumptions
│   ├── Environmental Assumptions
│   ├── Resource Assumptions
│   └── Safety Guarantees
├── Implementation
└── Verification Evidence
```

### 3.3 集成时验证

集成阶段必须验证 SEooC 的所有假设在目标 Item 中成立：

1. 将 SEooC 假设映射到目标系统安全概念
2. 识别假设与实际环境的差距
3. 必要时进行 tailoring（裁剪）或补偿措施
4. 生成集成侧的安全论证

## 4. ISO 26262:2025 关键更新

### 4.1 智能网联场景扩展

- **新增 ML 模块功能安全要求**：数据质量验证、模型训练安全、部署监控
- **车云协同与分布式架构**：跨域控制器（MDC / Zonal）硬件冗余、云端指令安全校验
- **V2X 通信功能安全**：消息认证、防篡改、延迟容错
- **功能安全与网络安全接口**：风险共评流程、安全需求协同映射

### 4.2 硬件级防护示例

- **条款 8.4.3**：AI 加速芯片内置硬件锁步校验（Lockstep），每帧计算误差率 ≤ 10⁻⁹
- **案例**：Tesla HW4.0 双核冗余设计通过 ASIL D 认证

### 4.3 模型安全生命周期（条款 11.7.2）

- 强制建立 AI 模型版本数据库
- 记录每次迭代的数据血缘、超参数变更及验证结果
- 传统工具链（如 Simulink）不足以支持神经网络可追溯性，需额外 AI 合规平台

## 5. ISO/PAS 8800:2023 — AI 安全补充

| 维度 | ISO 26262:2025 | ISO/PAS 8800:2023 |
|-----|---------------|------------------|
| 定位 | 确定性防护（芯片→模型） | 不确定性驾驭（数据→伦理） |
| 硬件 | 锁步校验、冗余设计 | 可解释性模块嵌入 |
| 数据 | 数据血缘标记 | 训练数据质量与偏见控制 |
| 测试 | 虚拟极端场景测试（11.8.3） | 统计充分性评估 |
| 文档 | 技术安全概念 | 伦理使用声明 |

> **行业预测**：2027 年后欧盟/中国市场可能强制要求出口车型通过双标认证。

## 6. IEC 61508 与 ISO 26262 软件映射

### 6.1 映射框架（IEC TR 61508-6-1 基础）

1. 将 ISO 26262-6 的技术与措施（T&M）映射到 IEC 61508-3 的 SIL 等级
2. 对 ISO 26262 适用的 T&M 应用 IEC 61508-3 附录 C.2 的系统性安全完整性保证属性
3. 按 IEC 61508 建议优先排序适用的 T&M

### 6.2 一致性与差异

- **一致性**：两者在基本原则上高度一致；Miller (2020) 确认总体一致性。
- **差异**：ISO 26262 增加了汽车行业特定要求；IEC 61508-3 对缓解措施的规定更开放，留下更多解释空间。
- **建议**：联合使用两者，在 ISO 26262 细节不足时参考 IEC 61508。

## 7. SEooC 维护与演化

| 场景 | 维护要求 |
|-----|---------|
| 假设不变，缺陷修复 | 变更影响分析 + 回归验证 |
| 假设微调 | 安全合同修订 + 集成方通知 |
| 新车辆平台适配 | 重新验证假设、可能调整 ASIL |
| 标准版本升级 | 差距分析、证据补全 |

## 8. 参考索引

- ISO 26262-1:2018 / :2025 (Vocabulary)
- ISO 26262-2:2018 / :2025 (Management of Functional Safety)
- ISO 26262-6:2018 / :2025 (Product Development at the Software Level)
- ISO/PAS 8800:2023 (Road Vehicles — Safety and artificial intelligence)
- IEC TR 61508-6-1 (Treatment of hardware or software developed to ISO 26262, JTG20 WG)
- Tuxera: "Software SEooCs: Making embedded software components for reuse" (Whitepaper, 2023)
- Mälardalen University: "Using Safety Contracts to Guide the Integration of Reusable Safety Elements within ISO 26262"
