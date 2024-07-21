"""
After unzipping `all_json.zip` (or whatever) to `/all`, this redistributes the retrieved
files into the `/matches` folder by gender and match type
"""

import json
from collections import defaultdict
from pathlib import Path

c: dict = defaultdict(int)


def check_match_dir(p: Path):
    if not p.exists():
        print(f"{p} not found, checking parent")
        check_match_dir(p.parent)
        Path.mkdir(p)


for p in Path("all").glob("*.json"):
    with p.open() as f:
        m = json.load(f)
    match_type = m["info"]["match_type"]
    gender = m["info"]["gender"]
    c[(match_type, gender)] += 1
    target_dir = Path("matches") / gender / match_type
    check_match_dir(target_dir)
    p.rename(target_dir / p.name)
print(c)
