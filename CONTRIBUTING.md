# 贡献指南

> **版本**: 2026-07-08
> **适用范围**: 软件工程架构复用知识体系项目

感谢你对本项目的关注！本指南帮助你快速了解如何参与贡献。

---

## 1. 贡献类型

我们欢迎以下形式的贡献：

- **内容补充**: 新增主题、案例、示例或反例
- **标准对齐**: 修正或更新国际标准引用
- **勘误**: 修正事实性错误、死链、格式问题
- **工具改进**: 改进 health-check、link-checker、standard-tracker 等脚本
- **国际化**: 英文摘要、术语翻译、英文文档
- **可视化**: Mermaid 图、架构图、幻灯片

---

## 2. 贡献流程

1. **Fork 仓库**（如果你是外部贡献者）
2. **创建 feature branch**: `git checkout -b feature/your-topic`
3. **修改或新增文件**: 遵循 `99-reference/book-format-guide.md`
4. **运行健康检查**: `python scripts/health-check.py`
5. **提交 PR**: 描述变更原因、影响范围与权威来源

---

## 3. 内容规范

### 3.1 文件结构

- 结构化内容放在 `struct/`
- 聚合卷册与历史快照放在 `view/`
- 工具脚本放在 `scripts/` 或 `struct/99-reference/tools/`
- 报告放在 `reports/`
- 交付物放在 `dist/`

### 3.2 Markdown 格式

- 使用 ATX 标题（`#` 而非 `=`）
- 标题层级不超过 4 级
- 表格前后保留空行
- 链接使用 Markdown 尖括号 `<https://...>` 或 `[文本](路径)`

### 3.3 标准引用

- 优先引用 `struct/99-reference/standards-index/authoritative-sources-v2.md` 中的条目
- 必须提供官方 URL
- 必须区分「已发布」「草案」「征求意见稿」「路线图」

### 3.4 术语

- 新术语请同步补充到 `struct/99-reference/glossary/glossary-master.md`
- 英文术语请补充到 `struct/99-reference/glossary/glossary-bilingual.md`

---

## 4. 质量门禁

提交 PR 前必须运行：

```bash
python scripts/health-check.py
```

确保：

- `struct/` 与 `view/` 质量门控 100% 通过
- 链接检查无死链
- 交叉索引一致
- 模板 padding 检查通过

---

## 5. 审查标准

维护者会重点审查：

- 权威来源是否官方、是否最新
- 是否存在事实性错误
- 是否破坏现有交叉引用
- 是否符合格式规范
- 是否通过 health-check

---

## 6. 行为准则

- 尊重不同背景与观点
- 以建设性方式提出批评
- 专注于技术与内容本身
- 遵守项目许可证

---

## 7. 联系方式

- 提交 Issue 或 Discussion 进行交流
- 重大变更建议先创建 Issue 讨论方向

---

> **最后更新**: 2026-07-08
