from nicegui import ui


class InplayView:
    def __init__(self) -> None:
        pass

    def show(self):
        with ui.row():
            ui.page_title("Inplay")
            with ui.card():
                ui.label("A load of balls")
