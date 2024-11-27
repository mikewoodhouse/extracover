from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from dataclasses_json import Undefined, dataclass_json

from app.utils import Database, StopWatch


def empty_list(size: int) -> list[int]:
    return [0] * size


def sql_text(query_filename: str) -> str:
    path = Path(__file__).parent / f"{query_filename}.sql"
    return path.read_text()


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Match:
    match_id: int
    start_date: date


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Ball:
    innings: int
    over: int
    ball: int
    ball_seq: int
    bowled_by: int
    batter: int
    non_striker: int
    batter_runs: int
    extra_runs: int
    extra_type: str
    wicket_fell: bool
    dismissed: str
    how_out: str

    @property
    def wide_noball(self) -> bool:
        return self.extra_type in ("wide", "noball")

    @property
    def batsman_out(self) -> bool:
        return bool(self.how_out) and not self.how_out.startswith("retired")

    @property
    def was_legal(self) -> bool:
        return self.extra_type == ""


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Player:
    player_id: int
    name: str
    matches: int = 0
    batting_positions: list[int] = field(default_factory=lambda: empty_list(11))
    balls_faced: int = 0
    times_out: int = 0
    scoring_shots: list[int] = field(default_factory=lambda: empty_list(7))
    overs_bowled: list[int] = field(default_factory=lambda: empty_list(20))
    balls_bowled: int = 0
    noballs: int = 0
    wides: int = 0
    runs_conceded: int = 0
    wickets_taken: int = 0

    def record_batting_position(self, pos: int) -> None:
        pos = min(
            pos, 10
        )  # b/c some leagues allow an injury substitute, BPL 2021/22 as an example
        self.batting_positions[pos] += 1

    def record_ball_bowled(self, ball: Ball) -> None:
        if ball.ball_seq == 0:
            self.overs_bowled[ball.over] += 1
        self.balls_bowled += 1
        match ball.extra_type:
            case "wide":
                self.wides += 1
            case "noball":
                self.noballs += 1
            case "bye", "legbye":
                self.runs_conceded += ball.batter_runs
        if ball.wicket_fell and ball.how_out not in (
            "run out",
            "retired hurt",
            "retired not out",
            "retired out",
        ):
            self.wickets_taken += 1

    def record_ball_faced(self, ball: Ball) -> None:
        self.balls_faced += 1
        if ball.wicket_fell and ball.dismissed == self.name:
            self.times_out += 1
        else:
            if not ball.wide_noball:
                runs = min(
                    ball.batter_runs, 6
                )  # count weird penalty additions as sixes
                self.scoring_shots[runs] += 1

    @property
    def total_runs_scored(self) -> int:
        return sum(
            shot_runs * times_recorded
            for shot_runs, times_recorded in enumerate(self.scoring_shots)
        )

    @property
    def strike_rate(self) -> float:
        return (
            0.0
            if self.balls_faced == 0
            else self.total_runs_scored * 100.0 / self.balls_faced
        )

    @property
    def economy(self) -> float:
        return (
            0.0
            if self.balls_bowled == 0
            else 6.0 * self.runs_conceded / self.balls_bowled
        )

    @property
    def wide_rate(self) -> float:
        return 0.0 if self.balls_bowled == 0 else float(self.wides) / self.balls_bowled

    @property
    def noball_rate(self) -> float:
        return (
            0.0 if self.balls_bowled == 0 else float(self.noballs) / self.balls_bowled
        )

    def __repr__(self) -> str:
        s = (
            f"{self.name=} {self.player_id=} {self.matches} apps,"
            f" {self.total_runs_scored=} off {self.balls_faced=} {self.strike_rate=:0.2f}"
            f" {self.runs_conceded=} from {self.balls_bowled=} {self.economy=:0.2f}"
            f" w: {self.wide_rate:0.2f} nb: {self.noball_rate:0.2f}"
        )
        return s.replace("self.", "")


@dataclass
class MatchState:
    total: int = 0
    target: int = 0
    wickets: int = 0
    balls_bowled: int = 0
    run_rate: float = 0.0
    req_rate: float = 0.0

    def update(self, ball: Ball) -> None:
        self.total += ball.batter_runs + ball.extra_runs
        if ball.batsman_out:
            self.wickets += 1
        if ball.was_legal:
            self.balls_bowled += 1
        self.run_rate = 6.0 * self.total / self.balls_bowled if self.balls_bowled else 0
        if ball.innings == 1:
            self.req_rate = (
                (self.target + 1.0) / (120.0 - self.balls_bowled)
                if self.balls_bowled < 120
                else 0
            )


class DatasetBuilder:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.players: dict[int, Player] = {}

    def run(self) -> None:
        with StopWatch(msg="match loop", decimals=5) as stopwatch:
            for row in self.db.query_result(
                "SELECT ROWID AS match_id, * FROM matches ORDER BY start_date"
            ):
                match = Match(**row)
                self.process_match(match.match_id)
                stopwatch.tick()

    def process_match(self, match_id: int):
        self.add_players(match_id)
        target = 0
        for innings in range(2):
            has_batted: set[int] = set()
            state = MatchState(target=target if innings == 1 else 0)
            for row in self.db.query_result(
                """SELECT
                        * FROM balls
                        WHERE match_id = :match_id
                        AND innings = :innings
                        ORDER BY over, ball_seq
                        """,
                {"match_id": match_id, "innings": innings},
            ):
                ball = Ball(**row)
                self.update_for_ball(has_batted, ball)
                state.update(ball)
            target = state.total

    def add_players(self, match_id):
        for row in self.db.query_result(
            """SELECT player_id, name
                    FROM players p
                    JOIN selections s
                    ON s.player_id = p.ROWID
                    WHERE s.match_id = :match_id
                    """,
            {"match_id": match_id},
        ):
            pid = row["player_id"]
            if not self.players.get(pid, None):
                self.players[pid] = Player(**row)
            self.players[pid].matches += 1

    def update_for_ball(self, has_batted, ball):
        batter = self.players[ball.batter]
        bowler = self.players[ball.bowled_by]

        # batting order
        if ball.batter not in has_batted:
            batter.record_batting_position(len(has_batted))
            has_batted.add(ball.batter)
        if ball.non_striker not in has_batted:
            self.players[ball.non_striker].record_batting_position(len(has_batted))
            has_batted.add(ball.non_striker)

        # ball-based events
        batter.record_ball_faced(ball)
        bowler.record_ball_bowled(ball)
