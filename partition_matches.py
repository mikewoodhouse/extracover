"""
After unzipping `all_json.zip` (or whatever) to `/all`, this redistributes the retrieved
files into the `/matches` folder by gender and match type
"""

import json
from collections import defaultdict
from pathlib import Path

from app.config import config
from app.utils import StopWatch

c: dict = defaultdict(int)


def check_match_dir(p: Path):
    if not p.exists():
        print(f"{p} not found, checking parent")
        check_match_dir(p.parent)
        Path.mkdir(p)


all_dir = config.data_path / "all"

with StopWatch("match_relocation", decimals=2, report_every=1000) as watch:
    for p in all_dir.glob("*.json"):
        with p.open() as f:
            m = json.load(f)
        match_type = m["info"]["match_type"]
        try:
            balls_per_over = m["info"]["balls_per_over"]
        except Exception as e:
            print(e)
            print(m["info"])
            exit()
        if balls_per_over == 5:
            match_type = "TheHundred"
        gender = m["info"]["gender"]
        c[(match_type, gender)] += 1
        target_dir = config.data_path / "matches" / gender / match_type
        check_match_dir(target_dir)
        p.rename(target_dir / p.name)
        watch.tick()
print(c)
