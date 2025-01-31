from app.model import InningsCard, Player, Scorebook


def fake_player(name: str = "") -> Player:
    return Player(name=name)


def fake_innings() -> InningsCard:
    return InningsCard(
        batters=[fake_player(name=f"P{str(_)}") for _ in range(11)],
        bowlers=[fake_player(name=f"P{str(_)}") for _ in range(5)],
    )


def fake_book() -> Scorebook:
    return Scorebook(
        first_innings=fake_innings(),
        second_innings=fake_innings(),
    )
