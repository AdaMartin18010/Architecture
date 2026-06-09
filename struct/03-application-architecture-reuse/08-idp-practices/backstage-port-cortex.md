# P5-T5：Backstage / Port / Cortex IDP 复用实践

> **权威来源**：backstage.io、CNCF Platform Engineering Maturity Model（2026 刷新中）、Spotify Plugins 生态
> **版本**：2026-06
> **适用范围**：平台工程团队选型、Golden Path 建设、复用度量体系

---

## 1. IDP 市场格局（2026）

### 1.1 核心玩家概览

| 平台 | 模式 | 目标规模 | 核心定位 |
|------|------|---------|---------|
| **Backstage** | 开源（Apache 2.0） | 1000+ 工程师 | 可定制开发者门户，生态最丰富 |
| **Port** | SaaS / 私有化 | 200-2000 工程师 | 低代码 IDP，快速上线 |
| **Cortex** | SaaS / 私有化 | 全规模 | Scorecards + 服务成熟度追踪 |

### 1.2 选型对比矩阵

| 维度 | Backstage | Port | Cortex |
|------|-----------|------|--------|
| **成本结构** | 自托管基础设施 + 维护人力 | SaaS 订阅（按开发者计费） | SaaS 订阅 + 专业服务 |
| **上线时间** | 3-6 个月（需团队投入） | 2-4 周（开箱即用） | 4-8 周（侧重成熟度） |
| **定制性** | ★★★★★（代码级定制） | ★★★☆☆（配置 + 低代码） | ★★★☆☆（模板 + API） |
| **插件/集成生态** | 200+ 社区插件 | 100+ 原生集成 | 80+ 集成（聚焦 DevOps 工具链） |
| **Software Catalog** | 核心能力（YAML 定义） | 核心能力（UI + API） | 辅助能力（自动发现为主） |
| **Scaffolder** | 内置（模板引擎） | 内置（工作流编排） | 较弱（依赖外部 CI） |
| **TechDocs** | 内置（MKDocs 集成） | 基础文档支持 | 较弱 |
| **Scorecards** | 需插件（如 Soundcheck） | 内置 | **核心能力** |

### 1.3 选型决策建议

- **选择 Backstage**：组织已有前端/Node.js 团队、需要深度定制、工程师规模大于500人、愿意长期投入平台工程人力
- **选择 Port**：需要快速验证 IDP 价值、工程师规模在200到1000人之间、偏好 SaaS 免运维模式
- **选择 Cortex**：已有成熟 CI/CD 但缺乏服务治理、需要强制的成熟度评分和合规追踪能力

**混合策略**：部分大型组织采用 **Backstage 作为主门户 + Cortex 作为成熟度数据源** 的架构，通过 Backstage 插件集成 Cortex Scorecards，兼顾定制性和治理深度。这种混合架构允许平台团队在保留 Backstage 强大扩展性的同时，复用 Cortex 成熟的评分引擎和合规报告能力。

---

## 2. Golden Path 作为复用载体

### 2.1 Scaffolder 模板复用

Golden Path 是 IDP 的核心复用机制——它将"最佳实践"编码为可一键生成的项目模板。Golden Path 的本质是**将隐性知识显性化、将最佳实践标准化、将标准执行自动化**。

**Backstage Scaffolder 模板结构**：

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: microservice-golden-path
  title: "标准微服务 Golden Path"
  description: "包含 CI/CD、可观测性、安全扫描的标准模板"
spec:
  owner: platform-team
  type: service
  parameters:
    - title: 基础配置
      required: [serviceName, language]
      properties:
        serviceName:
          type: string
          description: 服务名称
        language:
          type: string
          enum: [go, rust, python, java]
  steps:
    - id: fetch-base
      name: 获取基础代码骨架
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.serviceName }}
          language: ${{ parameters.language }}
    - id: ci-cd
      name: 生成 CI/CD 流水线
      action: fetch:template
      input:
        url: ./templates/cicd
    - id: register
      name: 注册到 Software Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.fetch-base.output.repoContentsUrl }}
```

**复用价值**：

- 新服务创建时间从 2 周缩短至 10 分钟
- 强制包含安全扫描（SAST/DAST）、可观测性（OpenTelemetry）、文档（TechDocs）
- 模板版本化管理，升级时批量推送至基于该模板创建的服务
- 降低认知负荷：开发者无需了解底层基础设施细节，专注于业务逻辑

### 2.2 Software Catalog 作为资产目录

Software Catalog 是组织级软件资产的统一目录，其复用价值体现在跨团队的知识共享和依赖关系透明化：

| 层级 | 实体类型 | 复用场景 |
|------|---------|---------|
| **系统层** | System | 业务域边界定义，复用系统架构认知 |
| **服务层** | Component/Service | API 契约发现、依赖关系可视化 |
| **资源层** | Resource | 数据库、消息队列等基础设施的共享状态 |
| **API 层** | API | OpenAPI 规范集中托管，跨团队契约复用 |
| **用户层** | User/Group | 组织关系映射，所有权自动分配 |

**关键实践**：将 Catalog 中的 API 实体与 NASA RRL（Reuse Readiness Level）评级关联，标记每个 API 的复用成熟度。高 RRL 等级的 API 应在 Catalog 中标注为"推荐复用"，并在开发者门户首页优先展示。

### 2.3 TechDocs 作为知识复用

Backstage 的 TechDocs 将文档与代码仓库绑定，实现"文档即代码"（Docs as Code）：

- **mkdocs.yml** 定义文档结构，与代码同版本管理
- **文档内嵌组件**自动读取 Software Catalog 元数据（所有者、SLA、依赖）
- **搜索聚合**跨所有服务文档提供统一检索入口
- **文档健康度评分**自动检查必填章节（架构概述、API 参考、运行手册、故障排查）的完整性

**复用度量**：文档健康度 =（必填章节完成数 / 总必填章节数）× 100%。纳入服务成熟度评分。

---

## 3. 平台工程成熟度

### 3.1 CNCF 五维度模型

CNCF Platform Engineering Maturity Model（2026 年刷新中）定义了五个评估维度：

| 维度 | Level 1（临时） | Level 2（可复现） | Level 3（可扩展） | Level 4（优化） |
|------|---------------|-----------------|-----------------|---------------|
| **Investment（投入）** | 自愿贡献 | 专用平台团队 | 平台即产品 | 平台生态共建 |
| **Adoption（采用）** | 口头推广 | 文档化路径 | 强制 Golden Path | 自服务度量驱动 |
| **Interfaces（接口）** | 工单驱动 | 脚本/CLI | 开发者门户（IDP） | API + 生态集成 |
| **Operations（运维）** | 手工运维 | IaC 自动化 | 平台 SRE + 可观测性 | 自愈 + 混沌工程 |
| **Measurement（度量）** | 无度量 | 基础指标 | 平台 ROI + DORA | 预测性分析 |

### 3.2 2026 刷新中的 AI 集成内容

2026 年 CNCF 刷新版本新增了 **AI-Native Platform** 维度，核心关注点包括：

- **Agent 托管**：IDP 是否提供 Agent 注册、发现、治理能力
- **AI 辅助开发**：Copilot 集成、代码生成模板、智能文档补全
- **模型服务目录**：将 ML 模型纳入 Software Catalog 统一管理
- **AI 成本可见性**：GPU/Token 消耗在开发者门户中的实时展示

**建议**：组织在评估当前成熟度时，应将 AI 维度作为**增量评估项**，而非独立维度，避免与现有五维体系割裂。建议从 Level 2 可复现阶段开始同步建设 AI 能力，避免平台工程与 AI 工程形成组织孤岛。

---

## 4. 复用度量指标

### 4.1 IDP 原生度量

| 指标 | 定义 | 目标值 | 采集方式 |
|------|------|--------|---------|
| **模板使用率** | 新服务通过 Golden Path 创建的比例 | 大于80% | Scaffolder 日志统计 |
| **目录覆盖率** | 生产服务在 Software Catalog 中的注册率 | 100% | Catalog API 定期扫描 |
| **文档健康度** | 服务文档必填章节完成率 | 大于90% | TechDocs 构建结果分析 |
| **自助服务率** | 开发者无需平台团队介入完成的操作比例 | 大于70% | IDP 审计日志分析 |
| **路径偏离率** | 服务偏离 Golden Path 的告警比例 | 小于10% | Scorecard 规则引擎 |
| **复用请求数** | 月度通过 Catalog 发现并复用的 API/组件数 | 逐月增长 | API 网关调用链分析 |

### 4.2 与 NASA RRL / RCMM 的映射

NASA 的复用成熟度模型可与 IDP 度量体系建立对照：

| NASA RRL 等级 | RCMM 阶段 | IDP 映射 | 判定标准 |
|--------------|----------|---------|---------|
| RRL 1-2（概念/开发中） | 初始 | Catalog 中标记为 experimental | 无 Golden Path，仅原型 |
| RRL 3-4（验证/集成中） | 可重复 | Catalog 中标记为 beta | 有对应 Golden Path 模板 |
| RRL 5-6（已验证/已发布） | 已定义 | Catalog 中标记为 production | 模板使用率大于50%，文档健康度大于80% |
| RRL 7-8（已采用/已维护） | 已管理 | Scorecard 评分大于80 | 自助服务率大于70%，路径偏离率小于10% |
| RRL 9（已优化） | 优化 | 跨组织外部共享 | 组件被外部团队或开源社区复用 |

**自动化映射**：在 Backstage 中通过自定义 Processor 自动将 Catalog 实体的元数据（生命周期、Scorecard 评分、使用统计）映射为 RRL 等级，展示在实体卡片中。这消除了人工评估的主观性，使复用成熟度成为客观可度量的指标。

---

## 5. 实施路线图建议

| 阶段 | 时间 | 目标 | 关键动作 |
|------|------|------|---------|
| **奠基期** | 0-2月 | 搭建 Catalog，导入现有服务 | 批量导入 YAML、定义所有权模型、建立实体关系 |
| **模板期** | 2-4月 | 上线 3-5 条 Golden Path | 覆盖主流服务类型（API、前端、Job、ML 推理） |
| **治理期** | 4-6月 | 引入 Scorecards，建立度量 | 定义成熟度规则、集成 CI/CD 数据源、设置告警 |
| **扩展期** | 6-12月 | 生态集成、AI 能力接入 | 插件开发、Copilot 集成、模型目录、Agent 注册 |

---

## 参考文献

1. Backstage Documentation, <https://backstage.io/docs>
2. Backstage v1.42.0 Release Notes — New Frontend System GA
3. Port Documentation, <https://docs.getport.io>
4. Cortex Documentation, <https://docs.cortex.io>
5. CNCF Platform Engineering Maturity Model, 2026 Refresh (Draft)
6. Spotify Backstage Plugins Marketplace, <https://backstage.io/plugins>
7. NASA Reuse Readiness Levels (RRL), NPR 7150.2D
8. NASA Reuse Capability Maturity Model (RCMM)
