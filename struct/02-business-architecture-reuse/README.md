# 02 业务架构复用

## 定位

最粗粒度的复用层次。从业务领域到业务服务，建立"业务语义可复用"的框架。

## 核心内容

- **Level 1**: 业务领域复用（跨行业/跨组织宏观领域）
- **Level 2**: 业务能力复用（Capability-Based Planning）
- **Level 3**: 价值流复用（端到端价值交付序列）
- **Level 4**: 业务流程复用（BPMN 2.0 可执行流程）
- **Level 5**: 业务服务复用（SOA/ArchiMate Business Service）
- BPMN 2.0 / DMN 1.5 的复用元素详解
- FEA BRM（联邦企业架构业务参考模型）五层业务线结构
- 业务复用反模式：流程克隆、能力膨胀、价值流断裂

## 权威对齐

- [OMG BPMN 2.0 Specification](https://www.omg.org/spec/BPMN)
- [OMG DMN 1.5 Specification](https://www.omg.org/spec/DMN)
- FEA BRM 2.0 (美国联邦跨机构复用基准)
- TOGAF 10 Phase B (Business Architecture)

## 关键公理
>
> **公理 2.1** (Capability Atomicity): 业务能力是可复用的最小业务语义单元，其边界由**价值创造**而非**组织结构**定义。

## 当前状态

- [x] 五层层次结构定义
- [x] 决策矩阵与判定树
- [ ] BPMN/DMN 可执行语义案例补充
- [ ] 行业垂直场景（金融、医疗、制造）案例库

## 关联主题

- `03-application-architecture-reuse`（业务服务是业务层与应用层的桥接点）
- `06-cross-layer-governance`（业务能力目录治理）
