import re
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent
books_db_path = db_path / "books.sqlite"
schema_path = db_path / "books_schema.sql"

parameter_fix_pattern = re.compile(r"('\{\{([^}]+)\}\}')")


def string_to_parameter(txt: str) -> str:
    """
    parameter fixing:
    Because I like formatted, syntax-coloured SQL, I like to use explicit .sql files.
    But because the formatter I'm currently using (Prettier) doesn't understand my SQLite
    named parameters (e.g. :parameter) and gives up, I've adopted a convention of putting
    the parameter name inside '{{}}' and regex-replacing on retrieval. This may change, but
    for now it seems like a workable workaraound
    """
    return re.sub(parameter_fix_pattern, r":\2", txt)


def sql(file_name: str) -> str:
    path = Path(__file__).parent.parent / "models/sql" / f"{file_name}.sql"
    txt = path.open().read()
    return string_to_parameter(txt)


def initialise_db(conn: sqlite3.Connection) -> None:
    sql = schema_path.read_text()
    conn.executescript(sql)
