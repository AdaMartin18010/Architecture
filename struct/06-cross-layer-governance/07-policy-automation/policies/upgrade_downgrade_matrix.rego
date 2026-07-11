package reuse.matrix

# 跨层复用升级/降级决策矩阵策略
# 输入：
#   current_layer              string  当前层级 (function/component/app_service/business_service)
#   consumers                  int     消费方数量
#   cross_team                 bool    是否跨团队使用
#   cross_org                  bool    是否跨组织使用
#   tech_compatibility_ratio   float   技术栈兼容比例 (0.0-1.0)
#   semantic_coverage_ratio    float   业务语义覆盖率 (0.0-1.0)
#   coupling_impact_ratio      float   变更影响范围比例 (0.0-1.0)
#   security_level_required    string  目标安全等级 (L0/L1/L2/L3/L4)
#   component_cert_level       string  组件当前认证等级 (L0/L1/L2/L3/L4)
#   confidence_gamma           float   AI 功能置信度 (0.0-1.0)，仅 AI 功能场景
#   config_conflicts           int     配置冲突数量
#   latency_requirement_ms     int     延迟要求 (ms)
#   shared_service_p99_ms      int     共享服务 P99 延迟 (ms)
#   upgrade_benefit            float   升级收益 (>0 表示正向)
#   downgrade_benefit          float   降级收益 (>0 表示正向)
# 输出：
#   decision     string  UPGRADE / DOWNGRADE / MAINTAIN / ADAPTER / SECURITY_REVIEW / DEPRECATE
#   target_layer string  目标层级
#   risk_level   string  低/中/高/极高
#   reason       string  决策理由

layer_order := ["function", "component", "app_service", "business_service"]

layer_index(layer) := i if {
    layer_order[i] == layer
}

current_index := layer_index(input.current_layer)

security_rank := {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4}

security_mismatch if {
    security_rank[input.security_level_required] > security_rank[input.component_cert_level]
}

# 升级触发条件
upgrade_trigger if {
    input.consumers >= 3
    input.cross_team
    input.semantic_coverage_ratio >= 0.8
    input.tech_compatibility_ratio >= 0.8
}

upgrade_trigger if {
    input.cross_org
}

upgrade_trigger if {
    input.upgrade_benefit > 0
    input.consumers >= 3
}

# 降级触发条件
downgrade_trigger if {
    input.coupling_impact_ratio > 0.3
}

downgrade_trigger if {
    input.tech_compatibility_ratio < 0.5
}

downgrade_trigger if {
    input.confidence_gamma < 0.8
}

downgrade_trigger if {
    input.config_conflicts >= 5
}

downgrade_trigger if {
    security_mismatch
}

downgrade_trigger if {
    input.latency_requirement_ms < input.shared_service_p99_ms
}

downgrade_trigger if {
    input.semantic_coverage_ratio < 0.8
    input.downgrade_benefit > 0
}

downgrade_trigger if {
    input.downgrade_benefit > 0
    input.coupling_impact_ratio > 0.2
}

# 未使用则弃用
deprecate_trigger if {
    input.consumers == 0
}

# 决策优先级：弃用 > 安全审查 > 降级 > 适配器 > 升级 > 维持
default decision := "MAINTAIN"
default target_layer := input.current_layer
default risk_level := "低"

decision := "DEPRECATE" if {
    deprecate_trigger
}

target_layer := input.current_layer if {
    deprecate_trigger
}

risk_level := "低" if {
    deprecate_trigger
}

reason := sprintf("消费方数量为 0，建议标记弃用 (当前层级: %s)", [input.current_layer]) if {
    deprecate_trigger
}

decision := "SECURITY_REVIEW" if {
    upgrade_trigger
    security_mismatch
    not deprecate_trigger
}

target_layer := next_layer(input.current_layer) if {
    upgrade_trigger
    security_mismatch
    not deprecate_trigger
}

risk_level := "极高" if {
    upgrade_trigger
    security_mismatch
    not deprecate_trigger
}

reason := sprintf("升级方向明确但安全等级不匹配 (要求 %s > 当前认证 %s)，需安全审查", [input.security_level_required, input.component_cert_level]) if {
    upgrade_trigger
    security_mismatch
    not deprecate_trigger
}

decision := "DOWNGRADE" if {
    downgrade_trigger
    not deprecate_trigger
}

target_layer := prev_layer(input.current_layer) if {
    downgrade_trigger
    not deprecate_trigger
}

risk_level := "高" if {
    decision == "DOWNGRADE"
    security_mismatch
}

risk_level := "中" if {
    decision == "DOWNGRADE"
    not security_mismatch
}

decision := "ADAPTER" if {
    upgrade_trigger
    input.tech_compatibility_ratio < 0.8
    not security_mismatch
    not downgrade_trigger
    not deprecate_trigger
}

target_layer := input.current_layer if {
    upgrade_trigger
    input.tech_compatibility_ratio < 0.8
    not security_mismatch
    not downgrade_trigger
    not deprecate_trigger
}

risk_level := "中" if {
    decision == "ADAPTER"
}

reason := sprintf("升级条件满足但技术栈兼容性 %.2f < 0.8，建议引入适配器/防腐层", [input.tech_compatibility_ratio]) if {
    decision == "ADAPTER"
}

decision := "UPGRADE" if {
    upgrade_trigger
    not downgrade_trigger
    not security_mismatch
    input.tech_compatibility_ratio >= 0.8
    not deprecate_trigger
}

target_layer := next_layer(input.current_layer) if {
    upgrade_trigger
    not downgrade_trigger
    not security_mismatch
    input.tech_compatibility_ratio >= 0.8
    not deprecate_trigger
}

risk_level := "高" if {
    decision == "UPGRADE"
    input.current_layer == "app_service"
}

risk_level := "中" if {
    decision == "UPGRADE"
    input.current_layer == "component"
}

risk_level := "低" if {
    decision == "UPGRADE"
    input.current_layer == "function"
}

risk_level := "极高" if {
    decision == "UPGRADE"
    input.current_layer == "business_service"
}

reason := sprintf("消费方 %d、语义覆盖率 %.2f、技术兼容性 %.2f，建议从 %s 升级至 %s",
    [input.consumers, input.semantic_coverage_ratio, input.tech_compatibility_ratio, input.current_layer, target_layer]) if {
    decision == "UPGRADE"
}

reason := sprintf("耦合影响 %.2f > 0.3，建议从 %s 降级至 %s",
    [input.coupling_impact_ratio, input.current_layer, prev_layer(input.current_layer)]) if {
    decision == "DOWNGRADE"
    input.coupling_impact_ratio > 0.3
}

reason := sprintf("技术栈兼容性 %.2f < 0.5，建议从 %s 降级至 %s",
    [input.tech_compatibility_ratio, input.current_layer, prev_layer(input.current_layer)]) if {
    decision == "DOWNGRADE"
    input.tech_compatibility_ratio < 0.5
}

reason := sprintf("AI 功能置信度 %.2f < 0.8，建议从 %s 降级至 %s 并引入规则引擎",
    [input.confidence_gamma, input.current_layer, prev_layer(input.current_layer)]) if {
    decision == "DOWNGRADE"
    input.confidence_gamma < 0.8
}

reason := sprintf("配置冲突数 %d >= 5，建议从 %s 降级至 %s 并简化配置空间",
    [input.config_conflicts, input.current_layer, prev_layer(input.current_layer)]) if {
    decision == "DOWNGRADE"
    input.config_conflicts >= 5
}

reason := sprintf("安全等级不匹配 (要求 %s > 认证 %s)，建议从 %s 降级隔离",
    [input.security_level_required, input.component_cert_level, input.current_layer]) if {
    decision == "DOWNGRADE"
    security_mismatch
}

reason := sprintf("延迟要求 %d ms < 共享服务 P99 %d ms，建议从 %s 降级至本地实现",
    [input.latency_requirement_ms, input.shared_service_p99_ms, input.current_layer]) if {
    decision == "DOWNGRADE"
    input.latency_requirement_ms < input.shared_service_p99_ms
}

reason := sprintf("语义覆盖率 %.2f < 0.8 且降级收益为正，建议从 %s 降级",
    [input.semantic_coverage_ratio, input.current_layer]) if {
    decision == "DOWNGRADE"
    input.semantic_coverage_ratio < 0.8
}

reason := sprintf("当前层级 %s 维持现状，未触发升级/降级条件", [input.current_layer]) if {
    decision == "MAINTAIN"
}

next_layer(layer) := layer_order[i] if {
    layer_order[j] == layer
    i := j + 1
    i < count(layer_order)
}

prev_layer(layer) := layer_order[i] if {
    layer_order[j] == layer
    i := j - 1
    i >= 0
}

allow if { decision == "UPGRADE" }
allow if { decision == "DOWNGRADE" }
allow if { decision == "ADAPTER" }
allow if { decision == "MAINTAIN" }
