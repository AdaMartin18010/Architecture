# 公理-定理推理树（总表）

> **版本**: 2026-06-06
> **定位**: 汇总全体系的公理与定理，形成可推导、可证伪的认识论框架

---

## 元公理层

> **M.1** (Architecture-Reuse Duality): 架构的本质是**约束的集合**；复用的本质是**约束的传递**。

> **M.2** (Variability Axiom): 复用的本质是管理**共性 (Commonality)** 与**变性 (Variability)** 的分离与绑定。没有变性管理的复用是克隆，不是工程。

> **M.3** (Hierarchy Non-Reduction): 复用具有层次性（业务→应用→组件→功能），层次间**不可约化**。

---

## 按主题分类的公理-定理

### 01 元模型层

| 编号 | 类型 | 命题 |
|------|------|------|
| M.1 | 公理 | Architecture-Reuse Duality |
| M.2 | 公理 | Variability Axiom |
| M.3 | 公理 | Hierarchy Non-Reduction |
| M.T1 | 定理 | Viewpoint Composition |
| M.T2 | 定理 | Standard Alignment Transitivity |

### 02 业务架构层

| 编号 | 类型 | 命题 |
|------|------|------|
| 2.1 | 公理 | Capability Atomicity |
| 2.2 | 公理 | Value Stream Conservation |
| 2.T1 | 定理 | Value Stream Composition |
| 2.T2 | 定理 | Process-Service Duality |
| 2.T3 | 定理 | Business-Application Bridging |

### 03 应用架构层

| 编号 | 类型 | 命题 |
|------|------|------|
| 3.1 | 公理 | Component Encapsulation |
| 3.2 | 公理 | Deployment Independence |
| 3.T1 | 定理 | Service Substitution |
| 3.T2 | 定理 | Data-Application Coupling |
| 3.T3 | 定理 | Microservice Decomposition Limit |

### 04 组件架构层

| 编号 | 类型 | 命题 |
|------|------|------|
| 4.1 | 公理 | Interface Contract Completeness |
| 4.2 | 公理 | Dependency Acyclicity |
| 4.T1 | 定理 | Dependency Transitivity |
| 4.T2 | 定理 | Liskov Substitution for Components |
| 4.T3 | 定理 | Semantic Versioning Validity |

### 05 功能架构层

| 编号 | 类型 | 命题 |
|------|------|------|
| 5.1 | 公理 | Function Purity |
| 5.2 | 公理 | Determinism Boundary |
| 5.T1 | 定理 | Functional Composition |
| 5.T2 | 定理 | AI Function Non-Determinism |
| 5.T3 | 定理 | MCP-A2A Complementarity |

### 06 治理层

| 编号 | 类型 | 命题 |
|------|------|------|
| 6.1 | 公理 | Governance Necessity |
| 6.2 | 公理 | Maturity Evolution |

### 07 形式化验证层

| 编号 | 类型 | 命题 |
|------|------|------|
| F.1 | 公理 | Formal Verification Trust Transfer |
| F.2 | 公理 | Specification-Implementation Gap |
| F.T1 | 定理 | Compositionality of Formal Verification |
| R.1 | 公理 | Ownership Trust Transfer |
| R.2 | 公理 | Trait Contract Completeness |
| R.T1 | 定理 | Cargo Unification Safety |
| R.T2 | 定理 | Unsafe Boundary |

### 08 认知架构层

| 编号 | 类型 | 命题 |
|------|------|------|
| C.1 | 公理 | Cognitive Load Conservation |
| C.2 | 公理 | Expertise Pattern Transfer |
| C.T1 | 定理 | AI Augmentation Ceiling |

### 09 价值量化层

| 编号 | 类型 | 命题 |
|------|------|------|
| V.1 | 公理 | Value Quantification Uncertainty |
| V.2 | 公理 | Strategic Value Non-Quantifiability |
| V.T1 | 定理 | ROI Threshold (AAF < 0.7) |
| V.T2 | 定理 | Break-Even Point |

### 10 供应链安全层

| 编号 | 类型 | 命题 |
|------|------|------|
| S.1 | 公理 | Trust Transitivity Collapse |
| S.2 | 公理 | SBOM Completeness Illusion |
| S.T1 | 定理 | SLSA Level Monotonicity |
| S.T2 | 定理 | XZ Backdoor Detection |
| ZT.1 | 公理 | Zero Trust Transitivity |
| ZT.2 | 公理 | Defense-in-Depth Redundancy |
| ZT.T1 | 定理 | SBOM Completeness Limit |

### 11 工业 IoT 层

| 编号 | 类型 | 命题 |
|------|------|------|
| I.1 | 公理 | OT Determinism Non-Negotiable |
| I.2 | 公理 | Lifecycle Mismatch |
| I.3 | 公理 | Safety-Security Duality |
| I.4 | 公理 | Gateway Eternity |
| I.5 | 公理 | Safety Certification Contextuality |
| I.T1 | 定理 | Brownfield Dominance |
| I.T2 | 定理 | Brownfield Migration Speed |
| I.T3 | 定理 | OT-IT Reuse Asymmetry |
| ISA.1 | 公理 | HierarchyScope Consistency |
| ISA.2 | 公理 | Capability-Resource Binding |
| ISA.T1 | 定理 | Object Model Composition |
| FX.1 | 公理 | Determinism Preservation |
| FX.2 | 公理 | Semantic Compatibility |
| FX.T1 | 定理 | C2C-C2D Migration Cost |
| FX.T2 | 定理 | Gateway Eternity (OPC UA FX) |

### 12 AI 原生复用层

| 编号 | 类型 | 命题 |
|------|------|------|
| AI.1 | 公理 | Probabilistic Contract Necessity |
| AI.2 | 公理 | Uncertainty Composition |
| AI.T1 | 定理 | Calibration Ceiling |
| AI.T2 | 定理 | Human-in-the-Loop Optimality |
| CP.1 | 定理 | Marginal Coverage |
| CP.2 | 定理 | Conditional Coverage |
| MCP.1 | 定理 | Stateless Scalability |
| A2A.1 | 定理 | Agent Card Trust |

### 13 新兴趋势层

| 编号 | 类型 | 命题 |
|------|------|------|
| PE.1 | 公理 | Platform as Product |

---

## 推理依赖图

```
M.1, M.2, M.3 (元公理)
    ├──→ 2.1 (Capability Atomicity)
    │       └──→ 2.T1 (Value Stream Composition)
    │
    ├──→ 3.1 (Component Encapsulation)
    │       └──→ 3.T1 (Service Substitution)
    │
    ├──→ 4.1 (Interface Contract Completeness)
    │       └──→ 4.T2 (Liskov Substitution)
    │
    ├──→ 5.1 (Function Purity)
    │       └──→ 5.T1 (Functional Composition)
    │
    ├──→ F.1 (Formal Verification Trust Transfer)
    │       └──→ R.1 (Ownership Trust Transfer)
    │
    └──→ C.1 (Cognitive Load Conservation)
            └──→ C.T1 (AI Augmentation Ceiling)
```

---

## 可证伪条件

| 公理/定理 | 反例条件 | 修正策略 |
|----------|---------|---------|
| M.2 (Variability Axiom) | 某类复用无需变性管理 | 限定公理适用范围 |
| 2.1 (Capability Atomicity) | 组织结构定义的能力边界成功复用 | 将"成功"量化为多场景验证 |
| 3.T2 (Data-Application Coupling) | 直接存储耦合仍能独立复用 | 重新定义"独立"的判定标准 |
| V.T1 (ROI Threshold) | AAF ≥ 0.7 仍产生正 ROI | 引入战略价值折现因子 |
| AI.T1 (Calibration Ceiling) | KL 散度大但校准误差小 | 检查真实分布估计方法 |

---

> 最后更新: 2026-06-06
> 维护规则: 每新增一个公理/定理，必须在此表中登记，并标注推理依赖
