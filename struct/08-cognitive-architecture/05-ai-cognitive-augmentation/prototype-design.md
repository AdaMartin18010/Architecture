# AI 辅助复用决策系统：原型设计

> **定位**：将 AI/LLM 作为架构复用决策的**认知增强层**，而非替代人类判断，实现“推荐 → 解释 → 验证 → 反馈”的闭环。
> **对齐**：ISO/IEC 26566:2026（复用成熟度）、FAIR4RS（可发现/可访问/可互操作/可重用）、MCP 2025-11-25（工具调用协议）。

---

## 1. 问题陈述

架构复用决策面临的信息困境：

| 困境 | 表现 |
|------|------|
| **发现难** | 已有组件散落在 Git、Artifactory、内部 Wiki，检索靠记忆。 |
| **评估难** | 候选组件的质量、安全态势、维护状态、接口稳定性难以量化。 |
| **适配难** | 找到组件后，集成成本、接口映射、依赖冲突需要大量人工分析。 |
| **信任难** | 决策者担心组件黑箱行为、供应链风险、长期维护承诺。 |

AI 辅助复用决策系统旨在**将上述信息密集型任务自动化**，同时把最终决策权保留给人类架构师。

---

## 2. 系统愿景

```
┌─────────────────────────────────────────────────────────────┐
│                    AI-Assisted Reuse Decision System        │
├─────────────────────────────────────────────────────────────┤
│  输入层：需求描述 + 约束条件 + 组织上下文                    │
├─────────────────────────────────────────────────────────────┤
│  检索层：向量检索（组件目录）+ 图检索（依赖/调用链）         │
├─────────────────────────────────────────────────────────────┤
│  评估层：多候选评分（技术、经济、风险、战略）                │
├─────────────────────────────────────────────────────────────┤
│  生成层：适配方案草稿 + 接口映射建议 + 集成代码片段          │
├─────────────────────────────────────────────────────────────┤
│  验证层：Conformal Prediction 过滤 + 形式化契约检查          │
├─────────────────────────────────────────────────────────────┤
│  决策层：可解释推荐 + 人类确认 + 反馈回路                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 架构设计

### 3.1 组件清单

| 模块 | 职责 | 技术选型 |
|------|------|----------|
| **Reuse Catalog** | 组件元数据存储 | PostgreSQL + pgvector |
| **Embedding Pipeline** | 文档/代码向量化 | Sentence-Transformers / CodeBERT |
| **Retrieval Engine** | 语义 + 结构化混合检索 | Dense + Sparse + GraphRAG |
| **Scoring Engine** | 多维度候选评分 | 规则 + 轻量 ML |
| **Generation Engine** | 适配方案与代码生成 | LLM（本地/云端） via MCP |
| **Verification Filter** | 统计保证与形式化校验 | Conformal Prediction + Alloy/TLA+ |
| **Decision UI** | 人机交互界面 | Streamlit / React |
| **Feedback Loop** | 决策结果追踪与模型改进 | 事件日志 + 在线学习 |

### 3.2 数据流

```
用户 query
   │
   ▼
[Query Parser] ──► 结构化需求（功能、NFR、约束）
   │
   ▼
[Retriever] ──► Top-K 候选组件（语义相似 + 依赖兼容）
   │
   ▼
[Scorer] ──► 候选排序（RAG 上下文注入 LLM）
   │
   ▼
[Generator] ──► 适配方案 draft + 集成代码
   │
[Verification Filter] ──► 仅保留通过 CP/formal 检查的方案
   │
   ▼
[Decision UI] ──► 可解释推荐 → 人类确认/修改/拒绝
   │
   ▼
[Feedback Loop] ──► 记录实际结果，优化检索与评分模型
```

---

## 4. 关键技术决策

### 4.1 检索：语义 + 结构化 + 图

- **语义检索**：用 CodeBERT / CodeT5+ 对 README、API 文档、代码片段生成 embedding。
- **结构化过滤**：按组织、领域、技术栈、许可证、SLSA 等级预过滤。
- **图增强**：将组件调用关系、依赖图构建为知识图谱，通过 GraphRAG 回答“哪些服务已经在用某组件”这类问题。

### 4.2 评分：多目标决策模型

对每个候选组件输出五维评分（1–5）：

| 维度 | 权重 | 数据来源 |
|------|------|----------|
| **功能匹配度** | 0.30 | 语义相似度 + LLM 判断 |
| **技术质量** | 0.25 | 测试覆盖率、Kani/Miri/Clippy 状态、SBOM |
| **经济价值** | 0.20 | COCOMO / 成本节省估算（复用 vs 自研） |
| **风险等级** | 0.15 | CVE、许可证冲突、供应链 SLSA 等级 |
| **战略契合** | 0.10 | 与组织技术雷达、架构原则的对齐度 |

### 4.3 生成：受控代码生成

- 使用 **MCP (Model Context Protocol)** 调用外部工具：
  - `search_catalog(query)`
  - `get_component_metadata(id)`
  - `compare_interfaces(a, b)`
  - `generate_adapter(a, b)`
  - `run_conformal_filter(candidates)`
- 所有 LLM 输出均通过 **Conformal Prediction 校准工具** 进行置信度过滤（见 `calibration-tool.py`）。
- 高风险方案自动触发形式化验证器（Alloy/TLA+/Kani）进行检查。

### 4.4 验证：统计 + 形式化双层过滤

```
LLM 生成候选适配方案
        │
        ▼
[Conformal Prediction 层]
   仅保留 P(correctness) ≥ 1-α 的候选
        │
        ▼
[Formal Verification 层]（可选）
   对关键不变量调用 Kani / Alloy / TLA+
        │
        ▼
[人类评审]
```

这一模式被称为 **Vericoding**：AI 生成 + 形式化验证。

---

## 5. 交互设计

### 5.1 查询示例

```text
用户：
"我需要一个支持 JWT RS256 验证的身份认证组件，
 要兼容 Java 17 和 Spring Boot 3.2，
 必须已通过 SLSA Build Level 3，
 偏好内部团队维护的组件。"

系统：
1. 解析出功能需求：JWT RS256 验证
2. 过滤：Java、Spring Boot 3.2、SLSA ≥ L3、internal
3. 检索 Top-5 候选
4. 生成对比表（功能、性能、安全、成本、维护者）
5. 对每个候选给出复用建议：推荐 / 有条件使用 / 不推荐
6. 对推荐候选生成 `pom.xml` 片段与配置示例
7. 输出 Conformal Prediction 置信度：α=0.10，选中 4/5 候选
```

### 5.2 决策输出格式

```json
{
  "query_id": "req-2026-0606-001",
  "candidates": [
    {
      "component_id": "auth-jwt-rs256",
      "score": 4.6,
      "recommendation": "RECOMMENDED",
      "confidence": 0.94,
      "rationale": [
        "功能匹配度 4.8/5：完整支持 RS256 + JWKS",
        "技术质量 4.5/5：测试覆盖率 87%，Kani 验证 3 个核心 harness",
        "经济价值 4.7/5：预计节省 42 人天",
        "风险等级 4.2/5：无 CVE，Apache-2.0 许可证",
        "战略契合 5.0/5：在组织技术雷达的 Adopt 象限"
      ],
      "adapter_snippet": "...",
      "warnings": []
    }
  ],
  "fallback": "若候选不可用，建议自研并贡献回内部目录。"
}
```

---

## 6. 与项目现有工具的集成

| 现有工具 | 集成方式 |
|----------|----------|
| `terminology-query.py` | 解析用户需求中的领域术语，标准化查询。 |
| `cocomo-calculator.py` | 估算复用 vs 自研的经济价值。 |
| `calibration-tool.py` | 对 LLM 生成的候选方案进行统计置信度过滤。 |
| `assessment-tool.py` | 评估组织复用成熟度，决定 AI 辅助深度。 |
| `verify-all.sh` | 对高风险候选触发 TLA+/Alloy/Coq 检查。 |

---

## 7. 实现路线图

### Phase A：MVP（0–4 周）

- 接入内部组件目录（Backstage / Artifactory / Git）。
- 实现基于向量的语义检索。
- 构建 Streamlit 演示界面。

### Phase B：增强（1–3 个月）

- 引入 GraphRAG 依赖图检索。
- 集成 `calibration-tool.py` 进行候选过滤。
- 接入 MCP 工具协议。

### Phase C：生产化（3–6 个月）

- 与人类评审闭环，收集反馈优化评分模型。
- 对关键路径组件触发 Kani / Alloy 自动验证。
- 建立审计日志与可解释性报告。

---

## 8. 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| LLM 幻觉推荐不存在的组件 | 检索结果必须来自受控目录，LLM 仅做摘要与比较。 |
| 生成代码引入漏洞 | 所有代码通过 SAST + Conformal Prediction 过滤 + 可选形式化验证。 |
| 评分偏见 | 公开评分公式与权重，允许用户调整组织偏好。 |
| 知识产权风险 | 集成许可证扫描，自动标记 copyleft / 冲突许可证。 |
| 决策责任不清 | 明确“AI 推荐，人类决策”，所有推荐附带可追溯依据。 |

---

## 9. 参考

- MCP 2025-11-25 规范: <https://modelcontextprotocol.io/>
- FAIR4RS Principles v1.0
- ISO/IEC 26566:2026 Reuse Maturity
- AutoVerus / AlphaVerus / Verina 论文（AI + 形式化验证）
- GraphRAG: <https://microsoft.github.io/graphrag/>

---

*文档生成时间：2026-06-06 · Phase 2 认知架构增强设计*
