from ctf.pipe import *
from typing import Callable, Any

import os
system = F(os.system)

from sys import stdin, stdout, stderr

import base64
from subprocess import run, Popen
from time import sleep
from string import ascii_letters as ALPHA, ascii_lowercase as LOWER, \
  ascii_uppercase as UPPER, digits as NUMER, punctuation as PUNCT, printable as PRINT, \
    whitespace as WS, hexdigits as HEXD

# builtins
fabs = F(abs)
fall = F(all)
fany = F(any)
fchr = F(chr)
ford = F(ord)
fdela= F(delattr)
fdir = F(dir)
fenum= F(enumerate)
feval= F(eval)
fexec= F(exec)
ffilter = F.R(filter)
fgeta = F(getattr)
fhasa = F(hasattr)
fisi = F(isinstance)
fiss = F(issubclass)
flen = F(len)
fmap = F.R(map)
fmax = F(max)
fmin = F(min)
fround = F(round)
fseta = F(setattr)
fsum = F(sum) # 区别于 __builtins__.sum
fzip = F(zip)
ls = F(list)
uniq = F(list) @ F(set)
sort = F(sorted)
uniqsort = F(list) @ F(dict.fromkeys)
man = F(help)


import math
# Python int method
floor = F(math.floor)
ceil = F(math.ceil)
ito0 = F(bin)
length0 = F(int.bit_length)
count1 = F(int.bit_count)
average = F(lambda x: (x | fsum) / (x | flen))

# ML-style list/string processor
head = S[0]
tail = S[1:]
last = S[-1]
init = S[:-1]
take = lambda x: S[:x]
drop = lambda x: S[x:]
splitAt = lambda x: (S[:x], S[x:])
null = F(lambda x: x | flen == 0)
reverse = S[::-1]


# Python string/bytes processor
strip = F(str.strip)
upper = F(str.upper)
lower = F(str.lower)
count = F(str.count)
find = F(str.find)
index = F(str.index)
join = DefaultR(str.join, "") # 为 join 方法提供默认参数
rfind = F(str.rfind)
rindex = F(str.rindex)
split = F(str.split)
def tr (set1: str, set2: str, delete: str = "") -> F:
  return F(str.translate, str.maketrans(set1, set2, delete))

endswith = F(str.endswith)
startswith = F(str.startswith)
isalpha = F(str.isalpha)
isalnum = F(str.isalnum)
isascii = F(str.isascii)
islower = F(str.islower)
isdigit = F(str.isdigit)
isdecimal = F(str.isdecimal)
isnumeric = F(str.isnumeric)
isspace = F(str.isspace)
isprintable = F(str.isprintable)
replace = F(str.replace)
zfill = F(str.zfill)


# Python bytes
bstrip = F(bytes.strip)

# C-style type converter
stoi = F(int)
itos = F(str)
itoh = F(hex)
itoo = F(oct)
htoi = F(int, 16)
otoi = F(int, 8)
stob = F(str.encode, encoding="utf-8")
itob = F(int.to_bytes, length=8)
ltob = F(bytes, encoding="utf-8")
htob = F(bytes.fromhex)
Btob = F(base64.b64decode)
btos = F(bytes.decode, encoding="utf-8")
btoi = F(int.from_bytes, byteorder='big')
btoh = F(bytes.hex)
btoB = F(base64.b64encode)
btol = F(list)

import re
search = F.R(re.search)
fmatch = F.R(re.match)
findall = F.R(re.findall)
finditer = F.R(re.finditer)
sub = F.R(re.sub)
rsplit = F.R(re.split)
groups = F(re.Match.groups)
expand = F(re.Match.expand)

import itertools
acc = F.R(itertools.accumulate)
comb = F.R(itertools.combinations) # 'ABCD' | comb(2)
perm = F.R(itertools.combinations) # 'ABCD' | perm(2)
compress = F(itertools.compress)
descarte = F(itertools.product)
repeat = F(itertools.repeat)
filterf = F.R(itertools.filterfalse)
zipl = F(itertools.zip_longest)
def predicate (fn: Callable[[Any], bool]) -> F:
  return F.R(map, fn)

# I have functools by myself: pipe.py

import operator
has = F(operator.__contains__)
ne = F(operator.__not__)
is_a = F(operator.is_)
isMod = lambda n: F(lambda x: x % n == 0)
product = F(operator.mul).slash

import hashlib
sha1sum = F(lambda x: hashlib.sha1(x).hexdigest())
sha256sum = F(lambda x: hashlib.sha256(x).hexdigest())
md5sum = F(lambda x: hashlib.md5(x).hexdigest())

import urllib.parse
urlquote = F(urllib.parse.quote_plus)
urlunquote = F(urllib.parse.unquote_plus)
urlencode = F(urllib.parse.urlencode)
 
import json
jdump = F(json.dump)
jload = F(json.load)

import pprint
info = F(pprint.pprint)