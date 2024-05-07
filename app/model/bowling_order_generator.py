import random
from collections import Counter, defaultdict
from dataclasses import dataclass, field


@dataclass
class OverFrequencyRecord:
    name: str
    over: int
    frequency: float


@dataclass
class OverWeightings:
    bowlers: dict[str, float] = field(default_factory=dict)

    def selected(self) -> str:
        weights = list(self.bowlers.values())
        choices = random.choices(list(self.bowlers.keys()), weights=weights)
        return choices[0]


class BowlingOrderGenerator:
    def __init__(self, orders: list[OverFrequencyRecord]) -> None:
        self.over_weights = [OverWeightings() for _ in range(20)]
        for ow in orders:
            self.over_weights[ow.over].bowlers[ow.name] = ow.frequency
        if any(len(wtg.bowlers) == 0 for wtg in self.over_weights):
            raise ValueError("no bowler frequencies for at least one overs")
        if len(Counter(order.name for order in orders)) < 5:
            raise ValueError("too few bowlers supplied - must be at least 5")

    def bowling_order(self) -> list[str]:
        num_bowled = defaultdict(int)
        b, last_b = "", ""
        bowling_order = []
        for ov in range(20):
            while b == last_b or num_bowled[b] == 4:
                b = self.over_weights[ov].selected()
            num_bowled[b] += 1
            bowling_order.append(b)
            last_b = b
        return bowling_order
