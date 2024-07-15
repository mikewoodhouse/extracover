from dataclasses import dataclass


@dataclass
class BallParams:
    p_wicket: float
    p_wide: float
    p_wide_runs: list[float]
    p_noball: float
    p_nb_runs: list[float]
    p_bye_runs: list[float]
    p_runs: list[float]


class Balluator:
    pass
