# 课程大纲：软件架构复用工程

> **版本**: 2026-07-08
> **课时**: 16 周 × 3 学时/周 = 48 学时
> **形式**: 讲授 50% + 案例研讨 30% + 工具实践 20%

---

## 概念定义

**软件架构复用工程（Software Architecture Reuse Engineering）**: 系统性地识别、设计、实现、治理和量化软件架构资产复用的工程学科。
**课程大纲（Syllabus）**: 规定课程目标、周历、作业、考核方式与推荐资源的教学文件。

---

## 课程目标

1. 理解架构复用的元模型、标准与公理体系。
2. 掌握业务/应用/组件/功能四层复用设计方法。
3. 能够运用成熟度模型、度量指标与治理流程评估复用能力。
4. 具备工业 IoT、AI 原生、供应链安全等垂直领域的复用分析能力。

---

## 正向示例

### 示例 1：标准对齐作业

学生为某金融系统建立 ISO 42010:2022、TOGAF 10、SLSA 1.2 的对齐矩阵，识别出 12 个复用决策点，获得优秀。

### 示例 2：复用 ROI 计算

学生使用 COCOMO II 2026 校准模型，量化某组件库复用在 3 年内的 NPV，证明复用在第 14 个月回本。

---

## 反例/反模式

- **反模式 1：课程只讲理论不讲工具**。学生能背诵标准号，但不会运行 `health-check.py` 或复用决策工具。
- **反模式 2：作业脱离真实约束**。设计的复用方案不考虑组织成熟度、安全合规或成本分摊，无法落地。
- **反模式 3：忽视版本与来源**。引用过时标准或无法核查的博客，导致架构决策失准。

---

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

---

## 考核方式

- 平时作业 40%（标准对齐、复用设计、治理流程）
- 期中项目 30%（选择一个垂直领域完成复用方案）
- 期末答辩 30%（基于 `struct/` 知识库输出可发布作品）

---

## 推荐工具

- 健康检查：`python scripts/health-check.py`
- 复用决策工具：`struct/99-reference/tools/reuse-decision-tool-v2/`
- COCOMO 计算器：`struct/99-reference/tools/cocomo-calculator.py`
- 全书构建：`python scripts/build-deliverables.py`

---

## 权威来源

- Anderson, L. W., & Krathwohl, D. R. (2001). *A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of Educational Objectives*. <https://www.uky.edu/~rsand1/china2018/texts/Anderson-Krathwohl%20Taxonomy.pdf>
- IEEE/ACM. *Software Engineering Body of Knowledge (SWEBOK) V4*. <https://www.computer.org/education/bodies-of-knowledge/software-engineering>
- The Open Group. *TOGAF® Standard, 10th Edition*. <https://www.opengroup.org/togaf>
- ISO/IEC/IEEE 42010:2022. *Systems and software engineering — Architecture description*. <https://www.iso.org/standard/74296.html>

---

## 交叉引用

- 学习路径：[learning-path.md](learning-path.md)
- 主术语表：[../glossary/glossary-master.md](../glossary/glossary-master.md)
- COCOMO 工具：[../tools/cocomo-calculator.py](../tools/cocomo-calculator.py)
- 复用决策工具：[../tools/reuse-decision-tool-v2/](../tools/reuse-decision-tool-v2/)
