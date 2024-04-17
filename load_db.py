import logging
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

from app.ingest.classes import Match
from app.ingest.match_writer import MatchWriter
from app.notebook_utils import t20_matches

db = sqlite3.connect("male_t20.sqlite")


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

logging.info("loading matches...")
matches: list[Match] = [m for m in t20_matches("female", "IT20")]
logging.info(f"... {len(matches)} matches loaded")

writer = MatchWriter(db)

writer.write(matches[0])

for row in db.execute("select * from teams").fetchall():
    print(row)
