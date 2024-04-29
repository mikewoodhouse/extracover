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

db = sqlite3.connect(f"{GENDER.lower()}_{MATCH_TYPE.lower()}.sqlite")


FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)


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
