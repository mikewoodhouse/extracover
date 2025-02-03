from matchday.models import Ball, Book


class InplayManager:
    def __init__(self, book: Book) -> None:
        self.book = book

    @property
    def title(self) -> str:
        return f"{self.book.team_1.name} vs {self.book.team_2.name}"

    def apply(self, ball: Ball) -> None:
        self.book.update(ball)

    @property
    def batters(self) -> dict[int, str]:
        return self.book.batting.batters
