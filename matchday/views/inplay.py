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

    def switch_batters(self, left: ui.select, right: ui.select) -> None:
        l_value, r_value = left.value, right.value
        print(f"switching {l_value=} , {r_value=}")
        left.value = r_value
        right.value = l_value

    def ball_creator(self):
        with ui.card():
            ui.label("Ball Creator").style("color: cyan")
            with ui.card():
                with ui.row():
                    ui.label("Facing:").style("valign: bottom")
                    striker = ui.select(self.manager.batters).style("width: 150px;").props("borderless filled")
                    non_striker = ui.select(self.manager.batters).style("width: 150px;").props("borderless filled")
                    ui.button("Switch", on_click=lambda: self.switch_batters(striker, non_striker))
            with ui.card():
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
            with ui.card():
                with ui.row():
                    ui.label("Extra:")
                    ui.select(
                        [e.value for e in Extra],
                        value="None",
                    ).bind_value(self.ball, "extra_type")
                with ui.row():
                    ui.button("Striker Out")
                    ui.button("Non-striker Out")
                    ui.label("Next:")
                    ui.select(self.manager.batters).style("height: 40px")
                with ui.row():
                    ui.button("Apply!", on_click=self.apply_ball).style("height: 70px; font-size: 200%;").props(
                        "color=red"
                    )

    def show(self):
        with ui.row():
            ui.page_title("Inplay")
            ui.label(self.manager.title).style("font-size: 200%; color: yellow")
        with ui.row():
            self.ball_creator()
