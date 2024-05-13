import pytest

from app.model.over_rate import OverRate


def test_construction():
    pass


def test_diff():
    first = OverRate(rates=[1.0 + i / 10 for i in range(20)])
    second = OverRate(rates=[2.1 + i / 10 for i in range(20)])
    diff = second - first
    assert all(rt == pytest.approx(1.1) for rt in diff.rates)


def test_addition():
    first = OverRate(rates=[1.0 + i / 10 for i in range(20)])
    second = OverRate(rates=[2.1 + i / 10 for i in range(20)])
    diff = second + first
    expected_sum = OverRate(rates=[3.1 + i * 2 / 10 for i in range(20)])
    assert all(
        actual == pytest.approx(expected)
        for actual, expected in zip(diff.rates, expected_sum.rates)
    )


def test_getitem():
    obj = OverRate(rates=list(range(20)))
    assert all(obj[i] == i for i in range(20))


def test_setitem():
    obj = OverRate()
    # sourcery skip: no-loop-in-tests
    for i in range(20):
        obj[i] = i
    assert all(obj[i] == i for i in range(20))
