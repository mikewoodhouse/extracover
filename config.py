class Configurator:
    gender: str = "male"
    match_type: str = "T20"

    @property
    def db_filename(self) -> str:
        return f"{self.gender.lower()}_{self.match_type.lower()}.db"


config = Configurator()
