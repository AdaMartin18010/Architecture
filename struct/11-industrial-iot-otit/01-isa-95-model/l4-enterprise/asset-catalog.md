# L4 企业层复用资产目录

> **版本**: 2026-06-06
> **层级**: ISA-95 Level 4 — 企业资源计划层 (Enterprise Resource Planning)
> **时间尺度**: 天–月 (d–mon)
> **管理域**: 业务管理、财务、供应链与客户关系域
> **对齐来源**: ANSI/ISA-95.00.01-2010, ISA-95 Part 5 (B2MML), ISO 9001, APICS SCOR

---

## 1. 层定义与复用范围

L4 企业层是 ISA-95 五层模型的最高层，面向业务规划与资源优化。
本层资产的复用聚焦于**业务流程模板**、**ERP 配置模板**与**主数据模型**——三者共同构成企业级"数字神经系统"的复用基线。
在多工厂、多法人实体的集团化部署中，标准化的 L4 复用资产可将 ERP 推广成本降低 40%–60%，并确保跨地域业务数据语义一致。

> **交叉引用**: L4 层资产是 `struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md` 中价值流建模的顶层输入。
> 业务流程模板直接对应"订单到现金""采购到付款""计划到生产"等经典价值流的能力编排与阶段间接口契约。

---

## 2. 资产分类表

| 序号 | 资产名称 | 描述 | 标准/规范 | 复用频率 | 成熟度 |
|-----|---------|------|----------|---------|--------|
| E1 | **采购到付款 (P2P) 流程模板** | 涵盖请购→采购申请→供应商选择→订单下达→收货→质检→发票校验→付款的标准业务流程模板，集成三单匹配 (PO-GR-Invoice) 规则。 | ISA-95 Part 5, ISO 9001:2015, APICS | 极高 (所有制造型企业) | 成熟 |
| E2 | **计划到生产 (P2P) 流程模板** | 从销售与运营计划 (S&OP)→主生产计划 (MPS)→物料需求计划 (MRP)→能力需求计划 (CRP)→工单下达的端到端流程模板，支持按库存/按订单/按装配 (MTS/MTO/ATO) 模式。 | ISA-95 Part 1–3, APICS, TOC | 极高 (制造核心流程) | 成熟 |
| E3 | **物流发运流程模板** | 销售订单→拣配→包装→装运→在途跟踪→客户签收的标准流程，集成运输管理 (TMS) 与仓库管理 (WMS) 接口。 | ISA-95, GS1, IATA (航空), IMO (海运) | 高 (供应链全球化) | 成熟 |
| E4 | **ERP 主数据模型模板** | 物料主数据 (Material Master)、供应商主数据、客户主数据、工作中心 (Work Center)、成本中心的标准字段定义、编码规则与分类体系模板。 | ISA-95 Part 2, ISO 8000 (数据质量), GS1 GDSN | 极高 (ERP 实施基础) | 成熟 |
| E5 | **BOM (物料清单) 配置模板** | 支持 E-BOM (工程)、M-BOM (制造)、S-BOM (服务) 多层结构与变型配置的模板，集成超级 BOM (150% BOM) 与订单 BOM 派生规则。 | ISO 10303-214 (AP214), ISA-95 Part 2 | 高 (复杂离散制造) | 成熟 |
| E6 | **成本核算模板 (标准成本/实际成本)** | 产品标准成本卷积模型与实际成本分摊规则模板，包含物料差异、人工差异、制造费用差异的自动计算与分摊逻辑。 | ISA-95 Part 4, IAS 2 / CAS 1, CO-PA | 高 (财务合规) | 成熟 |
| E7 | **ESG 与碳足迹报告模板** | 基于产品生命周期 (LCA) 的碳足迹计算模板，集成范围 1/2/3 排放因子、能耗数据接口与可持续发展报告 (CSRD/TCFD) 输出格式。 | ISO 14064-1:2018, GHG Protocol, CSRD | 中 (双碳与合规驱动) | 发展中 |
| E8 | **多组织间交易 (Intercompany) 流程模板** | 集团内跨法人实体采购、销售、库存转移的标准流程模板，包含转移定价、内部发票、合并抵消规则与税务合规检查。 | ISA-95, OECD 转让定价指南, IFRS 10 | 中 (集团型企业) | 成熟 |

---

## 3. 复用建议

### 3.1 业务流程模板的集团化复用

1. **全球模板 + 本地差异**: 建立集团级"黄金流程"(Golden Process) 模板，各地区/工厂通过预定义的扩展点（如审批层级、税码、货币）注入本地差异，主干流程 100% 复用。
2. **B2MML 契约先行**: 在与 L3 MES 集成前，优先复用 ISA-95 Part 5 定义的 B2MML XML Schema 作为 L4↔L3 的数据契约，避免后期昂贵的接口返工。
3. **主数据治理联邦制**: 核心主数据（如物料分类、单位、币种）由集团统一治理；运营主数据（如工作中心日历、质检特性）由工厂自治。通过 MDM (Master Data Management) 平台实现联邦复用。

### 3.2 ERP 配置模板的自动化复用

- **系统配置即代码 (Config-as-Code)**: 将 ERP 配置表（如公司代码、工厂、库存地、采购组织）导出为结构化 YAML/JSON，纳入 Git 版本控制，支持跨环境的配置漂移检测与自动化部署。
- **测试数据工厂**: 建立标准化的 ERP 测试数据模板（含典型业务场景数据集），支持单元测试、集成测试、UAT 的快速数据准备。

### 3.3 跨层复用接口

- **L4 → L3**: 通过 B2MML Work Order、Production Schedule、Material Definition 消息向下传递计划；通过 REST/OData 同步物料主数据与 BOM。
- **L4 ← L3**: 接收 B2MML Production Performance、Material Actual、Production Response 消息，更新库存、关闭工单、核算成本。
- **L4 ↔ 外部**: 通过 EDI (EDIFACT/X12/ODETTE) 与供应商、客户、物流服务商交换订单、发货通知、发票。

### 3.4 形式化验证提示

> **交叉引用**: 企业层业务流程（如 P2P、计划到生产）涉及复杂的并发与资源竞争。可借鉴 `struct/07-formal-verification/06-b-method/event-b-railway-refinement.md` 中的 **Event-B 上下文扩展** 机制：将业务规则（如三单匹配、信用额度检查）建模为可扩展的 Context 公理集，各法人实体通过上下文扩展注入本地法规约束，同时保持核心 Machine（流程状态机）不变，确保全局流程一致性。

---

## 4. 权威来源

1. ANSI/ISA-95.00.01-2010 / IEC 62264-1:2013 — Models and Terminology
2. ISA-95 Part 5 / B2MML (Business To Manufacturing Markup Language) — WBF XML Schemas
3. ISO 9001:2015 — Quality management systems
4. APICS SCOR (Supply Chain Operations Reference) Model V14.0
5. ISO 8000-1:2022 — Data quality
6. GS1 Global Data Synchronization Network (GDSN) Standard
7. ISO 14064-1:2018 — Greenhouse gases: Specification with guidance at the organization level
8. GHG Protocol Corporate Accounting and Reporting Standard

---

> 最后更新: 2026-06-06
