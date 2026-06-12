# 快速参考卡

> **版本**: 2026-06-06
> **用途**: 软件工程架构复用视角的一页纸速查

---

## 13 个一级主题速记

```text
基础层:      01 元模型  |  07 形式化验证  |  08 认知架构
层次层:      02 业务 → 03 应用 → 04 组件 → 05 功能
治理层:      06 跨层治理  |  09 价值量化
安全层:      10 供应链安全
垂直领域:    11 工业 IoT/OT-IT
前沿层:      12 AI 原生复用  |  13 新兴趋势
参考层:      99 参考索引
```

---

## 核心公理速查

| 编号 | 名称 | 一句话摘要 |
|------|------|-----------|
| M.1 | Reusability as Architectural Concern | 复用性是架构关注点，必须显式表达 |
| 2.1 | Capability Atomicity | 业务能力是可复用的最小业务语义单元 |
| 3.2 | Data-Application Coupling | 数据与应用复用独立 ⟺ 抽象数据服务 |
| 4.1 | Interface Contract Completeness | 可复用性取决于接口契约完备性 |
| 5.2 | AI Function Non-Determinism | AI 功能复用必须包含确定性边界 |
| 6.1 | Governance Necessity | 无治理→克隆；无度量→形式 |
| F.1 | Formal Verification Trust Transfer | 形式化验证的性质可被继承 |
| C.1 | Cognitive Load Conservation | 降低外在负荷，优化相关负荷 |
| V.1 | ROI Threshold | AAF < 0.7 是 ROI 为正的必要条件 |
| S.1 | Trust Transitivity Collapse | 信任链长度 > 5 时信任度 ≈ 0 |
| I.1 | OT Determinism Non-Negotiable | OT 复用必须以确定性为首要约束 |

---

## 决策速查

### 何时复用？

```text
AAF < 0.7          → 优先复用
0.7 ≤ AAF < 0.9    → 权衡决策（考虑战略价值）
AAF ≥ 0.9          → 重新实现
```

### 选择哪个架构模式？

| 条件 | 推荐模式 |
|------|---------|
| 团队 < 50人, 部署 < 1天/次 | 模块化单体 |
| 多团队, 独立部署, 技术多样性 | 微服务 + 服务网格 |
| 事件驱动, 高吞吐, 最终一致 | EDA |
| 计算密集型, 快速扩缩容 | Serverless |
| 跨语言复用, 边缘部署 | WASM 组件 |

### 选择哪个形式化方法？

| 场景 | 方法 | 成本 |
|------|------|------|
| 分布式协议 | TLA+ | 中 |
| 架构约束 | Alloy | 低 |
| 定理证明 | Coq/Isabelle | 高 |
| Rust 安全 | 类型系统 + Miri/Kani | 低-中 |
| 飞控软件 | SPARK/Ada | 高 |
| 铁路信号 | B Method | 高 |

---

## 标准索引速查

| 标准 | 主题 | 状态 |
|------|------|------|
| ISO 42010:2022 | 01 元模型 | 生效 |
| ISO 26566:2026 | 06 治理 | 最新 |
| SLSA 1.0 | 10 安全 | 生效 |
| MCP 2025-11-25 | 12 AI原生 | 当前稳定版 |
| A2A v1.0.0 | 12 AI原生 | 生效 |
| ISA-95 / IEC 62264 | 11 工业IoT | 生效 |

---

## 关键公式速查

```text
COCOMO II 复用调整:
  ESLOC = ASLOC × (1 - AT/100) × AAF
  AAF = 0.4 × DM + 0.3 × CM + 0.3 × IM

复用 ROI:
  ROI = (C_rebuild - C_reuse) × N_use + B_quality + B_consistency

信任传递:
  Trust(A, M) = ∏ Trust(Xᵢ, Xᵢ₊₁) ≈ 0, 当 chain_length > 5

认知负荷:
  CL_total = CL_intrinsic + CL_extraneous + CL_germane ≤ CL_capacity
```

---

## 紧急联系（虚构）

| 问题类型 | 参考文档 |
|---------|---------|
| 架构模式选择 | `03/07-cloud-native-patterns/reusability-matrix-2026.md` |
| 供应链攻击响应 | `10/03-attack-vectors/attack-tree.md` |
| MCP 协议问题 | `05/06-mcp-a2a-protocols/protocol-analysis.md` |
| 工业协议映射 | `11/01-isa-95-model/cross-layer-matrix/data-flow-mapping.md` |
| 成本估算 | `09/01-cocomo-ii-reuse/cocomo-2026-calibration.md` |

---

> 最后更新: 2026-06-06
