from nicegui import ui

from matchday.models import Book


class ScoreView:
    def __init__(self, book: Book) -> None:
        self.book = book

    def show(self) -> None:
        with ui.card():
            ui.label("Scorebook").style("color: cyan")
            ui.label().bind_text_from(self.book, "score")
