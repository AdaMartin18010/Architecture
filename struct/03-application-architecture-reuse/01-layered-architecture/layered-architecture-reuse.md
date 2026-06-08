# 分层架构复用模式

> **版本**: 2026-06-08
> **定位**: 应用架构层（Level 2）—— 经典分层架构的复用边界与模式提炼
> **对齐标准**: ISO/IEC/IEEE 42010:2022, SWEBOK v4
> **状态**: ⏳ 框架填充中

---

## 1. 核心概念

分层架构（Layered Architecture）是应用架构中最经典的组织模式，其核心思想是**将系统按职责垂直划分为若干层，每层仅与直接相邻层交互**。从复用视角看，分层架构的边界定义了复用粒度的自然切割面。

ISO/IEC/IEEE 42010:2022 将架构描述的基本单元定义为 **Architecture View Component**，而分层架构中的每一层（Layer）本质上就是一个可复用的 View Component。SWEBOK v4 在软件设计中进一步强调：层的独立性是复用可行性的前提条件。

### 1.1 经典分层 vs. 现代演进

| 模式 | 核心边界 | 复用单元 | 耦合特征 |
|------|---------|---------|---------|
| 经典三层架构 (Presentation/Business/Data) | 技术职责 | 层内模块 | 上层依赖下层 |
| Clean Architecture (Uncle Bob) | 业务逻辑为中心 | Use Case / Entity | 依赖规则指向内层 |
| Onion Architecture (Palermo) | 领域模型为核心 | Domain Service | 外层依赖内层 |
| Ports & Adapters (Hexagonal) | 端口-适配器边界 | Port / Adapter | 业务核心零外部依赖 |

---

## 2. 复用模式

### 2.1 层内模块复用（Intra-layer Reuse）

同一层内的模块通过**共享库（Shared Library）**或**内部开源（Inner Source）**实现复用。

- **适用场景**: 工具类、基础实体定义、通用校验逻辑
- **边界判定**: 当模块被 ≥3 个同层服务依赖时，应当提取为共享库
- **风险**: 隐式共享状态导致层内耦合上升

### 2.2 层间接口复用（Inter-layer Reuse）

通过**严格定义的层间契约**实现跨层复用。Clean Architecture 中的 **Interface Adapter** 层即为此模式的典型实现。

> **定理 L.1** (Layer Interface Stability): 分层架构的复用稳定性与层间接口的变更频率成反比。若某层接口在 6 个月内变更次数 > 3，则该层不适合作为复用边界。

### 2.3 领域核心复用（Domain Core Reuse）

Onion Architecture 和 Hexagonal Architecture 将**领域模型**置于最内层，该层具备最高的复用价值：

1. **业务规则实体（Entity）**: 跨项目复用，零外部依赖
2. **领域服务（Domain Service）**: 跨应用复用，仅依赖实体和值对象
3. **应用服务（Application Service）**: 通常不复用，因与特定用例绑定

---

## 3. 四种架构的复用决策矩阵

| 复用目标 | 经典三层 | Clean Architecture | Onion Architecture | Ports & Adapters |
|---------|---------|-------------------|-------------------|-----------------|
| 领域模型跨系统复用 | ⚠️ 困难（与数据层耦合） | ✅ 推荐 | ✅ 推荐 | ✅ 推荐 |
| 数据库适配器复用 | ✅ 容易 | ✅ 容易 | ✅ 容易 | ✅ 推荐 |
| UI/接口层复用 | ✅ 容易 | ⚠️ 需通过适配器 | ⚠️ 需通过适配器 | ⚠️ 需通过端口 |
| 跨技术栈迁移 | ❌ 困难 | ✅ 推荐 | ✅ 推荐 | ✅ 推荐 |

---

## 4. 实践约束

- **依赖方向不可违反**: 无论选择哪种分层模式，外层 → 内层的依赖方向是强制约束
- **层厚度控制**: 单层的代码量建议控制在总代码量的 20%-35%，过厚的层暗示职责未充分分离
- **测试金字塔对齐**: 内层应有最高的单元测试密度，外层以集成/E2E测试为主

---

> 最后更新: 2026-06-08
> 权威来源:
>
> - <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
> - <https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/>
> - <https://iso.org/standard/74296.html> (ISO/IEC/IEEE 42010:2022)
