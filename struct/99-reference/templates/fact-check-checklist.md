# 事实核查清单（Fact-Check Checklist）

> **版本**: 2026-06-08
> **定位**: 防止未来再次出现 ArchiMate 4.0 类事实错误的持续机制
> **适用范围**: 所有新增/更新的标准引用、技术声明、学者引用、版本号声明
> **对齐**: `SUBSEQUENT_PLAN_2026.md` 决策 5A + 调整建议 3

---

## 使用说明

每篇新增或更新文档在提交前，必须完成以下核查项。核查人需在文档头部或提交注释中标注：

```markdown
> **事实核查**: ✅ 已通过（核查人: ___，日期: ___）
```

---

## 核查维度

### 1. 标准/规范版本核查

| # | 核查项 | 核查方法 | 权威来源示例 |
|:---|:---|:---|:---|
| 1.1 | 引用的标准版本号是否为当前最新版？ | 访问 ISO/IEC/IEEE/The Open Group 官方网站的 "Current Status" 或 "Latest Version" 页面 | `iso.org/standard/XXXXX`, `opengroup.org/standards` |
| 1.2 | 声称的"正式发布"是否有官方 Press Release 佐证？ | 搜索组织官网的 Press Releases / News 板块 | `opengroup.org/press-releases`, `iso.org/news` |
| 1.3 | 声称的"草案/DIS"状态是否与官方一致？ | 查询 ISO DIS 数据库或工作组的公开文档 | `iso.org/drafts`, `ieee802.org` |
| 1.4 | 标准的发布日期是否准确？ | 交叉比对标准组织的官方目录和至少一个第三方权威来源 | 官方目录 + ACM/IEEE 数字图书馆 |
| 1.5 | 向后兼容性声明是否有官方文档支持？ | 查阅标准组织的兼容性声明页面或版本说明 | `opengroup.org/archimate-forum` |

### 2. 技术生态核查

| # | 核查项 | 核查方法 | 权威来源示例 |
|:---|:---|:---|:---|
| 2.1 | 声称的"最新稳定版"是否为当前实际稳定版？ | 访问技术的官方文档首页，检查 Version History 或 Changelog | `modelcontextprotocol.io/specification`, `slsa.dev/spec` |
| 2.2 | "RC/Beta/Preview" 是否被错误标注为稳定版？ | 明确区分 Release Candidate 与 Stable Release | 官方 Changelog 中的版本标注 |
| 2.3 | 引用的工具/项目是否仍在积极维护？ | 检查 GitHub 仓库的最近提交时间、README 中的维护状态声明 | `github.com/<org>/<repo>` 的 commit history |
| 2.4 | 声称的"社区已转向"是否有官方迁移声明？ | 查找官方博客、仓库 README 的迁移说明 | Bytecode Alliance 博客、官方 GitHub issues |
| 2.5 | 标准化阶段（W3C Phase 1/2/3）是否准确？ | 查询 W3C 官方 features 页面或 Community Group 文档 | `webassembly.org/features`, `w3.org/TR/` |

### 3. 学者/机构引用核查

| # | 核查项 | 核查方法 | 权威来源示例 |
|:---|:---|:---|:---|
| 3.1 | 引用的学者是否真实存在？ | 搜索学者的官方主页、Google Scholar、DBLP | `scholar.google.com`, `dblp.org` |
| 3.2 | 声称的"预言/论断"是否有原始文献支持？ | 查找原始论文、博客、演讲稿 | 学者主页、arXiv、会议论文集 |
| 3.3 | 引用的研究是否为该学者的实际研究方向？ | 浏览学者近 3 年的发表论文列表 | Google Scholar 的 "Recent" 标签 |
| 3.4 | 机构声明（如"SEI 推荐"）是否有官方报告编号？ | 查找 CMU/SEI 技术报告的官方编号和 URL | `resources.sei.cmu.edu/library` |

### 4. 版本号与日期核查

| # | 核查项 | 核查方法 | 工具/来源 |
|:---|:---|:---|:---|
| 4.1 | 所有版本号（v1.2, 2025-11-25 等）在全项目中是否一致？ | 使用 `grep -r "<版本号>" --include="*.md" struct/` 全局搜索 | `grep`, `rg` |
| 4.2 | 声称的"预计发布时间"是否已过？是否已更新实际状态？ | 对比声称日期与当前日期，检查后续更新 | 日历 + 官方公告 |
| 4.3 | 历史文档（view/）的勘误说明是否及时更新？ | 定期检查 view/ 文件头部的勘误列表 | 手动审计 + 自动化提醒 |

### 5. 链接健康检查

| # | 核查项 | 核查方法 | 工具 |
|:---|:---|:---|:---|
| 5.1 | 所有外部 URL 是否可访问（HTTP 200）？ | 批量 HTTP HEAD 请求 | `curl -I`, `lychee` |
| 5.2 | 链接内容是否与引用时的描述一致？ | 抽样访问并比对 | 手动检查 |

---

## 核查记录模板

```markdown
## 核查记录：`<文件名>`

| 维度 | 核查项 | 结果 | 核查来源 |
|:---|:---|:---:|:---|
| 标准版本 | 1.1 版本号最新 | ✅/❌ | |
| 标准版本 | 1.2 正式发布有 Press Release | ✅/❌ | |
| 技术生态 | 2.1 稳定版准确 | ✅/❌ | |
| 技术生态 | 2.2 RC 未误标为稳定 | ✅/❌ | |
| 学者引用 | 3.1 学者真实存在 | ✅/❌ | |
| 学者引用 | 3.2 论断有原始文献 | ✅/❌ | |
| 版本一致性 | 4.1 全项目一致 | ✅/❌ | |
| 链接健康 | 5.1 URL 可访问 | ✅/❌ | |

**核查结论**: ☐ 通过  ☐ 需修正（详见下方）  ☐ 需补充来源

**修正项**:
1. ...

**核查人**: ___  **日期**: ___
```

---

## 月度事实核查节奏

按 `MASTER_PLAN.md` 调整后的月度节奏：

```text
第 1 周: 选择一个二级主题进行深度写作
第 2 周: 对照权威来源进行对齐验证
第 3 周: 编写形式化约束（公理/定理/定义）
第 4 周: 审查、交叉引用、更新 MASTER_PLAN
第 5 周（月度审查）: 事实核查 — 抽查 5-10 个外部引用的事实准确性
```

---

## 标准 RSS / 监控列表

| 标准/组织 | 监控方式 | 更新频率 | 负责人 |
|:---|:---|:---:|:---|
| ISO/IEC 标准 | `iso.org` RSS + 邮件提醒 | 实时 | |
| The Open Group | `opengroup.org/press-releases` RSS | 实时 | |
| IEEE 标准 | `standards.ieee.org` 邮件提醒 | 实时 | |
| MCP | `modelcontextprotocol.io/specification` + GitHub releases | 每周 | |
| SLSA | `slsa.dev/blog` + GitHub releases | 每周 | |
| WASI / Wasmtime | `bytecodealliance.org/articles` + GitHub releases | 每周 | |
| ICSA / ECSA | `computer.org` 会议日程 | 每季度 | |
| Conformal Prediction | arXiv cs.LG + stat.ML | 每月 | |

---

> **历史勘误**
>
> - 2026-06-08: 建立本清单，源于 ArchiMate 4.0 虚假发布声明、MCP 版本混乱、Martin Kleppmann 不实引用等 6 项事实错误的系统性修复。
>
> **关联文件**
>
> - `SUBSEQUENT_PLAN_2026.md` 决策 5A
> - `99-reference/external-links/authoritative-sources.md`
> - `99-reference/audit/comprehensive-gap-analysis-2026-06-08.md`
