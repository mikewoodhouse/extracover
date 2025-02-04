from nicegui import app, ui

from matchday.viewmodels import BookBuilder


class BookSetupView:
    def __init__(self, builder: BookBuilder) -> None:
        self.builder = builder

    def update_team_name(self, field_name: str, label: ui.label, value: str):
        self.builder.set_team_name(field_name, value)
        label.set_text(value)

    def create_match(self) -> None:
        book_id = self.builder.add()
        app.storage.user["book_id"] = book_id
        self.team_list_section.set_visibility(False)
        self.show_the_toss()

    def show_the_toss(self) -> None:
        self.the_toss.set_visibility(True)
        with self.the_toss:
            with ui.card():
                ui.label("The Toss")
                ui.label("Bat first:")
                ui.button(self.builder.book.team_1.name, on_click=self.set_toss_winner_decision)
                ui.button(self.builder.book.team_2.name, on_click=self.team_2_bats_first)

    def team_2_bats_first(self) -> None:
        self.builder.switch_teams()
        self.set_toss_winner_decision()

    def set_toss_winner_decision(self) -> None:
        self.the_toss.set_visibility(False)
        self.show_player_selectors()
        self.player_lineup_section.set_visibility(True)

    def team_selector(self, label_text: str, field_name: str):
        with ui.card():
            team_name = ui.label(label_text).style("font-size: 200%")
            with ui.table(
                columns=[
                    {"name": "name", "label": "Name", "field": "name", "align": "left"},
                ],
                rows=self.builder.team_list(),
                pagination=10,
            ).props("dense") as table:
                with table.add_slot("top-right"):
                    with (
                        ui.input(placeholder="Search")
                        .props("type=search")
                        .bind_value(table, "filter")
                        .add_slot("append")
                    ):
                        ui.icon("search")
            table.on("rowClick", lambda e: self.update_team_name(field_name, team_name, e.args[1]["name"]))

    def show_player_selectors(self):
        with self.player_lineup_section:
            with ui.row():
                ui.button("Start!", on_click=self.switch_to_inplay_view)
                ui.label(f"Match id = {app.storage.user['book_id']}")
            with ui.row():
                self.player_selector(1)
                self.player_selector(2)

    def switch_to_inplay_view(self):
        self.builder.save()

    def player_selector(self, team_number: int) -> None:
        team = self.builder.book.team_1 if team_number == 1 else self.builder.book.team_2
        player_dicts = team.players_as_dicts()  # TODO : should come from builder?
        with ui.card():
            ui.label(team.name).style("font-size: 200%")
            with ui.table(
                columns=[
                    {"name": "name", "label": "Name", "field": "name"},
                    {"name": "last_match", "label": "Last", "field": "last_match", "align": "center"},
                ],
                rows=player_dicts,
                selection="multiple",
                row_key="player_id",
                on_select=lambda e: print(e.selection, players_table.selected),
            ).props("dense") as players_table:
                ui.skeleton()
            most_recent_match = player_dicts[0]["last_match"]
            players_table.selected = [p for p in player_dicts if p["last_match"] == most_recent_match]

    def show(self):
        self.team_list_section = ui.column()
        with self.team_list_section:
            with ui.row():
                self.team_selector("Team 1", "team_1")
                self.team_selector("Team 2", "team_2")
            with ui.card():
                ui.button("Create!", on_click=self.create_match)
        self.the_toss = ui.column()
        self.the_toss.set_visibility(False)
        self.player_lineup_section = ui.column()
        self.player_lineup_section.set_visibility(False)
