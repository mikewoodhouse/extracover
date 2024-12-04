from dataclasses import dataclass
from datetime import date

from dataclasses_json import Undefined, dataclass_json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Match:
    match_id: int
    match_number: int
    start_date: date
