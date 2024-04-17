from dataclasses import dataclass
from datetime import date


@dataclass
class Match:
    match_id: int
    start_date: date
    match_type: str  # may want to become an enum?
    gender: str  # enum?
    venue: str
    event: str  # might want to become a foreign key to a future events table?
    city: str
    overs: int
    balls_per_over: int
