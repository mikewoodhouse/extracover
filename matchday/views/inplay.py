from nicegui import ui

from matchday.models.ball import Extra
from matchday.viewmodels import InplayManager

BATTER_RUNS = [0, 1, 2, 3, 4, 6]
EXTRA_RUNS = [0, 1, 2, 3, 4, 5, 6]


class InplayView:
    def __init__(self, manager: InplayManager) -> None:
        self.manager = manager

    def show(self):
        with ui.row():
            ui.page_title("Inplay")
            ui.label(self.manager.title()).style("font-size: 200%; color: yellow")
        with ui.row():
            with ui.card():
                ui.label("Ball Creator").style("color: cyan")
                with ui.row():
                    ui.input(label="Striker", placeholder="Striker")
                    ui.input(label="Non-striker", placeholder="Non-striker")
                    ui.button("Switch")
                with ui.row():
                    ui.label("Batter runs")
                    ui.select(BATTER_RUNS, value=0)
                    ui.label("Extra runs")
                    ui.select(EXTRA_RUNS, value=0)
                    ui.label("penalty_runs")
                    ui.select(EXTRA_RUNS, value=0)
                with ui.row():
                    ui.label("Extra:")
                    ui.select([e.value for e in Extra], value="None")
                with ui.row():
                    ui.button("Striker Out")
                    ui.button("Non-striker Out")
                    # if either true, show "next man" dropdown
