import logging
import sqlite3
import sys
from contextlib import closing
from datetime import datetime
from pathlib import Path
from time import perf_counter
from typing import Any, Generator

from app.ingest.classes import Match


def t20_dirs(gender: str, match_type: str):
    yield from Path("matches").glob(f"{gender}/{match_type}")


def t20_matches(
    gender: str = "*", match_type: str = "*"
) -> Generator[Match, Any, Any]:  # list[Match]:
    for d in t20_dirs(gender, match_type):
        for p in d.glob("*.json"):
            match = Match.from_json(p.read_text())
            match.info.file_path = str(p)
            yield match


def setup_logging() -> None:
    FORMAT = "%(asctime)s %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def row_count(db: sqlite3.Connection, table: str) -> int:
    with closing(db.cursor()) as csr:
        row = csr.execute(f"SELECT Count(*) AS row_count FROM {table}").fetchone()
        return row["row_count"]


class StopWatch:
    def __init__(
        self, msg: str = "", decimals: int = 8, report_every: int = 1000
    ) -> None:
        self.msg = msg
        self.start_time = 0
        self.last_split = 0.0
        self.decimals = decimals
        self.ticks: int = 0
        self.report_every = report_every

    def __enter__(self):
        self.start_time = perf_counter()
        self.last_split = self.start_time
        if len(self.msg):
            print(f"{datetime.now()} {self.msg} entered")
        return self

    def __exit__(self, type, value, traceback):
        if self.msg:
            print(f"{datetime.now()} {self.elapsed_formatted} {self.msg} exited")

    @property
    def elapsed(self) -> float:
        return perf_counter() - self.start_time

    @property
    def elapsed_formatted(self) -> str:
        return f"{self.elapsed:.{self.decimals}f}"

    def report_split(self, msg: str = ""):
        time_now = perf_counter()
        split_time = time_now - self.last_split
        self.last_split = time_now
        print(
            f"{datetime.now()} {split_time:.{self.decimals}f}"
            f"{self.elapsed_formatted} {msg}{f' {str(self.ticks)}' if self.ticks else ''} "
        )

    def tick(self) -> None:
        self.ticks += 1
        if self.ticks % self.report_every == 0:
            self.report_split()
