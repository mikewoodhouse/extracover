from app.model.scorebook import Scorebook


class Predicto:
    """
    Controls the simulation of a match from a supplied state (which may be at the start)
    until its  conclusion, producing a MatchState object from which, with a suitably large
    number of others, distributions of interesting outcomes may be derived.
    """

    def __init__(self, book: Scorebook) -> None:
        self.book = book
