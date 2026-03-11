import logging
from typing import Optional

# 显式导入需要的 Sage 模块，而不是 import *，这在库文件中是好习惯
from sage.all import PolynomialRing, Zmod, Integer

# 初始化当前模块的日志记录器
logger = logging.getLogger(__name__)

def coppersmith_known_high_bits_p(
    n: int, 
    leak: int, 
    hidden_bits: int, 
    epsilon: float = 0.04
) -> Optional[int]:
    """
    已知 RSA 素数 p 的高位，使用 Coppersmith 定理恢复完整的 p。
    
    参数:
        n: RSA 模数 (N = p * q)
        leak: 泄露的 p 的高位数值
        hidden_bits: p 的低位被隐藏/缺失的比特数
        epsilon: 调节格大小的参数，越小越容易出解但越慢。默认 0.04
        
    返回:
        成功则返回完整的 p (int)，失败返回 None
    """
    logger.debug(f"Starting Coppersmith: hidden_bits={hidden_bits}, epsilon={epsilon}")
    
    # 1. 构造多项式环
    P = PolynomialRing(Zmod(n), names='x'); x = P.gen()
    
    # 2. 还原已知高位并构造目标多项式 f(x)
    p_high = leak << hidden_bits
    f = p_high + x
    
    # 3. 设定未知数 x 的上限 (X)
    X_bound = 2 ** hidden_bits
    
    # 4. 运行 small_roots (耗时操作)
    logger.info("Running small_roots... This might take a while.")
    roots = f.small_roots(X=X_bound, beta=0.5, epsilon=epsilon)
    
    if not roots:
        logger.warning(f"Failed to find roots with epsilon={epsilon}. Try a smaller epsilon.")
        return None
        
    # 5. 验证根是否正确
    for root in roots:
        p_recovered = p_high + Integer(root)
        if n % p_recovered == 0:
            logger.info("Successfully recovered p!")
            return int(p_recovered)  # 强制转换为标准 Python int
            
    logger.error("Roots found, but none are valid factors of N.")
    return None