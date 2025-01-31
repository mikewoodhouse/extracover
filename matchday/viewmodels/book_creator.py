from dataclasses import dataclass, field

from matchday.models import Book, Team


@dataclass
class BookCreator:
    book: Book = field(default_factory=Book)

    def set_team_name(self, which: str, name: str):
        setattr(self.book, which, Team(name=name))

    def team_list(self) -> list[dict]:
        return Team.all_as_dicts()
