from nicegui import ui

from matchday.viewmodels import InplayManager


class InplayView:
    def __init__(self, manager: InplayManager) -> None:
        self.manager = manager

    def show(self):
        with ui.row():
            ui.page_title("Inplay")
            with ui.card():
                ui.label("A load of balls")
