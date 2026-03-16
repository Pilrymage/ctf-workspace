import logging

logger = logging.getLogger(__name__)

def extended_gcd(a:int, b:int) -> tuple[int, int, int]:
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