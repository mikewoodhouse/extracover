import csv
import sqlite3
from pathlib import Path

from app.config import config
from app.utils import StopWatch

db = sqlite3.connect(config.db_filename)

DATA_DIR = Path.cwd() / "data"


with StopWatch("Player info update", 3) as timer:
    csv_path = DATA_DIR / "player_info.csv"
    done = 0
    with csv_path.open("r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            db.execute(
                """
                UPDATE players
                SET
                    datetime_spidered = :datetime_spidered
                ,   dob = :dob
                ,   role = :role
                ,   bat_style = :bat_style
                ,   bowl_style = :bowl_style
                WHERE rowid = :player_id
                """,
                row,
            )
            db.commit()
            done += 1
            if done % 500 == 0:
                timer.report_split(f"{done=}")
        timer.report_split(f"Complete: {done=}")
