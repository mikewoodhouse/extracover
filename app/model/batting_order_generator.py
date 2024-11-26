import copy
import random
from dataclasses import dataclass, field


def empty_freq_list() -> list[float]:
    return [0.01] * 11


@dataclass
class BatterPositionFrequencies:
    name: str = ""
    player_id: int = 0
    times_in_positions: list[float] = field(default_factory=lambda: empty_freq_list())

    @property
    def frequencies(self) -> list[float]:
        total = sum(self.times_in_positions)
        return [num_times / total for num_times in self.times_in_positions]

    def __repr__(self) -> str:
        return f"{self.name} [{self.player_id}]: {self.frequencies}"


class BattingOrderGenerator:
    def __init__(self, batter_freqs: list[BatterPositionFrequencies]) -> None:
        self.batters = batter_freqs

    def batting_order(self) -> list[int]:
        order = []
        batters: list[BatterPositionFrequencies] = copy.deepcopy(self.batters)
        for pos in range(11):
            # collect ids, freqs for batters remaining to be selected
            batter_freqs = [batter.frequencies[pos] for batter in batters]
            picked = random.choices(population=batters, weights=batter_freqs, k=1)
            order.append(picked[0].player_id)
            batters.remove(picked[0])
        return order
