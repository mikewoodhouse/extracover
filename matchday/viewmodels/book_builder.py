from dataclasses import dataclass

from matchday.data import BookRepository
from matchday.models import Book, Team


@dataclass
class BookBuilder:
    book: Book
    repo: BookRepository
    book_id: int = 0

    def add(self) -> int:
        self.book_id = self.repo.add(self.book)
        return self.book_id

    def set_team_name(self, which: str, name: str):
        setattr(self.book, which, Team(name=name))

    def team_list(self) -> list[dict]:
        return Team.all_as_dicts()
