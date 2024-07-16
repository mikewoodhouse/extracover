from dataclasses import dataclass, field


@dataclass
class Ball:
    batter_runs: int = 0
    extra_runs: int = 0
    wicket_fell: bool = False
    striker_out: bool = True
    wide: bool = False
    noball: bool = False
    bye: bool = False

    @property
    def is_extra(self) -> bool:
        return self.wide or self.noball or self.bye

    @property
    def is_wide_no_ball(self) -> bool:
        return self.wide or self.noball

    @property
    def runs_scored(self) -> int:
        return self.batter_runs + self.extra_runs


@dataclass
class Player:
    name: str = ""
    runs_scored: int = 0
    overs: int = 0
    runs_conceded: int = 0


@dataclass
class InningsCard:
    batters: list[Player] = field(default_factory=list)
    bowlers: list[Player] = field(default_factory=list)
    total: int = 0
    wickets: int = 0


@dataclass
class Scorebook:
    first_innings: InningsCard = field(default_factory=InningsCard)
    second_innings: InningsCard = field(default_factory=InningsCard)
