import sqlite3
from contextlib import closing

from app.ingest.classes import Info, Match


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
        self.write_match_info(match.info)

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

    def write_match_info(self, info: Info) -> None:
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
            self.match_id = csr.lastrowid
