from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from dataclass_csv import DataclassWriter
from dataclasses_json import Undefined, dataclass_json

from app.utils import Database, StopWatch

AVG_RUNS_PER_BALL = 1.21
AVG_WICKET_PROB = 0.054
AVG_WIDE_NOBALL_RATE = 0.036


def empty_list(size: int) -> list[int]:
    return [0] * size


def sql_text(query_filename: str) -> str:
    path = Path(__file__).parent / f"{query_filename}.sql"
    return path.read_text()


DATA_DIR = Path(__file__).parent.parent.parent / "data"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Match:
    match_id: int
    match_number: int
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

    # region methods

    @property
    def wide_noball(self) -> bool:
        return self.extra_type in ("wide", "noball")

    @property
    def batsman_out(self) -> bool:
        return bool(self.how_out) and not self.how_out.startswith("retired")

    @property
    def was_legal(self) -> bool:
        return self.extra_type == ""

    # endregion


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

    # region methods

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
        elif not ball.wide_noball:
            self.scoring_shots[min(ball.batter_runs, 6)] += 1

    @property
    def total_runs_scored(self) -> int:
        return sum(
            shot_runs * times_recorded
            for shot_runs, times_recorded in enumerate(self.scoring_shots)
        )

    @property
    def strike_rate(self) -> float:
        """
        runs per ball
        """
        return (
            AVG_RUNS_PER_BALL
            if self.balls_faced < 10
            else self.total_runs_scored / self.balls_faced
        )

    @property
    def economy(self) -> float:
        """
        runs per ball
        """
        return (
            AVG_RUNS_PER_BALL
            if self.balls_bowled < 12
            else self.runs_conceded / self.balls_bowled
        )

    @property
    def wicket_prob(self) -> float:
        """ "
        per ball
        """
        if self.balls_bowled < 24 or self.wickets_taken < 1:
            return AVG_WICKET_PROB
        return float(self.wickets_taken) / self.balls_bowled

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

    # endregion


@dataclass
class MatchState:
    match_number: int
    start_date: date
    innings: int = 0
    total: int = 0
    target: int = 0
    wickets: int = 0
    balls_bowled: int = 0
    run_rate: float = 0.0  # per *ball*
    req_rate: float = 0.0  # per *ball*
    balls_faced: defaultdict[int, int] = field(default_factory=lambda: defaultdict(int))

    # region methods

    def update(self, ball: Ball) -> None:
        self.total += ball.batter_runs + ball.extra_runs
        if ball.batsman_out:
            self.wickets += 1
        if ball.was_legal:
            self.balls_bowled += 1
        self.run_rate = (
            float(self.total) / self.balls_bowled if self.balls_bowled else 0.0
        )
        self.balls_faced[ball.batter] += 1
        if ball.innings == 1:
            self.req_rate = (
                (self.target - self.total + 1.0) / (120.0 - self.balls_bowled)
                if self.balls_bowled < 120
                else 0.0
            )
            # print(
            #     f"{self.target=} {self.total=}/{self.wickets} {self.balls_bowled} {self.req_rate=}"
            # )

    # endregion


@dataclass
class MLRow:
    # inputs
    match_number: int
    start_date: date
    innings: int
    ball_of_innings: int
    phase: int
    wickets_down: int
    run_rate: float
    req_rate: float  # what value when first innings?
    batter_in_first_10: int
    batter_strike_rate: float
    bowler_economy: float
    bowler_wicket_prob: float
    bowler_wide_noball_rate: float
    # outputs - what actually happened
    outcome: int
    # wide: int
    # noball: int
    # bye: int
    # legbye: int
    # wicket: int
    # dot_ball: int
    # single: int
    # two: int
    # three: int
    # four: int
    # six: int

    @classmethod
    def build(
        cls, ball: Ball, state: MatchState, batter: Player, bowler: Player
    ) -> MLRow:
        # wide = int(ball.extra_type == "wide"),
        # noball = int(ball.extra_type == "noball"),
        # bye = int(ball.extra_type == "bye"),
        # legbye = int(ball.extra_type == "legbye"),
        # wicket = int(ball.wicket_fell),
        # dot_ball = int(ball.batter_runs == 0),
        # single = int(ball.batter_runs == 1),
        # two = int(ball.batter_runs == 2),
        # three = int(ball.batter_runs == 3),
        # four = int(ball.batter_runs == 4),
        # six = int(ball.batter_runs > 4),
        outcome = -1
        if ball.extra_type == "wide":
            outcome = 0
        elif ball.extra_type == "noball":
            outcome = 1
        elif ball.extra_type == "bye":
            outcome = 2
        elif ball.extra_type == "legbye":
            outcome = 3
        elif ball.wicket_fell:
            outcome = 4
        elif ball.batter_runs == 0:
            outcome = 5
        elif ball.batter_runs == 1:
            outcome = 6
        elif ball.batter_runs == 2:
            outcome = 7
        elif ball.batter_runs == 3:
            outcome = 8
        elif ball.batter_runs == 4:
            outcome = 9
        elif ball.batter_runs > 4:
            outcome = 10
        else:
            print(ball)
            outcome = -1
        return MLRow(
            match_number=state.match_number,
            start_date=state.start_date,
            innings=state.innings,
            ball_of_innings=state.balls_bowled,
            phase=0 if ball.over < 6 else 2 if ball.over > 17 else 1,
            wickets_down=state.wickets,
            run_rate=state.run_rate,
            req_rate=state.req_rate,
            batter_in_first_10=int(state.balls_faced[batter.player_id] <= 10),
            batter_strike_rate=batter.strike_rate,
            bowler_economy=bowler.economy,
            bowler_wicket_prob=bowler.wicket_prob,
            bowler_wide_noball_rate=(
                AVG_WIDE_NOBALL_RATE
                if bowler.balls_bowled < 24
                else bowler.wide_rate + bowler.noball_rate
            ),
            outcome=outcome,
        )

    @staticmethod
    def in_bounds(row: MLRow) -> bool:
        return row.req_rate <= 6.0


class DatasetBuilder:
    def __init__(self, db: Database, warm_up_match_count: int = 1000) -> None:
        self.db = db
        self.players: dict[int, Player] = {}
        self.ml_rows: list[MLRow] = []
        self.warm_up_match_count = warm_up_match_count
        self.matches_run = 0
        self.outside_normal_req_rates: int = 0

    def run(self) -> None:
        with StopWatch(msg="DatasetBuilder.run()"):
            with StopWatch(msg="match loop", decimals=5) as stopwatch:
                for row in self.db.query_result(
                    """
                    SELECT
                        ROW_NUMBER() OVER (ORDER BY start_date, match_type_number, ROWID) AS match_number
                    ,	ROWID AS match_id
                    ,	*
                    FROM matches
                    ORDER BY start_date, match_type_number, ROWID
                    """
                ):
                    match = Match(**row)
                    self.process_match(match)
                    self.matches_run += 1
                    stopwatch.tick()

            csv_path = DATA_DIR / "ml_rows.csv"
            with csv_path.open("w") as csv:
                dataclass_writer = DataclassWriter(csv, self.ml_rows, MLRow)
                print(f"writing {len(self.ml_rows)} ML rows")
                dataclass_writer.write()
        print(f"{self.outside_normal_req_rates=}")

    def process_match(self, match: Match) -> None:
        match_id, start_date = match.match_id, match.start_date
        self.add_players(match_id)
        target = 0
        for innings in range(2):
            has_batted: set[int] = set()
            state = MatchState(
                match_number=match.match_number,
                start_date=start_date,
                innings=innings,
                target=target if innings == 1 else 0,
            )
            for row in self.db.query_result(
                """SELECT
                        *
                    FROM balls
                    WHERE match_id = :match_id
                    AND innings = :innings
                    ORDER BY over, ball_seq
                    """,
                {
                    "match_id": match_id,
                    "innings": innings,
                },
            ):
                ball = Ball(**row)

                batter = self.players[ball.batter]
                bowler = self.players[ball.bowled_by]

                ml_row = MLRow.build(ball, state, batter, bowler)
                if ml_row.req_rate >= 0 and ml_row.req_rate <= 6.0:
                    self.ml_rows.append(ml_row)
                else:
                    self.outside_normal_req_rates += 1

                self.update_for_ball(has_batted, ball, batter, bowler)
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

    def update_for_ball(self, has_batted, ball, batter, bowler):
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
