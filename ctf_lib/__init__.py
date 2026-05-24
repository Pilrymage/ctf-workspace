from os import *
from sys import *
from re import *
from math import *
from struct import *
from base64 import *
from hashlib import *
from binascii import *
from json import *
import urllib.parse
from itertools import permutations, combinations, cycle
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits, punctuation

try:
    from pwn import *
except ImportError:
    print("[!] Pwntools 未安装，Pwn 相关功能将不可用。")
    
try:
    from requests import *
except ImportError:
    print("[!] Requests 未安装，Web 请求功能将不可用。")

# [Crypto] PyCryptodome 密码学库
try:
    from Crypto.Util.number import *
    from Crypto.Cipher import AES, DES, ARC4
except ImportError:
    print("[!] PyCryptodome 未安装，Crypto 进阶功能将不可用。")

# [Misc / Reverse / Crypto] Z3 定理证明器，解方程神器
try:
    import z3
except ImportError:
    print("[!] z3-solver 未安装，约束求解功能将不可用。")   