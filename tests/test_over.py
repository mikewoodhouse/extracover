import random

from app.ingest.classes import Delivery, Extras, Over, Runs


def test_total_runs():
    balls = [random.randint(0, 6) for _ in range(6)]
    over = Over(
        over=0,
        deliveries=[
            Delivery(
                runs=Runs(total=ball),
            )
            for ball in balls
        ],
    )
    assert over.runs == sum(balls)


def test_ball_numbering():
    over = Over(
        over=3,
        deliveries=[
            Delivery(extras=Extras(noballs=1)),
            Delivery(),
            Delivery(),
            Delivery(extras=Extras(wides=1)),
            Delivery(extras=Extras(byes=1)),
            Delivery(extras=Extras(legbyes=1)),
            Delivery(),
            Delivery(extras=Extras(noballs=1)),
            Delivery(),
        ],
    )
    assert over
