# 课程与学习路径

> **版本**: 2026-07-08
> **定位**: Phase 6 整合输出——将知识体系转化为可教学、可学习、可评估的课程产品

---

## 概念定义

**课程产品（Course Product）**: 基于 `struct/` 知识体系，面向学习者设计的教学材料集合，包括学习路径、课程大纲、测验与幻灯片。

---

## 正向示例

- 学习者按 [学习路径](learning-path.md) 的架构师路径学习，8 周后完成一份可复用架构设计文档。
- 讲师使用 [课程大纲](syllabus.md) 和 [幻灯片生成脚本](../../../scripts/build-slides.py) 在 16 周内完成教学。

---

## 反例/反模式

- 只阅读文档不做测验，无法检验理解程度。
- 跳过元模型与标准，直接学习 MCP/A2A 等技术细节，导致缺乏体系化视角。

---

## 交付物清单

| 文件 | 说明 |
|------|------|
| [learning-path.md](learning-path.md) | 4 条递进式学习路径 + 13 主题索引 |
| [syllabus.md](syllabus.md) | 16 周课程大纲、考核方式 |
| [quiz.md](quiz.md) | 课程测验与参考答案 |
| [../../../scripts/build-slides.py](../../../scripts/build-slides.py) | 14 个主题 reveal.js 幻灯片生成脚本 |

---

## 权威来源

- Anderson, L. W., & Krathwohl, D. R. (2001). *A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of Educational Objectives*. <https://www.uky.edu/~rsand1/china2018/texts/Anderson-Krathwohl%20Taxonomy.pdf>
- IEEE/ACM. *Software Engineering Body of Knowledge (SWEBOK) V4*. <https://www.computer.org/education/bodies-of-knowledge/software-engineering>

---

## 交叉引用

- 主术语表：[../glossary/glossary-master.md](../glossary/glossary-master.md)
- 工具入口：[../tools/README.md](../tools/README.md)
- 全书构建：[../../../scripts/build-deliverables.py](../../../scripts/build-deliverables.py)
