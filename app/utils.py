import sqlite3
from contextlib import closing
from time import perf_counter


def row_count(db: sqlite3.Connection, table: str) -> int:
    with closing(db.cursor()) as csr:
        row = csr.execute(f"SELECT Count(*) AS row_count FROM {table}").fetchone()
        return row["row_count"]


class StopWatch:
    def __init__(self, msg: str = "", decimals: int = 8) -> None:
        self.msg = msg
        self.elapsed_time = 0
        self.start_time = 0
        self.last_split = 0
        self.decimals = decimals

    def __enter__(self):
        self.start_time = perf_counter()
        self.last_split = self.start_time
        return self

    def __exit__(self, type, value, traceback):
        print(f"{self.elapsed:.{self.decimals}f} {self.msg}")

    @property
    def elapsed(self) -> float:
        return perf_counter() - self.start_time

    def report_split(self, msg: str = ""):
        time_now = perf_counter()
        split_time = time_now - self.last_split
        self.last_split = time_now
        print(f"{split_time:.{self.decimals}f} {self.elapsed:.{self.decimals}f} {msg}")
