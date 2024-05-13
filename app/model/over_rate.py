from __future__ import annotations

from dataclasses import dataclass, field


def empty_t20_over_rates() -> list[float]:
    return [0] * 20


@dataclass
class OverRate:
    rates: list[float] = field(default_factory=empty_t20_over_rates)

    def __sub__(self, other: OverRate) -> OverRate:
        return OverRate([self.rates[i] - other.rates[i] for i in range(20)])

    def __add__(self, other: OverRate) -> OverRate:
        return OverRate([self.rates[i] + other.rates[i] for i in range(20)])

    def __getitem__(self, idx: int) -> float:
        return self.rates[idx]

    def __setitem__(self, idx: int, value: float):
        self.rates[idx] = value
