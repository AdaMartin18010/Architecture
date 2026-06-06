# IEEE 1517-2010 软件生命周期复用过程

> **定位**: 将 IEEE 1517 复用过程标准与 ISO/IEC/IEEE 12207:2017 及本体系四层复用架构对齐
> **对齐来源**: IEEE Std 1517-2010, ISO/IEC/IEEE 12207:2017, ISO/IEC/IEEE 42020:2019, TOGAF 10
> **状态**: Phase 2（2026-Q4）
> **权威链接**:
>
> - <https://standards.ieee.org/standard/1517-2010.html>
> - <https://www.iso.org/standard/63712.html> (ISO/IEC/IEEE 12207:2017)

---

## 1. 标准概述

**IEEE Std 1517-2010** — *Standard for Information Technology — System and Software Life Cycle Processes — Reuse Processes* 是 IEEE 对系统与软件生命周期中复用过程的专门规范。
它扩展了 IEEE Std 12207，定义了系统化的复用过程、活动和任务。

| 属性 | 内容 |
|------|------|
| 全称 | IEEE Std 1517-2010 |
| 基础 | IEEE Std 12207 / ISO/IEC/IEEE 12207 |
| 核心目标 | 构造可复用资产、从可复用资产构造系统、管理可复用资产 |
| 关键概念 | Domain Engineering, Reuse Asset Management, Reuse Program Management |

---

## 2. 核心复用过程组

IEEE 1517 定义了三大复用过程组，每个过程组包含若干活动和任务：

```text
┌─────────────────────────────────────────────────────────────┐
│              IEEE 1517 Reuse Processes                      │
├─────────────────────────────────────────────────────────────┤
│  1. Domain Engineering Process                              │
│     └── 识别、构建、维护特定领域的可复用资产                   │
├─────────────────────────────────────────────────────────────┤
│  2. Reuse Asset Management Process                          │
│     └── 存储、分类、检索、分发、版本控制复用资产               │
├─────────────────────────────────────────────────────────────┤
│  3. Reuse Program Management Process                        │
│     └── 规划、组织、监控、改进组织的复用计划                   │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Domain Engineering Process（领域工程过程）

| 活动 | 任务 | 对应本体系 |
|------|------|-----------|
| 领域分析 | 识别领域边界、共性和可变性 | `02-business-architecture-reuse` |
| 领域设计 | 定义参考架构和组件模型 | `03-application-architecture-reuse` / `04-component-architecture-reuse` |
| 领域实现 | 构建和测试可复用资产 | `04-component-architecture-reuse` / `05-functional-architecture-reuse` |
| 领域维护 | 根据反馈演进资产 | `06-cross-layer-governance` |

### 2.2 Reuse Asset Management Process（复用资产管理过程）

| 活动 | 任务 | 对应本体系 |
|------|------|-----------|
| 资产获取 | 从内部或外部获取资产 | `10-supply-chain-security` |
| 资产分类 | 按领域、质量、成熟度分类 | `01-meta-model-standards/07-omg-ras` |
| 资产存储 | 放入仓库/注册表 | `13-emerging-trends/01-platform-engineering` (IDP) |
| 资产检索 | 搜索和发现 | `99-reference/tools/terminology-query.py` |
| 资产分发 | 交付给复用者 | `06-cross-layer-governance` |
| 资产版本控制 | 管理版本和变更 | `10-supply-chain-security/02-sbom-standards` |

### 2.3 Reuse Program Management Process（复用项目管理过程）

| 活动 | 任务 | 对应本体系 |
|------|------|-----------|
| 复用规划 | 定义目标、范围、资源 | `09-value-quantification` |
| 复用组织 | 建立团队、角色、职责 | `06-cross-layer-governance` |
| 复用监控 | 收集度量、评估成熟度 | `06-cross-layer-governance/03-maturity-models` |
| 复用改进 | 持续优化复用流程 | `06-cross-layer-governance/05-metrics-kpi` |

---

## 3. 与 ISO/IEC/IEEE 12207:2017 的映射

ISO/IEC/IEEE 12207:2017 将复用 concern 作为**跨生命周期过程的注记和活动**嵌入，而 IEEE 1517 则提供了更详细的复用专用过程。

| IEEE 1517 过程 | 12207:2017 中的对应位置 | 说明 |
|---------------|------------------------|------|
| Domain Engineering | 技术过程（Stakeholder Requirements, Architectural Design, Implementation） | 1517 细化为领域专用活动 |
| Reuse Asset Management | 支持过程（Configuration Management, Quality Assurance） | 1517 提升为独立过程 |
| Reuse Program Management | 项目管理过程 + 组织项目使能过程 | 1517 聚焦复用特有的治理 |

**关键差异**:

- **12207:2008** 曾有独立的“Software Reuse Processes”过程组
- **12207:2017** 将其整合为跨过程的 activities/tasks，更强调复用是**横切关注点**
- **IEEE 1517** 保留了独立的复用过程视图，便于组织实施

---

## 4. 与 ISO/IEC/IEEE 42020:2019 的映射

ISO/IEC/IEEE 42020:2019 定义了架构过程。IEEE 1517 的复用过程可映射到 42020 的架构过程：

| 42020 架构过程 | 1517 复用活动 |
|---------------|--------------|
| Architecture Planning | Reuse Program Management — 规划 |
| Architecture Development | Domain Engineering — 领域设计 |
| Architecture Evaluation | Reuse Asset Management — 质量评估 |
| Architecture Maintenance | Domain Engineering — 领域维护 |

---

## 5. 与 TOGAF ADM 的映射

| TOGAF 10 ADM 阶段 | IEEE 1517 过程 | 复用活动 |
|------------------|---------------|----------|
| Phase A: Architecture Vision | Reuse Program Management | 定义复用目标和范围 |
| Phase B: Business Architecture | Domain Engineering | 业务领域分析 |
| Phase C: Information Systems Architectures | Domain Engineering | 应用/数据架构设计 |
| Phase D: Technology Architecture | Domain Engineering | 技术参考架构 |
| Phase E: Opportunities & Solutions | Reuse Asset Management | 资产检索和适配决策 |
| Phase F: Migration Planning | Reuse Program Management | 复用推广计划 |
| Phase G: Implementation Governance | Reuse Asset Management | 资产分发和版本控制 |
| Phase H: Architecture Change Management | Domain Engineering | 领域资产维护 |

---

## 6. 与四层复用架构的映射

| 本体系层次 | IEEE 1517 重点活动 | 示例 |
|-----------|-------------------|------|
| 02 业务架构 | Domain Engineering — 领域分析 | 业务能力目录、领域模型 |
| 03 应用架构 | Domain Engineering — 领域设计 | 参考架构、应用框架 |
| 04 组件架构 | Domain Engineering — 领域实现 | 组件库、框架、设计模式 |
| 05 功能架构 | Domain Engineering — 领域实现 | 算法、函数、MCP Tool |
| 06 跨层治理 | Reuse Program Management | 成熟度评估、度量、FinOps |
| 10 供应链安全 | Reuse Asset Management | SBOM、来源审查、资产获取 |

---

## 7. 关键活动：复用决策检查清单

基于 IEEE 1517 和本体系，一个完整的复用决策应包括：

1. **识别候选资产**
   - [ ] 资产是否有全局唯一标识？（F1 / FAIR4RS）
   - [ ] 资产元数据是否完整？（F2 / OMG RAS Classification）
   - [ ] 资产是否在可信来源？（R1.2 / SLSA provenance）

2. **评估适配成本**
   - [ ] AAF（改编调整因子）是否 < 0.7？（COCOMO II / 定理 V.1）
   - [ ] 依赖链长度是否 < 5？（公理 S.1）
   - [ ] 许可证是否兼容？（R1.1 / SPDX）

3. **验证资产质量**
   - [ ] 是否有测试覆盖？
   - [ ] 是否有 SBOM？（I2 / SPDX / CycloneDX）
   - [ ] 是否有形式化验证或安全审计？（07-formal-verification）

4. **集成与治理**
   - [ ] 是否符合架构决策和 Golden Path？
   - [ ] 是否纳入 FinOps 成本分摊？
   - [ ] 是否更新复用度量指标？

---

## 8. 批判性评估

### 8.1 优势

- **过程完整**: 覆盖领域工程、资产管理、项目管理的全生命周期
- **与主流标准兼容**: 与 12207、42020、TOGAF 均有清晰映射
- **实践导向**: 提供了可落地的活动和任务清单

### 8.2 局限

- **发布较早**: 2010 年标准，未涉及 AI、云原生、容器、MCP 等现代复用形态
- **缺少具体技术格式**: 不规定资产包装格式（需结合 OMG RAS、SBOM 等）
- **度量不够量化**: 对复用 ROI、成本的计算需要结合 COCOMO II 等补充

### 8.3 2026 年应用建议

1. **将 1517 作为过程框架**: 用其三大过程组组织本体系的治理内容
2. **结合现代工具链**: 用 Backstage IDP 替代传统 RAS 仓库，用 SBOM 替代手工依赖记录
3. **结合 AI 复用**: 在 Domain Engineering 中增加 LLM/Agent 能力域；在 Asset Management 中增加 MCP Tool Registry
4. **持续跟踪 IEEE 更新**: 关注 IEEE 1517 的后续修订或 ISO 对应标准的发布

---

## 9. 公理映射

> **公理 1517.1** (Reuse Process Closure): 有效的复用必须形成闭环：领域工程产生资产 → 资产管理存储分发 → 项目管理监控改进 → 反馈驱动领域工程演进。

> **公理 1517.2** (Asset-Process Coherence): 复用资产的质量上限由复用过程成熟度决定；再优秀的资产，在没有资产管理过程的组织中也无法被有效复用。

---

## 10. 参考链接

- IEEE Std 1517-2010: <https://standards.ieee.org/standard/1517-2010.html>
- ISO/IEC/IEEE 12207:2017: <https://www.iso.org/standard/63712.html>
- ISO/IEC/IEEE 42020:2019: <https://www.iso.org/standard/71898.html>
- TOGAF 10 Architecture Development Method: <https://www.opengroup.org/togaf>
