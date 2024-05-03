import sqlite3
from contextlib import closing

from app.ingest.classes import Info, Innings, Match


class MatchWriter:
    def __init__(self, db: sqlite3.Connection) -> None:
        self.db: sqlite3.Connection = db
        self.db.row_factory = sqlite3.Row
        self.team_ids: dict[str, int] = {}
        self.match_id: int = -1
        self.player_ids: dict[str, int] = {}

    def write(self, match: Match):
        self.write_teams(match.info.teams)
        self.write_match_from_info(match.info)
        self.write_participating_teams(match.innings)
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

    def write_participating_teams(self, innings: list[Innings]) -> None:
        bat_first = innings[0].team
        with closing(self.db.cursor()) as csr:
            for team_name, team_id in self.team_ids.items():
                innings_index = 0 if team_name == bat_first else 1
                csr.execute(
                    """
                    INSERT INTO participation (match_id,team_id,innings)
                    VALUES
                    (:match_id, :team_id, :innings)
                """,
                    {
                        "match_id": self.match_id,
                        "team_id": team_id,
                        "innings": innings_index,
                    },
                )

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
        player_id_sql = """
        SELECT p.name, p.rowid
        FROM players p
        JOIN selections s ON s.match_id = :match_id AND s.player_id = p.rowid
        """
        with closing(self.db.cursor()) as csr:
            csr.execute(player_id_sql, {"match_id": self.match_id})
            self.player_ids = {row["name"]: row["rowid"] for row in csr.fetchall()}

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
        SELECT
          :match_id
        , :innings
        , :over
        , :ball_seq
        , :ball
        , pbowl.rowid
        , pbat.rowid
        , pnons.rowid
        , :batter_runs
        , :extra_runs
        , :extra_type
        , :wicket_fell
        , :dismissed
        , :how_out
        FROM selections sbowl
        JOIN selections sbat ON sbat.match_id = sbowl.match_id
        JOIN selections snons ON snons.match_id = sbowl.match_id
        JOIN players pbowl ON pbowl.rowid = sbowl.player_id AND pbowl.name = :bowled_by
        JOIN players pbat ON pbat.rowid = sbat.player_id AND pbat.name = :batter
        JOIN players pnons ON pnons.rowid = snons.player_id AND pnons.name = :non_striker
        WHERE sbowl.match_id = :match_id
        """
        match_key_info = {
            "match_id": self.match_id,
            "innings": index,
        }
        insert_list = innings.database_balls()
        with closing(self.db.cursor()) as csr:
            csr.executemany(
                sql,
                [ball_dict | match_key_info for ball_dict in insert_list],
            )
