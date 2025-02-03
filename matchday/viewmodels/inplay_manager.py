from matchday.models import Book


class InplayManager:
    def __init__(self, book: Book) -> None:
        self.book = book

    def title(self) -> str:
        return f"{self.book.team_1.name} vs {self.book.team_2.name}"
