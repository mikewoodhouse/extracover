from dataclasses import dataclass, field


def empty_freq_list() -> list[float]:
    return [0.01] * 11


@dataclass
class BatterPositionFrequencies:
    name: str = ""
    player_id: int = 0
    frequencies: list[float] = field(default_factory=lambda: empty_freq_list())

    def __repr__(self) -> str:
        return f"{self.name} [{self.player_id}]: {self.frequencies}"


class BattingOrderGenerator:
    def __init__(self, batter_freqs: list[BatterPositionFrequencies]) -> None:
        self.batters = batter_freqs
