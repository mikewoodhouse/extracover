import requests


class PlayerNotFoundError(TypeError):
    pass


class CricinfoPlayer:
    def __init__(self, cricinfo_id: str, cricinfo_id_2: str) -> None:
        self.headers = {"user-agent": "Mozilla/5.0"}
        self.json = ""
        if cricinfo_id:
            try:
                self.json = self.get_json(cricinfo_id)
            except PlayerNotFoundError:
                self.json = ""
            except Exception as e:
                raise e
        if cricinfo_id_2 and not self.json:
            try:
                self.json = self.get_json(cricinfo_id_2)
            except PlayerNotFoundError:
                self.json = ""
            except Exception as e:
                raise e

    def get_json(self, id: str) -> str:
        url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/player/home?playerId={id}"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 404:
            raise PlayerNotFoundError
        return r.json()
