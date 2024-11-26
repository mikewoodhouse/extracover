from app.model.predicto import Predicto
from app.model.scorebook import Scorebook


def test_it_builds():
    assert Predicto(Scorebook()) is not None
