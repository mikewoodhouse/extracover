import random

from app.ingest.classes import Delivery, Over, Runs


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
