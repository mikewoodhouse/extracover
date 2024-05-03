import json
import sqlite3
from datetime import datetime
from pathlib import Path

from app.ingest.cricinfo_player import CricinfoPlayer
from app.utils import StopWatch
from config import config

SQL = """
SELECT
    peeps.key_cricinfo
,	peeps.key_cricinfo_2
,   plyr.rowid AS player_id
, 	plyr.reg
, 	plyr.name
FROM people peeps
JOIN players plyr ON plyr.reg = peeps.identifier
WHERE plyr.datetime_spidered IS NULL
"""

db = sqlite3.connect(config.db_filename)
db.row_factory = sqlite3.Row

rows = db.execute(SQL).fetchall()

done = 0
not_done = 0

print(f"{datetime.now()} {len(rows)} players to process")

with StopWatch("Cricinfo spider", 3) as timer:

    for row in rows:
        cricinfo_id = row["key_cricinfo"]
        cricinfo_id_2 = row["key_cricinfo_2"]
        player_id = row["player_id"]
        try:
            info_getter = CricinfoPlayer(cricinfo_id, cricinfo_id_2)
        except Exception as e:
            print(f"Exception {e} querying cricinfo for {row}")
            not_done += 1
        if player_info := info_getter.json:
            out_path = Path(__file__).parent / "player_json" / f"{player_id}.json"
            with out_path.open("w") as f:
                json.dump(player_info, f)
            db.execute(
                """
                UPDATE players
                SET datetime_spidered = datetime(current_timestamp, 'localtime')
                WHERE rowid = :player_id
                """,
                {"player_id": player_id},
            )
            db.commit()
            done += 1
            if done % 20 == 0:
                timer.report_split(f"{done=} {not_done=}")

timer.report_split(f"{done=} {not_done=}")
