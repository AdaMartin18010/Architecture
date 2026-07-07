# 学习路径：从架构复用新手到专家

> **版本**: 2026-07-08
> **目标**: 为不同背景读者提供 4 条递进式学习路径
> **生成命令**: `python scripts/build-deliverables.py`

---

## 概念定义

**学习路径（Learning Path）**: 按能力进阶顺序组织的主题序列，包含学习目标、推荐资源、实践任务与产出物检查点。
**专家（Expert）**: 能在真实约束下，综合运用元模型、标准、治理与量化方法，设计并演进可复用架构的从业者。

---

## 路径总览

| 路径 | 适合人群 | 预计学时 | 关键产出 |
|------|----------|----------|----------|
| 🏗️ 架构师路径 | 企业架构师、技术负责人 | 40h | 可复用架构设计文档 |
| 💻 工程师路径 | 软件工程师、DevOps | 35h | 复用组件/服务设计 |
| 🔒 安全工程师路径 | 安全架构师、合规专员 | 25h | 供应链安全评估报告 |
| 🤖 AI 原生路径 | AI 平台工程师、Agent 开发者 | 30h | MCP/A2A 复用方案 |

---

## 正向示例

### 示例 1：架构师路径成功学习

某企业架构师按「元模型 → 业务复用 → 应用复用 → 治理」顺序学习，8 周后输出一份基于 TOGAF 10 与 ArchiMate 4.0 的复用架构设计，被采纳为部门标准。

### 示例 2：工程师路径成功学习

后端工程师重点学习 `04-component-architecture-reuse` 的接口契约与版本策略，3 周内将团队公共库的重构频率降低 40%。

---

## 反例/反模式

- **反模式 1：跳跃式学习**。未理解元模型与标准，直接复制微服务或 MCP 代码示例，导致架构决策缺乏一致性。
- **反模式 2：只读不练**。阅读全部文档但不完成实践作业，无法将知识转化为可复用资产。
- **反模式 3：忽视权威来源**。将博客文章或旧版标准当作依据，造成标准引用错误。

---

## 按主题学习索引

### 01 元模型与标准对齐

- [ISO/IEC/IEEE 42010:2022 更新](../../01-meta-model-standards/01-iso-420xx-family/iso-42010-2022.md)
- [TOGAF 10 企业连续体复用](../../01-meta-model-standards/02-togaf-10-alignment/togaf-enterprise-continuum-reuse.md)
- [形式化公理体系](../../01-meta-model-standards/06-formal-axioms/axiom-system.md)

### 02 业务架构复用

- [业务能力复用](../../02-business-architecture-reuse/02-business-capability/capability-reuse.md)
- [价值流组合](../../02-business-architecture-reuse/03-value-stream/value-stream-composition.md)

### 03 应用架构复用

- [微服务复用模式](../../03-application-architecture-reuse/02-microservices/microservices-reuse-patterns.md)
- [云原生复用性矩阵](../../03-application-architecture-reuse/07-cloud-native-patterns/reusability-matrix-2026.md)

### 04 组件架构复用

- [组件模型理论](../../04-component-architecture-reuse/01-component-models/component-models-reuse.md)
- [接口契约设计](../../04-component-architecture-reuse/02-interface-contracts/interface-contracts-reuse.md)
- [6 大语言生态深度对比](../../04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md)

### 05 功能架构复用

- [API 设计复用模式](../../05-functional-architecture-reuse/01-api-design/api-design-reuse-patterns.md)
- [MCP + A2A 协议分析](../../05-functional-architecture-reuse/06-mcp-a2a-protocols/)

### 06 跨层治理与量化

- [成熟度模型评估问卷](../../06-cross-layer-governance/03-maturity-models/assessment-questionnaire.md)
- [度量指标框架](../../06-cross-layer-governance/05-metrics-kpi/metrics-framework.md)

### 07 形式化验证

- [TLA+ 案例库](../../07-formal-verification/01-tla-plus/)
- [Alloy 案例库](../../07-formal-verification/02-alloy/)

### 08 认知架构

- [ACT-R 认知复用](../../08-cognitive-architecture/01-act-r-model/act-r-cognitive-reuse.md)
- [AI 认知增强架构](../../08-cognitive-architecture/05-ai-cognitive-augmentation/augmentation-architecture.md)

### 09 价值量化

- [COCOMO II 复用模型深入](../../09-value-quantification/01-cocomo-ii-reuse/cocomo-ii-reuse-model-deep-dive.md)
- [ROI 框架](../../09-value-quantification/02-roi-npv-models/roi-framework.md)

### 10 供应链安全

- [SLSA 1.2 多轨道](../../10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md)
- [攻击树分析](../../10-supply-chain-security/03-attack-vectors/attack-tree.md)

### 11 工业 IoT / OT-IT 融合

- [ISA-95 资产目录深入](../../11-industrial-iot-otit/01-isa-95-model/isa-95-asset-catalog-deep-dive.md)
- [OPC UA FX 复用层次](../../11-industrial-iot-otit/02-opc-ua-fx/opc-ua-fx-reuse-hierarchy.md)

### 12 AI 原生复用

- [MCP 2025-11-25 权威更新](../../12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-authoritative.md)
- [A2A v1 权威更新](../../12-ai-native-reuse/02-a2a-protocol/a2a-v1-authoritative.md)

### 13 前沿趋势

- [平台工程成熟度模型](../../13-emerging-trends/01-platform-engineering/platform-maturity-model.md)
- [WASM 组件模型 2026](../../13-emerging-trends/03-webassembly-components/wasm-component-model-2026.md)

---

## 思维模型

```text
新手 → 标准对齐者 → 复用设计者 → 治理者 → 专家
   │        │            │           │        │
   └────────┴────────────┴───────────┴────────┘
              每条路径都经过：概念 → 示例 → 反例 → 实践
```

---

## 权威来源

- Anderson, L. W., & Krathwohl, D. R. (2001). *A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of Educational Objectives*. <https://www.uky.edu/~rsand1/china2018/texts/Anderson-Krathwohl%20Taxonomy.pdf>
- Merrill, M. D. (2002). *First Principles of Instruction*. <https://www.mdpi.com/2227-7102/9/3/202>
- The Open Group. *TOGAF® Standard, 10th Edition*. <https://www.opengroup.org/togaf>
- ISO/IEC/IEEE 42010:2022. *Systems and software engineering — Architecture description*. <https://www.iso.org/standard/74296.html>

---

## 交叉引用

- 课程大纲：[syllabus.md](syllabus.md)
- 主术语表：[../glossary/glossary-master.md](../glossary/glossary-master.md)
- 形式化验证环境：[../tools/formal-verification-env/README.md](../tools/formal-verification-env/README.md)
