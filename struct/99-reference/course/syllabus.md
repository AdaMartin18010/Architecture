# 课程大纲：软件架构复用工程

> **版本**: 2026-07-08
> **课时**: 16 周 × 3 学时/周 = 48 学时
> **形式**: 讲授 50% + 案例研讨 30% + 工具实践 20%

---

## 课程目标

1. 理解架构复用的元模型、标准与公理体系。
2. 掌握业务/应用/组件/功能四层复用设计方法。
3. 能够运用成熟度模型、度量指标与治理流程评估复用能力。
4. 具备工业 IoT、AI 原生、供应链安全等垂直领域的复用分析能力。

## 教学周历

| 周次 | 主题 | 核心内容 | 实践作业 |
|------|------|----------|----------|
| 1 | 课程导论 | 知识体系结构、复用经济学、权威来源 | 建立个人知识索引 |
| 2-3 | 元模型与标准 | ISO 42010/42020/42030、TOGAF 10、ArchiMate 4.0 | 标准对齐矩阵 |
| 4-5 | 业务架构复用 | 业务能力、价值流、BPMN/DMN | 业务服务目录设计 |
| 6-7 | 应用架构复用 | 微服务、事件驱动、云原生模式 | 复用性评估问卷 |
| 8-9 | 组件与功能复用 | 接口契约、设计模式、API/MCP/A2A | 复用组件原型 |
| 10 | 跨层治理 | 成熟度模型、度量、FinOps、Agentic 治理 | 治理流程图 |
| 11 | 形式化验证 | TLA+/Alloy 案例、公理-定理推导 | 规约小练习 |
| 12 | 价值量化 | COCOMO II 2026、ROI/NPV、碳排模型 | 复用 ROI 计算 |
| 13 | 供应链安全 | SLSA、SBOM、OWASP SCVS、零信任供应链 | 攻击树分析 |
| 14 | 工业 IoT / OT-IT | ISA-95、OPC UA FX、AAS、功能安全 | 工业资产目录 |
| 15 | AI 原生复用 | MCP/A2A、Agentic Infrastructure、概率契约 | Agent 复用方案 |
| 16 | 整合输出 | 全书框架、个人项目答辩 | 可发布知识产品 |

## 考核方式

- 平时作业 40%（标准对齐、复用设计、治理流程）
- 期中项目 30%（选择一个垂直领域完成复用方案）
- 期末答辩 30%（基于 `struct/` 知识库输出可发布作品）

## 推荐工具

- 健康检查：`python scripts/health-check.py`
- 复用决策工具：`struct/99-reference/tools/reuse-decision-tool-v2/`
- COCOMO 计算器：`struct/99-reference/tools/cocomo-calculator.py`
- 全书构建：`python scripts/build-deliverables.py`

---

## 定义

**定义**：本课程大纲是软件架构复用工程知识的系统化教学安排，覆盖元模型、四层架构、治理、安全与前沿趋势。

## 示例

**示例**：第 2-3 周通过 ISO/IEC/IEEE 42010:2022/42020/42030、TOGAF Standard 10 与 ArchiMate 4.0 建立元模型与标准对齐基础，为后续各主题提供统一术语与视点框架。

## 反例

**反例**：课程若缺少权威标准来源与可验证的案例实践，学员容易将厂商特定概念误当作通用架构复用知识。

## 权威来源

> - [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74296.html) — ISO
> - [The Open Group - ArchiMate 4.0 Specification](https://www.opengroup.org/archimate-licensed-downloads) — The Open Group（2026-04-27 正式发布）
> - 核查日期：2026-07-08
