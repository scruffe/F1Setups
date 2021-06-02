from sql import *


class SqlDB:
    def __init__(self):
        self.setups = setup_sql.SetupSql()
        self.leagues = league_sql.LeagueSql()
        self.tracks = track_sql.TrackSql()
        self.weathers = weather_sql.WeatherSql()
        self.teams = team_sql.TeamSql()
        self.game_modes = game_mode_sql.GameModeSql()

    def save_setup_to_db(self, car_setup):
        print(
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
            print(db_setup[0][0], "didn't save, already exists, updating")
            car_setup.setup_id = db_setup[0][0]
            self.setups.update_setup_values(car_setup)
            print(car_setup.values)
            print(self.setups.get_setup_by_setup_id(car_setup.setup_id))

    def get_ids(self, league, country, weather, game_mode, team):
        league_id = self.leagues.get_id_from_name(league)
        track_id = self.tracks.get_track_id_by_country(country)
        weather_id = self.weathers.get_weather_id_from_name(weather)
        game_mode_id = self.game_modes.get_game_mode_id_from_name(game_mode)
        team_id = self.teams.get_team_id(team, league_id)

        return league_id, track_id, weather_id, game_mode_id, team_id
