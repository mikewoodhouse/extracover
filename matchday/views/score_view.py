from nicegui import ui

from matchday.models import Book


class ScoreView:
    def __init__(self, book: Book) -> None:
        self.book = book

    def show(self) -> None:
        with ui.card():
            ui.label("Scorebook").style("color: cyan")
            ui.textarea().bind_value_from(self.book, "score").style("font-size: 150%")
        with ui.card().tight():
            ui.table(
                rows=self.book.current_innings.batting_card,
            ).props("dense")
        with ui.card().tight():
            ui.table(
                rows=self.book.current_innings.bowling_card,
            ).props("dense")
