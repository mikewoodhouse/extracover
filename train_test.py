import sqlite3
from pathlib import Path

from app.config import config
from app.model.batting_order_generator import (BatterPositionFrequencies,
                                               BattingOrderGenerator)
from app.model.bowling_order_generator import (BowlingOrderGenerator,
                                               OverFrequencyRecord)
from app.model.scorebook import Match, Player, Team

match = Match(
    teams=[
        Team(
            name="West Indies",
            players=[
                Player(player_id=684, name="BA King"),
                Player(player_id=461, name="KR Mayers"),
                Player(player_id=46, name="J Charles"),
                Player(player_id=59, name="N Pooran"),
                Player(player_id=686, name="R Powell"),
                Player(player_id=687, name="SO Hetmyer"),
                Player(player_id=688, name="R Shepherd"),
                Player(player_id=465, name="JO Holder"),
                Player(player_id=60, name="AJ Hosein"),
                Player(player_id=52, name="AS Joseph"),
                Player(player_id=469, name="OC McCoy"),
            ],
        ),
        Team(
            name="India",
            players=[
                Player(player_id=947, name="Ishan Kishan"),
                Player(player_id=1464, name="Shubman Gill"),
                Player(player_id=950, name="SA Yadav"),
                Player(player_id=949, name="Tilak Varma"),
                Player(player_id=1011, name="HH Pandya"),
                Player(player_id=486, name="SV Samson"),
                Player(player_id=71, name="AR Patel"),
                Player(player_id=565, name="Kuldeep Yadav"),
                Player(player_id=946, name="Arshdeep Singh"),
                Player(player_id=146, name="YS Chahal"),
                Player(player_id=1762, name="Mukesh Kumar"),
            ],
        ),
    ]
)

SQL_DIR = Path(__file__).parent / "app" / "model" / "sql"


def sql_text(query_filename: str) -> str:
    return open(SQL_DIR / f"{query_filename}.sql").read()


# put player ids into `target_match` database, `players` table
player_data = [(p.name, p.player_id) for team in match.teams for p in team.players]
target_match_db_path = config.db_dir / "target_match.db"
with sqlite3.connect(target_match_db_path) as con:
    con.execute("DELETE FROM players")
    con.executemany("INSERT INTO players (name, player_id) VALUES (?, ?)", player_data)

with config.db_connection as db:
    db.execute(f"ATTACH DATABASE '{target_match_db_path}' AS tm;")

    # get bowler over freqs
    csr = db.execute(sql_text("bowler_over_frequencies"), match.db_params)
    bowler_over_freqs = [OverFrequencyRecord(**row) for row in csr.fetchall()]
    csr.close()

    # get batter position freqs
    csr = db.execute(sql_text("batting_position_frequencies"), match.db_params)
    batting_pos_freqs: dict[int, BatterPositionFrequencies] = {
        pid: BatterPositionFrequencies(player_id=pid, name=nm)
        for nm, pid in player_data
    }
    for row in csr.fetchall():
        player_id = int(row["player_id"])
        position = int(row["position"]) - 1
        num_times = float(row["times_in_position"])
        batting_pos_freqs[player_id].times_in_positions[position] = num_times
    csr.close()

    for team in match.teams:
        team_player_ids = [p.player_id for p in team.players]

        team_bowling_freqs = list(
            filter(lambda f: f.player_id in team_player_ids, bowler_over_freqs)
        )
        team.bowling_order_gen = BowlingOrderGenerator(team_bowling_freqs)

        team_batting_freqs = list(
            filter(lambda f: f.player_id in team_player_ids, batting_pos_freqs.values())
        )
        team.batting_order_gen = BattingOrderGenerator(team_batting_freqs)


# get batter aggressions
# get bowler_economies
# select team to bat first
# for each innings
# # build batting order
# # build bowling order
