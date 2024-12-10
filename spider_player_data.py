import json
from datetime import datetime
import sqlite3
from app.ingest.cricinfo_player import CricinfoPlayer
from app.utils import StopWatch

from app.config import config

json_dir = config.data_path / "player_json"


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

db = config.db_connection
db.row_factory = sqlite3.Row
rows = db.execute(SQL).fetchall()

print(f"retrieved {len(rows)} people rows")

done = 0
not_done = 0

print(f"{datetime.now()} {len(rows)} players to process")

with StopWatch("Cricinfo spider", decimals=3) as timer:

    for row in rows:
        cricinfo_id = row["key_cricinfo"]
        cricinfo_id_2 = row["key_cricinfo_2"]
        player_id = row["player_id"]
        try:
            info_getter = CricinfoPlayer(cricinfo_id, cricinfo_id_2)
        except Exception as e:
            print(
                f"Exception {e} querying cricinfo for {cricinfo_id=}, {cricinfo_id_2=}, {row}"
            )
            not_done += 1
            continue
        if player_info := info_getter.json:
            out_path = json_dir / f"{player_id}.json"
            with out_path.open("w") as f:
                json.dump(player_info, f)
            done += 1
            if done % 20 == 0:
                timer.report_split(f"{done=} {not_done=}")

timer.report_split(f"{done=} {not_done=}")
