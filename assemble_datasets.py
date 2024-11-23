import csv
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

from app.config import config

DATA_DIR = Path.cwd() / "data"
SQL_DIR = Path.cwd() / "app/analysis/sql"
db = config.db_connection


params = {
    "max_match_date": date(2023, 7, 1),
    "min_balls_faced": 250,
    "min_balls_faced_in_over": 10,
    "min_balls_bowled": 240,
    "min_balls_bowled_in_over": 18,
}


def sql_text(query_filename: str) -> str:
    return open(SQL_DIR / f"{query_filename}.sql").read()


batter_aggrs = {
    int(row["batter"]): row["aggression"]
    for row in db.execute(sql_text("batter_aggression"), params)
}
print(f"got {len(batter_aggrs)} batter aggressions")

with open(DATA_DIR / "batter_aggrs.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows([k, v] for k, v in batter_aggrs.items())

bowler_econs = {
    int(row["bowler"]): row["economy"]
    for row in db.execute(sql_text("bowler_economy"), params)
}
print(f"got {len(bowler_econs)} bowler economies")

with open(DATA_DIR / "bowler_econs.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows([k, v] for k, v in bowler_econs.items())


def enriched_row(row: dict) -> dict[Any, Any]:
    row["batter_aggro"] = batter_aggrs.get(row["batter"], 0)
    row["bowler_econ"] = bowler_econs.get(row["bowler"], 0)
    return row


res: list = db.execute(sql_text("all_balls_input_data"), params).fetchall()
rows = [dict(r) for r in res]
print(f"got {len(rows)} bowled ball outcomes")


def enhanced_row(d: dict) -> dict:
    d["batter_aggr"] = batter_aggrs.get(d["batter_id"], 0.0)
    d["bowler_econ"] = bowler_econs.get(d["bowler_id"], 0.0)
    d.pop("batter_id")
    d.pop("bowler_id")
    return d


data = [enhanced_row(r) for r in rows]
df = pd.DataFrame(data)

df.to_parquet(DATA_DIR / "data.parquet")
