from matchday.models.ball import Ball
from matchday.models.player import Player
from matchday.models.team import Team


def test_construction():
    assert Team()


def test_first_two_batters_positions_updated():
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

    assert len(tm.batters) == len(players)


def test_first_bowler_position_updated():
    arthur = Player(name="Arthur", player_id=1)
    bert = Player(name="Bert", player_id=2)
    chas = Player(name="Chas", player_id=3)

    players = {p.player_id: p for p in [arthur, bert, chas]}

    tm = Team(players=players)

    ball = Ball(bowler=chas.player_id)

    tm.update_bowling(ball)

    assert arthur.bowl_position == 0
    assert bert.bowl_position == 0
    assert chas.bowl_position == 1
