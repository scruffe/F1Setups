from F1Setups.DB.local_sqlite3.setup_sql import SetupSql
from F1Setups.DB.local_sqlite3.league_sql import LeagueSql
from F1Setups.DB.local_sqlite3.track_sql import TrackSql
from F1Setups.DB.local_sqlite3.weather_sql import WeatherSql
from F1Setups.DB.local_sqlite3.team_sql import TeamSql
from F1Setups.DB.local_sqlite3.game_mode_sql import GameModeSql

# from F1Setups.DB.local_sqlite3 import *


class LocalSqlite3:
    def __init__(self):
        self.setups = SetupSql()
        self.leagues = LeagueSql()
        self.tracks = TrackSql()
        self.weathers = WeatherSql()
        self.teams = TeamSql()
        self.game_modes = GameModeSql()

    def save_setup_to_db(self, car_setup):
        print(
            "saving to db : \n "
            "    S L C W G T \n    ",
            car_setup.setup_id,
            car_setup.league_id,
            car_setup.track_id,
            car_setup.weather_id,
            car_setup.game_mode_id,
            car_setup.team_id)

        db_setup = self.setups.get_setup_by_ids(
            car_setup.league_id,
            car_setup.track_id,
            car_setup.weather_id,
            car_setup.game_mode_id,
            car_setup.team_id)
        if not db_setup:
            self.setups.insert_setup(car_setup)
            print('saved')
        else:
            print(db_setup[0][0], " already exists, updating instead")
            car_setup.setup_id = db_setup[0][0]
            self.setups.update_setup_values_on_setup_id(car_setup)
            print("car setup info: ", car_setup.info)
            print("car setup values: ", car_setup.values)

            print(self.setups.get_setup_by_setup_id(car_setup.setup_id))

    def get_ids(self, league, country, weather, game_mode, team):
        league_id = self.leagues.get_id_from_name(league)
        track_id = self.tracks.get_track_id_by_country(country)
        weather_id = self.weathers.get_weather_id_from_name(weather)
        game_mode_id = self.game_modes.get_game_mode_id_from_name(game_mode)
        team_id = self.teams.get_team_id(team, league_id)

        return league_id, track_id, weather_id, game_mode_id, team_id
