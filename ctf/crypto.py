from pipe import *

# [Crypto] PyCryptodome 密码学库
try:
  from Crypto.Util.number import *
  from Crypto.Util.Padding import pad, unpad
  from Crypto.Cipher import AES, DES, ARC4
  from Crypto.Random.random import getrandbits
  itob = F(long_to_bytes)
except ImportError:
  print("[!] PyCryptodome 未安装，Crypto 进阶功能将不可用。")

# [Misc / Reverse / Crypto] Z3 定理证明器，解方程神器
try:
  import z3
except ImportError:
  print("[!] z3-solver 未安装，约束求解功能将不可用。")   


try:
  import tqdm
except ImportError:
  print("[!] tqdm 未安装")

