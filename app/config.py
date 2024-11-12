import sqlite3
from pathlib import Path


class Configurator:
    gender: str = "male"
    match_type: str = "T20"

    def __init__(self) -> None:
        self.connection = None

    @property
    def db_filename(self) -> str:
        return f"{self.gender.lower()}_{self.match_type.lower()}.db"

    @property
    def db_connection(self) -> sqlite3.Connection:
        if self.connection:
            return self.connection
        db_path = Path(__file__).parent / self.db_filename
        print(f"Connecting to {db_path}")
        self.connection = sqlite3.connect(db_path)
        return self.connection


config = Configurator()
