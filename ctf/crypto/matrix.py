from typing import Optional
import logging

logger = logging.getLogger(__name__)

def solve_matrix_2x2_dlp(
        A_raw: list[list[int]],
        B_raw: list[list[int]],
        p: int,
        drop_largest_prime : bool = False
    ) -> tuple[int, int]:
    """求解2x2矩阵的DLP问题：B = A ^ k (mod p)

    Args:
        A_raw (list[list[int]]): 矩阵底数
        B_raw (list[list[int]]): 矩阵幂
        p (int): 有限域模数
        drop_some_largest_prime (int): 去掉不光滑的因子个数，会降低当前求解信息量，默认不去掉

    Returns:
        (k, m) (tuple[int, int]): 若可以计算，矩阵的离散对数值及其模数
    """
    from sage.all import GF, Matrix, ZZ, factor, discrete_log, crt, lcm, ceil, floor

    def eigenvalues_over_split_field(A, p):
        F = GF(p)
        AF = A.change_ring(F)
        roots = AF.charpoly().roots(multiplicities=False)
        if len(roots) == 2:
            return roots, F
        K = GF(p**2, name='t', modulus=AF.charpoly()); t=K.gen()
        AK = AF.change_ring(K)
        roots = [r[0] for r in AK.charpoly().roots()]
        return roots, K


    def solve_k_mod_factor(a, b, p, drop_largest_prime=0):
        roots_A, K = eigenvalues_over_split_field(a, p)
        AK = a.change_ring(K)
        BK = b.change_ring(K)
        roots_B = [r[0] for r in BK.charpoly().roots()]

        pairs = []
        for perm in [(0, 1), (1, 0)]:
            congr = []
            mods = []
            ok = True
            for i in [0, 1]:
                lamA = roots_A[i]
                lamB = roots_B[perm[i]]
                ordA = ZZ(lamA.multiplicative_order())
                if drop_largest_prime:
                    fac = factor(ordA)
                    largest = max(ZZ(pr) for pr, _ in fac)
                    m = ordA // largest
                    base = lamA**largest
                    target = lamB**largest
                else:
                    m = ordA
                    base = lamA
                    target = lamB

                try:
                    k_i = ZZ(discrete_log(target, base, ord=m, operation="*"))
                except Exception:
                    ok = False
                    break
                congr.append(k_i)
                mods.append(ZZ(m))

            if not ok:
                continue

            try:
                k_mod = crt(congr[0], congr[1], mods[0], mods[1])
                m_mod = lcm(mods[0], mods[1])
            except Exception:
                continue
            pairs.append((ZZ(k_mod), ZZ(m_mod)))

        if not pairs:
            raise RuntimeError(f"no dlog solution modulo prime factor p={p}")

        pairs.sort(key=lambda km: km[1].nbits(), reverse=False)
        print(pairs)
        return pairs[0]

    F = GF(p)
    A = Matrix(F, A_raw)
    B = Matrix(F, B_raw)
    
    k, m = solve_k_mod_factor(A, B, p, drop_largest_prime)

    if not drop_largest_prime and A**k != B:
        raise RuntimeError("sanity check failed: A^k != B")
    if drop_largest_prime:
        print("[-] check ignored for dropping largest prime")
    return k, m