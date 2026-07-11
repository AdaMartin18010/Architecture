# 03 攻击向量与攻击树

> **定位**: 系统化分析软件供应链攻击路径，为纵深防御与威胁建模提供决策基础。
> **权威来源**: SLSA、OpenSSF、NIST SP 800-204D、OWASP SCVS、MITRE ATT&CK。

---

## 文件清单

| 文件 | 说明 | 用途 |
|------|------|------|
| `attack-tree.md` | 软件供应链攻击树主文档 | 7 大攻击路径详解、典型案例、防御矩阵 |
| `attack-tree.mmd` | Mermaid `flowchart TD` 源文件 | 在 Markdown/GitHub/Mermaid Live Editor 中渲染 |
| `attack-tree.dot` | Graphviz DOT 源文件 | 生成 PDF/PNG/SVG 高清矢量图 |
| `attack-tree-mitre-mapping.md` | MITRE ATT&CK 映射 | Technique / Mitigation 速查与参考链接 |
| `attack-tree-interactive.py` | Python CLI 可视化工具 | 生成 HTML/Mermaid/DOT，支持 MITRE 标注与自测 |

---

## `attack-tree-interactive.py` 用法

### 1. 生成 HTML 交互式报告（默认）

```bash
# 生成全部场景
python attack-tree-interactive.py --format html --output report.html

# 仅生成指定场景
python attack-tree-interactive.py --scenario dependency-confusion --output dep-confusion.html

# 可用场景
python attack-tree-interactive.py --scenario all
# dependency-confusion, typosquatting, maintainer-takeover,
# build-system-compromise, upstream-repo-tampering
```

### 2. 生成 Mermaid 攻击树

```bash
# 基础版本
python attack-tree-interactive.py --format mermaid --output attack-tree.mmd

# 包含 MITRE ATT&CK Technique ID
python attack-tree-interactive.py --format mermaid --mitre --output attack-tree-mitre.mmd
```

### 3. 生成 Graphviz DOT 攻击树

```bash
# 基础版本
python attack-tree-interactive.py --format graphviz --output attack-tree.dot

# 包含 MITRE ATT&CK Technique ID（以 tooltip 形式写入 SVG）
python attack-tree-interactive.py --format graphviz --mitre --output attack-tree-mitre.dot
```

### 4. 转换为 PDF/PNG/SVG

```bash
# 使用 Graphviz 命令行
dot -Tsvg attack-tree.dot -o attack-tree.svg
dot -Tpng attack-tree.dot -o attack-tree.png
dot -Tpdf attack-tree.dot -o attack-tree.pdf

# 使用 Mermaid CLI
mmdc -i attack-tree.mmd -o attack-tree.svg -b transparent
```

### 5. 内置自测

```bash
python attack-tree-interactive.py --test
```

预期输出：

```text
TEST PASSED
  - HTML nodes: 35
  - Mermaid lines: 263
  - Graphviz lines: 261
  - MITRE annotations present in Mermaid and Graphviz
```

---

## 攻击树图例

| 节点类型 | Mermaid 形状 | Graphviz 形状 | 含义 |
|---------|-------------|---------------|------|
| OR 节点 | 圆角矩形 | 圆角矩形 | 任一子路径成功即可 |
| AND 节点 | 菱形 | 菱形 | 必须同时满足所有子条件 |
| 叶节点 | 矩形 / 椭圆 | 椭圆 | 原子级攻击手段 |

| 风险等级 | 颜色 | 说明 |
|---------|------|------|
| Critical | `#e53e3e` | 红色，最高优先级 |
| High | `#dd6b20` | 橙色 |
| Medium | `#d69e2e` | 黄色 |
| Low | `#38a169` | 绿色 |

---

## 与 MITRE ATT&CK 的映射

详见 `attack-tree-mitre-mapping.md`。核心映射：

| 攻击路径 | 主 Technique | 相关 Techniques |
|---------|-------------|----------------|
| 3.1 开发环境渗透 | T1195.001 | T1078, T1552, T1566, T1056 |
| 3.2 构建系统篡改 | T1195.001 | T1059, T1078, T1552 |
| 3.3 包管理器投毒 | T1195.001 | T1583, T1584, T1078 |
| 3.4 依赖混淆 | T1195.001 | T1593, T1594, T1071, T1567 |
| 3.5 上游代码植入 | T1195.001 | T1071, T1199 |
| 3.6 分发渠道劫持 | T1195.001 | T1584, T1557, T1553 |
| 3.7 运行时加载恶意组件 | T1195.001 | T1059, T1071, T1105, T1574 |

---

## 维护说明

- 修改攻击树结构时，请同步更新 `attack-tree.md`、`attack-tree.mmd`、`attack-tree.dot` 以及 `attack-tree-interactive.py` 中的 `SUPPLY_CHAIN_SEVEN_PATHS` 数据。
- 新增或调整 MITRE Technique 映射时，同步更新 `attack-tree-mitre-mapping.md` 与脚本中的 `mitre` 字段。
- 每次修改后运行 `python attack-tree-interactive.py --test` 验证三种格式输出正常。

---

> 最后更新: 2026-06-12


---

## 补充章节

## 概念定义

**定义**：供应链攻击向量指攻击者通过依赖注入、构建环境污染、仓库劫持、typosquatting、恶意贡献等路径，将有害代码引入复用资产并传播到下游系统。

## 示例

**示例**：攻击者在流行 npm 包名中注册拼写错误包（typosquat），诱导开发者安装并窃取环境变量；通过依赖扫描与私有仓库策略可有效缓解。

## 反例

**反例**：安全团队仅关注自有代码漏洞扫描，忽视第三方依赖与 CI/CD 凭证安全，导致攻击者通过被入侵的构建代理注入后门。

## 分析

**分析**：攻击向量分析应从“防御自家代码”转向“审计整条供应链”，覆盖人、工具与仓库。