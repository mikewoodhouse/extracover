from nicegui import ui

from matchday.models import Book


class ScoreView:
    def __init__(self, book: Book) -> None:
        self.book = book

    def show(self) -> None:
        with ui.card():
            ui.label("Scorebook").style("color: cyan")
            ui.html().bind_content_from(self.book.current_innings, "score").style("font-size: 150%")
            ui.html().bind_content_from(self.book.current_innings, "boundaries")

        with ui.card().tight():
            for i, _ in enumerate(self.book.current_innings.batting.players):
                ui.html().bind_content_from(
                    self.book.current_innings, f"batter_{i + 1}", backward=lambda p: p().batting_line.html
                )

        with ui.card().tight():
            for i, _ in enumerate(self.book.current_innings.bowling.players):
                ui.html().bind_content_from(
                    self.book.current_innings, f"bowler_{i + 1}", backward=lambda p: p().bowling_line.html
                )
