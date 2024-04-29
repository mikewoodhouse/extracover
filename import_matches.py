import logging
import sqlite3
from contextlib import closing
from pathlib import Path

from app.ingest.match_writer import MatchWriter
from app.notebook_utils import t20_matches
from app.utils import StopWatch, row_count, setup_logging
from config import config

db = sqlite3.connect(config.db_filename)

setup_logging()


with closing(db.cursor()) as csr:
    csr.executescript(Path("schema.sql").read_text())
    logging.info("created tables")


with StopWatch("match_loading", 2) as timer:
    for done, match in enumerate(
        t20_matches(config.gender, config.match_type), start=1
    ):
        MatchWriter(db).write(match)
        if done % 200 == 0:
            timer.report_split(f"{done=}")


for table in ["matches", "teams", "participation", "balls", "players", "selections"]:
    print(f"{table}:", row_count(db, table))
