# 交互式复用决策工具 v2.0

> **定位**: 支持六阶段复用决策流程的交互式工具（CLI + Streamlit Web）
> **版本**: 2.0.0
> **技术栈**: Python 3.10+ · Streamlit · 标准库为主

---

## 功能概览

本工具实现本项目核心框架中的**六阶段复用决策流程**，帮助架构师和开发团队系统化评估复用候选资产，降低复用风险，提升决策透明度。

### 六阶段决策流程

| 阶段 | 名称 | 核心判定 | 失败后果 |
|------|------|----------|----------|
| 1 | 语义兼容性判定 | 业务语义 ⊇ 需求？技术约束 ⊆ 上下文？ | 领域/技术不匹配，无法复用 |
| 2 | 变性绑定判定 | 变性模型可交集？绑定时机选择可行？ | 配置过于复杂，维护成本激增 |
| 3 | 质量达标判定 | RRL ≥ 要求？成熟度 ≥ 可靠性要求？ | 质量不达标，引入技术债 |
| 4 | 安全合规判定 | 许可证 ⊆ 策略？安全等级 ≥ 要求？ | 合规风险、法律纠纷 |
| 5 | 成本收益判定 | COCOMO II AAF < 0.7？NPV > 0？ | 经济上不如自研 |
| 6 | 治理合规判定 | 组织成熟度 ≥ 要求？流程标准化？ | 缺乏治理能力，复用难以持续 |

---

## 安装与运行

### 环境要求

- Python 3.10+
- pip

### 安装依赖

```bash
cd ./struct/99-reference/tools/reuse-decision-tool-v2/
pip install -r requirements.txt
```

### CLI 使用

#### 1. 完整决策流程

```bash
python -m reuse_decision_tool decide \
  --asset "支付网关组件" \
  --context "电商微服务架构" \
  --domain "电商,金融" \
  --tech "Kubernetes,Java,gRPC" \
  --rrl 4.2 \
  --maturity 4 \
  --reliability 0.92 \
  --maintainability 0.88 \
  --license "Apache-2.0" \
  --security-level L3 \
  --slsa-level 2 \
  --aaf 0.30 \
  --npv 5.0 \
  --org-maturity 4 \
  --process-standardized \
  --asset-catalog \
  --output report.md
```

#### 2. 快速检查标准对齐状态

```bash
python -m reuse_decision_tool check-standard --standard iso42010 --version 2022
python -m reuse_decision_tool check-standard --standard slsa
python -m reuse_decision_tool check-standard --standard mcp
```

#### 3. 评估复用成熟度

```bash
# 全维度评估目标等级 3
python -m reuse_decision_tool assess-maturity --level 3 --dimension all

# 仅评估「战略与投资」维度
python -m reuse_decision_tool assess-maturity --level 4 --dimension D1
```

#### 4. 生成复用决策卡片

```bash
# Markdown 格式
python -m reuse_decision_tool card --asset-id PAT-MICRO-002 --format markdown

# JSON 格式
python -m reuse_decision_tool card --asset-id PAT-MICRO-002 --format json --output card.json
```

### Web 界面（Streamlit）

```bash
streamlit run web_app.py
```

界面布局：

- **左侧边栏**：输入面板（资产信息、上下文需求、约束条件、组织治理）
- **右侧主面板**：
  - 📊 决策结果标签页：最终决策、置信度、阶段详情、推荐行动、升级/降级路径
  - 🌡️ 风险热力图标签页：按阶段分组的风险可视化、风险登记详情表
  - 📥 导出报告标签页：Markdown / JSON 格式下载

---

## 项目结构

```
reuse-decision-tool-v2/
├── __init__.py              # 包初始化
├── main.py                  # CLI 主入口
├── decision_engine.py       # 复用决策引擎核心
├── web_app.py               # Streamlit Web 界面
├── test_decision_engine.py  # 单元测试
├── requirements.txt         # Python 依赖
├── README.md                # 本文档
├── data/
│   ├── decision_rules.json      # 六阶段决策规则配置（可扩展）
│   ├── reuse_patterns.json      # 内置复用模式数据库
│   ├── standards_index.json     # 标准版本跟踪数据库
│   └── maturity_matrix.json     # 五级成熟度评估问卷数据
└── templates/
    └── report_template.md       # Jinja2 Markdown 报告模板（预留）
```

---

## 数据层说明

### `decision_rules.json`

决策规则以 JSON 配置，**不硬编码在 Python 中**。每个阶段包含多条规则，支持：

- 条件表达式与阈值判定
- 权重分配与加权得分
- 失败动作：`REJECT` / `CONDITIONAL`
- 全局规则：置信度计算、风险惩罚、最大条件通过阶段数

### `reuse_patterns.json`

内置 6 种常见复用模式：

- 分层架构复用模式
- 微服务架构复用模式
- Serverless 架构复用模式
- 事件驱动架构复用模式
- MCP (Model Context Protocol) 复用模式
- WebAssembly 组件复用模式

每种模式包含语义兼容性、变性模型、质量画像、成本画像、安全合规、治理要求等完整属性。

### `standards_index.json`

跟踪 8 项国际标准/行业框架：

- ISO/IEC/IEEE 42010:2022
- ISO/IEC/IEEE DIS 42042
- ISO/IEC 25010:2024
- ISO/IEC 26566:2026
- TOGAF Standard 10
- ArchiMate 3.2
- SLSA v1.2
- Model Context Protocol

### `maturity_matrix.json`

基于 ISO/IEC 26566:2026 / RCMM / NASA RRL 的 6 维度 × 5 级成熟度问卷：

- D1 复用战略与投资
- D2 复用过程与管理
- D3 资产开发与维护
- D4 基础设施与支持
- D5 人员与培训
- D6 度量与改进

---

## 可扩展性

### 1. 决策规则热更新

修改 `data/decision_rules.json` 中的规则阈值、权重或新增阶段，无需重启 Python 进程（Web 界面会缓存引擎，CLI 每次重新加载）。

### 2. 插件式扩展

```python
from decision_engine import ReuseDecisionEngine

engine = ReuseDecisionEngine()

# 注册自定义评估钩子
def my_plugin(phase_result, asset, context):
    print(f"阶段 {phase_result.phase_name} 评估完成")

engine.plugins.register("post_phase_eval", my_plugin)
```

支持的钩子：

- `pre_phase_eval`: 阶段评估前执行
- `post_phase_eval`: 阶段评估后执行
- `final_decision`: 最终决策后执行

### 3. 标准数据库外部更新

`standards_index.json` 可通过外部脚本或 CI 流程自动更新，跟踪标准演进。

---

## 核心算法说明

### 置信度评分

```
final_score = average(phase_scores) * (1 - risk_penalty)

risk_penalty = min(
    high_risk_count * 0.05 * 2 + medium_risk_count * 0.05,
    0.5
)
```

### 最终决策逻辑

| 条件 | 结果 |
|------|------|
| 任一阶段 REJECT | **拒绝复用** |
| 条件通过阶段 > 2 | **条件批准** |
| 存在条件通过阶段 | **条件批准** |
| 全部通过 | **批准复用** |

### COCOMO II 集成

```
ESLOC = AAF * KSLOC_reused
PM = A * ESLOC^B * EM
```

### NPV 计算

```
NPV = -initial_cost + Σ[(annual_savings - annual_maintenance) / (1 + r)^t]
```

---

## 测试

```bash
# 使用 pytest
pytest test_decision_engine.py -v

# 使用 unittest 直接运行
python test_decision_engine.py

# 运行特定测试类
python -m pytest test_decision_engine.py::TestReuseDecisionEngine -v
```

测试覆盖：

- 引擎初始化和数据加载
- 六阶段决策评估（通过/拒绝/条件通过）
- 结果序列化
- 标准对齐检查
- 成熟度评估
- 决策卡片生成
- COCOMO / NPV / ROI 财务计算
- 插件机制

---

## 与 v1.0 的差异

| 特性 | v1.0 | v2.0 |
|------|------|------|
| 决策流程 | 6 阶段概念框架 | **可执行规则引擎** |
| CLI | 无 | **完整 argparse 接口** |
| Web 界面 | 概念规划 | **Streamlit 实现** |
| 决策规则 | 硬编码 | **JSON 配置化** |
| 风险登记 | 无 | **自动生成 Risk Register** |
| 升级/降级建议 | 无 | **层级路径推荐** |
| 插件扩展 | 无 | **Hook 机制** |
| 标准跟踪 | 独立脚本 | **集成对齐检查** |
| 成熟度评估 | 独立脚本 | **集成 gap analysis** |
| COCOMO 集成 | 独立脚本 | **内置财务计算** |
| 置信度评分 | 无 | **0-100 量化评分** |
| 单元测试 | 无 | **pytest/unittest 覆盖** |

---

## 贡献与演进

- 如需新增复用模式，编辑 `data/reuse_patterns.json`
- 如需调整决策阈值，编辑 `data/decision_rules.json`
- 如需对接外部系统，使用 `decision_engine.py` 中的 `ReuseDecisionEngine` 类
- 如需自定义报告模板，扩展 `templates/report_template.md`（建议配合 Jinja2）

---

> **最后更新**: 2026-06-10
> **对齐标准**: ISO/IEC 26566:2026 · ISO 25010:2024 · ISO 42010:2022 · NASA RRL
