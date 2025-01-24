from nicegui import ui

from app.model import Ball, InningsCard, Player, Scorebook

book = Scorebook(
    first_innings=InningsCard(
        batters=[
            Player(name="Alice"),
            Player(name="Bob"),
            Player(name="Charlie"),
            Player(name="Daisy"),
            Player(name="Eve"),
            Player(name="Fred"),
            Player(name="George"),
            Player(name="Harry"),
            Player(name="Jack"),
            Player(name="Ivy"),
            Player(name="Keith"),
        ],
        bowlers=[
            Player(name="Sylvia"),
            Player(name="Tallulah"),
            Player(name="Ursula"),
            Player(name="Violet"),
            Player(name="Wendy"),
        ],
    ),
    second_innings=InningsCard(
        batters=[
            Player(name="Mary"),
            Player(name="Nicola"),
            Player(name="Olivia"),
            Player(name="Paula"),
            Player(name="Quentin"),
            Player(name="Rose"),
            Player(name="Sylvia"),
            Player(name="Tallulah"),
            Player(name="Ursula"),
            Player(name="Violet"),
            Player(name="Wendy"),
        ],
        bowlers=[
            Player(name="George"),
            Player(name="Harry"),
            Player(name="Jack"),
            Player(name="Ivy"),
            Player(name="Keith"),
        ],
    ),
)

BALLS = [0, 1, 2, 3, 4, 6]

ui.colors(maroon="#800000", cyan="#00FFFF")

RUN_BALLS = {str(i): Ball(batter_runs=i) for i in BALLS}

WIDE_BALLS = {f"w+{i}": Ball(wide=True, extra_runs=1 + i) for i in BALLS}

NOBALL_BALLS_WITH_RUNS = {f"nb+{i}": Ball(noball=True, extra_runs=1, batter_runs=i) for i in BALLS}

NOBALL_BALLS_WITH_BYES = {f"nbb+{i}": Ball(noball=True, extra_runs=1 + i) for i in BALLS}

BYE_BALLS = {f"{i} b": Ball(bye=True, extra_runs=i) for i in BALLS}

LEGBYE_BALLS = {f"{i} lb": Ball(bye=True, extra_runs=i) for i in BALLS}

ALL_BALLS = RUN_BALLS | WIDE_BALLS | NOBALL_BALLS_WITH_RUNS | NOBALL_BALLS_WITH_BYES | BYE_BALLS | LEGBYE_BALLS


def update_book(sender) -> None:
    book.update(ALL_BALLS[sender.text])


with ui.row():
    with ui.column():
        with ui.card():
            with ui.grid(columns=7):
                ui.label("Runs")
                for i in BALLS:
                    ui.button(text=str(i), on_click=lambda e: update_book(e.sender)).style("height: 70px;").props(
                        "color=black"
                    )
                ui.label("Wides")
                for i in BALLS:
                    ui.button(text=f"w+{i}", on_click=lambda e: update_book(e.sender)).props("color=red")
                ui.label("NB(runs)")
                for i in BALLS:
                    ui.button(text=f"nb+{i}", on_click=lambda e: update_book(e.sender)).props("color=maroon")
                ui.label("NB(byes)")
                for i in BALLS:
                    ui.button(text=f"nbb+{i}", on_click=lambda e: update_book(e.sender)).props("color=brown")
                ui.label("Byes")
                for i in BALLS:
                    ui.button(text=f"{i} b", on_click=lambda e: update_book(e.sender)).props("color=green")
                ui.label("Legbyes")
                for i in BALLS:
                    ui.button(text=f"{i} lb", on_click=lambda e: update_book(e.sender)).props("color=cyan")
                ui.label("Out!")
                ui.button(text="b/c/lbw", on_click=lambda: book.update(Ball(wicket_fell=True))).props("color=black")
                ui.button(text="RO+1", on_click=lambda: book.update(Ball(wicket_fell=True, batter_runs=1))).props(
                    "color=black"
                )
                ui.button(text="RO+2", on_click=lambda: book.update(Ball(wicket_fell=True, batter_runs=2))).props(
                    "color=black"
                )
                ui.button(text="RO+1b", on_click=lambda: book.update(Ball(wicket_fell=True, extra_runs=1))).props(
                    "color=black"
                )
                ui.button(text="RO+2b", on_click=lambda: book.update(Ball(wicket_fell=True, extra_runs=2))).props(
                    "color=black"
                )
                ui.skeleton()  # placeholder
                ui.label("Other")
                ui.button("Chg Ends")
                ui.button("+1")
                ui.button("-1")
                # some kind of general ball-defining form here? FOr cases not handled above?
    with ui.column():
        with ui.card():
            ui.label(str(book.first_innings.score)).style("font-size: 5em;").bind_text_from(book.first_innings, "score")
            ui.label(str(book.first_innings.rates)).style("font-size: 1em;").bind_text_from(book.first_innings, "rates")
            ui.label(str(book.first_innings.boundaries)).style("font-size: 1em;").bind_text_from(
                book.first_innings, "boundaries"
            )
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[0].batting_html))
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[1].batting_html))
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[2].batting_html))
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[3].batting_html))
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[4].batting_html))
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[5].batting_html))
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[6].batting_html))
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[7].batting_html))
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[8].batting_html))
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[9].batting_html))
            ui.html("").bind_content_from(book.first_innings, "batters", backward=lambda x: str(x[10].batting_html))
ui.run()
