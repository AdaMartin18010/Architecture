# 01 元模型与标准对齐 — 推进路线图

> **版本**: 2026-06-06
> **状态**: 结构完成，内容填充中

---

## 当前进度

- [x] 01-iso-420xx-family 目录结构
- [x] 02-togaf-10-alignment 目录结构
- [x] 03-iso-26550-ple 目录结构
- [x] 04-archimate-4 目录结构
- [x] 05-swebok-v4 目录结构
- [x] 06-formal-axioms 目录结构
- [x] 核心对齐矩阵文档（alignment-matrix.md）
- [x] TOGAF 10 详细映射 → `02-togaf-10-alignment/detailed-mapping.md`
- [x] ArchiMate 4.0 更新 → `04-archimate-4/archimate-iso-mapping.md`
- [x] SWEBOK V4 对齐 → `05-swebok-v4/swebok-alignment.md`
- [x] 形式化公理体系完整版 → `06-formal-axioms/axiom-system.md` + `theorem-derivations.md`

---

## Phase 1: 概念地基（已完成，2026-06-06）

**任务**:

- [x] T01: 提取 view/ 中 8 份文档的元模型相关内容
- [x] T02: 搜索 ISO 420xx 官方资料和 IREB 术语表
- [x] T03: 创建标准族谱图
- [x] T04: 编写核心对齐矩阵

**交付物**:

- `alignment-matrix.md`
- `master-alignment-matrix.md`（99-reference）

---

## Phase 2: 深度映射（2026-06 第二周）— 已完成

**任务**:

- [x] T05: 编写 TOGAF 10 ABB/SBB 与 ISO 42010 的详细映射
  - 交付: `02-togaf-10-alignment/detailed-mapping.md`（覆盖 10 个 ADM 阶段）
- [x] T06: 编写 ArchiMate 3.2/4.0 元素与 ISO 42010 的对照表
  - 交付: `04-archimate-4/archimate-iso-mapping.md`（四层全覆盖）
- [x] T07: 编写 ISO 26550:2015 与 ISO 42010/42020 的交叉映射
  - 交付: `03-iso-26550-ple/ple-iso-integration.md`（双轨映射）
- [x] T08: 编写 SWEBOK V4 知识领域与本体系的对应关系
  - 交付: `05-swebok-v4/swebok-alignment.md`（15 个 KAs 全覆盖）

**交付物**:

- `02-togaf-10-alignment/detailed-mapping.md`
- `04-archimate-4/archimate-iso-mapping.md`
- `03-iso-26550-ple/ple-iso-integration.md`
- `05-swebok-v4/swebok-alignment.md`

---

## Phase 3: 形式化公理体系（2026-06 第三周）

**任务**:

- [x] T09: 完善元公理、存在性公理、结构性公理、过程性公理
- [x] T10: 推导 15+ 定理并给出证明概要
- [x] T11: 建立公理-定理之间的依赖关系图
- [x] T12: 识别各公理的可证伪条件

**交付物**:

- `06-formal-axioms/axiom-system.md` — 15 条公理，含形式化表述、可证伪条件
- `06-formal-axioms/theorem-derivations.md` — 17 条定理，含证明概要、应用示例
- `06-formal-axioms/dependency-graph.md` — Mermaid 图、邻接表、关键路径与脆弱性分析
- `06-formal-axioms/critique-and-boundaries.md` — 每条公理的反例、边界、反模式映射、体系局限性
- `99-reference/glossary/axiom-theorem-tree.md` — 已同步更新

---

## Phase 4: 可视化与工具（2026-06 第四周）— 部分完成

**已完成**:

- [x] T13: 制作标准族谱 Mermaid 图 → `99-reference/visualizations/standard-family-tree.mmd`
- [x] T14: 制作概念映射 Mermaid 图 → `99-reference/visualizations/concept-mapping.mmd`
- [x] T16: 更新术语交叉对照 → `99-reference/terminology-crosswalk/terminology-crosswalk.md`

**待完成**:

- [ ] T15: 开发术语查询脚本（支持跨标准术语翻译）

**交付物**:

- `99-reference/visualizations/standard-family-tree.mmd`
- `99-reference/visualizations/concept-mapping.mmd`
- `99-reference/glossary/terminology-crosswalk.md`

---

## 依赖关系

```
T01-T04 (已完成)
    ↓
T05-T08 (深度映射)
    ↓
T09-T12 (形式化公理)
    ↓
T13-T16 (可视化与工具)
```

---

> 最后更新: 2026-06-06
