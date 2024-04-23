import logging
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

from app.ingest.match_writer import MatchWriter
from app.notebook_utils import t20_matches
from app.utils import StopWatch, row_count

GENDER = "male"
MATCH_TYPE = "T20"

db = sqlite3.connect(f"{GENDER}_{MATCH_TYPE}.sqlite")


FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)


def clear_down_db(target_db: sqlite3.Connection):
    rows = target_db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    logging.info(f"{len(rows)} tables to drop")
    for row in rows:
        table_name = row[0]
        target_db.execute(f"DROP TABLE IF EXISTS {table_name}")


clear_down_db(db)

with closing(db.cursor()) as csr:
    csr.executescript(Path("schema.sql").read_text())
    logging.info("created tables")


with StopWatch("match_loading", 2) as timer:
    for done, match in enumerate(t20_matches(GENDER, MATCH_TYPE), start=1):
        MatchWriter(db).write(match)
        if done % 200 == 0:
            timer.report_split(f"{done=}")


for table in ["matches", "teams", "participation", "balls", "players", "selections"]:
    print(f"{table}:", row_count(db, table))
