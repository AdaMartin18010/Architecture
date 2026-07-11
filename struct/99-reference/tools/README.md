# 可执行工具目录

> **定位**: 将知识体系中的理论模型转化为可运行的代码原型
> **开发策略**: 按 `SUBSEQUENT_PLAN_2026_NETWORK_ALIGNED_v2.md` 决策 3A，采用 Python CLI + Streamlit 快速原型
> **版本**: 2026-07-06

---

## 依赖安装

在项目根目录激活 `.venv` 后安装全部依赖：

```bash
# Windows PowerShell / Git Bash
source .venv/Scripts/activate
pip install -r struct/99-reference/tools/requirements.txt
```

依赖列表：`numpy`、`scipy`、`openpyxl`、`pyyaml`、`streamlit`、`pytest`。

`reuse-decision-tool-v2/` 也可使用自身 `requirements.txt`：`pip install -r struct/99-reference/tools/reuse-decision-tool-v2/requirements.txt`。

---

## 工具清单

| 工具 | 路径 | 用途 | 状态 |
|------|------|------|------|
| 术语查询 | `terminology-query.py` | 跨标准术语搜索、对比、版本提示、导出、同步 | ✅ 可用 |
| COCOMO II 计算器 | `cocomo-calculator.py` | 复用模型工作量估算 | ✅ 可用 |
| 成熟度评估 CLI | `../../06-cross-layer-governance/03-maturity-models/reuse-maturity-assessment-cli.py` | ISO/IEC 26565 / RCMM / RiSE 复用成熟度评估（26566 提供产品线纹理支撑） | ✅ 可用 |
| FinOps 成本分摊 | `../../06-cross-layer-governance/04-finops-cost/templates/finops-exporter.py` | L1–L4 成本分摊 Excel/CSV 导出 | ✅ 可用 |
| 概率契约校准 | `../../12-ai-native-reuse/05-probabilistic-contracts/calibration-tool.py` | Conformal Prediction 校准、漂移检测 | ✅ 可用 |
| PIU 贝叶斯验证 | `../../11-industrial-iot-otit/06-functional-safety/piu-bayesian-tool.py` | IEC 61508 Proven-in-Use 统计验证 | ✅ 依赖就绪 |
| 供应链攻击树可视化 | `../../10-supply-chain-security/03-attack-vectors/attack-tree-interactive.py` | 5 种攻击场景、单文件 HTML 生成 | ✅ 可用 |
| EU CRA 合规检查 | `../../10-supply-chain-security/06-case-studies/eu-cra-checklist.py` | 20 项检查清单、JSON/Markdown 报告 | ✅ 可用 |
| 复用决策工具 v1 | `reuse-decision-tool/` | 交互式六阶段复用决策（生命周期视角，历史概念稿） | 📦 已归档（DEPRECATED，权威实现为 v2） |
| 复用决策工具 v2 | `reuse-decision-tool-v2/main.py` | 增强版复用决策（判定门径视角，Streamlit / CLI）— **权威实现** | ✅ help 可用 |
| 形式化验证环境 | `formal-verification-env/` | Docker 化 TLA+/Alloy/Coq/Isabelle | ⚠️ 仅文档/占位，未安装验证 |

> **说明**: 形式化验证工具按用户要求仅保留内容与占位，不进行 Docker 安装或运行时验证。

---

## 术语数据库

- 术语数据外部化到同目录的 `terminology-db.yaml`（推荐）或 `terminology-db.json`。
- 文件结构包含三个顶层键：`terms`（术语定义）、`aliases`（标准别名）、`version_hints`（权威版本提示）。
- 脚本启动时优先加载外部文件；若文件不存在，则回退到内置字典，保证单文件可运行。
- 使用 `sync` 命令可从 Markdown 表格自动同步术语别名与标准版本提示到数据库（默认 dry-run，需 `--apply` 才会写入）。

---

## 快速开始

```bash
cd struct/99-reference/tools

# 查询术语
python terminology-query.py search "architecture view"
python terminology-query.py search "复用" --lang zh

# 跨标准对比
python terminology-query.py compare "reusability" --standards iso25010,ieee1517 --lang zh

# 列出某标准下的术语
python terminology-query.py list --standard togaf10 --lang zh

# 权威版本提示
python terminology-query.py version-hint "reusability" --lang zh

# 导出生词表
python terminology-query.py export-glossary --format md --output glossary.md
python terminology-query.py export-glossary --format json --output glossary.json
python terminology-query.py export-glossary --format yaml --output glossary.yaml

# 从 Markdown 来源同步（默认 dry-run）
python terminology-query.py sync \
  --sources ../../99-reference/glossary/terminology-crosswalk.md,../../99-reference/standards-index/authoritative-sources-v2.md \
  --lang zh

# 应用同步到 terminology-db.yaml
python terminology-query.py sync \
  --sources ../../99-reference/glossary/terminology-crosswalk.md,../../99-reference/standards-index/authoritative-sources-v2.md \
  --apply --lang zh

# 运行内置单元测试
python terminology-query.py --test

# COCOMO II 计算
python cocomo-calculator.py --ksloc-reused 50 --aaf 0.4 --em 1.2

# 形式化验证环境（仅文档占位，不启动容器）
cd formal-verification-env
# docker compose up -d
# bash verify-all.sh
```

---

## 验证记录（2026-07-06）

已执行的最小验证命令：

```bash
python cocomo-calculator.py --test
python terminology-query.py --test
python ../../12-ai-native-reuse/05-probabilistic-contracts/calibration-tool.py --test
python ../../10-supply-chain-security/03-attack-vectors/attack-tree-interactive.py --test
python ../../06-cross-layer-governance/03-maturity-models/reuse-maturity-assessment-cli.py --demo
python ../../06-cross-layer-governance/04-finops-cost/templates/finops-exporter.py --input ../../06-cross-layer-governance/04-finops-cost/templates/example-costs.yaml --output /tmp/finops.xlsx
python ../../10-supply-chain-security/06-case-studies/eu-cra-checklist.py --help
python ../../11-industrial-iot-otit/06-functional-safety/piu-bayesian-tool.py --help
python reuse-decision-tool-v2/main.py --help
```

结果：全部通过或 help 输出正常。部分脚本需用户提供输入数据/YAML/JSON 才能跑完整流程。

---

---

## 计划中的工具（按 `SUBSEQUENT_PLAN_2026_NETWORK_ALIGNED_v2.md`）

- 成熟度评估 CLI 增强（导出 Markdown/JSON、权重自定义） — Phase 1
- FinOps 单位经济学与 AI 成本模块 — Phase 1
- 概率契约校准 GUI / Streamlit 版 — Phase 1
- MCP/Agentic 安全治理扫描器（策略/工具清单） — Phase 1
- ISO/IEC 25010:2023/25040 质量矩阵评估器 — Phase 1
- PIU 贝叶斯验证完整输入示例 — Phase 2
- 供应链攻击树可视化扩展（MCP/Agentic 攻击向量） — Phase 2
- ~~`reuse-decision-tool/` 与 v2 能力对齐 — Phase 6~~ **已取消**：v1 已于 2026-07-12 归档，以 `reuse-decision-tool-v2/` 为权威实现，不再做能力对齐

---

> 最后更新: 2026-07-06


---

## 补充说明：可执行工具目录

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

## 分析

**分析**：参考层的价值不在于内容本身，而在于建立知识之间的信任锚点；必须随标准演进定期审计与更新。
