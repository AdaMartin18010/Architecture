# 零信任软件供应链原则

> **版本**: 2026-06-06
> **定位**: 将零信任安全模型应用于软件供应链

---

## 1. 零信任的核心原则

零信任（Zero Trust）的安全模型基于以下原则：

1. **永不信任，始终验证** (Never Trust, Always Verify)
2. **假设 breach** (Assume Breach)
3. **最小权限** (Least Privilege)
4. **微分段** (Micro-segmentation)
5. **持续验证** (Continuous Verification)

> **公理 ZT.1** (Zero Trust Transitivity): 在软件供应链中，零信任要求对**每一个组件**、**每一个环节**、**每一次构建**都进行验证，而非信任上游供应商的安全声明。

---

## 2. 零信任供应链的五个验证点

```text
软件供应链
│
├── 1. 源代码验证
│   ├── 提交者身份验证（SSH/GPG）
│   ├── 代码审查（至少 2 人）
│   ├── 静态安全分析
│   └── 秘密扫描
│
├── 2. 依赖验证
│   ├── SBOM 生成与验证
│   ├── 已知漏洞扫描
│   ├── 许可证合规检查
│   └── 依赖来源验证（非 typosquatting）
│
├── 3. 构建验证
│   ├── 构建环境隔离
│   ├── 构建步骤签名
│   ├── 可复现构建验证
│   └── SLSA Provenance 验证
│
├── 4. 制品验证
│   ├── 二进制签名验证
│   ├── 哈希校验
│   ├── 容器镜像扫描
│   └── 运行时行为基线
│
└── 5. 部署验证
    ├── 部署审批流程
    ├── 运行时完整性监控
    ├── 网络微分段
    └── 持续行为监控
```

---

## 3. 关键控制措施

### 源代码层

| 控制 | 工具/方法 |
|------|----------|
| 强制提交签名 | Git commit signing |
| 分支保护 | GitHub/GitLab branch protection |
| 代码审查 | Pull request review |
| 静态分析 | Semgrep, CodeQL, SonarQube |
| 秘密检测 | GitLeaks, TruffleHog |

### 依赖层

| 控制 | 工具/方法 |
|------|----------|
| SBOM 生成 | Syft, Trivy, GitHub Dependency Graph |
| 漏洞扫描 | Snyk, Dependabot, OWASP DC |
| 依赖锁定 | lockfile, hash pinning |
| 私有注册表 | Nexus, Artifactory |

### 构建层

| 控制 | 工具/方法 |
|------|----------|
| 隔离构建环境 | GitHub Actions hosted runners |
| SLSA Provenance | SLSA GitHub Generator |
| 可复现构建 | Reproducible Builds |
| 构建签名 | Sigstore/cosign |

### 部署层

| 控制 | 工具/方法 |
|------|----------|
| 镜像签名验证 | Kyverno, OPA/Gatekeeper |
| 运行时安全 | Falco, Tetragon |
| 网络策略 | Kubernetes NetworkPolicy |
| 持续监控 | Prometheus + Alertmanager |

---

## 4. 关键定理

> **公理 ZT.2** (Defense-in-Depth Redundancy): 零信任不是单一控制措施，而是**多层控制的重叠**。任何单一控制措施的失效不应导致安全边界崩溃。
> **定理 ZT.T1** (SBOM Completeness Limit): 完整的 SBOM 是零信任供应链的**必要但不充分**条件。SBOM 只能回答"有什么"，不能回答"是否安全"。安全还需要漏洞扫描、行为分析、持续监控。

---

## 5. 成熟度模型

| 级别 | 特征 |
|------|------|
| **L1 基础** | 有 SBOM，有漏洞扫描 |
| **L2 管理** | 依赖锁定，构建签名，代码审查 |
| **L3 定义** | SLSA L3，可复现构建，部署验证 |
| **L4 量化** | 运行时监控，行为基线，自动化响应 |
| **L5 优化** | AI 辅助威胁检测，自适应安全 |

---

> 最后更新: 2026-06-06
