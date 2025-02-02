from matchday.models import Book


class InplayManager:
    def __init__(self, book: Book) -> None:
        self.book = book
