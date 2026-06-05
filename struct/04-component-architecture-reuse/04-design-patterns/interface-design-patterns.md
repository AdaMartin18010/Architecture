# 组件接口契约设计模式

> **版本**: 2026-06-06
> **定位**: 将组件复用的接口设计模式系统化，支持从语法契约到语义契约的演进

---

## 目录

- [组件接口契约设计模式](#组件接口契约设计模式)
  - [目录](#目录)
  - [1. 接口契约的层次](#1-接口契约的层次)
  - [2. 核心设计模式](#2-核心设计模式)
    - [模式 1: Stable Abstraction Principle (SAP)](#模式-1-stable-abstraction-principle-sap)
    - [模式 2: Interface Segregation Principle (ISP)](#模式-2-interface-segregation-principle-isp)
    - [模式 3: Dependency Inversion Principle (DIP)](#模式-3-dependency-inversion-principle-dip)
    - [模式 4: Liskov Substitution for Components](#模式-4-liskov-substitution-for-components)
    - [模式 5: Semantic Versioning (SemVer)](#模式-5-semantic-versioning-semver)
    - [模式 6: Consumer-Driven Contracts (CDC)](#模式-6-consumer-driven-contracts-cdc)
  - [3. 反模式与重构](#3-反模式与重构)
  - [4. 评估清单](#4-评估清单)

---

## 1. 接口契约的层次

组件接口契约不是单一事物，而是由浅入深的四个层次：

```
Layer 1: 语法契约 (Syntax Contract)
    └── "调用的形状是什么"
    └── 方法签名、参数类型、返回类型、异常声明

Layer 2: 前置/后置契约 (Pre/Post Condition)
    └── "调用前后必须满足什么"
    └── @Requires, @Ensures, 不变量

Layer 3: 协议契约 (Protocol Contract)
    └── "调用顺序必须是什么"
    └── 状态机、时序约束、调用顺序规则

Layer 4: 语义契约 (Semantic Contract)
    └── "调用意味着什么"
    └── 业务语义、领域不变量、SLA/SLO
```

**定义 C.1** (Contract Strength): 接口契约的强度 S 定义为上述四个层级的覆盖完整性：

```
S = (s_syntax × 0.15) + (s_prepost × 0.25) + (s_protocol × 0.30) + (s_semantic × 0.30)

其中 s ∈ [0, 1]
```

> **定理 4.1** (Reuse Confidence-Contract Monotonicity): 给定相同的功能正确性，接口契约强度 S 越高，复用者对该组件的信任度 T 越高，且呈单调不减关系：T ∝ S。

---

## 2. 核心设计模式

### 模式 1: Stable Abstraction Principle (SAP)

**描述**: 包的抽象程度应与其稳定性成正比。稳定的包应更抽象，易变的包可以更具体。

```
抽象性 A = 抽象类数 / 总类数
不稳定性 I = 出向依赖数 / (出向依赖数 + 入向依赖数)

理想关系: A + I ≈ 1
```

**复用意义**: 稳定且抽象的组件是最佳复用目标。不稳定或具体的组件复用价值低，易随需求变更而失效。

### 模式 2: Interface Segregation Principle (ISP)

**描述**: 客户端不应依赖它们不使用的接口。一个组件应暴露多个小接口，而非一个大接口。

**复用意义**: 小接口降低复用者的认知负担和依赖范围。大接口强制复用者接受不必要的约束。

### 模式 3: Dependency Inversion Principle (DIP)

**描述**: 高层模块不应依赖低层模块，二者都应依赖抽象。

**复用意义**: 抽象是复用的媒介。依赖具体实现导致替换成本高昂。

### 模式 4: Liskov Substitution for Components

**描述**: 子类型（或替代组件）必须能够替换其基类型（或被替代组件）而不破坏程序正确性。

**形式化**:

```
Let C 是组件，C' 是 C 的替代。
C' ⊑ C  iff
    Pre(C') ⊆ Pre(C)   (弱化前置条件)
    Post(C') ⊇ Post(C) (强化后置条件)
    Invariant(C') ⊇ Invariant(C)
```

> **定理 4.2** (Component Liskov Substitution): 若 C' ⊑ C，则在任何正确调用 C 的上下文中，C' 可安全替换 C 而不引入新的失败模式。

### 模式 5: Semantic Versioning (SemVer)

**描述**: MAJOR.MINOR.PATCH 版本号明确表达兼容性语义。

**复用意义**: SemVer 是复用者信任机制的一部分。稳定的版本策略允许复用者安全升级。

### 模式 6: Consumer-Driven Contracts (CDC)

**描述**: 由消费者定义其期望的契约，供应商确保满足这些契约。

**复用意义**: 复用者（消费者）主动表达需求，避免供应商单方面设计接口导致的适配成本。

---

## 3. 反模式与重构

| 反模式 | 症状 | 重构策略 |
|--------|------|---------|
| **God Interface** | 一个接口有 50+ 方法 | 拆分为角色接口 |
| **Leaky Abstraction** | 实现细节暴露到接口 | 增加适配层或抽象层 |
| **Tight Coupling** | 调用者与被调用者共享状态 | 引入事件/消息/依赖注入 |
| **Fragile Base** | 基组件的修改导致所有复用者失效 | 强化契约，使用 SemVer |
| **Version Confusion** | 多个不兼容版本共存 | 命名空间隔离、虚拟依赖 |
| **False Semantic** | 接口名称与实际行为不符 | 重命名接口或拆分功能 |

---

## 4. 评估清单

**接口契约质量检查表**:

- [ ] 语法层：参数类型、返回值、异常是否完整文档化？
- [ ] 前置/后置层：关键方法是否有前置条件和后置条件？
- [ ] 协议层：调用顺序是否通过状态机或时序图说明？
- [ ] 语义层：业务语义是否与领域术语对齐？
- [ ] 版本层：是否遵循 SemVer，并在变更时更新版本号？
- [ ] 测试层：是否通过 CDC 或契约测试保证兼容性？
- [ ] 治理层：接口所有者是否明确，变更审批流程是否清晰？

---

> 最后更新: 2026-06-06
