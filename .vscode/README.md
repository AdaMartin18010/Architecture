# VSCode/Cursor 配置说明

本目录包含 VSCode/Cursor 的配置文件，用于在保存 Markdown 文件时自动格式化。

## 📦 需要安装的扩展

打开 Cursor/VSCode 后，会自动提示安装推荐的扩展，或者手动安装：

1. **Markdownlint** (必需)
   - ID: `DavidAnson.vscode-markdownlint`
   - 功能：Markdown 格式检查和自动修复

2. **Markdown All in One** (推荐)
   - ID: `yzhang.markdown-all-in-one`
   - 功能：TOC 生成、快捷键、列表自动续写等

## ⚙️ 配置文件说明

### `settings.json`

主要配置：

- ✅ 保存时自动格式化 Markdown
- ✅ 自动删除行尾空格
- ✅ 文件末尾自动添加新行
- ✅ 允许使用 HTML 标签（`<details>`, `<summary>` 等）
- ✅ 允许同级标题重复

### `.markdownlint.json`

Markdownlint 规则配置（项目根目录）：

- MD033: false - 允许内联 HTML
- MD024: siblings_only - 允许非同级标题重复
- MD013: false - 不限制行长度
- MD012: false - 允许多个空行

## 🚀 使用方法

### 自动格式化

1. 打开任意 Markdown 文件
2. 修改内容
3. 按 `Ctrl+S` (Windows) 或 `Cmd+S` (Mac) 保存
4. 文件会自动格式化

### 手动格式化

- **格式化整个文档**: `Shift+Alt+F` (Windows) / `Shift+Option+F` (Mac)
- **格式化选中内容**: 选中文本后右键 → "Format Selection"

### 查看和修复 Linter 错误

1. 打开 Markdown 文件
2. 查看编辑器中的波浪线提示
3. 点击灯泡图标 💡 查看快速修复选项
4. 或在命令面板中运行: `Markdownlint: Fix all supported markdownlint violations in document`

## 🎯 快捷键

| 功能 | Windows/Linux | Mac |
| ------ | -------------- | ----- |
| 保存并格式化 | `Ctrl+S` | `Cmd+S` |
| 格式化文档 | `Shift+Alt+F` | `Shift+Option+F` |
| 修复所有错误 | `Ctrl+Shift+P` → "Fix all" | `Cmd+Shift+P` → "Fix all" |

## 📝 规则说明

### 允许的格式

```markdown
<!-- ✅ 允许使用 HTML -->
<details>
<summary>点击展开</summary>
内容
</details>

<!-- ✅ 允许重复标题（不同章节） -->
## 概述
### 示例
## 实现
### 示例  <!-- 允许，因为不是同级 -->

<!-- ✅ 允许长行（代码块、链接等） -->
这是一个很长很长很长的行...
```

### 自动修复的问题

- ❌ 行尾空格 → ✅ 自动删除
- ❌ 缺少文件末尾新行 → ✅ 自动添加
- ❌ 不一致的列表缩进 → ✅ 自动修正
- ❌ 代码块缺少语言标识 → ✅ 自动添加空标识

## 🔧 自定义配置

如果需要修改规则，编辑以下文件：

- **VSCode 设置**: `.vscode/settings.json`
- **Markdownlint 规则**: `.markdownlint.json`（项目根目录）

## 🐛 故障排除

### 格式化不生效

1. 确认已安装 Markdownlint 扩展
2. 重新加载窗口: `Ctrl+Shift+P` → "Reload Window"
3. 检查输出面板: `Ctrl+Shift+U` → 选择 "Markdownlint"

### 某些规则想要禁用

在 `.markdownlint.json` 中设置为 `false`:

```json
{
  "MD规则编号": false
}
```

### 某个文件想要跳过检查

在文件开头添加注释：

```markdown
<!-- markdownlint-disable -->
文件内容
<!-- markdownlint-enable -->
```

或禁用特定规则：

```markdown
<!-- markdownlint-disable MD033 -->
<details>内容</details>
<!-- markdownlint-enable MD033 -->
```

## 概念定义

- **Markdownlint**：基于 Node.js 的 Markdown 静态检查工具，通过规则集（如 MD013 行长度、MD033 HTML 标签、MD024 重复标题）统一文档格式。
- **EditorConfig / VSCode Settings**：编辑器配置层，定义保存行为、格式化规则与文件编码，确保多维护者环境下文档风格一致。
- **Lint-as-Code**：将文档格式规则纳入版本控制，使写作规范像代码一样可审计、可复用、可自动化。

## 反例/反模式

- **反模式 1：禁用所有 Linter 规则**。为省事关闭 MD013/MD024，导致长行、重复标题泛滥，降低长文档可维护性。
- **反模式 2：本地不安装扩展，依赖 CI 发现格式问题**。反馈循环过长，返工成本高。
- **反模式 3：配置文件与项目约定脱节**。例如允许 HTML 但实际文档大量依赖 HTML 布局，破坏 Markdown 原生可移植性。

## 权威来源

> **权威来源**:
>
> - David Anson. *markdownlint*. GitHub. <https://github.com/DavidAnson/markdownlint>
> - Microsoft. *Markdown and Visual Studio Code*. <https://code.visualstudio.com/docs/languages/markdown>
> - EditorConfig. *EditorConfig Specification*. <https://editorconfig-specification.readthedocs.io/>
>
> **核查日期**: 2026-07-07

## 分析

`.vscode/` 配置将文档格式规则下沉到编辑器层，是本项目“质量左移”策略的一部分。它把原本由 `scripts/quality-gate.py` 在 CI 阶段发现的问题提前到保存瞬间，降低修复成本。但该层仅解决格式问题，概念正确性、权威来源、反例完整性仍需人工与门控脚本共同保证。

---

## 📚 参考文档

- [Markdownlint 规则列表](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [VSCode Markdown 支持](https://code.visualstudio.com/docs/languages/markdown)
