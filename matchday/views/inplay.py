from nicegui import ui

from matchday.models.ball import Ball, Extra
from matchday.viewmodels import InplayManager

BATTER_RUNS = [0, 1, 2, 3, 4, 6]
EXTRA_RUNS = [0, 1, 2, 3, 4, 5, 6]


class InplayView:
    def __init__(self, manager: InplayManager) -> None:
        self.manager = manager
        self.ball = Ball()

    def apply_ball(self) -> None:
        self.manager.apply(self.ball)

    def ball_creator(self):
        with ui.card():
            ui.label("Ball Creator").style("color: cyan")
            with ui.row():
                print(self.manager.batters)
                ui.select(self.manager.batters).style("height: 40px")
                ui.input(label="Striker", placeholder="Striker")
                ui.input(label="Non-striker", placeholder="Non-striker")
                ui.button("Switch")
            with ui.row():
                ui.label("Runs")
                ui.select(
                    BATTER_RUNS,
                    value=0,
                    label="Batter",
                ).style("width: 6em").bind_value(self.ball, "batter_runs")
                ui.select(
                    EXTRA_RUNS,
                    value=0,
                    label="Extra",
                ).style("width: 6em").bind_value(self.ball, "extra_runs")
                ui.select(
                    EXTRA_RUNS,
                    value=0,
                    label="Penalty",
                ).style("width: 6em").bind_value(self.ball, "penalty_runs")
            with ui.row():
                ui.label("Extra:")
                ui.select(
                    [e.value for e in Extra],
                    value="None",
                ).bind_value(self.ball, "extra_type")
            with ui.row():
                ui.button("Striker Out")
                ui.button("Non-striker Out")
                ui.select(["Next Man"], label="Next man")
            with ui.row():
                ui.button("Apply!", on_click=self.apply_ball).style("height: 70px; font-size: 200%;").props("color=red")

    def show(self):
        with ui.row():
            ui.page_title("Inplay")
            ui.label(self.manager.title).style("font-size: 200%; color: yellow")
        with ui.row():
            self.ball_creator()
