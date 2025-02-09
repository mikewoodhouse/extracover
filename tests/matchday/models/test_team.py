from matchday.models.ball import Ball
from matchday.models.player import Player
from matchday.models.team import Team


def test_construction():
    assert Team()


def test_first_batter_marked_position_1():
    arthur = Player(name="Arthur", player_id=1)
    bert = Player(name="Bert", player_id=2)
    chas = Player(name="Chas", player_id=3)

    players = {p.player_id: p for p in [arthur, bert, chas]}

    tm = Team(players=players)

    ball = Ball(striker=bert.player_id, non_striker=chas.player_id)

    tm.update_batting(ball)

    assert arthur.bat_position == 0
    assert bert.bat_position == 1
    assert chas.bat_position == 2
