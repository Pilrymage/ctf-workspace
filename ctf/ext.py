from pipe import *

try:
  import pwnlib
  log_level = pwnlib.context.context.log_level
  info = F(pwnlib.log.info)
  debug = F(pwnlib.log.debug)
  
  from pwn import *
except ImportError :
    print("[!] Pwntools 未安装")

try:
  import requests
  get = F(requests.get)
  post = F(requests.post)
except ImportError:
  print("[!] Requests 未安装")
  
try:
  import tqdm
  tqdm = F(tqdm.tqdm)
except ImportError:
  print("[!] tqdm 未安装")