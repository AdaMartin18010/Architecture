package ai.model.selection

# AI 模型选择决策策略
# 输入：
#   task_type               string  任务类型 (critical/classification/summarization/creative/chat)
#   min_accuracy            float   最低可接受准确率 (0.0-1.0)
#   max_latency_p99_ms      int     最大可接受 P99 延迟 (ms)
#   max_cost_per_1k_tokens  float   每 1K tokens 最高可接受成本
#   data_privacy_required   bool    是否要求数据隐私/私有化部署
#   safety_level_required   string  安全等级要求 (high/medium/low)
#   available_tiers         array   可用模型层级 ["premium", "balanced", "economy"]
# 输出：
#   decision  string  PREMIUM / BALANCED / ECONOMY / REJECT
#   reason    string  决策理由
#   allow     bool    是否允许使用选定层级

default decision := "REJECT"

decision := "REJECT" if {
    input.min_accuracy > 0.98
}

decision := "REJECT" if {
    input.max_latency_p99_ms < 20
}

decision := "REJECT" if {
    input.safety_level_required == "high"
    not tier_available("premium")
}

decision := "REJECT" if {
    input.data_privacy_required == true
    not tier_available("premium")
    not tier_available("balanced")
}

decision := "PREMIUM" if {
    decision != "REJECT"
    input.safety_level_required == "high"
    tier_available("premium")
}

decision := "PREMIUM" if {
    decision != "REJECT"
    input.min_accuracy >= 0.92
    tier_available("premium")
}

decision := "PREMIUM" if {
    decision != "REJECT"
    input.max_latency_p99_ms <= 100
    tier_available("premium")
}

decision := "BALANCED" if {
    decision != "REJECT"
    decision != "PREMIUM"
    input.min_accuracy >= 0.85
    tier_available("balanced")
}

decision := "BALANCED" if {
    decision != "REJECT"
    decision != "PREMIUM"
    input.max_latency_p99_ms <= 300
    input.max_cost_per_1k_tokens <= 0.05
    tier_available("balanced")
}

decision := "ECONOMY" if {
    decision != "REJECT"
    decision != "PREMIUM"
    decision != "BALANCED"
    input.max_cost_per_1k_tokens <= 0.01
    tier_available("economy")
}

decision := "BALANCED" if {
    decision != "REJECT"
    decision != "PREMIUM"
    decision != "ECONOMY"
    tier_available("balanced")
}

tier_available(tier) if {
    input.available_tiers[_] == tier
}

reason := sprintf("准确率要求 %.2f 超出可保障上限 0.98，建议调整业务预期", [input.min_accuracy]) if {
    input.min_accuracy > 0.98
}

reason := sprintf("延迟要求 %d ms 低于最低可行阈值 20 ms", [input.max_latency_p99_ms]) if {
    input.max_latency_p99_ms < 20
}

reason := "高安全等级场景必须使用 PREMIUM 层级模型" if {
    input.safety_level_required == "high"
    not tier_available("premium")
}

reason := "数据隐私要求场景至少需 BALANCED 层级私有化部署" if {
    input.data_privacy_required == true
    not tier_available("premium")
    not tier_available("balanced")
}

reason := sprintf("高安全等级要求，选择 PREMIUM 层级 (可用层级: %v)", [input.available_tiers]) if {
    decision == "PREMIUM"
    input.safety_level_required == "high"
}

reason := sprintf("高准确率要求 %.2f 或低延迟 %d ms，选择 PREMIUM 层级", [input.min_accuracy, input.max_latency_p99_ms]) if {
    decision == "PREMIUM"
    input.min_accuracy >= 0.92
}

reason := sprintf("P99 延迟要求 %d ms 严格，选择 PREMIUM 层级", [input.max_latency_p99_ms]) if {
    decision == "PREMIUM"
    input.max_latency_p99_ms <= 100
}

reason := sprintf("中等准确率 %.2f / 中等延迟 %d ms，选择 BALANCED 层级", [input.min_accuracy, input.max_latency_p99_ms]) if {
    decision == "BALANCED"
    input.min_accuracy >= 0.85
}

reason := sprintf("成本约束 %.4f $/1K tokens，选择 ECONOMY 层级", [input.max_cost_per_1k_tokens]) if {
    decision == "ECONOMY"
}

reason := sprintf("无严格约束，默认选择 BALANCED 层级 (可用层级: %v)", [input.available_tiers]) if {
    decision == "BALANCED"
    not input.min_accuracy >= 0.85
}

allow if { decision == "PREMIUM" }
allow if { decision == "BALANCED" }
allow if { decision == "ECONOMY" }
