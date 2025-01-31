from dataclasses import dataclass, field

from icecream import ic

from matchday.models import Book, Team


@dataclass
class BookCreator:
    book: Book = field(default_factory=Book)

    def set_team_name(self, which: str, name: str):
        ic(which, name)
        setattr(self.book, which, Team(name=name))
        ic(self.book)

    def save(self) -> int:
        book_id = self.book.create()
        return book_id

    def team_list(self) -> list[dict]:
        return Team.all_as_dicts()
