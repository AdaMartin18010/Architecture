# 更新日志

> **版本**: 2026-06-08
> **定位**: 记录知识库的重大更新、勘误和权威来源对齐

---

## 2026-06-12 Phase A P0 权威来源对齐修复

> **触发原因**: 经与国际权威来源（ISO、The Open Group、NIST、IEC）交叉复核，发现项目中对部分标准版本/状态的描述存在事实性错误，集中修复以恢复知识库权威性。

### 已修正的标准状态

| 标准 | 原表述 | 修正后 | 权威来源 |
|------|--------|--------|----------|
| **ISO/IEC 25010** | 2024 版已发布 | **2023** 版为正式版 | ISO 78175 |
| **ArchiMate 4.0** | 厂商预发布/未获官方确认 | **已正式发布（2026-04-27）** | The Open Group 新闻稿 |
| **ISO/IEC/IEEE 12207** | 仍在制定中 | **已发布（2026-04-29）** | ISO 90219 |
| **ISO/IEC 30141** | 被误审为“不存在 2024 版” | **已发布（2024-08）**，确认存在 | ISO 88800 |
| **NIST SSDF 1.2** | 正式版 | **Initial Public Draft（征求意见稿）** | NIST CSRC |
| **ISO/IEC 26550** | 多处误写为 2023/2025 | **2015** 版为现行版 | ISO 69529 |
| **IEC 62443-4-2** | 误写为 2025 版 | **2019** 版为现行版 | IEC 67463 |
| **ISO/IEC 5338** | 制定中 | **2023** 版已发布 | ISO 81118 |
| **ISO/IEC 25040** | URL 指向 /standard/64768.html | 修正为 /standard/83467.html | ISO 83467 |
| **ISO/IEC/IEEE 42030 AWI** | URL 指向 /standard/82606.html | 区分现行版（73436）与 AWI 项目（93814） | ISO |

### 关键勘误说明

**ArchiMate 4.0 状态追溯（2026-06-12 最终结论）**

项目早期曾因 The Open Group 官网未即时更新，将 ArchiMate 4.0 标记为“厂商预发布”；随后又基于第三方信息误判为“已正式发布”，并在 2026-06-08 二次勘误中回退为“厂商预发布”。经最终复核 The Open Group 官方新闻稿（Document C260, April 2026），**ArchiMate 4 Specification 已于 2026-04-27 正式发布**，与 ArchiMate 3.2 向后兼容。2026-06-12 起，项目统一采用“已正式发布（2026-04-27）”作为权威表述，并在 view/ 历史文档中以三次勘误标记保留认知演进记录。

### 新增文件

- `struct/99-reference/standards-index/authoritative-sources-v2.md` — 全项目事实基准索引
- `struct/99-reference/tools/standards-version-audit.py` — 全项目标准编号一致性扫描脚本
- `struct/99-reference/tools/fix-p0-standards.py` — P0 事实修复批量替换脚本

### 主要修改文件

- `README.md` — 更新标准列表与勘误说明
- `view/software_architecture_reuse_framework_2026.md` — 回滚 ISO 25010 版本号、修正勘误说明
- `view/software_architecture_reuse_full_2026.md` — 回滚 ISO 25010 版本号、更新 ArchiMate 勘误
- `struct/99-reference/standards-index/master-alignment-matrix.md` — 更新 ArchiMate 4.0 状态
- `struct/13-emerging-trends/09-frontier-tracking/frontier-status-2026-06.md` — 更新 12207/26550/5338/62443/ArchiMate 状态与 URL
- `struct/10-supply-chain-security/06-case-studies/nist-ssdf-1-2-alignment.md` — 修正 SSDF 1.2 为征求意见稿

---

## 2026-06-08 Phase 4 安全与供应链纵深完成

### 供应链安全

- **SLSA 1.2 Multi-Track 深度解析**: `10/01-slsa-framework/slsa-1-2-multi-track.md` — Build/Source/Build Environment三轨道×L1-L3矩阵
- **SLSA L4 分布式构建验证**: `10/01-slsa-framework/slsa-l4-distributed-builds.md` — sigstore/cosign实践、多签名构建概念验证
- **供应链攻击树可视化**: `10/03-attack-vectors/attack-tree-interactive.py` — 5种攻击场景、纯Python生成单文件HTML、防御矩阵联动
- **NIST SSDF 1.2 对齐**: `10/06-case-studies/nist-ssdf-1-2-alignment.md` — 四大实践组映射、正式版变化追踪
- **EU CRA 合规工具**: `10/06-case-studies/eu-cra-checklist.py` — 20项检查清单(Annex I/II/III)、交互式评估、JSON/Markdown报告

### 元模型与标准对齐

- **IEEE 1517 复用过程映射**: `01/01-iso-420xx-family/ieee-1517-reuse-processes.md` — 三过程组(领域/应用/管理)、与12207/26550对照、30项检查清单

---

## 2026-06-08 Phase 3 垂直领域扩展完成

### 工业 IoT / OT-IT 融合

- **IEC 61508 PIU 贝叶斯统计验证工具**: `11/06-functional-safety/piu-bayesian-tool.py` — 支持单组件/多站点池化分析、Gamma-Poisson共轭模型、威布尔过程扩展
- **ISO 26262 SEooC 复用流程模板**: `11/06-functional-safety/iso26262-seooc-template.md` — 含三阶段流程、安全手册模板、20项集成检查清单、SEooC vs PIU对比
- **工业边缘 AI 模型部署规范**: `11/07-edge-ai/model-deployment-spec.md` — 五阶段部署框架、TFLite/ONNX Runtime/TensorRT/TVM对比、功能安全约束
- **MCP for Industrial AI 协议草案**: `11/07-edge-ai/mcp-industrial-ai-draft.md` — Tools/Resources/Prompts工业适配、OPC UA FX映射、IEC 62443安全扩展
- **AAS-OPC UA NodeSet 完整映射规范**: `11/05-digital-twin-aas/aas-opcua-mapping.md` — 11项映射表、JSON/XML示例、生命周期同步规则

### 元模型与标准对齐

- **FAIR4RS 原则与软件复用对照**: `01/08-fair4rs/fair4rs-alignment.md` — 4×4架构映射矩阵、40项检查清单(0-3分评分)、与ISO 25010/OMG RAS/IEEE 1517对照

---

## 2026-06-08 Phase 2 形式化与量化深化完成

### 新增内容

- **03 应用架构基础填充**: 分层架构 / 微服务 / Serverless / 事件驱动 四个子目录核心文档
- **01 元模型标准对齐**: ISO/IEC 25010:2023 AI质量特性影响矩阵、OMG RAS v2.2 对齐章节
- **07 形式化验证内容梳理**: Coq/Isabelle定理证明纲要、Alloy ISA-95约束、Rust工具链概念说明
- **09 价值量化工具**: COCOMO II 2026计算器 (Python CLI)
- **06 跨层治理工具**: FinOps成本分摊模板 + Excel导出脚本、复用成熟度评估问卷CLI
- **08 认知架构**: AI辅助复用决策系统原型设计
- **12 AI原生工具**: AI功能概率契约校准工具 (Python CLI)
- **99 参考工具**: 术语查询脚本 (Python CLI)

### 可执行工具交付

| 工具 | 路径 | 功能 |
|------|------|------|
| COCOMO II 2026 计算器 | `09-value-quantification/tools/cocomo-calculator.py` | 成本估算、ROI计算 |
| FinOps Excel 导出器 | `06-cross-layer-governance/04-finops-cost/templates/finops-exporter.py` | 四级成本分摊、Excel导出 |
| 成熟度评估问卷 | `06-cross-layer-governance/03-maturity-models/reuse-maturity-assessment-cli.py` | 25题评估、雷达图报告 |
| AI概率契约校准 | `12-ai-native-reuse/05-probabilistic-contracts/calibration-tool.py` | Conformal Prediction校准、漂移检测 |
| 术语查询 | `99-reference/tools/terminology-query.py` | 34术语跨标准检索 |

---

## 2026-06-08 HOTFIX-4：ISO/IEC 25010:2023 → 2024 统一更新

> **勘误原因**：ISO/IEC 25010:2023 已于 2024 年发布，取代 2011 版，新增 AI/ML 系统质量特性考量。项目中此前多处引用 "25010:2023" 系版本号滞后。

**已更新文件**：

- `struct/01-meta-model-standards/01-iso-420xx-family/alignment-matrix.md` — 25010:2023 → 25010:2023
- `struct/01-meta-model-standards/01-iso-420xx-family/iso-25010-2023-update.md` — 文件名与内容全部更新（原 `iso-25010-2023-update.md`）
- `struct/01-meta-model-standards/README.md` — 版本号更新
- `struct/99-reference/CHANGELOG.md` — 添加本条目
- `struct/99-reference/audit/comprehensive-gap-analysis-2026-06-08.md` — 更新相关引用，标注 HOTFIX-4 已完成
- `struct/99-reference/external-links/authoritative-sources.md` — 链接与版本号更新（<https://www.iso.org/standard/78175.html>）
- `struct/99-reference/glossary/cross-topic-index.md` — 索引更新
- `struct/99-reference/standards-index/master-alignment-matrix.md` — 矩阵更新
- `struct/99-reference/templates/checklist-template.md` — 对照标准更新
- `struct/99-reference/tools/terminology-query.py` — 术语库键名更新
- `struct/99-reference/visualizations/standard-family-tree.mmd` — 节点标签更新
- `struct/MASTER_PLAN_2026_NETWORK_ALIGNED.md` — 对齐来源更新
- `struct/README.md` — 标准索引更新
- `struct/SUBSEQUENT_PLAN_2026.md` — 差距分析引用更新
- `view/software_architecture_reuse_framework_2026.md` — 添加头部勘误说明，正文保留历史记录
- `view/software_architecture_reuse_full_2026.md` — 添加头部勘误说明，正文保留历史记录
- `README.md`（项目根）— 标准列表更新

**修正原则**：

- 所有 "25010:2023" 统一替换为 "25010:2023"
- `iso-25010-2023-update.md` 更名为 `iso-25010-2023-update.md`，文件内版本号全部更新，保留历史演进说明
- view/ 历史文档添加勘误头部，正文保留早期认知记录价值

---

## 2026-06-06 Phase 2 前沿标准纠偏 + A2A+MCP PoC 增强

### ArchiMate 4.0 官方发布纠偏

> **关键纠正**：The Open Group 已于 **2026-04-27 正式发布 ArchiMate 4 Specification**。此前项目中将 "ArchiMate 4.0" 标注为"厂商预告/未获官方确认"属于**过渡期间的保守误判**，现全面纠正。

**已更新文件**：

- `struct/01-meta-model-standards/04-archimate-4/archimate-iso-mapping.md` — 标题改为 "ArchiMate 3.2/4.0"，移除勘误警告，更新参考来源为官方发布链接
- `struct/01-meta-model-standards/01-iso-420xx-family/iso-42024-42042-dis-alignment.md` — 状态表更新：ArchiMate 4.0 标记为"已发布（2026-04-27）"，ArchiMate 3.2 标记为"仍有效，向后兼容"
- `struct/01-meta-model-standards/README.md` — 描述更新为 "ArchiMate 4.0（2026-04-27 官方发布）"
- `struct/01-meta-model-standards/02-togaf-10-alignment/detailed-mapping.md` — 移除"未获官方确认"注释
- `struct/01-meta-model-standards/05-swebok-v4/swebok-alignment.md` — 两处引用更新
- `struct/07-formal-verification/02-alloy/cross-layer-mapping.md` — 更新为"ArchiMate 4.0（2026-04-27 官方发布）"
- `struct/99-reference/chapters/ch02.md` — 两处引用更新
- `struct/99-reference/book-outline.md` — 核心贡献与核心论点中的引用更新
- `struct/99-reference/standards-index/master-alignment-matrix.md` — 状态表更新
- `struct/SUBSEQUENT_PLAN_2026.md` — blocker 状态改为 "✅ 已完成"

## 2026-06-08 重大勘误：ArchiMate 4.0 发布声明撤回

> **勘误原因**：经网络核查，The Open Group 官方网站在 2026-06-08 仍显示 ArchiMate 最新版本为 3.1，无 ArchiMate 4.0 正式发布信息。此前项目将厂商预发布/第三方声明误判为官方正式发布。

> **2026-06-12 更新**：The Open Group 已于 **2026-04-27 正式发布 ArchiMate 4 Specification**（Document C260, April 2026），官方新闻稿确认。项目已据此更新为正式发布状态。

**已勘误文件**（将"已正式发布"声明回退为"厂商预发布"）：

- `struct/01-meta-model-standards/README.md`
- `struct/01-meta-model-standards/04-archimate-4/archimate-iso-mapping.md`
- `struct/99-reference/book-outline.md`
- `struct/SUBSEQUENT_PLAN_2026.md`
- `struct/01-meta-model-standards/01-iso-420xx-family/iso-42024-42042-dis-alignment.md`
- `struct/01-meta-model-standards/02-togaf-10-alignment/detailed-mapping.md`
- `struct/01-meta-model-standards/05-swebok-v4/swebok-alignment.md`
- `struct/07-formal-verification/02-alloy/cross-layer-mapping.md`
- `struct/99-reference/standards-index/master-alignment-matrix.md`
- `view/software_architecture_reuse_full_2026.md`
- `view/software_architecture_reuse_extension_2026.md`
- 以及本项目其他引用 ArchiMate 4.0 的文件

**修正原则**：

- struct/ 文件：直接修正声明，标注为"厂商预发布/未获官方确认"
- view/ 文件：添加头部勘误说明，正文保留历史记录价值

### ISO 26262 / IEC 61508 状态更新

**已更新文件**：

- `struct/11-industrial-iot-otit/06-functional-safety/iec-61508/iec-61508-ed3-reuse.md` — 对齐来源更新为 "IEC 61508 Ed.3 (CDV 投票已完成 2026-01-28，预计 2026 末正式发布)"
- `struct/11-industrial-iot-otit/06-functional-safety/iso-26262/iso-26262-seooc-reuse.md` — 对齐来源更新为 "ISO 26262:2018 (当前版); 第三版新工作项已注册 (2026 初)，目标发布 ~2029"；"ISO 26262:2025 关键更新"章节重命名为 "ISO 26262 第三版 (Ed.3) 预期方向"并添加重要说明
- `struct/11-industrial-iot-otit/06-functional-safety/iec-61508-iso-26262-sotif-alignment.md` — 警告更新为"不存在 ISO 26262:2025 官方版本"
- `struct/11-industrial-iot-otit/07-edge-ai/tinyml-onnx-edge-ai.md` — "ISO 26262:2025 对 ML 的要求"更新为 "ISO 26262 第三版 (Ed.3) 对 ML 的预期要求"
- `struct/99-reference/standards-index/master-alignment-matrix.md` — ISO 26262 / IEC 61508 状态行更新

### view/ 目录 ArchiMate 4.0 批量替换（历史文档勘误更新）

**处理原则**：view/ 为历史文档（约 31 万字），保留正文历史记录价值，重点更新头部勘误说明和明确的错误断言。

**已更新文件**：

- `view/software_architecture_reuse_full_2026.md` — 9 处修改：
  - 对齐标准列表：`ArchiMate 3.2` → `ArchiMate 4.0 (2026-04-27 正式发布, 与 3.2 向后兼容)`
  - 勘误说明：将 "未获官方确认/厂商预告" 更正为 "【已纠正】The Open Group 已于 2026-04-27 正式发布"
  - 目录与章节标题：`ArchiMate Next (2026 Q2)` → `ArchiMate 4.0`
  - 表格内容："Dynamic Connection" → "Path / Realization"；"2026 Q2 预期发布" → "2026-04-27 正式发布"
  - 标准滞后性说明：划线更正为 "ArchiMate 4.0 已于 2026-04-27 正式发布"
  - Mermaid 图：节点标签同步更新
- `view/software_architecture_reuse_extension_2026.md` — 2 处修改：对齐标准列表 + 勘误说明更新
- `view/software_architecture_reuse_framework_2026.md` — 1 处修改：`ArchiMate 3.2/Next` → `ArchiMate 3.2/4.0`

### A2A + MCP PoC 增强（真实 MCP SDK 集成 + 端到端验证）

**更新文件**：

- `struct/12-ai-native-reuse/04-hybrid-a2a-mcp-poc/hybrid_agent_server.py` — 全面升级：
  - 新增 `RealMCPClient` 类：基于 `mcp.ClientSession` + `stdio_client` 连接外部 MCP Server
  - 新增 `MCPToolManager` 类：自动管理真实 Client / Mock fallback 切换
  - 启动时通过 `MCP_SERVER_COMMAND` 环境变量自动连接真实 MCP Server（超时 15s，失败降级）
  - 新增 `GET /mcp/tools` 端点：列出当前可用的 MCP 工具（含 mode 标识）
  - 当连接真实 MCP Server 时，支持基于关键词模糊匹配所有可用工具
  - 根端点返回 `mcp_mode` 和 `mcp_sdk_available` 状态
  - 保留全部原有 A2A 端点（Agent Card、tasks/send、tasks/get、tasks/sendSubscribe）
  - `process_task` 修复：search 前缀匹配改为大小写不敏感；真实 MCP 返回的纯文本结果直接透传，不再强制 JSON 解析

**新增测试文件**：

- `struct/12-ai-native-reuse/04-hybrid-a2a-mcp-poc/test_mcp_server.py` — 基于 `mcp.server.fastmcp` 的测试 MCP Server，提供 `get_weather` / `calculator` / `search_docs` 三个工具
- `struct/12-ai-native-reuse/04-hybrid-a2a-mcp-poc/test_e2e.py` — 端到端自动化测试脚本（7 项断言）

**端到端验证结果**（7/7 通过 ✓）：

| 测试项 | 结果 |
|--------|------|
| Root endpoint / MCP mode | `real (3 tools)` ✓ |
| Agent Card discovery | 3 skills ✓ |
| MCP Tool Discovery | get_weather / calculator / search_docs ✓ |
| Weather Query → real MCP | "Weather in Shanghai: cloudy, 26°C. (Source: TestMCP)" ✓ |
| Calculator → real MCP | "Result of '15 * 23 + 7' = 352 (Source: TestMCP)" ✓ |
| Document Search → real MCP | "Found 1 document(s) for 'reusable': - Reusable Component Patterns v2.1" ✓ |
| Unknown Intent Fallback | 友好提示 ✓ |

---

## 2026-06-06 Phase 1.5 修复（用户确认 1A/2A/3A/4A/5A 后执行）

### 修复内容

#### 目录结构与一致性

- 重写 `struct/README.md` — 以实际 `struct/` 目录结构为准，明确标注与早期 MASTER_PLAN 规划树的差异
- 清理 `.vscode/README.md` — 删除约 200 行 PostgreSQL 18+ 残留内容，恢复为 VSCode/Cursor 配置说明
- 更新 `struct/MASTER_PLAN.md` — 修正 FinOps 实际路径、MCP 版本引用（2025-11-25）、SLSA 版本引用（1.1/1.2），添加 `SUBSEQUENT_PLAN_2026.md` 链接和关键决策确认
- 更新 `struct/99-reference/audit/roadmap-consistency-audit.md` — 追加修复记录

#### 形式化验证环境

- 创建 `struct/99-reference/tools/formal-verification-env/`:
  - `README.md` — 环境使用说明
  - `docker-compose.yml` — TLA+/Alloy/Coq/Isabelle 四容器配置
  - `verify-all.sh` — 批量检查脚本
- 创建 `struct/07-formal-verification/03-coq-isabelle/README.md` — Coq/Isabelle 占位与 Phase 2 计划
- 更新 `struct/07-formal-verification/README.md` — 添加验证环境引用和验收标准
- 更新 `struct/07-formal-verification/plans-tasks/roadmap.md` — 修正目录结构声明，移除不存在的 `07-model-checking`

### 关键决策

- **1A**: 目录结构以实际文件为准
- **2A**: Docker 化形式化验证环境，新增规约必须自动验证
- **3A**: 可执行工具采用 Python CLI + Streamlit
- **4A**: 重点补齐 CP+形式化、WASI 0.3、Agentic Governance；暂缓量子计算
- **5A**: 每篇文档列出 1-3 个国际权威来源 URL

---

## Phase 2 持续推进（2026-06）— 国际权威内容对齐

### 新增标准对齐文档

#### 元模型与标准对齐

- `07-omg-ras/ras-alignment.md` — 对齐 OMG RAS v2.2（formal/05-11-02），覆盖 Core RAS 四元组（Classification/Solution/Usage/RelatedAssets）、Profile 扩展、`.ras` 包格式、仓库服务接口，以及与 ISO 42010 / TOGAF 的映射
- `08-fair4rs/fair4rs-alignment.md` — 对齐 FAIR4RS Principles v1.0 (RDA, 2022)，覆盖 F/A/I/R 17 条子原则、与 SBOM/MCP/容器注册表的整合、架构资产 FAIR4RS 合规行动清单
- `01-iso-420xx-family/ieee-1517-reuse-processes.md` — 对齐 IEEE 1517-2010 软件生命周期复用过程，映射 Domain Engineering / Reuse Asset Management / Reuse Program Management 与 ISO 12207 / 42020 / TOGAF ADM

#### AI 原生复用

- `01-mcp-protocol/mcp-2025-11-25-deep-dive.md` — **关键勘误**：将项目中所有 "MCP 2026-07-28 RC" 引用更新为官方当前稳定版 **MCP 2025-11-25**。深度解析 Tasks、Icons、Sampling with Tools、Elicitation URL 模式、OAuth 企业级增强、Linux Foundation Agentic AI Foundation 治理变化

### 新增可执行工具原型

- `99-reference/tools/terminology-query.py` — 跨标准术语查询 CLI（ISO 42010 / ISO 25010 / TOGAF / SLSA / MCP / A2A）
- `99-reference/tools/cocomo-calculator.py` — COCOMO II 复用模型 2026 版计算器
- `12-ai-native-reuse/05-probabilistic-contracts/calibration-tool.py` — 基于 **Conformal Prediction** 的 AI 功能概率契约校准工具，输出 P(correctness) ≥ 1-α 的统计保证
- `06-cross-layer-governance/03-maturity-models/assessment-tool.py` — 基于 **ISO/IEC 26566:2026 / RCMM / RiSE / NASA RRL** 的复用成熟度评估问卷 CLI，生成分维度雷达图和总体成熟度报告

### 更新的 README/状态

- `struct/01-meta-model-standards/README.md` — 新增 OMG RAS、FAIR4RS、IEEE 1517 内容
- `struct/12-ai-native-reuse/README.md` — 修正 MCP 版本为 2025-11-25，添加 calibration-tool 状态
- `struct/05-functional-architecture-reuse/README.md` — 修正 MCP 版本引用
- `struct/06-cross-layer-governance/README.md` — 标记成熟度评估问卷 CLI 已完成

### 对齐的权威来源

- OMG RAS v2.2 formal/05-11-02: <https://www.omg.org/spec/RAS/2.2/PDF>
- FAIR4RS v1.0 (RDA, 2022): <https://doi.org/10.15497/RDA00068>
- IEEE 1517-2010: <https://standards.ieee.org/standard/1517-2010.html>
- MCP 2025-11-25 Spec: <https://modelcontextprotocol.io/specification/2025-11-25>
- MCP Linux Foundation Governance: <https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation>
- Angelopoulos & Bates, "A Gentle Introduction to Conformal Prediction" (2021): <https://arxiv.org/abs/2107.07511>
- ISO/IEC 26566:2026: <https://www.iso.org/standard/81437.html>

---

## 2026-06-06 本轮更新

### 新增文档

#### 元模型与标准对齐

- `iso-42010-2022-update.md` — 对齐 ISO 42010:2022 第二版关键变更（EoI、ADF、View Component、Aspect、Perspective）
- `iso-25010-2023-update.md` — 对齐 ISO 25010:2023 九大质量特性（勘误：此前误写为 2023 版，已统一更正）

#### 供应链安全

- `slsa-1-1-1-2-update.md` — 对齐 SLSA 1.1/1.2 多轨道模型（Build/Source/Attested Build Environments）
- `nist-ssdf-1-2-alignment.md` — 对齐 NIST SSDF 1.2 征求意见稿
- `eu-cra-compliance.md` — 对齐欧盟网络弹性法案（EU CRA）

#### 工业 IoT

- `iec-63278-roadmap.md` — 对齐 IEC 63278 AAS 系列标准路线图
- `iec-ieee-60802-profile.md` — 对齐 IEC/IEEE 60802 TSN 工业自动化配置文件
- `plcopen-motion-control.md` — 对齐 PLCopen Motion Control Part 1–4 + Safety，状态机与功能块复用
- `iec-61508-ed3-reuse.md` — 对齐 IEC 61508 功能安全与 Proven-In-Use 复用路径
- `iso-26262-seooc-reuse.md` — 对齐 ISO 26262 SEooC 与安全合同驱动的软件组件复用
- `tinyml-onnx-edge-ai.md` — 对齐 TinyML / Edge AI 模型复用技术栈

#### AI 原生复用

- `mcp-2025-11-25-authoritative.md` — 基于官方规范解读 MCP 2025-11-25
- `a2a-v1-authoritative.md` — 对齐 A2A v1.0 正式发布版本
- `owasp-llm-mcp-security.md` — 对齐 OWASP LLM/MCP/Agentic AI Top 10

#### 形式化验证

- `spark-ada-do333-industrial.md` — 对齐 SPARK Ada + DO-178C/DO-333 工业形式验证替代测试
- `event-b-railway-refinement.md` — 对齐 Event-B / B Method 铁路信号精化复用

#### 新兴趋势

- `platform-engineering-cncf-2026.md` — 对齐 CNCF 平台工程成熟度模型、Golden Path、IDP
- `wasm-component-model-2026.md` — 对齐 WebAssembly Component Model、WASI 0.3/1.0、wasmCloud
- `rust-wasm-formal-verification.md` — 对齐 Rust 类型系统、Kani/Miri、WASM 组件开发

#### 元模型与标准对齐

- `togaf-enterprise-continuum-reuse.md` — 对齐 TOGAF 10 企业连续体、ABB/SBB、架构仓库与 ISO 42010:2022 映射

#### 应用架构复用

- `nist-sp-800-204-microservices-security.md` — 对齐 NIST SP 800-204 系列微服务安全策略（五种代码类型、MS-SS 策略、DevSecOps）
- `gateway-api-gamma-2026.md` — 对齐 CNCF Gateway API / GAMMA、Istio Ambient Multicluster Beta、AI 推理扩展
- `eda-cqrs-event-sourcing-patterns.md` — 对齐 EDA/CQRS/Event Sourcing/Saga 模式与云原生实现栈
- `data-mesh-data-product-reuse.md` — 对齐 Data Mesh 四原则、数据产品、2026 IDP-for-data 合成模式

#### 业务架构复用

- `bpmn-dmn-reuse-orchestration.md` — 对齐 OMG BPMN 2.0.2 / DMN 1.5 业务过程与决策复用编排

#### 组件架构复用

- `open-source-supply-chain-reuse.md` — 对齐 NIST SP 800-161r1、OWASP SCVS、开源供应链治理与 SBOM 全生命周期

#### 功能架构复用

- `llm-function-reuse-patterns.md` — 对齐 LLM Function Calling、MCP Tool、A2A Agent Card、Microsoft Agent Framework

#### 跨层治理

- `finops-unit-economics-2026.md` — 对齐 FinOps 框架、单位经济学、Cloud COGS、AI 成本管理
- `reuse-maturity-models-rcmm-rise.md` — 对齐 RCMM、RiSE-RM、CMMI、Koltun-Hudson、Automotive SPICE 复用成熟度

#### 价值量化

- `cocomo-ii-reuse-model-deep-dive.md` — 对齐 COCOMO II 复用模型方程、AAM/SU/UNFM 参数、本地校准方法
- `roi-real-options-strategic-value.md` — 对齐软件复用 ROI、实物期权二项式-高斯模型、SaaS 估值倍数

#### 认知架构

- `act-r-cognitive-reuse.md` — 对齐 ACT-R 认知架构与知识复用机制
- `bdi-agent-reuse.md` — 对齐 BDI 智能体架构、计划库复用、MCP/A2A 语义映射

#### 工业 IoT/OT-IT

- `isa-95-asset-catalog-deep-dive.md` — ISA-95 五层资产目录、设备类型/属性/语义模型、OMAC PackML 集成、与 AAS 映射
- `aas-submodel-templates-full-catalog.md` — IDTA 子模型模板全清单（已发布+开发中）、DPP 映射、选择指南

#### 形式化验证

- `spark-ada-vs-rust-verification-matrix.md` — SPARK Ada 与 Rust 安全关键验证方法全面对比（安全属性、工具链、工业生态、决策矩阵）

#### 参考索引

- 更新 `terminology-crosswalk.md` — 增加版本对照表
- 更新 `authoritative-sources.md` — 增加最新权威链接
- 更新 `master-alignment-matrix.md` — 修正 MCP 版本，新增 PLCopen/FinOps/WASM/Gateway API/Data Mesh 等条目
- 新增 `cross-topic-index.md` — 跨主题综合索引与快速查找表
- 新增 `CHANGELOG.md` — 本更新日志

### 重要勘误

| 原内容 | 修正后 | 说明 |
|--------|--------|------|
| MCP 2026-07-28 RC（假设的未来修订） | MCP 2025-11-25 当前稳定版 | 官方规范仍为 stateful，2026-07-28 尚未正式发布 |
| A2A v1.0.0 2026-03-12 | A2A v1.0 2026-04 Cloud Next | 官方正式发布时间 |
| SLSA 1.0 单一等级模型 | SLSA 1.2 Multi-Track 模型 | Build/Source/Environment 三轨道 |
| ISO 42010 SoI / AF | ISO 42010 EoI / ADF | 2022 版新术语 |

### 权威来源

本轮更新主要对齐以下权威来源：

- ISO/IEC/IEEE 42010:2022 官方规范
- ISO/IEC 25010:2023 官方规范
- SLSA Specification v1.1 / v1.2 (slsa.dev)
- NIST SP 800-218r1 Initial Public Draft (2025-12-17)
- Regulation (EU) 2024/2847 (EU CRA)
- IEC 63278-1:2023 / IDTA-01001-3-0
- IEC/IEEE 60802 TSN Profile
- Model Context Protocol Specification 2025-11-25
- Google A2A Protocol v1.0 (Cloud Next 2026)
- OWASP Top 10 for LLM Applications 2025
- OWASP Top 10 for MCP 2025
- OWASP Top 10 for Agentic AI Applications 2026

---

### Phase 1 全面深化（本轮新增）

本轮更新按照 `MASTER_PLAN.md` Phase 1（2026-Q3）计划，对 7 条轨道进行了全面深化：

#### Track A: 01 元模型与标准对齐

- `02-togaf-10-alignment/detailed-mapping.md` — TOGAF 10 ABB/SBB 与 ISO 42010:2022 的详细映射（覆盖10个ADM阶段）
- `04-archimate-4/archimate-iso-mapping.md` — ArchiMate 3.2/4.0 元素与 ISO 42010:2022 的对照表（四层全覆盖）
- `03-iso-26550-ple/ple-iso-integration.md` — ISO 26550:2015 与 ISO 42010/42020 的交叉映射（双轨）
- `05-swebok-v4/swebok-alignment.md` — SWEBOK V4 知识领域与本体系 13 个主题的对应关系

#### Track B1: 02 业务架构复用

- `02-business-capability/fea-brm-togaf-mapping.md` — FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射
- `06-bpmn-dmn/bpmn-dmn-executable-cases.md` — BPMN 2.0 / DMN 1.5 可执行语义案例集（3个生产级案例）
- `case-studies/industry-vertical-cases.md` — 行业垂直场景案例库（金融开放银行、医疗 FHIR、制造 ISA-95）

#### Track B2: 03 应用架构复用

- `05-cloud-native-patterns/reusability-matrix-2026.md` — 云原生架构模式复用性矩阵 2026 版（9种模式 × 8维度）
- `06-service-mesh/service-mesh-communication-patterns.md` — 服务网格通信模式复用（Istio/Envoy/Cilium）

#### Track B3: 04 组件架构复用

- `07-language-ecosystems/comparison-matrix-2026.md` — 6大语言生态复用成熟度深度对比 2026
- `04-design-patterns/interface-design-patterns.md` — 设计模式与接口设计模式复用（跨语言对比 + 反模式）
- `07-language-ecosystems/open-source-supply-chain-reuse.md` — 依赖管理策略深度对比（PubGrub/MVS/SAT + 供应链安全）

#### Track B4: 05 功能架构复用

- `06-mcp-a2a-protocols/protocol-analysis.md` — MCP 2025-11-25 + A2A v1.0.0 协议架构复用分析
- `04-workflow-orchestration/temporal-reuse-patterns.md` — Temporal 工作流复用模式（Saga/Parallel/Child/Schedule）
- `decision-tree-granularity-cost-roi.md` — 功能复用的粒度-成本-收益决策树

#### Track C: 06 治理与量化 + 09 价值量化

- `05-metrics-kpi/metrics-framework.md` — 复用度量指标体系四级框架（资产/项目/组织/生态级）
- `04-finops-cost/cost-allocation-template.md` — FinOps 跨层复用成本分摊模型（含 Excel/Python 模板）
- `01-cocomo-ii-reuse/cocomo-2026-calibration.md` — COCOMO II 2026 校准版（AI辅助开发/Serverless/低代码适配）

#### Track D: 10 供应链安全

- `03-attack-vectors/attack-tree.md` — 软件供应链攻击树（7条路径 + 典型案例映射 + 防御矩阵）

#### Track E: 11 工业 IoT/OT-IT

- `01-isa-95-model/l0-field/asset-catalog.md` — ISA-95 L0 现场层复用资产目录
- `01-isa-95-model/l1-control/asset-catalog.md` — ISA-95 L1 控制层复用资产目录
- `01-isa-95-model/l2-supervisory/asset-catalog.md` — ISA-95 L2 监控层复用资产目录
- `01-isa-95-model/l3-mes/asset-catalog.md` — ISA-95 L3 MES 层复用资产目录
- `01-isa-95-model/l4-enterprise/asset-catalog.md` — ISA-95 L4 企业层复用资产目录
- `01-isa-95-model/cross-layer-matrix/data-flow-mapping.md` — 跨层数据流映射（ERP↔MES↔SCADA↔PLC↔Field）

#### Track F: 07 形式化验证

- `04-rust-type-system/cargo-sat-resolution.md` — Cargo 依赖解析的 SAT 求解详细说明（PubGrub 算法）
- `04-rust-type-system/polonius-vs-nll.md` — Rust Polonius 借用检查器 vs NLL 对比（4个代码示例）
- `04-rust-type-system/unsafe-verification.md` — unsafe 边界验证策略（7工具对比矩阵 + 4级检查清单）

#### Track 认知架构: 08 认知架构

- `03-cognitive-load-theory/quantitative-model.md` — 开发者复用决策认知负荷量化模型（NASA-TLX 适配版）
- `05-ai-cognitive-augmentation/augmentation-architecture.md` — AI 辅助复用决策的认知增强架构设计（RAG+LLM）

#### 参考索引: 99 参考索引

- `glossary/axiom-theorem-tree.md` — 公理-定理推理树（24条已确立，目标20+公理30+定理）
- `visualizations/standard-family-tree.mmd` — 国际标准族谱图（Mermaid）
- `visualizations/concept-mapping.mmd` — 核心概念映射图（Mermaid）
- `templates/document-template.md` — 文档写作统一模板
- `templates/quick-reference-card.md` — 快速参考卡（一页纸速查）

## 2026-06-08 HOTFIX-5: 统一 Coq/Isabelle 状态标记

> **修正原因**：`SUBSEQUENT_PLAN_2026.md` 2.1 节将 Coq/Isabelle 标注为"已完成"，与 `07-formal-verification/README.md` 及 `roadmap.md` 中 T18 的 `[ ]` 未完成状态矛盾。实际仅存在 `insertion_sort.v`、`bounded_counter.v`、`Turnstile.thy` 三个教学级示例，无安全关键组件定理证明。

**已更新文件**：

- `struct/07-formal-verification/README.md` — `## 当前状态` 段落：拆分原条目为"教学示例已完成"与"安全关键证明待启动"
- `struct/07-formal-verification/plans-tasks/roadmap.md` — T18 拆分为 T18a（已完成）与 T18b（Phase 2 2026-Q4）
- `struct/SUBSEQUENT_PLAN_2026.md` — 2.1 节拆分条目并同步 2.3 节描述

**修正原则**：

- 明确区分"教学示例完成"与"安全关键证明完成"
- 所有文件状态标记一致
- 不删除任何已有文件内容

---

> 最后更新: 2026-06-08
