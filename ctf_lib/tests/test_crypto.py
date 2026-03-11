from ctf_lib.crypto.rsa_utils import coppersmith_known_high_bits_p

def test_coppersmith_known_high_bits_p():
    """
    测试 Coppersmith 攻击：已知 p 的高位，恢复完整的 p
    使用真实的 CTF 题目数据进行黑盒测试
    """
    # 1. 准备已知的测试数据 (Arrange)
    n = 103581608824736882681702548494306557458428217716535853516637603198588994047254920265300207713666564839896694140347335581147943392868972670366375164657970346843271269181099927135708348654216625303445930822821038674590817017773788412711991032701431127674068750986033616138121464799190131518444610260228947206957
    leak = 6614588561261434084424582030267010885893931492438594708489233399180372535747474192128
    hidden_bits = 230
    
    # 2. 调用我们要测试的函数 (Act)
    # epsilon 设为 0.04 是我们上一题验证过可以秒出结果的参数
    recovered_p = coppersmith_known_high_bits_p(n, leak, hidden_bits, epsilon=0.04)
    
    # 3. 进行断言验证 (Assert)
    
    assert recovered_p is not None, "攻击失败，函数返回了 None"
    assert isinstance(recovered_p, int), f"返回类型错误，期望 int，实际是 {type(recovered_p)}"
    assert n % recovered_p == 0, "恢复出的 p 不是 n 的因子"
    assert 1 < recovered_p < n, "恢复出了平凡因子"