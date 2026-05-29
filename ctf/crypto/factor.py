import requests 
from urllib.parse import urlencode
from typing import Optional

def fetch_factors_from_factordb(n: int) -> Optional[list[int]]:
    query = urlencode({"query": str(n)})
    url = "https://factordb.com/api?" + query
    r = requests.get(url)
    if r.status_code != 200:
        return None
    fs: list[int] = []
    data = r.json()
    if data["status"] not in ("FF", "P"):
        return None
    for p_str, exp in data["factors"]:
        p = int(p_str)
        for _ in range(int(exp)):
            fs.append(p)
    return fs