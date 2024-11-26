import copy
import random
from collections import Counter, defaultdict
from dataclasses import dataclass, field


@dataclass
class OverFrequencyRecord:
    player_id: int = 0
    name: str = ""
    over: int = 0
    frequency: float = 0.0

    def __post_init__(self) -> None:
        self.player_id = int(self.player_id)


@dataclass
class OverWeightings:
    bowlers: dict[int, float] = field(default_factory=dict)

    def selected(self, exclude: list[int]) -> int:
        available_bowlers = {k: v for k, v in self.bowlers.items() if k not in exclude}
        names = list(available_bowlers.keys())
        weights = list(available_bowlers.values())
        choices = random.choices(population=names, weights=weights)
        return choices[0]


class BowlingOrderGenerator:
    def __init__(self, freqs: list[OverFrequencyRecord]) -> None:
        self.over_weights = [OverWeightings() for _ in range(20)]
        for ow in freqs:
            self.over_weights[ow.over].bowlers[ow.player_id] = ow.frequency
        if any(len(wtg.bowlers) == 0 for wtg in self.over_weights):
            raise ValueError("no bowler frequencies for at least one overs")
        if len(Counter(order.player_id for order in freqs)) < 5:
            raise ValueError("too few bowlers supplied - must be at least 5")

    def bowling_order(self) -> list[str]:
        def make_an_order() -> list[str]:
            num_bowled: dict[int, int] = defaultdict(int)
            b, last_b = 0, 0
            bowling_order = []
            bowled_out: list[int] = []
            weights = copy.deepcopy(self.over_weights)
            for ov in weights:
                b = ov.selected(exclude=[last_b] + bowled_out)
                num_bowled[b] += 1
                if num_bowled[b] >= 4:
                    bowled_out.append(b)
                bowling_order.append(b)
                last_b = b
            return bowling_order

        # Messy. Deal with the possibility that we could reach an "illegal"
        # order, where we might be forced to use the same bowler in consecutive overs.
        # random.choices will get empty lists and raise, so retry when that happens
        done = False
        res = []
        while not done:
            try:
                res = make_an_order()
                done = True
            except Exception:
                done = False
        return res
