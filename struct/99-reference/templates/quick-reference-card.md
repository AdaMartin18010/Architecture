# 架构复用快速参考卡

> **版本**: 2026-06-06
> **用途**: 一张卡片快速回顾架构复用的核心概念和决策要点

---

## 四层架构复用

```
业务层    → 业务能力、价值流、业务服务
应用层    → 应用服务、API 契约、数据架构
组件层    → 组件、库、接口契约、设计模式
功能层    → 函数、算法、业务规则、工作流
```

## 复用决策三问

1. **稳定性**: 该资产是否足够稳定以支持复用？
2. **通用性**: 该资产是否在多个上下文中适用？
3. **成本**: 复用成本是否显著低于自研？

## 关键公理速查

| 公理 | 核心命题 |
|------|---------|
| M.1 | 架构 = 约束集合；复用 = 约束传递 |
| M.2 | 复用 = 共性 + 变性的分离与绑定 |
| M.3 | 复用层次不可约化 |
| 4.1 | 接口契约强度 ∝ 复用信任度 |
| V.T1 | AAF < 0.7 是 ROI 为正的必要条件 |
| S.T1 | SLSA(A) ≤ min(SLSA(Bᵢ)) |
| AI.1 | LLM Agent 需要概率性契约 |

## 标准对齐速查

| 主题 | 关键标准 |
|------|---------|
| 架构描述 | ISO 42010, TOGAF, ArchiMate |
| 供应链安全 | SLSA 1.0, SPDX, CycloneDX |
| 工业 IoT | IEC 63278 (AAS), OPC UA FX, ISA-95 |
| 形式化验证 | TLA+, Alloy, Coq, Rust Type System |
| AI 原生 | MCP 2026-07-28, A2A v1.0 |

## 工具链速查

| 用途 | 工具 |
|------|------|
| SBOM 生成 | Syft, Trivy, GitHub Dependency Graph |
| 漏洞扫描 | Snyk, OWASP DC, Dependabot |
| 形式化验证 | TLA+ Toolbox, Alloy Analyzer, Kani |
| 架构建模 | Archi, Enterprise Architect, draw.io |
| IDP | Backstage, Port, Cortex |
| AI Agent | LangGraph, CrewAI, Google ADK |

## 反模式清单

- [ ] 分布式单体
- [ ] 共享数据库
- [ ] God Interface
- [ ] 过度工程化的复用
- [ ] 版本地狱
- [ ] 抽象泄漏

## 质量门禁

- [ ] 单元测试覆盖率 ≥ 80%
- [ ] 无 HIGH/CRITICAL 安全漏洞
- [ ] API 文档完整
- [ ] 使用示例 ≥ 3 个
- [ ] SemVer 声明清晰
- [ ] SBOM 已生成

---

> 最后更新: 2026-06-06
