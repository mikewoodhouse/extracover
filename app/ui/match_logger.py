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
    print(sender.props)
    ball = Ball(**sender.props)
    print(ball)
    book.update(ball)


def run_match_logger():
    with ui.row():
        with ui.column():
            with ui.card():
                with ui.grid(columns=7):
                    ui.label("Runs")
                    for i in BALLS:
                        ui.button(text=str(i), on_click=lambda e: update_book(e.sender)).props(
                            f"color=black batter_runs={i}"
                        ).style("height: 70px;")
                    ui.label("Wides")
                    for i in BALLS:
                        ui.button(text=f"w:{i + 1}", on_click=lambda e: update_book(e.sender)).props(
                            f"color=red extra_runs={i + 1} extra_type=wide"
                        )
                    ui.label("NB(runs)")
                    for i in BALLS:
                        ui.button(text=f"nb+{i}", on_click=lambda e: update_book(e.sender)).props(
                            f"color=maroon batter_runs={i} extra_runs=1 extra_type=noball"
                        )
                    ui.label("NB(byes)")
                    for i in BALLS:
                        ui.button(text=f"nb+{i}b", on_click=lambda e: update_book(e.sender)).props(
                            f"color=brown extra_runs={i + 1} extra_type=noball"
                        )
                    ui.label("Byes")
                    for i in BALLS:
                        ui.button(text=f"{i + 1} b", on_click=lambda e: update_book(e.sender)).props(
                            f"color=green extra_runs={i + 1} extra_type=bye"
                        )
                    ui.label("Legbyes")
                    for i in BALLS:
                        ui.button(text=f"{i + 1} lb", on_click=lambda e: update_book(e.sender)).props(
                            f"color=cyan extra_runs={i + 1} extra_type=legbye"
                        )
                    ui.label("Out!")
                    ui.button(text="B/C/LB/St", on_click=lambda e: update_book(e.sender)).props(
                        "color=black wicket_fell=true how_out=bowled"
                    )
                    ui.button(text="RO+1", on_click=lambda: book.update(Ball(wicket_fell=True, batter_runs=1))).props(
                        "color=black how_out=runout"
                    )
                    ui.button(text="RO+2", on_click=lambda: book.update(Ball(wicket_fell=True, batter_runs=2))).props(
                        "color=black how_out=runout"
                    )
                    ui.button(text="RO+1b", on_click=lambda: book.update(Ball(wicket_fell=True, extra_runs=1))).props(
                        "color=black how_out=runout"
                    )
                    ui.button(text="RO+2b", on_click=lambda: book.update(Ball(wicket_fell=True, extra_runs=2))).props(
                        "color=black how_out=runout"
                    )
                    ui.skeleton()  # placeholder
                    ui.label("Other/Fix:")
                    ui.button("Over")
                    ui.button("Chg Ends")
                    ui.button("+1")
                    ui.button("-1")
                    # some kind of general ball-defining form here? FOr cases not handled above?
                with ui.card():
                    with ui.row():
                        ui.label("Select bowler for next ball/over")
                        ui.select(
                            [p.name for p in book.current_innings.bowlers if not p.is_bowler],
                        )
        with ui.column():
            with ui.card().tight():
                ui.label(str(book.current_innings.score)).style("font-size: 5em;").bind_text_from(
                    book.current_innings, "score"
                )
                ui.label(str(book.current_innings.rates)).style("font-size: 1em;").bind_text_from(
                    book.current_innings, "rates"
                )
                ui.label(str(book.current_innings.boundaries)).style("font-size: 1em;").bind_text_from(
                    book.current_innings, "boundaries"
                )
            with ui.card().tight():
                for i, _ in enumerate(book.current_innings.batters):
                    ui.html().bind_content_from(
                        book.current_innings, f"batter_{i}", backward=lambda x: x().batting_html
                    )
            with ui.card().tight():
                for i, _ in enumerate(book.current_innings.bowlers):
                    ui.html().bind_content_from(
                        book.current_innings, f"bowler_{i}", backward=lambda x: x().bowling_html
                    )

    ui.run()
