# 供应链攻击树 MITRE ATT&CK 映射

> **版本**: 2026-06-12
> **定位**: 将 `attack-tree.md` 中的 7 条软件供应链攻击路径映射到 MITRE ATT&CK Enterprise 技术与缓解措施，便于与 SIEM/SOAR、威胁情报及红队演练对齐。
> **权威来源**: [MITRE ATT&CK Enterprise v16](https://attack.mitre.org/)

---

## 1. 映射总览

| 编号 | 攻击路径 | 主 Technique | 相关 Techniques | 主要 Mitigations | 风险等级 |
|------|---------|-------------|----------------|------------------|---------|
| 3.1 | 开发环境渗透 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | T1078, T1552, T1566, T1059 | M1013, M1017, M1026, M1027, M1030 | High |
| 3.2 | 构建系统篡改 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | T1059, T1078, T1552 | M1013, M1030, M1045, M1047, M1051 | Critical |
| 3.3 | 包管理器投毒 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | T1583, T1584, T1078 | M1013, M1016, M1019, M1021, M1045 | High |
| 3.4 | 依赖混淆 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | T1593, T1594, T1071 | M1013, M1016, M1021, M1047 | High |
| 3.5 | 上游代码植入 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | T1071, T1199, T1059 | M1013, M1045, M1047, M1051 | Critical |
| 3.6 | 分发渠道劫持 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | T1584, T1557, T1553 | M1030, M1037, M1041, M1042 | High |
| 3.7 | 运行时加载恶意组件 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | T1059, T1071, T1105, T1574 | M1038, M1042, M1045, M1052 | High |

---

## 2. 各路径详细映射

### 3.1 开发环境渗透（Compromise Development Environment）

**核心目标**: 通过控制开发者工作站、IDE 或本地工具链，向最终产品注入恶意代码。

| 子攻击手段 | MITRE Technique | 说明 |
|-----------|-----------------|------|
| 网络钓鱼攻击 | [T1566](https://attack.mitre.org/techniques/T1566/) Phishing | 窃取开发者凭据或诱导安装恶意扩展 |
| 凭证填充攻击 | [T1078](https://attack.mitre.org/techniques/T1078/) Valid Accounts | 使用泄露凭据登录开发者账户 |
| 键盘记录恶意软件 | [T1056](https://attack.mitre.org/techniques/T1056/) Input Capture | 捕获 IDE/仓库访问凭据 |
| 恶意 IDE 扩展 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | 通过插件市场分发恶意代码 |
| 被篡改的编译器 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | 经典“Trusting Trust”攻击 |

**缓解措施**: M1013 Application Developer Guidance、M1017 User Training、M1026 Privileged Account Management、M1027 Password Policies、M1030 Network Segmentation。

---

### 3.2 构建系统篡改（Compromise Build System）

**核心目标**: 在 CI/CD 或构建基础设施中植入后门，使恶意产物获得合法签名。

| 子攻击手段 | MITRE Technique | 说明 |
|-----------|-----------------|------|
| 被攻陷的 CI/CD 流水线 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | SolarWinds Orion (2020) 典型路径 |
| 恶意构建脚本 | [T1059](https://attack.mitre.org/techniques/T1059/) Command and Scripting Interpreter | 在 build script 中执行任意命令 |
| 伪造构建来源证明 | [T1078](https://attack.mitre.org/techniques/T1078/) Valid Accounts + [T1552](https://attack.mitre.org/techniques/T1552/) Unsecured Credentials | 盗用签名凭据伪造 provenance |
| 构建后替换二进制 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | 在 artifact repository 中 swaps 二进制 |

**缓解措施**: M1013 Application Developer Guidance、M1030 Network Segmentation、M1045 Code Signing、M1047 Audit、M1051 Update Software。

---

### 3.3 包管理器投毒（Compromise Package Manager）

**核心目标**: 在公共或私有包注册表中发布或篡改包，使下游消费者自动拉取恶意代码。

| 子攻击手段 | MITRE Technique | 说明 |
|-----------|-----------------|------|
| 拼写混淆 Typosquatting | [T1583](https://attack.mitre.org/techniques/T1583/) Acquire Infrastructure | 注册与流行包近似的包名 |
| 窃取维护者凭证 | [T1078](https://attack.mitre.org/techniques/T1078/) Valid Accounts | 合法包被恶意发布 |
| 社会工程学接管 | [T1199](https://attack.mitre.org/techniques/T1199/) Trusted Relationship | XZ Utils 后门 (2024) 前期步骤 |
| 操纵注册表元数据 | [T1584](https://attack.mitre.org/techniques/T1584/) Compromise Infrastructure | 控制注册表推荐算法或统计 |

**缓解措施**: M1013 Application Developer Guidance、M1016 Vulnerability Scanning、M1019 Threat Intelligence Program、M1021 Restrict Web-Based Content、M1045 Code Signing。

---

### 3.4 依赖混淆（Dependency Confusion Attack）

**核心目标**: 利用包解析器优先选择公共注册表高版本包的机制，使内部项目拉取攻击者发布的同名包。

| 子攻击手段 | MITRE Technique | 说明 |
|-----------|-----------------|------|
| 扫描公开仓库识别内部包名 | [T1593](https://attack.mitre.org/techniques/T1593/) Search Open Websites/Domains | 从公开代码中收集内部依赖名 |
| 分析错误信息 | [T1594](https://attack.mitre.org/techniques/T1594/) Search Victim-Owned Websites | 从 CI 日志/错误堆栈推断包名 |
| 发布更高版本到公共注册表 | [T1583](https://attack.mitre.org/techniques/T1583/) Acquire Infrastructure | Alex Birsan (2021) 经典研究 |
| 回连 C2 / 外泄数据 | [T1071](https://attack.mitre.org/techniques/T1071/) Application Layer Protocol | 混淆包内置数据回传 |

**缓解措施**: M1013 Application Developer Guidance、M1016 Vulnerability Scanning、M1021 Restrict Web-Based Content、M1047 Audit。

---

### 3.5 上游代码植入（Compromise Upstream Source）

**核心目标**: 在开源/第三方源代码仓库中植入后门，通过正常合并流程进入下游依赖。

| 子攻击手段 | MITRE Technique | 说明 |
|-----------|-----------------|------|
| 伪装良性的隐藏后门 PR | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | 通过测试文件、构建脚本隐藏载荷 |
| 利用对维护者的信任 | [T1199](https://attack.mitre.org/techniques/T1199/) Trusted Relationship | 长期社会工程学获取提交权限 |
| 强制推送重写历史 | [T1071](https://attack.mitre.org/techniques/T1071/) Application Layer Protocol / [T1491](https://attack.mitre.org/techniques/T1491/) Defacement | 篡改已发布标签或提交 |
| 破坏代码审查 | [T1078](https://attack.mitre.org/techniques/T1078/) Valid Accounts | 控制审查者账户绕过双人复核 |

**缓解措施**: M1013 Application Developer Guidance、M1045 Code Signing、M1047 Audit、M1051 Update Software。

---

### 3.6 分发渠道劫持（Compromise Distribution Channel）

**核心目标**: 在软件分发阶段（下载、CDN、镜像）篡改传输内容或重定向下载地址。

| 子攻击手段 | MITRE Technique | 说明 |
|-----------|-----------------|------|
| DNS 劫持 | [T1584](https://attack.mitre.org/techniques/T1584/) Compromise Infrastructure | 重定向下载域名 |
| BGP 劫持 | [T1584](https://attack.mitre.org/techniques/T1584/) Compromise Infrastructure | 劫持路由前缀 |
| 下载过程 MITM | [T1557](https://attack.mitre.org/techniques/T1557/) Man-in-the-Middle | Codecov Bash Uploader (2021) 类型事件 |
| 攻陷证书颁发机构 | [T1553](https://attack.mitre.org/techniques/T1553/) Subvert Trust Controls | 签发伪造 TLS 证书 |

**缓解措施**: M1030 Network Segmentation、M1037 Filter Network Traffic、M1041 Encrypt Sensitive Information、M1042 Disable or Remove Feature or Program。

---

### 3.7 运行时加载恶意组件（Runtime Malicious Component Loading）

**核心目标**: 利用运行时的动态加载、插件系统或解释器供应链，在程序运行阶段执行恶意代码。

| 子攻击手段 | MITRE Technique | 说明 |
|-----------|-----------------|------|
| 运行时无验证下载 | [T1105](https://attack.mitre.org/techniques/T1105/) Ingress Tool Transfer | 动态拉取远程模块 |
| 无沙箱的插件系统 | [T1059](https://attack.mitre.org/techniques/T1059/) Command and Scripting Interpreter | 插件具备完整进程权限 |
| 被攻陷的 JVM / Node.js / Python 运行时 | [T1195.001](https://attack.mitre.org/techniques/T1195/001/) Software Supply Chain Compromise | 解释器或运行时本身被污染 |
| 动态版本解析歧义 | [T1574](https://attack.mitre.org/techniques/T1574/) Hijack Execution Flow | 利用版本解析加载非预期组件 |

**缓解措施**: M1038 Execution Prevention、M1042 Disable or Remove Feature or Program、M1045 Code Signing、M1052 User Account Control。

---

## 3. Technique 与 Mitigation 速查表

### Techniques（技术）

| ID | 英文名称 | 中文含义 | 适用路径 |
|----|---------|---------|---------|
| T1195 | Supply Chain Compromise | 供应链妥协 | 全部 |
| T1195.001 | Software Supply Chain Compromise | 软件供应链妥协 | 全部 |
| T1059 | Command and Scripting Interpreter | 命令与脚本解释器 | 3.2, 3.7 |
| T1071 | Application Layer Protocol | 应用层协议 | 3.4, 3.5, 3.7 |
| T1078 | Valid Accounts | 有效账户 | 3.1, 3.2, 3.3, 3.5 |
| T1105 | Ingress Tool Transfer | 入口工具传输 | 3.7 |
| T1199 | Trusted Relationship | 信任关系 | 3.3, 3.5 |
| T1552 | Unsecured Credentials | 不安全的凭据 | 3.1, 3.2 |
| T1553 | Subvert Trust Controls | 颠覆信任控制 | 3.6 |
| T1557 | Man-in-the-Middle | 中间人 | 3.6 |
| T1566 | Phishing | 网络钓鱼 | 3.1 |
| T1567 | Exfiltration Over Web Service | 通过 Web 服务外泄 | 3.3, 3.4 |
| T1574 | Hijack Execution Flow | 劫持执行流 | 3.7 |
| T1583 | Acquire Infrastructure | 获取基础设施 | 3.3, 3.4 |
| T1584 | Compromise Infrastructure | 攻陷基础设施 | 3.3, 3.6 |
| T1593 | Search Open Websites/Domains | 搜索公开网站/域名 | 3.4 |
| T1594 | Search Victim-Owned Websites | 搜索受害者拥有的网站 | 3.4 |
| T1056 | Input Capture | 输入捕获 | 3.1 |
| T1491 | Defacement | 篡改 | 3.5 |

### Mitigations（缓解措施）

| ID | 英文名称 | 中文含义 | 适用路径 |
|----|---------|---------|---------|
| M1013 | Application Developer Guidance | 应用开发者指南 | 全部 |
| M1016 | Vulnerability Scanning | 漏洞扫描 | 3.2, 3.3, 3.4, 3.7 |
| M1017 | User Training | 用户培训 | 3.1, 3.3 |
| M1019 | Threat Intelligence Program | 威胁情报计划 | 3.3 |
| M1021 | Restrict Web-Based Content | 限制 Web 内容 | 3.3, 3.4 |
| M1026 | Privileged Account Management | 特权账户管理 | 3.1, 3.2 |
| M1027 | Password Policies | 密码策略 | 3.1 |
| M1030 | Network Segmentation | 网络分段 | 3.1, 3.2, 3.6 |
| M1037 | Filter Network Traffic | 过滤网络流量 | 3.6 |
| M1038 | Execution Prevention | 执行防护 | 3.7 |
| M1041 | Encrypt Sensitive Information | 加密敏感信息 | 3.6 |
| M1042 | Disable or Remove Feature or Program | 禁用或移除功能/程序 | 3.6, 3.7 |
| M1045 | Code Signing | 代码签名 | 3.2, 3.3, 3.5, 3.7 |
| M1047 | Audit | 审计 | 3.2, 3.4, 3.5 |
| M1051 | Update Software | 更新软件 | 3.2, 3.5 |
| M1052 | User Account Control | 用户账户控制 | 3.7 |

---

## 4. 参考链接

- [MITRE ATT&CK Enterprise Matrix](https://attack.mitre.org/matrices/enterprise/)
- [T1195 Supply Chain Compromise](https://attack.mitre.org/techniques/T1195/)
- [T1195.001 Software Supply Chain Compromise](https://attack.mitre.org/techniques/T1195/001/)
- [MITRE ATT&CK Mitigations](https://attack.mitre.org/mitigations/enterprise/)
- [SLSA Specification v1.0](https://slsa.dev/spec/v1.0/)
- [OpenSSF Supply Chain Security](https://openssf.org/)
- [NIST SP 800-204D](https://csrc.nist.gov/publications/detail/sp/800-204d/final)
- [OWASP SCVS](https://owasp.org/www-project-software-component-verification-standard/)

---

> **对齐验证**:
>
> - Technique 映射对照 MITRE ATT&CK Enterprise v16 官方条目验证。
> - 缓解措施覆盖 SLSA 1.0、OpenSSF、NIST SSDF 1.2 的核心控制。
> - 案例映射参见 `attack-tree.md` 第 4 节“典型案例映射”。
>
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