# 跨标准术语对照表

> **版本**: 2026-06-06
> **定位**: 建立不同标准/框架之间的术语映射，降低跨标准理解的摩擦

---

## ISO 42010 vs TOGAF 10

| ISO 42010 | TOGAF 10 | 说明 |
|-----------|---------|------|
| Architecture Description | Architecture Repository / Catalog | 架构描述的载体 |
| Stakeholder | Stakeholder | 利益相关者 |
| Concern | Concern / Architecture Requirement | 关注点/架构需求 |
| Viewpoint | Viewpoint | 视点 |
| View | View / Architecture View | 视图 |
| Model Kind | Model / Artifact | 模型种类 |
| Correspondence | Relationship / Traceability | 对应关系 |
| Architecture Rationale | Architecture Decision / ADR | 架构依据 |

## ArchiMate vs UML

| ArchiMate | UML | 说明 |
|-----------|-----|------|
| Business Actor | Actor | 业务参与者 |
| Business Role | Role | 业务角色 |
| Business Process | Activity Diagram | 业务流程 |
| Business Function | Package / Component | 业务功能 |
| Business Service | Interface | 业务服务 |
| Application Component | Component | 应用组件 |
| Application Service | Provided Interface | 应用服务 |
| Data Object | Class | 数据对象 |
| Node | Deployment Node | 节点 |
| Device | Node | 设备 |

## ISO 26550 vs 本体系

| ISO 26550 | 本体系对应主题 | 说明 |
|-----------|--------------|------|
| Domain Engineering | 01-元模型, 02-业务架构 | 领域工程产生可复用资产 |
| Application Engineering | 03-应用架构, 04-组件架构 | 应用工程使用可复用资产 |
| Product Line | 06-跨层治理 | 产品线管理复用资产 |
| Variability Model | 02-业务架构, 04-组件架构 | 变性模型 |
| Core Asset | 04-组件架构, 05-功能架构 | 核心资产 |

## SLSA vs NIST SSDF

| SLSA 1.0 | NIST SSDF | 说明 |
|-----------|-----------|------|
| L1 Source / Build | PO.1 Secure Software | 保护软件 |
| L2 Build Track | PW.4 Reusable Code | 复用代码安全 |
| L3 Build Environment | PW.6 Configure Compiler | 编译器配置 |
| L4 Reproducible Build | PW.8 Test Executable | 测试可执行文件 |
| Provenance | PS.1 Protect Software | 保护软件发布 |

## Industrial Standards Crosswalk

| IEC 63278 (AAS) | OPC UA | ISA-95 | 说明 |
|-----------------|--------|--------|------|
| AssetAdministrationShell | Server / Object | Enterprise / Site / Area | 资产的管理壳 |
| Submodel | ObjectType / Folder | Work Unit / Cell | 子模型 |
| Property | Variable | Tag / Attribute | 属性 |
| Operation | Method | Operation / Phase | 操作 |
| ConceptDescription | VariableType | Data Structure | 概念描述 |

## AI Native Terminology

| MCP 2026 | A2A v1.0 | 通用含义 |
|----------|---------|---------|
| Server | Agent | 提供服务/能力的实体 |
| Tool | Skill | 可调用的具体能力 |
| Resource | Artifact | 可被访问的数据/内容 |
| Prompt | Message Part | 与 LLM 交互的单元 |
| Capability | Agent Card | 声明的能力集合 |
| Session (removed) | Task | 交互上下文 |

---

> 最后更新: 2026-06-06
