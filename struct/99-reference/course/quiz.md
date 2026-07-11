# 课程测验：软件架构复用工程

> **版本**: 2026-07-08
> **形式**: 单选 + 多选 + 简答
> **建议时长**: 60 分钟

---

## 概念定义

**课程测验（Course Quiz）**: 用于评估学习者对软件架构复用知识体系掌握程度的题目集合，通常包含概念辨析、标准识别、案例分析等题型。

---

## 正向示例

### 示例 1：有效测验设计

某测验要求学员为真实金融系统建立 ISO/IEC/IEEE 42010:2022 / TOGAF / SLSA 对齐矩阵，学员通过查阅 `struct/` 权威来源完成，评分 90+。

### 示例 2：简答型高阶评估

"为复用而复用"简答题迫使学员区分抽象过度与价值驱动复用，显著提升了架构决策质量。

---

## 反例/反模式

- **反模式 1：只考标准号记忆**。学员能背诵 ISO/IEC/IEEE 42010:2022 但无法解释其视点机制。
- **反模式 2：题目无权威来源**。答案基于个人经验而非国际标准，导致评分失真。

---

## 一、概念辨析（单选）

### 1. 什么是架构复用中的"单一真源"？

- A. 所有代码都放在一个仓库里
- B. 以 `struct/` 为权威来源，`view/` 为其只读聚合视角 ✅
- C. 只允许一位架构师修改文档
- D. 所有项目使用同一套技术栈

### 2. ISO/IEC/IEEE 42010:2022 主要解决什么问题？

- A. 软件测试流程
- B. 架构描述的语言与视点 ✅
- C. 项目管理方法论
- D. 数据库设计规范

---

## 二、标准与框架（多选）

### 3. 下列哪些标准/框架与本知识体系直接对齐？

- A. TOGAF Standard 10 ✅
- B. ArchiMate 4.0 ✅
- C. ISO/IEC 26550:2015 ✅
- D. SLSA 1.2 ✅
- E. ISO 9001:2015

### 4. 软件供应链安全应关注哪些要素？

- A. SBOM ✅
- B. Provenance ✅
- C. SLSA 等级 ✅
- D. OWASP SCVS ✅
- E. UML 类图

---

## 三、正向示例与反模式（简答）

### 5. 请举一个成功的架构复用正向示例，并说明其关键成功因素

**参考答案要点**:

- 选择可复用资产时进行了成本/收益分析；
- 建立了清晰的接口契约与版本策略；
- 通过成熟度模型持续度量复用效果。

### 6. "为复用而复用"是一种什么反模式？应如何避免？

**参考答案要点**:

- 过度抽象导致不必要的复杂性；
- 应基于真实业务价值和复用频次进行决策；
- 使用复用决策树或 ROI 模型量化评估。

---

## 四、形式化与量化（计算/分析）

### 7. 某组件库开发成本为 80 人天，预计在第 3、5、8 个项目中分别节省 20、35、50 人天。假设无贴现，该复用是否值得？

**参考答案**:

- 总节省 = 20 + 35 + 50 = 105 人天
- 开发成本 = 80 人天
- 净收益 = 25 人天 > 0，值得复用。

### 8. 为什么 TLA+ 适合验证分布式协议（如 MCP/A2A）？

**参考答案要点**:

- TLA+ 能精确描述状态机与并发行为；
- TLC 模型检查器可发现死锁、活锁与不变量违反；
- 适合验证消息协议、任务生命周期等场景。

---

## 五、权威来源核查

### 9. 以下哪个引用存在潜在问题？

- A. ISO/IEC 25010:2023
- B. TOGAF® Standard, 10th Edition
- C. SLSA 1.2
- D. MCP 2026-07-28 RC（已废弃） ✅

---

## 评分标准

| 题型 | 分值 |
|------|------|
| 单选 | 每题 5 分，共 10 分 |
| 多选 | 每题 10 分，共 20 分 |
| 简答 | 每题 15 分，共 45 分 |
| 计算/分析 | 每题 12.5 分，共 25 分 |
| **总计** | **100 分 |

---

## 权威来源

- Anderson, L. W., & Krathwohl, D. R. (2001). *A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of Educational Objectives*. <https://www.uky.edu/~rsand1/china2018/texts/Anderson-Krathwohl%20Taxonomy.pdf>
- ISO/IEC/IEEE 42010:2022. *Systems and software engineering — Architecture description*. <https://www.iso.org/standard/74296.html>
- The Open Group. *TOGAF® Standard, 10th Edition*. <https://www.opengroup.org/togaf>
- OpenSSF. *SLSA 1.2*. <https://slsa.dev/spec/v1.2/levels>
- OWASP. *Software Component Verification Standard*. <https://owasp.org/scvs/>

---

## 交叉引用

- 课程大纲：[syllabus.md](syllabus.md)
- 学习路径：[learning-path.md](learning-path.md)
- 主术语表：[../glossary/glossary-master.md](../glossary/glossary-master.md)