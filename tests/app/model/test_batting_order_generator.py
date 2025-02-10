import random

from app.model.batting_order_generator import (BatterPositionFrequencies,
                                               BattingOrderGenerator)


def test_construction():
    freqs = [BatterPositionFrequencies()] * 11
    gen = BattingOrderGenerator(freqs)
    assert gen
    assert gen.batters
    assert len(gen.batters) == 11


def test_order_is_list_of_11_ints():
    freqs = [
        BatterPositionFrequencies(player_id=random.randint(1, 1000000))
        for _ in range(11)
    ]
    gen = BattingOrderGenerator(freqs)
    order = gen.batting_order()
    assert len(order) == 11
    assert all(isinstance(item, int) for item in order)
    assert len(set(order)) == 11, "should be no duplicates in batting order"


def test_a_valid_order_is_generated():
    freqs = [
        BatterPositionFrequencies(
            f"X-{idx:02d}", random.randint(1, 1000000), [random.random()] * 11
        )
        for idx in range(11)
    ]
    gen = BattingOrderGenerator(freqs)
    order = gen.batting_order()
    assert len(order) == 11
    assert all(isinstance(item, int) for item in order)
    assert len(set(order)) == 11, "should be no duplicates in batting order"
    assert not all(
        a < b for a, b in zip(order[:-1], order[1:])
    ), "all ids in order? highly suspicious!"
    print(order)
