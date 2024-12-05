from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from dataclass_csv import DataclassWriter

from app.model.classes import Ball, Match, MatchState, Player
from app.utils import Database, StopWatch

AVG_WIDE_NOBALL_RATE = 0.036


def empty_list(size: int) -> list[int]:
    return [0] * size


def sql_text(query_filename: str) -> str:
    path = Path(__file__).parent / f"{query_filename}.sql"
    return path.read_text()


DATA_DIR = Path(__file__).parent.parent.parent / "data"


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
