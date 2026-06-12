# 标准引用规范：版本 + URL + 核查日期三元组

> **版本**: 2026-06-10
> **适用范围**: 本项目全部 Markdown 文档
> **强制执行**: 自 2026-06-10 起，所有新增或更新的标准引用必须遵循本规范

---

## 1. 目的

防止以下问题再次发生：

- ArchiMate 4.0 虚假发布声明（2026-06-08 HOTFIX-1）
- MCP 版本号引用混乱（2026-06-08 HOTFIX-2）
- ISO/IEC 25010 版本号滞后（2026-06-08 HOTFIX-4）

通过强制**版本 + URL + 核查日期**三元组，确保所有标准引用可追溯、可验证、可审计。

---

## 2. 引用格式规范

### 2.1 文档头部元数据

每篇涉及标准对齐的文档，必须在头部 YAML 或引用块中包含：

```markdown
> **对齐标准**: [标准编号]:[年份/版本], [标准编号]:[年份/版本]
> **核查日期**: YYYY-MM-DD
> **来源 URL**:
> - [标准1]: <URL>
> - [标准2]: <URL>
```

**示例（正确）**：

```markdown
> **对齐标准**: ISO/IEC/IEEE 42010:2022, ISO/IEC 12207:2026
> **核查日期**: 2026-06-10
> **来源 URL**:
> - ISO 42010: <https://www.iso.org/standard/74296.html>
> - ISO 12207: <https://www.iso.org/obp/ui/#iso:std:iso-iec-ieee:12207:ed-2:v1:en>
```

**示例（错误）**：

```markdown
> **对齐标准**: ISO 42010, ISO 12207  <!-- 缺少版本号 -->
> **来源**: 网络  <!-- 缺少具体 URL -->
```

### 2.2 正文内联引用

正文中首次提及某标准时，必须使用完整格式：

```markdown
**ISO/IEC/IEEE 42010:2022**（架构描述）[来源](https://www.iso.org/standard/74296.html)（核查日期: 2026-06-10）
```

后续可简写为：

```markdown
42010:2022
```

但必须在文档末尾的"权威来源"章节中列出完整信息。

### 2.3 文档末尾权威来源章节

所有文档必须在末尾包含以下章节：

```markdown
---

> **权威来源**:
>
> - [标准全名]. [版本/年份]. [URL] (核查日期: YYYY-MM-DD)
> - [论文/书籍]. [作者]. [年份]. [URL/DOI] (核查日期: YYYY-MM-DD)
>
> **核查日期**: YYYY-MM-DD
```

---

## 3. 核查日期规则

| 标准状态 | 核查频率 | 示例 |
|:---|:---:|:---|
| **已发布且稳定**（如 42010:2022） | 每年复审一次 | 每年 1 月统一核查 |
| **已发布但预计更新**（如 42030:2019 → AWI 修订中） | 每季度跟踪 | 3/6/9/12 月核查 |
| **草案/DIS/FDIS**（如 DIS 42042） | 每月跟踪 | 持续跟踪至发布 |
| **技术规范/社区标准**（如 MCP, SLSA） | 每月跟踪 | 关注官方 Changelog |
| **法规**（如 EU CRA） | 每季度或按事件触发 |  deadlines 前密集跟踪 |

### 3.1 核查操作步骤

1. **访问官方来源 URL**，确认页面显示的标准版本号与文档引用一致
2. **检查标准生命周期状态**（ISO: stages 00-95；IEEE: Active/Superseded）
3. **记录核查日期**，更新文档元数据
4. **如发现版本变更**，立即触发 HOTFIX 流程（参见 `99-reference/CHANGELOG.md`）

---

## 4. 标准来源分级

| 优先级 | 来源类型 | 示例 | 说明 |
|:---|:---:|:---|:---|
| **P0** | 官方标准组织 | ISO.org, IEC.ch, IEEE.org, The Open Group, OMG | 必须优先引用 |
| **P1** | 官方技术委员会文档 | JTC 1/SC 7 工作报告, WG 会议纪要 | 可作为过程引用 |
| **P2** | 权威第三方验证 | NIST, ENISA, CNCF, OpenSSF, Linux Foundation | 技术框架引用 |
| **P3** | 学术来源 | IEEE Xplore, ACM, arXiv (已发表/审稿中) | 研究内容引用 |
| **P4** | 厂商/社区博客 | Anthropic Blog, Google Cloud Blog, CNCF Blog | 仅用于补充说明，不可作为标准状态的唯一来源 |

> **红线规则**：
>
> - 不得以已正式发布/博客文章作为"标准已正式发布"的唯一证据
> - 引用 ArchiMate 版本时，必须以 The Open Group 官方页面为准
> - 引用 MCP 版本时，必须以 modelcontextprotocol.io 官方规范页为准

---

## 5. 常见标准核查入口

| 标准/框架 | 官方核查 URL | 备注 |
|:---|:---|:---|
| ISO 全部标准 | <https://www.iso.org/obp/ui/> | 使用标准号搜索 |
| IEC 全部标准 | <https://webstore.iec.ch/> | 可查看预览 |
| IEEE 标准 | <https://standards.ieee.org/> | 需订阅查看全文 |
| The Open Group (TOGAF/ArchiMate) | <https://www.opengroup.org/> | ArchiMate 版本以 archimate-forum 页为准 |
| OMG 规范 | <https://www.omg.org/spec/> | 含 RAS, SysML 等 |
| NIST 出版物 | <https://csrc.nist.gov/publications> | 含 SP 800 系列 |
| ENISA | <https://www.enisa.europa.eu/> | EU 网络安全 |
| OpenSSF / SLSA | <https://slsa.dev/> | 供应链安全 |
| MCP 规范 | <https://modelcontextprotocol.io/specification/> | 当前稳定版首页 |
| A2A 协议 | <https://google.github.io/A2A/> | Google / LF |
| CloudEvents | <https://cloudevents.io/> | CNCF |
| BIAN | <https://bian.org/> | 银行业架构 |
| TMForum | <https://www.tmforum.org/> | 电信架构 |

---

## 6. 自动化核查脚本（未来扩展）

建议在 `99-reference/tools/` 中开发自动化脚本：

```python
# 伪代码：标准引用核查脚本
# 路径: 99-reference/tools/citation-checker.py (未来开发)

import re
from datetime import datetime

STANDARD_PATTERNS = {
    "ISO": r"ISO/IEC(?:/IEEE)? \d+(?::\d{4})?",
    "IEEE": r"IEEE \d+(?:-\d{4})?",
    "TOGAF": r"TOGAF \d+(?:\.\d+)?",
    "ArchiMate": r"ArchiMate (?:3\.2|4\.0|3\.1)",
    "MCP": r"MCP (?:2025-11-25|2026-\d{2}-\d{2})",
}

def check_document(filepath):
    """
    检查文档是否包含核查日期和权威来源章节
    返回: (合规状态, 缺失项列表)
    """
    pass

def check_standard_version(standard_name, cited_version):
    """
    联网核查标准当前最新版本
    返回: (状态: current/outdated/draft, 官方最新版本)
    """
    pass
```

---

> **权威来源**:
>
> - ISO/IEC Directives, Part 2. Principles and rules for the structure and drafting of ISO and IEC documents. <https://www.iso.org/sites/directives/current/part2/index.xhtml>
> - The Open Group, ArchiMate Forum. <https://www.opengroup.org/archimate-forum/archimate-overview> (核查日期: 2026-06-10)
> - Model Context Protocol Specification. <https://modelcontextprotocol.io/specification/2025-11-25> (核查日期: 2026-06-10)
>
> **核查日期**: 2026-06-10
