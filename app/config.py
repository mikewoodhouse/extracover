import sqlite3
from datetime import date
from pathlib import Path

# SEE: https://docs.python.org/3/library/sqlite3.html#sqlite3-adapter-converter-recipes


def adapt_date_iso(val: date) -> str:
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()


def convert_date(val) -> date:
    """Convert ISO 8601 date to datetime.date object."""
    return date.fromisoformat(val.decode())


sqlite3.register_adapter(date, adapt_date_iso)
sqlite3.register_converter("date", convert_date)


class Configurator:
    gender: str = "male"
    match_type: str = "T20"

    def __init__(self) -> None:
        self.connection = None

    @property
    def db_filename(self) -> str:
        return f"{self.gender.lower()}_{self.match_type.lower()}.db"

    @property
    def db_dir(self) -> Path:
        return Path(__file__).parent.parent

    @property
    def db_path(self) -> Path:
        return self.db_dir / self.db_filename

    @property
    def db_connection(self) -> sqlite3.Connection:
        if self.connection:
            return self.connection
        print(f"Connecting to {self.db_path}")
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection


config = Configurator()
