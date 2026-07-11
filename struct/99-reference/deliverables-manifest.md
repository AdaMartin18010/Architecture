# 全量交付物清单

> **版本**: 2026-07-08 | **统计范围**: `struct/` 目录（含 `99-reference/`）

---

## 统计概览

| 类别 | 数量 | 说明 |
|------|------|------|
| Markdown 文档 | 332 | 知识体系核心载体（struct/ 309 + view/ 23） |
| Python 工具 | 12+ | CLI / Streamlit / 分析脚本 |
| TLA+ 规约 | 3 | 时序逻辑形式化规约 |
| Alloy 模型 | 4 | 约束求解与结构验证 |
| Coq/Isabelle 证明 | 2+ | 定理证明纲要 |
| Mermaid 架构图 | 75 | 13 主题 × 5 类图 + 综合图 |
| SVG 渲染图 | 75 | 矢量图（透明背景） |
| 课程/测验/幻灯片 | 4+ | Phase 6 整合输出 |
| **总计** | **~500** | 跨 13 个一级主题 + 参考索引 |

---

## 按主题交付物

### 01 元模型与标准对齐

- **核心文档**: ISO/IEC/IEEE 42010:2022/42020/42030 族谱、TOGAF Standard 10 ADM 对齐、ArchiMate 4.0 映射、SWEBOK V4 覆盖分析
- **形式化基础**: 4 元公理、存在性公理、结构性公理、过程性公理（20 条公理体系）
- **标准追踪**: `99-reference/tools/standard-tracker.py`（8 项标准自动监控）

### 02 业务架构复用

- **流程模型**: BPMN 2.0 Call Activity、DMN 1.5 Decision Service、CMMN 案例管理
- **能力映射**: Business Capability / Value Stream 复用映射
- **可视化**: `02-business-architecture-reuse.mmd` + `.svg`

### 03 应用架构复用

- **架构演进**: Monolith → Modular Monolith → Microservices → Serverless → Data Mesh
- **云原生模式**: Sidecar、BFF、Strangler、Service Mesh、Dapr
- **可视化**: `03-application-architecture-reuse.mmd` + `.svg`

### 04 组件架构复用

- **接口契约**: Design-by-Contract（Pre/Post/Invariant/Side-effect）
- **封装形态**: 静态库、OSGi/JPMS、WASM Component、容器、微服务接口
- **6 大语言生态**: JVM、Node.js、Rust、Go、Python、.NET
- **可视化**: `04-component-architecture-reuse.mmd` + `.svg`

### 05 功能架构复用

- **协议栈**: MCP、A2A、REST/OpenAPI、gRPC、GraphQL、Event
- **复用单元**: 纯函数、Tool、Resource、Prompt、Agent Card、Task、Workflow
- **质量保障**: 单元测试、Mock、契约测试（Pact）、性能基准
- **可视化**: `05-functional-architecture-reuse.mmd` + `.svg`

### 06 跨层复用治理

- **治理框架**: ISO/IEC/IEEE 42020:2019/42030/26565 产品线成熟度框架 / 26566 产品线纹理方法 三层治理与纹理体系
- **成熟度模型**: RCMM 5 级、资产/项目/组织/生态四级度量
- **决策支持**: ADR、RACI、FinOps、升级/降级矩阵
- **自动化**: 架构 Lint、Scorecard、策略即代码（OPA）
- **可视化**: `06-cross-layer-governance.mmd` + `.svg`

### 07 形式化验证（T18b 完成）

- **TLA+**: 时序逻辑规约、PlusCal 算法、Amazon AWS 实践
- **Alloy**: 约束求解、结构验证、轻量级形式化
- **Coq/Isabelle**: 安全关键组件证明纲要（seL4、CompCert、Rate-Monotonic）
- **Rust**: 类型系统安全、Borrow Checker、Prusti/Aeneas
- **比较矩阵**: 6 大方法的能力矩阵与选型指南
- **可视化**: `07-formal-verification.mmd` + `.svg`

### 08 认知架构

- **认知模型**: ACT-R、BDI、Kahneman 双系统、认知组块理论
- **认知负荷**: 内在/外在/相关负荷与工作记忆瓶颈
- **AI 增强**: RAG 检索、LLM 推荐、Agent 辅助分析、可解释性
- **可视化**: `08-cognitive-architecture.mmd` + `.svg`

### 09 价值量化

- **成本模型**: COCOMO II 2026、ESLOC、AAF、EM、AF
- **收益模型**: 直接/间接/战略/质量溢价
- **决策指标**: ROI、NPV、BEP、IRR
- **度量框架**: DORA 四大指标、SPACE、DevEx
- **工具**: COCOMO 计算脚本
- **可视化**: `09-value-quantification.mmd` + `.svg`

### 10 供应链安全

- **SLSA**: 1.2 Multi-Track（Build/Source/Env）、L1→L4 递进
- **SBOM**: SPDX / CycloneDX / SWID、VEX
- **签名**: Sigstore（Fulcio/Rekor/Cosign）
- **合规**: NIST SSDF 1.2、EU CRA、OWASP SCVS、EO 14028
- **可视化**: `10-supply-chain-security.mmd` + `.svg`

### 11 工业 IoT/OT-IT 融合

- **ISA-95**: L0-L4 五层架构、资产目录
- **OPC UA FX**: C2C/C2D/D2D 复用层次、Pub/Sub
- **TSN**: IEEE 802.1Qbv、IEC 60802、确定性网络
- **AAS**: IEC 63278 资产管理壳、数字孪生
- **功能安全**: IEC 61508、ISO 26262、SEooC、Proven-in-Use
- **边缘智能**: TinyML、ONNX Runtime、MCP Industrial
- **可视化**: `11-industrial-iot-otit.mmd` + `.svg`

### 12 AI 原生架构复用

- **协议**: MCP 2025-11-25、A2A v1.0.0.0.0.0.0、ANP（实验性）
- **Agent 架构**: ReAct、Plan-and-Execute、Multi-Agent、主管-工作者
- **模型资产**: RAG、LoRA/QLoRA/DoRA、Adapter、Prompt 模板库
- **运行时治理**: 温度控制、漂移检测、Guardrails、Token 预算
- **概率契约**: γ(x) 期望分布、Conformal Prediction、在线校准
- **可视化**: `12-ai-native-reuse.mmd` + `.svg`

### 13 前沿趋势

- **平台工程**: IDP、Golden Path、Backstage、CNCF 成熟度
- **运行时演进**: WASM Component Model、WASI 0.3 async、模块化单体
- **智能体经济**: Agent 服务市场、微支付、信誉评级
- **可持续**: 绿色软件工程（SCI）、RegTech AI、SBOM 经济
- **语言生态**: Rust 扩展、FFI 边界治理、内存安全倡议
- **可视化**: `13-emerging-trends.mmd` + `.svg`

---

## 参考索引层（99-reference）

| 子目录 | 内容 | 关键文件 |
|--------|------|----------|
| `book-outline.md` | 全书 12 章框架 | 12 章 + 附录 + 读者分层 |
| `glossary/` | 术语与推理体系 | `axiom-theorem-tree.md`（20 公理 + 35 定理） |
| `standards-index/` | 标准对齐总矩阵 | `master-alignment-matrix.md`（30 标准 × 5 层次） |
| `visualizations/` | 架构图库 | 13 主题 `.mmd` + `.svg` + `README.md` |
| `tools/` | 交互式工具 | `terminology-query.py`、`reuse-toolkit-dashboard.py`、`standard-tracker.py` |
| `templates/` | 文档模板 | 学术引用模板（生成中） |
| `knowledge-index/` | 知识问答索引 | `qa-index.md`（生成中） |
| `chapters/` | 全书章节草稿 | ch01-ch06 |
| `external-links/` | 权威来源外链 | 大学课程、标准官网、论文 |
| `audit/` | 审查记录 | 事实核查、版本变更 |

---

## 交互式工具清单

| 工具 | 类型 | 功能 | 路径 |
|------|------|------|------|
| `terminology-query.py` | CLI | 跨标准术语查询（34+ 术语） | `99-reference/tools/` |
| `reuse-toolkit-dashboard.py` | Streamlit | Web 仪表盘（术语+成熟度+决策树） | `99-reference/tools/` |
| `standard-tracker.py` | CLI | 标准状态监控与报告生成 | `99-reference/tools/` |
| `cocomo-calculator.py` | CLI | COCOMO II 复用成本计算 | `09-value-quantification/tools/` |
| `maturity-assessment.py` | CLI | RCMM 成熟度评估问卷 | `06-cross-layer-governance/03-maturity-models/` |
| `reuse-decision-tree.py` | CLI | 6 阶段复用决策流程 | `99-reference/tools/reuse-decision-tool/` |

---

## 使用建议

1. **快速入门**: 从 `struct/README.md` → `book-outline.md` → 感兴趣的主题目录
2. **术语查询**: 运行 `python 99-reference/tools/terminology-query.py query <术语>`
3. **可视化浏览**: 查看 `99-reference/visualizations/README.md` 和 `.svg` 图
4. **标准跟踪**: 运行 `python 99-reference/tools/standard-tracker.py --generate-report`
5. **学术引用**: 参考 `99-reference/templates/academic-citation-template.md`
6. **问题检索**: 查阅 `99-reference/knowledge-index/qa-index.md`


---

## 补充说明：全量交付物清单

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

---

## Phase 6 整合输出物

| 交付物 | 路径 | 说明 |
|--------|------|------|
| 全书聚合稿 | `dist/book-full.md` | 由 `scripts/build-deliverables.py` 生成 |
| 主题分卷 | `dist/book-volumes/volume-*.md` | 14 个主题卷册 |
| HTML 幻灯片 | `dist/slides/*.html` | 由 `scripts/build-slides.py` 生成（reveal.js） |
| PDF/ePub | `dist/book-full.pdf` / `.epub` | 由 `scripts/build-pdf.py` 生成（需 pandoc） |
| 学习路径 | `99-reference/course/learning-path.md` | 4 条递进式学习路径 |
| 课程大纲 | `99-reference/course/syllabus.md` | 16 周课程安排 |
| 课程测验 | `99-reference/course/quiz.md` | 单选/多选/简答/计算题 |
| 统一 CLI | `scripts/knowledge-cli.py` | health / build / render / search / stats |
| 知识门户 | `99-reference/tools/knowledge-portal/app.py` | Streamlit 交互式门户 |
| CI 工作流 | `.github/workflows/health-check.yml` | 自动 health-check + 构建产物上传 |

---

> **生成命令**: `python scripts/knowledge-cli.py build`
