import json


class Json:
    def __init__(self):
        self.data = self.load_json_data()
        self.tracks_sorted = self.data["tracks_sorted"]
        self.tracks_season = self.data["tracks_season"]
        self.tracks_id = self.data["tracks_id"]
        self.cars = self.data["cars"]
        self.weather = self.data["weather"]
        self.game_modes = self.data["game_modes"]
        self.preset_setups = self.data["preset_setups"]

    @staticmethod
    def load_json_data():
        with open('F1Setups/data.json', encoding='utf-8') as json_file:
            jf = json.load(json_file)
        json_file.close()
        return jf
