import sqlite3
from contextlib import closing

from app.ingest.classes import Info, Innings, Match


class MatchWriter:
    def __init__(self, db: sqlite3.Connection) -> None:
        self.db: sqlite3.Connection = db
        self.db.row_factory = sqlite3.Row
        self.team_ids: dict[str, int] = {}
        self.match_id: int = -1

    def write(self, match: Match):
        """
        1. insert teams where not already present - store ids
        2. insert match - save id from cursor.lastrowid
        3. record team participating in match
        4. insert players where not already present
        5. insert selections - should be able to get player_id using reg
        6. insert balls
        """
        self.write_teams(match.info.teams)
        self.write_match_from_info(match.info)
        self.write_player_selections(match.info)
        for innings_index, innings in enumerate(match.innings):
            self.write_innings_deliveries(innings_index, innings)
        self.db.commit()

    def write_teams(self, teams: list[str]) -> None:
        sql = """
        INSERT OR IGNORE INTO teams (name)
        VALUES (:name)
        ON CONFLICT DO NOTHING
        """
        for team in teams:
            with closing(self.db.cursor()) as csr:
                if row := csr.execute(
                    "SELECT rowid AS team_id FROM teams WHERE name = :name",
                    {"name": team},
                ).fetchone():
                    team_id = row["team_id"]
                else:
                    csr.execute(sql, {"name": team})
                    team_id = csr.lastrowid
                    assert team_id, f"inserted team id for {team} was null"
            self.team_ids[team] = team_id

    def write_match_from_info(self, info: Info) -> None:
        fields = info.database_fields()
        sql = """
        INSERT INTO matches (
          start_date
        , match_type
        , gender
        , venue
        , event
        , city
        , overs
        , balls_per_over
        )
        VALUES (
          :start_date
        , :match_type
        , :gender
        , :venue
        , :event
        , :city
        , :overs
        , :balls_per_over
        )
        """
        with closing(self.db.cursor()) as csr:
            csr.execute(sql, fields)
            match_id = csr.lastrowid
            assert match_id, f"inserted match id is null: {info}"
            self.match_id = match_id

    def write_player_selections(self, info: Info) -> None:
        player_sql = """
        INSERT OR IGNORE INTO players (name, reg)
        VALUES (:name, :reg)
        ON CONFLICT DO NOTHING
        """
        selection_sql = """
        INSERT INTO selections (match_id, team_id, player_id)
        SELECT
            :match_id, :team_id, p.rowid
        FROM players p
        WHERE p.name = :name
        AND p.reg = :reg
        """
        with closing(self.db.cursor()) as csr:
            csr.executemany(player_sql, info.selected_player_regs)
            csr.executemany(
                selection_sql,
                [
                    {
                        "match_id": self.match_id,
                        "team_id": self.team_ids[selection["team"]],
                    }
                    | selection
                    for selection in info.selected_player_regs
                ],
            )

    def write_innings_deliveries(self, index: int, innings: Innings) -> None:
        sql = """
        INSERT INTO balls (
          match_id
        , innings
        , over
        , ball_seq
        , ball
        , bowled_by
        , batter
        , non_striker
        , batter_runs
        , extra_runs
        , extra_type
        , wicket_fell
        , dismissed
        , how_out
        )
        VALUES (
          :match_id
        , :innings
        , :over
        , :ball_seq
        , :ball
        , :bowled_by
        , :batter
        , :non_striker
        , :batter_runs
        , :extra_runs
        , :extra_type
        , :wicket_fell
        , :dismissed
        , :how_out
        )
        """
        match_key_info = {
            "match_id": self.match_id,
            "innings": index,
        }
        with closing(self.db.cursor()) as csr:
            csr.executemany(
                sql,
                [ball_dict | match_key_info for ball_dict in innings.database_balls()],
            )
