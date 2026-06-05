# AAS 与 OPC UA 的映射规范

> **版本**: 2026-06-06
> **对齐标准**: IEC 63278 (AAS), OPC UA Companion Specification for AAS, IEC 61360
> **定位**: 详细说明资产管理壳 (AAS) 与 OPC UA 信息模型的映射规则

---

## 1. 为什么需要 AAS-OPC UA 映射

AAS (Asset Administration Shell) 是工业 4.0 的数字孪生核心标准。OPC UA 是工业通信的事实标准。二者的映射实现了：

- **物理资产 ↔ 数字孪生**: 通过 OPC UA 读写 AAS 中的实时数据
- **跨厂商互操作**: 不同厂商的 OPC UA Server 都可以暴露 AAS 结构
- **IT/OT 桥接**: AAS 面向 IT 层，OPC UA 面向 OT 层

---

## 2. 核心概念映射

| AAS 概念 | OPC UA 对应 | 说明 |
|---------|------------|------|
| **AssetAdministrationShell** | ObjectType 或 Folder | AAS 的根节点 |
| **Submodel** | ObjectType / Folder | AAS 子模型 |
| **SubmodelElement** | Variable / Object / Method | 子模型元素 |
| **Property** | Variable (DataValue) | 标量属性 |
| **Operation** | Method | 可执行操作 |
| **EventElement** | Event | 事件通知 |
| **Entity** | Object | 复杂实体 |
| **RelationshipElement** | Reference | 元素间关系 |
| **ConceptDescription** | VariableType / Dictionary | 概念描述 |

---

## 3. AAS 子模型映射示例

### 输入：AAS JSON

```json
{
  "assetAdministrationShells": [{
    "idShort": "MotorAAS_001",
    "identification": {
      "idType": "IRI",
      "id": "https://example.com/aas/MotorAAS_001"
    },
    "submodels": [{
      "keys": [{"type": "Submodel", "value": "https://example.com/sm/Nameplate"}]
    }]
  }],
  "submodels": [{
    "idShort": "Nameplate",
    "identification": {
      "idType": "IRI",
      "id": "https://example.com/sm/Nameplate"
    },
    "submodelElements": [
      {
        "modelType": "Property",
        "idShort": "ManufacturerName",
        "valueType": "string",
        "value": "Siemens AG"
      },
      {
        "modelType": "Property",
        "idShort": "SerialNumber",
        "valueType": "string",
        "value": "SN-12345678"
      },
      {
        "modelType": "Property",
        "idShort": "YearOfConstruction",
        "valueType": "string",
        "value": "2024"
      }
    ]
  }]
}
```

### 输出：OPC UA 地址空间

```
Objects
└── AssetAdministrationShells
    └── MotorAAS_001
        ├── Identification
        │   ├── Id: "https://example.com/aas/MotorAAS_001"
        │   └── IdType: "IRI"
        └── Submodels
            └── Nameplate
                ├── ManufacturerName: "Siemens AG" [String]
                ├── SerialNumber: "SN-12345678" [String]
                └── YearOfConstruction: "2024" [String]
```

---

## 4. 映射规则详解

### 规则 1: 标识符处理

AAS 的 `identification.id`（IRI 格式）映射到 OPC UA 的 NodeId：

```
NodeId = IRI 的 URL-safe 编码
NamespaceIndex = 分配给 AAS 命名空间的索引
```

### 规则 2: 属性值映射

| AAS valueType | OPC UA DataType |
|---------------|-----------------|
| string | String |
| integer | Int32 / Int64 |
| double | Double |
| boolean | Boolean |
| dateTime | UtcTime |
| base64Binary | ByteString |

### 规则 3: 操作映射

AAS `Operation` 映射为 OPC UA `Method`：

```
AAS Operation.inVariable  → Method InputArguments[]
AAS Operation.outVariable → Method OutputArguments[]
```

### 规则 4: 事件映射

AAS `EventElement` 映射为 OPC UA `EventType`：

```
AAS EventElement.observed → OPC UA EventNotifier
AAS EventElement.messageTopic → OPC UA EventType 的 BrowseName
```

---

## 5. 子模型模板清单

| 模板名称 | 用途 | IEC 参考 |
|----------|------|---------|
| Nameplate | 设备铭牌信息 | IDTA-02006 |
| Technical Data | 技术规格 | IDTA-02003 |
| Identification | 资产识别 | IDTA-02007 |
| Handover Documentation | 移交文档 | IDTA-02008 |
| Contact Information | 联系信息 | IDTA-02002 |
| Carbon Footprint | 碳足迹 | IDTA-02023 |
| Time Series Data | 时序数据 | IDTA-02022 |

---

## 6. 复用策略

### 子模型复用

同一类型的设备共享相同的子模型模板。例如所有电机都使用 Nameplate + Technical Data 子模型。

### OPC UA Companion Specification 复用

设备厂商根据行业标准 Companion Specification 实现 OPC UA Server，自动暴露 AAS 结构。

### AASX 包交换

AAS 配置以 AASX（ZIP + JSON/XML）格式交换，实现跨工具、跨厂商的复用。

---

## 7. 关键定理

> **定理 I.AAS.1** (AAS-OPC UA Interoperability): 若 AAS 子模型严格遵循标准模板，且 OPC UA Server 正确实现 Companion Specification，则不同厂商的工具可以无需适配即消费该 AAS 的内容。

> **定理 I.AAS.2** (Submodel Template Reuse): AAS 子模型模板的复用价值与其在行业中的采纳率成正比。单个企业的自定义模板复用价值有限；行业标准模板（如 IDTA 模板）复用价值最高。

---

> 最后更新: 2026-06-06
