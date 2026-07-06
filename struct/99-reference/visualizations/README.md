# 架构复用知识体系可视化图库

> **版本**: 2026-06-10 | **生成工具**: Mermaid CLI (`mmdc`) | **格式**: SVG (透明背景)

## 图库总览

本目录包含 13 个一级主题的全部架构可视化图，覆盖业务架构到前沿趋势的完整知识域。

| # | 主题 | Mermaid 源文件 | SVG 渲染图 | 大小 | 子图数 |
|---|------|---------------|-----------|------|--------|
| 02 | 业务架构复用 | `02-business-architecture-reuse.mmd` | `02-business-architecture-reuse.svg` | 40 KB | 4 |
| 03 | 应用架构复用 | `03-application-architecture-reuse.mmd` | `03-application-architecture-reuse.svg` | 49 KB | 4 |
| 04 | 组件架构复用 | `04-component-architecture-reuse.mmd` | `04-component-architecture-reuse.svg` | 42 KB | 4 |
| 05 | 功能架构复用 | `05-functional-architecture-reuse.mmd` | `05-functional-architecture-reuse.svg` | 43 KB | 4 |
| 06 | 跨层复用治理 | `06-cross-layer-governance.mmd` | `06-cross-layer-governance.svg` | 39 KB | 4 |
| 07 | 形式化验证 (T18b) | `07-formal-verification.mmd` | `07-formal-verification.svg` | 45 KB | 4 |
| 08 | 认知架构 | `08-cognitive-architecture.mmd` | `08-cognitive-architecture.svg` | 41 KB | 4 |
| 09 | 价值量化 | `09-value-quantification.mmd` | `09-value-quantification.svg` | 35 KB | 4 |
| 10 | 供应链安全 | `10-supply-chain-security.mmd` | `10-supply-chain-security.svg` | 38 KB | 4 |
| 11 | 工业 IoT/OT-IT | `11-industrial-iot-otit.mmd` | `11-industrial-iot-otit.svg` | 46 KB | 5 |
| 12 | AI 原生复用 | `12-ai-native-reuse.mmd` | `12-ai-native-reuse.svg` | 44 KB | 5 |
| 13 | 前沿趋势 | `13-emerging-trends.mmd` | `13-emerging-trends.svg` | 38 KB | 5 |

## 跨主题综合图

| 图名 | 描述 | 文件 |
|------|------|------|
| 公理-定理全图 | 20 公理 + 35 定理 + 5 猜想的完整推导网络 | `axiom-theorem-full-graph.mmd` |
| 概念映射图 | 核心概念间的语义关联 | `concept-mapping.mmd` |
| 标准族谱树 | 30 个标准的层次与依赖关系 | `standard-family-tree.mmd` |

## 按主题子目录索引

部分主题因内容纵深，在子目录中维护独立的可视化源文件，统一在此索引以便引用。

| 主题 | 子图名 | Mermaid 源文件 | Graphviz 源文件 | 位置 |
|------|--------|---------------|-----------------|------|
| 10 供应链安全 | 供应链攻击树 | `10-supply-chain-security/03-attack-vectors/attack-tree.mmd` | `10-supply-chain-security/03-attack-vectors/attack-tree.dot` | `struct/10-supply-chain-security/03-attack-vectors/` |

> 说明: 该攻击树基于 `attack-tree.md` 的 7 大攻击路径绘制，区分 OR/AND/叶节点并按风险等级着色。可使用 `attack-tree-interactive.py --format mermaid|graphviz` 重新生成。

## 使用方式

### 嵌入 Markdown 文档

```markdown
![业务架构复用](02-business-architecture-reuse.svg)
```

### 嵌入 HTML/PDF

直接引用 `.svg` 文件，矢量无损缩放。

### 修改与重渲染

```bash
cd struct/99-reference/visualizations
# 修改 .mmd 源文件后
mmdc -i <主题>.mmd -o <主题>.svg -b transparent
```

### 批量重渲染全部

```bash
for f in *.mmd; do
  mmdc -i "$f" -o "${f%.mmd}.svg" -b transparent
done
```

## 设计规范

- **配色**: 每层/子图使用不同背景色区分
  - 🔵 蓝色系: 标准/协议层 (`#e3f2fd`)
  - 🟢 绿色系: 实现/运行时层 (`#e8f5e9`)
  - 🟠 橙色系: 决策/度量层 (`#fff3e0`)
  - 🟣 紫色系: AI/前沿层 (`#f3e5f5`)
  - 🔴 红色系: 安全/关键层 (`#fbe9e7` / `#c8e6c9`)
- **布局**: 水平流 (`LR`) 或垂直流 (`TB`)，根据内容密度选择
- **节点**: `key["label<br/>详细说明"]` 格式，支持换行
- **版本头**: 每个 `.mmd` 文件顶部注释标注版本与状态


---

## 补充说明：架构复用知识体系可视化图库

## 概念定义

**定义**：参考层是结构化知识体系的“地图”，汇总权威来源、术语表、标准索引、课程对标与审计报告，为各主题提供可追溯的引用与一致性校验。

## 示例

**示例**：维护 authoritative-sources.md 登记所有 ISO/IEC、IEEE、NIST、CNCF 来源 URL 与核查日期，确保全书引用可验证。

## 反例

**反例**：参考层链接长期不更新，术语表与正文定义冲突，读者无法确认内容准确性与时效性。

## 权威来源

> **权威来源**:
>
> - [ISO](https://www.iso.org)
> - [IEEE Standards](https://standards.ieee.org)
> - [NIST](https://www.nist.gov)
> - [CNCF](https://www.cncf.io)
> - 核查日期：2026-07-07
