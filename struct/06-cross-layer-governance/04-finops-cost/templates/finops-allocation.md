# FinOps 跨层成本分摊模板使用说明

> **对齐标准**：FinOps Foundation Framework 2025、FOCUS 1.0、Allocation Accuracy Index（AAI）

---

## 1. 快速开始

```bash
cd struct/06-cross-layer-governance/04-finops-cost/templates/
python3 finops-allocation.py --demo
```

## 2. CSV 输入格式

CSV 必须包含以下列：

| 列名 | 说明 |
|------|------|
| `line_id` | 唯一行 ID |
| `provider` | aws / azure / gcp / saas / ai / onprem |
| `resource_id` | 资源标识 |
| `effective_cost` | FOCUS 标准化有效成本 |
| `tag_business_unit` | 业务单元 |
| `tag_app` | 应用 |
| `tag_component` | 组件 |
| `tag_feature` | 功能 |
| `tag_env` | 环境 |
| `usage_quantity` | 使用量 |
| `usage_unit` | 使用单位 |

## 3. 分配方法

- **direct**：按标签直接归属（如 `tag_business_unit`）。
- **proportional**：按驱动量比例拆分（如 compute hours、API 调用数、token 数）。
- **step_down**：阶梯式分摊，适用于平台团队→应用团队的场景。
- **equal**：均分，仅作为最后手段（不推荐）。

## 4. 关键指标

### Allocation Accuracy Index（AAI）

```
AAI = 直接归属成本 / 总基础设施成本 × 100%
```

- ≥ 95%：财务级 chargeback / P&L 报告
- 80–94%：showback 级，可用于内部透明度
- < 80%：治理可信度不足

### 复用节省估算

```
Reuse Savings = (重复建设成本 × 消费方数量) - (共享平台成本 + 分摊开销)
```

## 5. 跨层模型

```
Business Unit
└── Application
    ├── Component A (直接归属)
    ├── Component B (直接归属)
    └── Shared Platform Component (按比例/阶梯分摊)
        ├── Function 1
        └── Function 2
```

## 6. 与 Excel 集成

TODO：通过 `xlsxwriter` 或 `openpyxl` 导出带公式的 Excel 模板，供财务人员直接使用。

## 7. 权威参考

- FinOps Foundation: <https://www.finops.org/framework/>
- FOCUS: <https://focus.finops.org/>
- Token Economics: <https://www.finops.org/insights/token-economics-the-atomic-unit-of-ai-value/>
