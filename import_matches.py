import logging
import sqlite3
from contextlib import closing
from dataclasses import asdict
from pathlib import Path

from dataclass_csv import DataclassReader

from app.config import config
from app.ingest.classes import Person
from app.ingest.match_writer import MatchWriter
from app.utils import StopWatch, row_count, setup_logging, t20_matches


def load_match_data(db: sqlite3.Connection):

    with closing(db.cursor()) as csr:
        csr.executescript(Path("schema.sql").read_text())
        logging.info("created tables")

    with StopWatch("match_loading", decimals=2) as timer:
        ignored = 0
        for done, match in enumerate(
            t20_matches(config.gender, config.match_type), start=1
        ):
            # don't write Hundred matches (yet?)
            if match.info.balls_per_over == 6:
                MatchWriter(db).write(match)
            else:
                ignored += 1
            if done % 500 == 0:
                timer.report_split(f"{done=}, {ignored=}")

    for table in [
        "matches",
        "teams",
        "participation",
        "balls",
        "players",
        "selections",
    ]:
        print(f"{table}:", row_count(db, table))


def load_people(db: sqlite3.Connection):
    path = Path("data/people.csv")
    with path.open() as f:
        reader = DataclassReader(f, Person)
        persons = list(reader)
        print("rows:", len(persons))
    values = [asdict(person) for person in persons]

    sql = """INSERT INTO people (
        identifier, name, unique_name, key_bcci, key_bcci_2, key_bigbash, key_cricbuzz,
        key_cricheroes, key_crichq, key_cricinfo, key_cricinfo_2, key_cricingif, key_cricketarchive,
        key_cricketarchive_2, key_nvplay, key_nvplay_2, key_opta, key_opta_2, key_pulse, key_pulse_2
        )
    VALUES (
        :identifier, :name, :unique_name, :key_bcci, :key_bcci_2, :key_bigbash, :key_cricbuzz,
        :key_cricheroes, :key_crichq, :key_cricinfo, :key_cricinfo_2, :key_cricingif, :key_cricketarchive,
        :key_cricketarchive_2, :key_nvplay, :key_nvplay_2, :key_opta, :key_opta_2, :key_pulse, :key_pulse_2
    )"""

    db.executemany(sql, values)
    db.commit()

    print("people:", row_count(db, "people"))


if __name__ == "__main__":
    db = sqlite3.connect(config.db_filename)
    db.row_factory = sqlite3.Row
    setup_logging()
    load_match_data(db)
    load_people(db)
