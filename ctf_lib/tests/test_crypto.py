
def test_coppersmith_known_high_bits_p():
    """
    测试 Coppersmith 攻击：已知 p 的高位，恢复完整的 p
    使用真实的 CTF 题目数据进行黑盒测试
    """
    from ctf_lib.crypto.rsa_utils import coppersmith_known_high_bits_p

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
    
def test_egcd():
    from ctf_lib.crypto.math import egcd
    a,b = 26513, 32321
    
    gcd, x, y = egcd(a,b)
    assert gcd == 1
    assert x == 10245
    assert y == -8404
    
def test_fourth_roots():
    from ctf_lib.crypto.math import fourth_roots
    p= 192727101346792420690851183107786009159
    q= 213791247881086783717490511527686010383
    c= 27872160381271215432744556706983596441965355425069208829644036875403222860004

    rp = fourth_roots(c, p)
    assert len(rp) == 2
    assert 130269443945815627411303225969232316704 in rp
    assert 62457657400976793279547957138553692455 in rp

    rq = fourth_roots(c, q)
    assert len(rq) == 2
    assert 70940219739169660676656017679156145870 in rq
    assert 142851028141917123040834493848529864513 in rq

def test_fetch_factors_from_factordb():
    from ctf_lib.crypto.factor import fetch_factors_from_factordb
    from sage.misc.misc_c import prod

    fs = fetch_factors_from_factordb(1145141919810)
    assert isinstance(fs,list)
    assert isinstance(fs[0],int)
    assert prod(fs) == 1145141919810
    
    n = 144709507748526661267852152217031923282704243254105275252262414154410511284347828603240755427862752297392095652561239549522158121842455510674435510821274029842500154931546666242034086499872050823824437303603895977092291834159890433746969317535636398062008995784281741721729948231010601796589449187553147904043991226174291329
    fs = fetch_factors_from_factordb(n)
    assert isinstance(fs,list)
    assert isinstance(fs[0],int)
    assert prod(fs) == n
    
