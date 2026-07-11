# 课程大纲：软件架构复用工程

> **版本**: 2026-07-08
> **课时**: 16 周 × 3 学时/周 = 48 学时
> **形式**: 讲授 50% + 案例研讨 30% + 工具实践 20%

---

## 概念定位：课程大纲的范围

**课程大纲（Syllabus）** 在本目录中的定义是：将 `struct/` 知识体系转化为 16 周教学周期的结构化方案，规定每周的主题、核心内容与实践作业。它与 `learning-path.md` 的分工是：学习路径按**读者角色**组织（4 条并行路径），课程大纲按**时间轴**组织（16 周串行推进）；二者共享同一套 `struct/` 源文档，因此大纲的周次主题与 13 个一级主题一一对应，不引入知识体系之外的内容。

### 示例：一周教学单元的构成

例如：第 2-3 周"元模型与标准"单元，核心内容取自 `struct/01-meta-model-standards/`（ISO 42010/42020/42030、TOGAF 10、ArchiMate 4.0），实践作业是完成一份标准对齐矩阵——该作业的模板与评分口径可直接复用 `struct/99-reference/templates/` 与 `alignment-matrix.md` 的现有结构。

### 反例：不属于本大纲的内容

- 具体知识点的详细讲解文本（属于 `struct/` 各主题文档，大纲只索引不复制）；
- 随技术演进每季度变化的标准状态细节（属于 `99-reference/frontier-tracking/`，大纲只标注主题稳定性）；
- 面向自学者而非课堂的个性化路径（属于 `learning-path.md`）。

### 权威来源

> **权威来源**（课程设置所依据的知识体系与标准框架）：
>
> - SWEBOK V4（软件工程知识体系，课程知识领域划分基准）：<https://www.computer.org/education/bodies-of-knowledge/software-engineering>
> - The Open Group TOGAF Standard（企业架构教学单元基准）：<https://pubs.opengroup.org/togaf-standard/>
> - ISO/IEC/IEEE 42010:2022（架构描述教学单元基准）：<https://www.iso.org/standard/74393.html>
>
> **核查日期**: 2026-07-08
> **参见**: `struct/99-reference/course/learning-path.md`（按角色组织的学习路径）、`struct/99-reference/course/quiz.md`（配套测验）

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
