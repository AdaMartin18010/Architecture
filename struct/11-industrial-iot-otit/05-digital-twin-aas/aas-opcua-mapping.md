# AAS v3.2 到 OPC UA NodeSet 完整映射规范

> **版本**: 2026-06-08
> **对齐标准**: IDTA AAS Specification Part 1 v3.2, OPC UA for AAS Companion Specification (I4AAS), IEC 63278-1:2023, IEC 62541
> **定位**: 确立资产管理壳元模型与 OPC UA NodeSet 的逐元素映射规则、标识符转换与生命周期同步机制
> **状态**: ✅ 已完成
> **交叉引用**: [`aas-v32-opcua-fx-2026-alignment.md`](./aas-v32-opcua-fx-2026-alignment.md)

---

## 1. AAS v3.2 元模型概述

IDTA AAS Specification Part 1 v3.2 (2026-03) 定义了工业数字孪生的核心元模型。四个顶层元素构成可复用的语义资产：

| 元模型元素 | 语义 | 关键属性 |
|-----------|------|---------|
| **AssetAdministrationShell** | 资产的数字代表 | `id`, `idShort`, `assetInformation`, `submodels[]` |
| **Submodel** | 描述资产某方面的结构化数据 | `id`, `kind` (Instance/Template), `semanticId`, `submodelElements[]` |
| **ConceptDescription** | 语义定义与数据规范 | `id`, `embeddedDataSpecifications[]`, `isCaseOf[]` |
| **Identifiable** | 所有可独立标识元素的抽象基类 | `id` (IRI/IRDI/Custom), `administration` (版本/修订) |

核心关系：
- **hasSubmodel**: `AssetAdministrationShell → Submodel`，通过 `Reference` 实现一对多引用
- **hasSemanticId**: `Submodel` / `SubmodelElement → ConceptDescription`，通过 `semanticId` 指向外部语义字典（ECLASS / IEC CDD）
- **hasDataSpecification**: 任意 `HasDataSpecification` 元素 → `DataSpecification`，承载 IEC 61360 模板约束

---

## 2. OPC UA NodeSet 基础

OPC UA 信息模型以 **AddressSpace** 为全局命名图，节点通过 `NodeId` 唯一标识，引用通过 `ReferenceType` 标注语义。

### 2.1 NodeClass 体系

| NodeClass | 语义 | AAS 映射场景 |
|-----------|------|-------------|
| **Object** | 复合实体，可包含子节点 | AAS 根对象、Submodel、Entity、File |
| **Variable** | 数据值，含 `DataValue` (值/时间戳/质量) | Property、SubmodelElement 数值 |
| **Method** | 可调用操作，含输入/输出参数 | Operation |
| **ObjectType** | 对象类型定义 | AASType、SubmodelType、FileType |
| **VariableType** | 变量类型定义 | PropertyType、语义数据类型约束 |
| **ReferenceType** | 引用语义定义 | HasComponent、HasProperty、HasDictionaryEntry |
| **DataType** | 值域与结构约束 | xs:string → String, xs:double → Double |

### 2.2 AddressSpace 结构

```text
Objects (i=85)
└── AssetAdministrationShells (FolderType)
    └── <AAS> (AASAssetAdministrationShellType)
        ├── Identification
        ├── AssetInformation
        └── Submodels (FolderType)
            └── <Submodel> (AASSubmodelType)
                ├── SemanticId (HasDictionaryEntry)
                └── SubmodelElements...
```

---

## 3. AAS → OPC UA NodeSet 映射表

### 3.1 核心概念映射

| AAS 概念 | OPC UA 映射 | 说明 |
|----------|------------|------|
| AssetAdministrationShell | `Object` (AASAssetAdministrationShellType) | 根对象，Organizes 引用挂接于 AddressSpace |
| Submodel | `Object` (AASSubmodelType) | AAS 的组件，通过 `HasComponent` 关联到 AAS |
| SubmodelElement | `Variable` / `Object` | 根据具体类型映射（见下） |
| Property | `Variable` (AASPropertyType) | 具有 `DataValue`，`valueType` 映射为 `DataType` |
| Operation | `Method` (AASOperationType) | 可调用，`inputVariables` → `InputArguments` |
| File | `Object` + `HasComponent` → `FileType` | 文件引用，`value` 映射为 URL 字符串变量 |
| ReferenceElement | `Object` + `ReferenceType` | 外部引用，通过自定义 `ReferenceType` 表达语义 |
| Entity | `Object` | 复杂实体，`entityType` 映射为 `HasTypeDefinition` |
| RelationshipElement | `Reference` (语义化 ReferenceType) | `first`/`second` 映射为源/目标 `NodeId` |
| ConceptDescription | `ObjectType` / `VariableType` + `DictionaryEntry` | 语义定义，通过 `HasDictionaryEntry` 被引用 |
| Identifiable.id | `NodeId` | IRI/IRDI 映射为 `ns=<idx>;s=<id>` |

### 3.2 数据类型映射

| AAS `valueType` | OPC UA `DataType` |
|----------------|------------------|
| `xs:string` | `String` |
| `xs:integer` | `Int32` / `Int64` |
| `xs:double` | `Double` |
| `xs:boolean` | `Boolean` |
| `xs:dateTime` | `UtcTime` |
| `xs:base64Binary` | `ByteString` |

---

## 4. XML/JSON 示例：温度传感器资产

### 4.1 AAS JSON 示例（简化）

```json
{
  "assetAdministrationShells": [{
    "id": "https://example.com/aas/TempSensor_001",
    "idShort": "TempSensor_001",
    "assetInformation": {
      "assetKind": "Instance",
      "globalAssetId": "https://example.com/assets/TS-001"
    },
    "submodels": [{
      "keys": [{"type": "Submodel", "value": "https://example.com/sm/Measurement"}]
    }]
  }],
  "submodels": [{
    "id": "https://example.com/sm/Measurement",
    "idShort": "Measurement",
    "semanticId": {
      "keys": [{"type": "GlobalReference", "value": "https://admin-shell.io/idta/SubmodelTemplate/TechnicalData/1/2"}]
    },
    "submodelElements": [
      {
        "modelType": "Property",
        "idShort": "CurrentTemperature",
        "semanticId": {"keys": [{"type": "ConceptDescription", "value": "0173-1#02-BAA129#008"}]},
        "valueType": "xs:double",
        "value": "23.5"
      },
      {
        "modelType": "Property",
        "idShort": "Unit",
        "valueType": "xs:string",
        "value": "°C"
      },
      {
        "modelType": "Operation",
        "idShort": "Calibrate",
        "inputVariables": [{
          "value": {"idShort": "ReferenceValue", "valueType": "xs:double", "value": "25.0"}
        }],
        "outputVariables": [{
          "value": {"idShort": "Deviation", "valueType": "xs:double"}
        }]
      }
    ]
  }]
}
```

### 4.2 OPC UA NodeSet XML 片段

```xml
<?xml version="1.0" encoding="utf-8"?>
<UANodeSet xmlns="http://opcfoundation.org/UA/2008/02/Types.xsd"
           xmlns:aas="http://opcfoundation.org/UA/I4AAS/">
  <NamespaceUris>
    <Uri>http://opcfoundation.org/UA/I4AAS/</Uri>
    <Uri>https://example.com/aas/</Uri>
  </NamespaceUris>

  <UAObject NodeId="ns=2;s=https://example.com/aas/TempSensor_001"
            BrowseName="2:TempSensor_001" ParentNodeId="i=85">
    <DisplayName>TempSensor_001</DisplayName>
    <References>
      <Reference ReferenceType="HasTypeDefinition">aas:AASAssetAdministrationShellType</Reference>
      <Reference ReferenceType="Organizes" IsForward="false">i=85</Reference>
    </References>
  </UAObject>

  <UAObject NodeId="ns=2;s=https://example.com/sm/Measurement"
            BrowseName="2:Measurement"
            ParentNodeId="ns=2;s=https://example.com/aas/TempSensor_001">
    <DisplayName>Measurement</DisplayName>
    <References>
      <Reference ReferenceType="HasTypeDefinition">aas:AASSubmodelType</Reference>
      <Reference ReferenceType="HasComponent" IsForward="false">
        ns=2;s=https://example.com/aas/TempSensor_001
      </Reference>
    </References>
  </UAObject>

  <UAVariable NodeId="ns=2;s=https://example.com/sm/Measurement/CurrentTemperature"
              BrowseName="2:CurrentTemperature"
              ParentNodeId="ns=2;s=https://example.com/sm/Measurement"
              DataType="Double" ValueRank="-1">
    <DisplayName>CurrentTemperature</DisplayName>
    <References>
      <Reference ReferenceType="HasTypeDefinition">aas:AASPropertyType</Reference>
      <Reference ReferenceType="HasProperty" IsForward="false">
        ns=2;s=https://example.com/sm/Measurement
      </Reference>
      <Reference ReferenceType="HasDictionaryEntry">ns=3;s=0173-1#02-BAA129#008</Reference>
    </References>
    <Value><uax:Double>23.5</uax:Double></Value>
  </UAVariable>

  <UAMethod NodeId="ns=2;s=https://example.com/sm/Measurement/Calibrate"
            BrowseName="2:Calibrate"
            ParentNodeId="ns=2;s=https://example.com/sm/Measurement">
    <DisplayName>Calibrate</DisplayName>
    <References>
      <Reference ReferenceType="HasTypeDefinition">aas:AASOperationType</Reference>
      <Reference ReferenceType="HasComponent" IsForward="false">
        ns=2;s=https://example.com/sm/Measurement
      </Reference>
    </References>
  </UAMethod>
</UANodeSet>
```

---

## 5. 映射规则约束

### 5.1 标识符映射（IRI ↔ NodeId）

| AAS 标识类型 | OPC UA NodeId 格式 | 示例 |
|------------|------------------|------|
| IRI | `ns=<idx>;s=<IRI>` | `ns=2;s=https://example.com/aas/TS-001` |
| IRDI | `ns=<idx>;s=<IRDI>` | `ns=3;s=0173-1#02-BAA129#008` |
| Custom | `ns=<idx>;i=<localId>` | `ns=2;i=1001` |

规则：NamespaceUri 在 `NamespaceUris` 数组中的索引决定 `ns` 值。推荐为 AAS ID 空间分配独立 Namespace。

### 5.2 语义映射（semanticId ↔ ReferenceType / HasTypeDefinition）

- **Submodel.semanticId** → `HasTypeDefinition` 引用指向标准化的 `AASSubmodelType` 子类型
- **Property.semanticId** / **ConceptDescription** → `HasDictionaryEntry` 引用指向外部数据字典节点（ECLASS / IEC CDD）
- **RelationshipElement** → 自定义 `ReferenceType`（如 `HasPart`、`IsConnectedTo`）表达语义关系

### 5.3 生命周期同步（AAS 更新 → NodeSet 更新）

| AAS 变更类型 | OPC UA NodeSet 响应 | 机制 |
|-------------|-------------------|------|
| SubmodelElement 值变更 | Variable `Value` 属性更新 | `DataChangeNotification` (发布-订阅) |
| SubmodelElement 增删 | AddressSpace 节点增删 | `ModelChangeEvent` 通知客户端重建缓存 |
| AAS 元数据变更（版本/修订） | `administration` 变量更新 | 强制客户端重新读取 `NodeVersion` |
| AAS 整体删除 | 根 Object 删除 + `Reference` 清理 | `GeneralModelChangeEvent` |

> **公理 I.AAS.4** (Mapping Consistency): 若 AAS 实例发生状态变更 ΔS，则 OPC UA AddressSpace 必须在确定的时间边界 τ 内达到与 ΔS 语义等价的状态，其中 τ 由应用场景的实时性等级决定（OT 场景 τ ≤ 100 ms，IT 场景 τ ≤ 5 s）。

---

## 6. 权威来源

- IDTA. *Details of the Asset Administration Shell — Part 1: Metamodel*. v3.2, 2026-03.
- OPC Foundation. *OPC UA Companion Specification for I4AAS*. OPC 30270.
- IEC 63278-1:2023. *Asset Administration Shell for industrial applications — Part 1: Administration Shell structure*.
- IEC 62541 (OPC UA). *OPC Unified Architecture*.
- IEC 61360. *IEC Common Data Dictionary (CDD)*.
- Industrial Digital Twin Association (IDTA). [https://industrialdigitaltwin.org](https://industrialdigitaltwin.org)
- OPC Foundation I4AAS Working Group. [https://opcfoundation.org/markets-collaboration/I4AAS/](https://opcfoundation.org/markets-collaboration/I4AAS/)
- Eclipse BaSyx. [https://www.eclipse.org/basyx/](https://www.eclipse.org/basyx/)
