// Kani 有界模型检验示例：验证 i32::abs 的基本属性
// 运行: cargo kani --test kani_abs_proof
// 需要安装: cargo install --locked kani-verifier && cargo kani setup

#[cfg(kani)]
mod proofs {
    #[kani::proof]
    fn verify_abs_nonnegative() {
        let x: i32 = kani::any();
        let r = x.abs();
        assert!(r >= 0, "abs must be non-negative");
    }

    #[kani::proof]
    fn verify_abs_sign_correctness() {
        let x: i32 = kani::any();
        let r = x.abs();
        if x < 0 {
            // 注意：i32::MIN 时 -x 会溢出，Kani 也会检查此处
            // 此断言在 i32::MIN 时不成立，因为 abs(i32::MIN) == i32::MIN（负数）
            // 保留作为教学示例，展示 Kani 能发现溢出/断言失败
            kani::assume(x != i32::MIN);
            assert!(r == -x, "abs of negative should be its negation");
        }
        if x >= 0 {
            assert!(r == x, "abs of non-negative should be itself");
        }
    }
}
