from app.match import PowerPlay


def test_powerplay_properties():
    pp = PowerPlay(type="", ball_from=0.1, ball_to=5.6)
    assert pp.first_over == 0
    assert pp.last_over == 5
    assert pp.overs == range(0, 6)
