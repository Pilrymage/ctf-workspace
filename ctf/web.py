from pipe import *

  
  
try:
  from scapy.all import *
except ImportError:
  print("[!] scapy 未安装，以太网管理功能。") 