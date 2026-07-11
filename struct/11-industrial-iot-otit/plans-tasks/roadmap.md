# 11 工业 IoT/OT-IT 融合 — 推进路线图

> **版本**: 2026-06-06
> **状态**: OPC UA FX 分析已完成，其他子主题待深化

---

## 当前进度

- [x] 01-isa-95-model 目录结构（含 L0-L4 子目录）
- [x] 02-opc-ua-fx 目录结构
- [x] 03-tsn-deterministic 目录结构
- [x] 04-plcopen-motion 目录结构
- [x] 05-digital-twin-aas 目录结构
- [x] 06-functional-safety 目录结构
- [x] 07-edge-ai 目录结构
- [x] OPC UA FX 复用层次分析
- [x] ISA-95 资产目录
- [x] PLCopen 功能块 TLA+ 验证 → `04-plcopen-motion/plcopen-motion.tla`
- [x] AAS-OPC UA 映射规范（文件存在，需确认完整度）→ `05-digital-twin-aas/aas-opcua-mapping.md`
- [x] 功能安全（IEC 61508 / ISO 26262）复用决策树工具

---

## Phase 1: ISA-95 资产目录（2026-06 第二周）

**任务**:

- [x] T01: L0 现场层复用资产（设备描述文件、Companion Specifications）
- [x] T02: L1 控制层复用资产（FB、UDT、控制算法）
- [x] T03: L2 监控层复用资产（HMI 模板、报警规则、趋势图）
- [x] T04: L3 MES 层复用资产（配方、SOP、质量规则、KPI 模板）
- [x] T05: L4 企业层复用资产（业务流程模板、ERP 配置模板）
- [x] T06: 跨层数据流映射（ERP↔MES↔SCADA↔PLC↔Field）

**交付物**:

- `01-isa-95-model/l0-field/asset-catalog.md`
- `01-isa-95-model/l1-control/asset-catalog.md`
- `01-isa-95-model/l2-supervisory/asset-catalog.md`
- `01-isa-95-model/l3-mes/asset-catalog.md`
- `01-isa-95-model/l4-enterprise/asset-catalog.md`
- `01-isa-95-model/cross-layer-matrix/data-flow-mapping.md`

---

## Phase 2: OPC UA FX 深化（2026-06 第三周）

**任务**:

- [x] T07: OPC UA FX 复用层次分析
- [x] T08: UADP 帧结构详解（C2C/C2D/D2D 对比）
- [x] T09: TSN 门控表（GCL）配置模板
- [x] T10: FX Connection Manager 状态机 TLA+ 规约
- [x] T11: 2026 厂商支持矩阵持续更新
- [x] T12: 棕地/绿地/混合场景决策模板

**交付物**:

- `02-opc-ua-fx/frame-structure/uadp-frame-analysis.md`
- `03-tsn-deterministic/gcl-config/templates.md`
- `02-opc-ua-fx/connection-manager/tla-specification.tla`

---

## Phase 3: PLCopen 与数字孪生（2026-06 第四周）— 已完成

**任务**:

- [x] T13: PLCopen Motion Control V2.0 核心功能块接口定义 → `04-plcopen-motion/function-block-interfaces.md`
- [x] T14: MC_Power / MC_MoveAbsolute 状态机的 TLA+ 验证 → `04-plcopen-motion/plcopen-motion.tla`
- [x] T15: AAS 元模型与 OPC UA 信息模型的完整映射（文件存在，需确认完整度）→ `05-digital-twin-aas/aas-opcua-mapping.md`
- [x] T16: AAS 子模型模板清单（14 个标准子模型） → `05-digital-twin-aas/submodel-templates/catalog.md`
- [x] T17: AASX 包格式交换规范 → 已整合于 AAS-OPC UA 映射文档

**交付物**:

- `04-plcopen-motion/function-block-interfaces.md`
- `04-plcopen-motion/tla-verification.md`
- `05-digital-twin-aas/aas-opcua-mapping.md`
- `05-digital-twin-aas/submodel-templates/catalog.md`

---

## Phase 4: 功能安全与边缘 AI（2027-Q1）— 已完成

**任务**:

- [x] T18: IEC 61508 Proven-in-Use 统计验证方法工具 → `06-functional-safety/piu-bayesian-tool.py`
- [x] T19: ISO 26262 SEooC 复用流程模板 → `06-functional-safety/iso26262-seooc-template.md`
- [x] T20: 工业边缘 AI 模型部署规范（ONNX/TFLite）→ `07-edge-ai/model-deployment-spec.md`
- [x] T21: 工业 AI 的 MCP for Industrial AI 协议草案 → `07-edge-ai/mcp-industrial-ai-draft.md`

**交付物**:

- `06-functional-safety/piu-statistical-tool.md`
- `06-functional-safety/iso26262-seooc-template.md`
- `07-edge-ai/model-deployment-spec.md`

---

## 依赖关系

```text
T01-T06 (ISA-95 资产目录)
    ↓
T07-T12 (OPC UA FX 深化)
    ↓
T13-T17 (PLCopen + AAS)
    ↓
T18-T21 (功能安全 + 边缘 AI)
```

---

> 最后更新: 2026-06-10