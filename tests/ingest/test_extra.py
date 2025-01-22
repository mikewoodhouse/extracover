import pytest

from app.ingest.classes import Extras


@pytest.mark.parametrize(
    "noballs,wides,byes,legbyes,penalty,expected_type",
    [
        (1, 0, 0, 0, 0, "noball"),
        (0, 1, 0, 0, 0, "wide"),
        (0, 0, 1, 0, 0, "bye"),
        (0, 0, 0, 1, 0, "legbye"),
        (0, 0, 0, 0, 1, "penalty"),
        (0, 0, 0, 0, 0, ""),
    ],
)
def test_extra_type_derived(noballs: int, wides: int, byes: int, legbyes: int, penalty: int, expected_type: str):
    extras = Extras(
        noballs=noballs,
        wides=wides,
        byes=byes,
        legbyes=legbyes,
        penalty=penalty,
    )
    assert extras.extra_type == expected_type
