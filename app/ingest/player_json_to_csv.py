import csv
import json
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path.cwd() / "data"

json_dir = DATA_DIR / "player_json"

fieldnames = [
    "player_id",
    "dob",
    "role",
    "bat_style",
    "bowl_style",
    "datetime_spidered",
]


def isodate_from(dob: dict) -> str | None:
    if not dob:
        return None
    yy = dob.get("year")
    mm = dob.get("month")
    dd = dob.get("date")
    return date(int(yy), int(mm), int(dd)).isoformat() if yy and mm and dd else None


def first_from(ary: list[str]) -> str | None:
    return ary[0] if ary else None


def player_info(player_id: str, j: dict, mod_time) -> dict:
    p = j["player"]
    return {
        "player_id": int(player_id),
        "dob": isodate_from(p.get("dateOfBirth")),
        "role": first_from(p.get("playingRoles", [])),
        "bat_style": first_from(p.get("battingStyles", [])),
        "bowl_style": first_from(p.get("bowlingStyles", [])),
        "datetime_spidered": datetime.fromtimestamp(mod_time),
    }


outfile = DATA_DIR / "player_info.csv"

with outfile.open("w") as fout:
    writer = csv.DictWriter(fout, fieldnames)
    writer.writeheader()
    for path in json_dir.glob("*.json"):
        player_id = path.stem
        with path.open() as fin:
            player_json = json.load(fin)
        writer.writerow(player_info(player_id, player_json, path.stat().st_mtime))
