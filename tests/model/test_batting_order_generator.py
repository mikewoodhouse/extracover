from app.model.batting_order_generator import (
    BatterPositionFrequencies,
    BattingOrderGenerator,
)


def test_construction():
    freqs = [BatterPositionFrequencies()] * 11
    gen = BattingOrderGenerator(freqs)
    assert gen
    assert gen.batters
    assert len(gen.batters) == 11
