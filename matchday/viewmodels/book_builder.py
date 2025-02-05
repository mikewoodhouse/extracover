from dataclasses import dataclass

from matchday.data import BookRepository
from matchday.models import Book, Team


@dataclass
class BookBuilder:
    book: Book
    repo: BookRepository

    def add(self, team_1_name: str, team_2_name: str) -> int:
        team_1 = Team(name=team_1_name)
        team_2 = Team(name=team_2_name)

        self.book.team_1 = team_1_name
        self.book.team_2 = team_2_name

        self.book.inns_1.batting = team_1
        self.book.inns_1.bowling = team_2

        self.book.inns_2.bowling = team_1
        self.book.inns_2.batting = team_2

        self.book.book_id = self.repo.add(self.book)
        print(self.book)
        return self.book.book_id

    def save(self) -> None:
        self.repo.save(self.book)

    def team_list(self) -> list[dict]:
        return Team.all_as_dicts()

    def switch_teams(self) -> None:
        self.book.team_1, self.book.team_2 = self.book.team_2, self.book.team_1
        self.book.inns_1, self.book.inns_2 = self.book.inns_2, self.book.inns_1
        print(self.book)
