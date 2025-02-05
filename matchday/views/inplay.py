from nicegui import ui

from matchday.viewmodels import InplayManager
from matchday.views.ball_creator import BallCreator
from matchday.views.score_view import ScoreView


class InplayView:
    def __init__(self, manager: InplayManager) -> None:
        self.manager = manager

    def show(self):
        with ui.row():
            ui.page_title("Inplay")
            ui.label(self.manager.title).style("font-size: 200%; color: yellow")
        with ui.row():
            with ui.column():
                BallCreator(self.manager).show()
                with ui.card():
                    ui.label("History").style("color: cyan; width: 50em")
                    ui.textarea().bind_value_from(self.manager, "last_6")
            with ui.column():
                ScoreView(self.manager.book).show()
