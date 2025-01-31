from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin

from matchday.common.db import books_db_path
from matchday.models.team import Team


@dataclass
class Book(DataClassJsonMixin):
    team_1: Team = field(default_factory=Team)
    team_2: Team = field(default_factory=Team)

    def create(self: Book) -> int:
        with sqlite3.connect(books_db_path) as conn:
            csr = conn.execute(
                "INSERT INTO books (content) VALUES (:json) RETURNING *",
                {"json": self.to_json()},
            )
            row = csr.fetchone()
            return row[0]
