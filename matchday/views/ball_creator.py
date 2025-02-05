from nicegui import ui

from matchday.models.ball import Ball, Extra
from matchday.viewmodels import InplayManager

BATTER_RUNS = [0, 1, 2, 3, 4, 6]
EXTRA_RUNS = [0, 1, 2, 3, 4, 5, 6]


class BallCreator:
    def __init__(self, manager: InplayManager):
        self.ball = Ball()
        self.manager = manager

    def apply_ball(self) -> None:
        self.manager.apply(self.ball)
        if self.ball.changes_ends:
            self.switch_batters()
        self.ball.reset()

    def switch_batters(self) -> None:
        self.ball.striker, self.ball.non_striker = self.ball.non_striker, self.ball.striker

    def notify_end_of_over(self) -> None:
        self.manager.notify_end_of_over()
        self.switch_batters()

    def notify_end_of_innings(self) -> None:
        self.manager.notify_end_of_innings()

    def show(self):
        with ui.card():
            ui.label("Ball Creator").style("color: cyan")
            with ui.card():
                with ui.row():
                    ui.label("Bowling")
                    (
                        ui.select(self.manager.bowlers)
                        .style("width: 150px;")
                        .props("borderless filled")
                        .bind_value(self.ball, "bowler")
                    )
                with ui.row():
                    ui.label("Facing:").style("valign: bottom")
                    (
                        ui.select(self.manager.batters)
                        .style("width: 150px;")
                        .props("borderless filled")
                        .bind_value(self.ball, "striker")
                    )
                    (
                        ui.select(self.manager.batters)
                        .style("width: 150px;")
                        .props("borderless filled")
                        .bind_value(self.ball, "non_striker")
                    )
                    ui.button("Switch", on_click=self.switch_batters)
            with ui.card():
                with ui.row():
                    ui.label("Runs")
                    ui.select(
                        BATTER_RUNS,
                        value=0,
                        label="Batter",
                    ).bind_value(self.ball, "batter_runs").style("width: 6em").bind_value(self.ball, "batter_runs")
                    ui.select(
                        EXTRA_RUNS,
                        value=0,
                        label="Extra",
                    ).bind_value(self.ball, "extra_runs").style("width: 6em").bind_value(self.ball, "extra_runs")
                    ui.select(
                        EXTRA_RUNS,
                        value=0,
                        label="Penalty",
                    ).bind_value(self.ball, "penalty_runs").style("width: 6em").bind_value(self.ball, "penalty_runs")
            with ui.card():
                with ui.row():
                    ui.label("Extra:")
                    ui.select(
                        [e.value for e in Extra],
                        value="None",
                    ).bind_value(self.ball, "extra_type")
                with ui.row():
                    ui.checkbox("Striker Out").bind_value(self.ball, "striker_out")
                    ui.checkbox("Non-striker Out").bind_value(self.ball, "non_striker_out")
                with ui.row():
                    ui.button("Apply!", on_click=self.apply_ball).style("height: 70px; font-size: 200%;").props(
                        "color=red"
                    )
                    ui.button("End over", on_click=self.notify_end_of_over)
                    ui.button("End innings", on_click=self.notify_end_of_innings)
        with ui.card():
            ui.textarea().bind_value_from(self.ball, "as_string").style("width: 50em")
