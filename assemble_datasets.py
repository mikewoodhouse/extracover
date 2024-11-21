from datetime import date
from pathlib import Path

from app.config import config

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


res = db.execute(sql_text("batter_aggression"), params)
batter_aggrs = {int(row["batter"]): row["aggression"] for row in res}
print(f"got {len(batter_aggrs)} batter aggressions")

res = db.execute(sql_text("bowler_economy"), params)
bowler_econs = {int(row["bowler"]): row["economy"] for row in res}
print(f"got {len(bowler_econs)} bowler economies")
