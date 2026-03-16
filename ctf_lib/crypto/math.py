import logging

logger = logging.getLogger(__name__)

def egcd(a:int, b:int) -> tuple[int, int, int]:
    """
    扩展欧几里德公式，求解方程 ax+by=gcd(a,b)，
    
    参数:
        a: 整数
        b: 整数
        
    返回:
        返回 gcd, x, y
    """
    logger.debug(f"calculate ax+by=gcd(a,b), {a=}, {b=}")
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def fourth_roots(c:int, p:int) -> list[int]:
    """基于sage的模平方根计算四次方根，一般会有正负两个解

    参数:
        c (int): 被开方的数
        p (int): 整数环，要求奇素数

    Returns:
        list[int]: 四次方根的个数

    """
    from sage.rings.finite_rings.integer_mod import Mod, square_root_mod_prime
    r = Mod(c, p)
    r = square_root_mod_prime(r)
    if r is None:
        return []
    roots = set()
    for y in (r, -r):
        s = square_root_mod_prime(y)
        if s is None:
            continue
        roots.add(int(s))
        roots.add(int(-s))
    return list(roots)