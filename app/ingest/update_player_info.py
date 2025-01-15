import csv
import sqlite3
from pathlib import Path

# from app.utils import StopWatch


def update_player_info():
    # db = sqlite3.connect(config.db_filename)
    db = sqlite3.connect(Path.cwd() / "male_t20.db")

    DATA_DIR = Path.cwd() / "data"

    # db.execute("""
    #         UPDATE players
    #         SET
    #           cricinfo = ppl.key_cricinfo
    #         , cricinfo_2 = ppl.key_cricinfo_2
    #         FROM
    #             people ppl
    #         WHERE
    #             ppl.identifier = reg;""")

    # with StopWatch("Player info update", 3) as timer:
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
                WHERE cricinfo = :cricinfo
                """,
                row,
            )
            db.commit()
            done += 1
            #     if done % 500 == 0:
            #         timer.report_split(f"{done=}")
            # timer.report_split(f"Complete: {done=}")


if __name__ == "__main__":
    update_player_info()
