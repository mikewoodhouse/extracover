from nicegui import ui


class ScoreView:
    def show(self):
        with ui.card():
            ui.label("Scorebook").style("color: cyan")
