# 季度前沿跟踪复核标准作业程序（SOP）

> **版本**: 1.0
> **生效日期**: 2026-07-08
> **适用范围**: `struct/99-reference/frontier-tracking/` 与全项目权威来源对齐
> **维护人**: 软件工程架构复用知识体系项目组

---

## 1. 目的

建立可重复、可审计的季度前沿跟踪流程，确保知识体系中的标准、框架、协议引用与国际权威来源保持同步。

### 概念定位：SOP 的定义与边界

**标准作业程序（Standard Operating Procedure, SOP）** 在本目录中指：将"季度前沿跟踪"这一周期性活动拆解为固定步骤、固定角色与固定输出物的操作规范，使任何接任的跟踪负责人都能在不依赖个人经验的情况下复现同等质量的复核结果。本 SOP 的边界是"标准状态复核与索引更新"，不包括主题文档的内容创作（后者由各领域负责人按 `struct/MASTER_PLAN.md` 执行）。

### 示例：一次紧急复核的实际执行

例如：2026-05-29 MCP 官方发布 RC 2026-07-28 时，跟踪负责人按本 SOP 的"紧急复核"路径执行：运行 `standard-status-checker.py` → 人工访问 modelcontextprotocol.io 确认 RC 状态 → 在 `2026-q3-frontier-report.md` 中登记"RC 已发布，稳定版仍为 2025-11-25" → 更新本目录 README 的活跃跟踪项。该记录可在 `../2026-q3-frontier-report.md` 中查证。

### 反例：违反本 SOP 的做法

- 仅凭第三方报道或记忆就修改 `authoritative-sources-v2.md` 中的标准状态（跳过步骤 3 的人工官方页面复核）；
- 将"征求意见稿（IPD）"直接标注为"已发布"（违反状态四分类原则）；
- 更新索引后跳过步骤 7 的质量门禁，导致死链或格式破坏进入主干。

因此，本 SOP 将"人工权威来源复核"（步骤 3）设为不可跳过环节：自动化脚本只负责发现候选变更，状态确认必须有人工访问官方页面的记录。

---

## 2. 频率与触发条件

| 类型 | 频率 | 触发条件 |
|---|---|---|
| 轻量复核 | 每月第一周 | CI 定时任务或人工触发 |
| 深度复核 | 每季度首月（3/6/9/12 月） | 季度报告周期开始 |
| 紧急复核 | 即时 | 官方发布重大版本/征求意见稿/安全通告时 |

---

## 3. 责任人与角色

| 角色 | 职责 |
|---|---|
| **跟踪负责人** | 运行脚本、收集权威来源信息、起草季度报告 |
| **事实审查人** | 核对每条状态变更的官方来源 URL、版本号、发布日期 |
| **内容整合人** | 将确认后的变更更新到 `authoritative-sources-v2.md` 与相关主题文档 |
| **质量守门人** | 运行 `health-check.py`，确保无新增死链、无格式破坏 |

---

## 4. 作业步骤

### 步骤 1：准备环境

```bash
cd /path/to/Architecture
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤 2：运行自动化脚本

```bash
# 2.1 标准状态自动复核（生成报告与 JSON 快照）
python scripts/standard-status-checker.py

# 2.2 标准跟踪监控（含 RSS/Atom feed 解析）
python struct/99-reference/tools/standard-tracker.py --quarterly-report

# 2.3 项目内部版本一致性审计
python struct/99-reference/tools/standards-version-audit.py .
```

### 步骤 3：人工权威来源复核

对以下重点项逐一访问官方页面确认：

1. **ISO/IEC 标准**: `https://www.iso.org/standard/<number>.html`
2. **IEC 标准**: `https://webstore.iec.ch/publication/<number>`
3. **The Open Group**: `https://www.opengroup.org/press-releases/feed` 与官方下载页
4. **NIST**: `https://csrc.nist.gov/news/feed`
5. **MCP（Model Context Protocol） / A2A（Agent-to-Agent Protocol） / SLSA 1.2 / WASI**: GitHub releases / 官方博客 feed
6. **OWASP / OpenSSF / CNCF**: 官方项目页面与 GitHub releases

### 步骤 4：评估影响并更新索引

1. 打开 `struct/99-reference/standards-index/authoritative-sources-v2.md`
2. 更新发生变更的条目：版本、状态、官方 URL、`Last Verified` 日期
3. 新增本季度发现的标准（如有）
4. 在 `CHANGELOG.md` 中记录重大变更

### 步骤 5：更新前沿跟踪报告

1. 复制 `templates/quarterly-frontier-template.md` 到 `YYYY-qN-frontier-report.md`
2. 填写本季度新发布/变更的标准、未变更项、影响评估、下季度重点
3. 更新 `README.md` 中的“当前活跃跟踪项”

### 步骤 6：联动更新主题文档

根据影响评估，按需更新引用该标准的主题 Markdown 文件：

- 仅状态文字变更：更新描述与脚注
- 版本号变更：全局搜索替换，并更新勘误说明
- 新增标准：在相关主题中增加对应章节或案例

### 步骤 7：质量门禁

```bash
python scripts/health-check.py
```

确保：

- `struct/` 与 `view/` 质量门控 100% 通过
- 链接检查无死链
- 交叉索引一致
- 模板 padding 检查通过

### 步骤 8：提交与审阅

1. 创建 feature branch：`frontier/YYYY-QN-update`
2. 提交变更，附上前沿报告摘要
3. 由事实审查人与质量守门人审阅
4. 合并到 `main`

---

## 5. 输出物清单

| 输出物 | 路径 |
|---|---|
| 季度前沿跟踪报告 | `struct/99-reference/frontier-tracking/YYYY-qN-frontier-report.md` |
| 标准状态复核报告 | `reports/standard-status-report.md` |
| 标准状态快照 | `reports/standard-status-snapshot.json` |
| 标准跟踪季度报告 | `struct/99-reference/tools/standard-tracker-quarterly-report.md` |
| 更新后的权威来源索引 | `struct/99-reference/standards-index/authoritative-sources-v2.md` |
| 变更日志 | `struct/99-reference/CHANGELOG.md` |

---

## 6. 常见问题处理

| 现象 | 处理方式 |
|---|---|
| 官方 URL 返回 403 | 使用浏览器人工访问确认；如为反爬策略，在报告中标注“需人工复核” |
| 官方 feed 无法解析 | 检查 feed 是否迁移到新的域名或格式；更新 `standard-tracker.py` 配置 |
| 同一标准出现多个版本 | 在 `authoritative-sources-v2.md` 中分行列出，并标注“仍有效”/“已取代” |
| 发现第三方来源与官方冲突 | 一律以官方来源为准，并在报告中记录冲突点 |

---

## 7. 关联脚本与文档

### 权威来源与核查

> **权威来源**（本 SOP 步骤 3 人工复核所访问的官方页面）：
>
> - ISO 标准检索：<https://www.iso.org/standards.html>
> - IEC Webstore：<https://webstore.iec.ch/>
> - The Open Group 标准库：<https://pubs.opengroup.org/togaf-standard/>
> - NIST CSRC 出版物：<https://csrc.nist.gov/publications/detail/sp/800-218/final>
> - MCP 官方规范：<https://modelcontextprotocol.io/specification/2025-11-25>
>
> **核查日期**: 2026-07-08

### 相关文档与脚本

- `scripts/standard-status-checker.py`
- `struct/99-reference/tools/standard-tracker.py`
- `struct/99-reference/tools/standards-version-audit.py`
- `scripts/health-check.py`
- `struct/99-reference/standards-index/authoritative-sources-v2.md`
- `struct/99-reference/CHANGELOG.md`

---

> **最后更新**: 2026-07-08
