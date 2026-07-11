package reuse.economic

# 默认拒绝
default allow := false

# 统一阈值（与 Python 常量保持一致）
AAF_ECONOMIC_FLOOR := 0.7
AAF_REBUILD_CEILING := 0.9

# 归一化 AAF：>1.0 视为百分比
normalize_aaf(aaf) := aaf / 100.0 if aaf > 1.0
normalize_aaf(aaf) := aaf if aaf <= 1.0

# 主判定：输入资产 JSON
allow if {
    decision.verdict == "REUSE_ECONOMIC"
}

allow if {
    decision.verdict == "TRADE_OFF"
    input.strategic_value == true
}

decision := d if {
    aaf := normalize_aaf(input.aaf)
    v_ratio := object.get(input, "v_reuse_ratio", 0.0)
    strategic := object.get(input, "strategic_value", false)
    absolute_upper := 1.0 + v_ratio

    d := {
        "aaf": aaf,
        "absolute_upper": absolute_upper,
        "verdict": verdict(aaf, absolute_upper, strategic),
        "reason": reason(aaf, absolute_upper, strategic),
    }
}

verdict(aaf, upper, strategic) := "REUSE_ECONOMIC" if { aaf < AAF_ECONOMIC_FLOOR }
verdict(aaf, upper, strategic) := "TRADE_OFF"      if { aaf >= AAF_ECONOMIC_FLOOR; aaf < AAF_REBUILD_CEILING }
verdict(aaf, upper, strategic) := "TRADE_OFF"      if { aaf >= AAF_REBUILD_CEILING; aaf < upper; strategic == true }
verdict(aaf, upper, strategic) := "REBUILD"        if { aaf >= upper }
verdict(aaf, upper, strategic) := "REBUILD"        if { aaf >= AAF_REBUILD_CEILING; not strategic }

reason(aaf, upper, strategic) := sprintf("AAF %.2f < %.2f, 优先复用", [aaf, AAF_ECONOMIC_FLOOR]) if { aaf < AAF_ECONOMIC_FLOOR }
reason(aaf, upper, strategic) := sprintf("AAF %.2f 在 [%.2f, %.2f) 区间，需权衡战略价值", [aaf, AAF_ECONOMIC_FLOOR, AAF_REBUILD_CEILING]) if { aaf >= AAF_ECONOMIC_FLOOR; aaf < AAF_REBUILD_CEILING }
reason(aaf, upper, strategic) := sprintf("AAF %.2f >= %.2f 但存在战略价值且低于理论上限 %.2f，进入权衡", [aaf, AAF_REBUILD_CEILING, upper]) if { aaf >= AAF_REBUILD_CEILING; aaf < upper; strategic == true }
reason(aaf, upper, strategic) := sprintf("AAF %.2f >= 理论上限 %.2f，建议重新实现", [aaf, upper]) if { aaf >= upper }
reason(aaf, upper, strategic) := sprintf("AAF %.2f >= %.2f 且无战略价值，建议重新实现", [aaf, AAF_REBUILD_CEILING]) if { aaf >= AAF_REBUILD_CEILING; not strategic }
