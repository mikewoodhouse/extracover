from datetime import date

from app.ingest.classes import Event, Info, Match, Meta


def test_info_database_fields():
    match = Match(
        meta=Meta(),
        info=Info(
            dates=[date.today()],
            balls_per_over=5,
            gender="unknown",
            match_type="banana",
            overs=42,
            venue="bolton",
            event=Event(name="the cup", stage="first"),
            city="apple",
        ),
    )
    expected = {
        "start_date": date.today().isoformat(),
        "match_type": "banana",
        "gender": "unknown",
        "venue": "bolton",
        "event": "the cup|first",
        "city": "apple",
        "overs": 42,
        "balls_per_over": 5,
    }
    assert match.info.database_fields() == expected
