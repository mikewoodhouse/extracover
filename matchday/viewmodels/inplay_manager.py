from matchday.models import Ball, Book


class InplayManager:
    def __init__(self, book: Book) -> None:
        self.book = book
        self.balls: list[Ball] = []
        self.history: list[str] = []
        self.over_num: int = 0
        self.ball_num: int = 0

    @property
    def title(self) -> str:
        return f"{self.book.team_1.name} vs {self.book.team_2.name}"

    def apply(self, ball: Ball) -> None:
        print("applying", ball)
        self.book.update(ball)
        self.balls.append(ball)
        self.ball_num += 1 if ball.is_legal else 0
        if self.ball_num > 6:
            self.over_num += 1
            self.ball_num -= 6
        desc = (
            f"{self.over_num}.{self.ball_num}: "
            f"{self.bowlers[ball.bowler]} to {self.batters[ball.striker]}:"
            f"{'' if ball.is_legal else ball.extra_type} {ball.batter_runs} + {ball.extra_runs}"
        )
        self.history.append(desc)
        print(self.history)

    @property
    def batters(self) -> dict[int, str]:
        return self.book.batting.batters

    @property
    def bowlers(self) -> dict[int, str]:
        return self.book.bowling.bowlers

    @property
    def last_6(self) -> str:
        return "\n".join(self.history[:-6:-1])
