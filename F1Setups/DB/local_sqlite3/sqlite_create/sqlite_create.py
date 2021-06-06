import sqlite3

from . import *
from ..local_sqlite3 import *

# from F1Setups import jsondata

conn = sqlite3.connect('F1Setups/DB/local_sqlite3/data.db')

c = conn.cursor()

track_table = track_sql.TrackSql()
user_table = user_sql.UserSql()
game_mode_table = game_mode_sql.GameModeSql()
league_table = league_sql.LeagueSql()
team_table = team_sql.TeamSql()
weather_table = weather_sql.WeatherSql()

json = "jsondata.Json()"


def get_joined():
    c.execute("""SELECT
                    front_wing,
                    rear_wing,
                    track_name,
                    team_name
                FROM setups 
                LEFT JOIN tracks ON setups.track_id = tracks.track_id
                LEFT JOIN teams ON setups.team_id = teams.team_id
                    WHERE setups.league_id = teams.league_id;
                        """)
    return c.fetchall()


def make_league_and_teams():
    try:
        league_id = 0
        for _league in json.cars:
            league_table.insert_league(league.League(league_id, _league))
            team_id = 0
            for _team in json.cars[league]:
                team_table.insert_teams(team.Team(league_id, team_id, _team))
                team_id += 1
            league_id += 1
    except sqlite3.IntegrityError:
        pass


def make_tracks():
    try:
        country_id = 0
        for country in json.tracks_id:
            track_table.insert_track(track.Track(country_id, country, json.tracks_id[country]))
            country_id += 1
    except sqlite3.IntegrityError:
        pass


def make_game_modes():
    try:
        for _game_mode in json.game_modes:
            game_mode_table.insert_game_mode(game_mode.GameModes(json.game_modes[_game_mode], _game_mode))
    except sqlite3.IntegrityError:
        pass


def make_weathers():
    weathers = ["Wet", "Dry", "Mixed"]
    i = 0
    try:
        for w in weathers:
            weather_table.insert_weather(i, w)
            i += 1
    except sqlite3.IntegrityError:
        pass


def make_presets(_presets):
    try:
        for p in _presets:
            presets_sql.PresetSql().insert_carsetup(p)
    except sqlite3.IntegrityError:
        pass


def close_conn():
    conn.close()


"""

    preset1 = CarSetup(
        1, 0, "Preset 1", 0, 0, 0, 0,
        8, 9, 70, 65, -3.1, -1.6, 0.09, 0.32, 3, 1, 3, 5, 4, 3, 100, 58, 21.4, 21.4, 19.5, 19.5, 0, 10, 0)
    preset2 = CarSetup(
        2, 0, "Preset 2", 0, 0, 0, 0,
        6, 7, 70, 65, -3, -1.5, 0.1, 0.35, 4, 3, 5, 7, 7, 7, 100, 58, 22.6, 22.6, 21.1, 21.1, 0, 10, 0)
    preset3 = CarSetup(
        3, 0, "Preset 3", 0, 0, 0, 0,
        5, 6, 70, 65, -3.1, -1.6, 0.09, 0.32, 5, 3, 5, 7, 6, 5, 100, 58, 22.6, 22.6, 21.1, 21.1, 0, 10, 0)
    preset4 = CarSetup(
        4, 0, "Preset 4", 0, 0, 0, 0,
        4, 4, 70, 65, -2.6, -1.1, 0.06, 0.2, 4, 4, 4, 5, 5, 5, 100, 58, 21.8, 21.8, 20.7, 20.7, 0, 10, 0)
    preset5 = CarSetup(
        5, 0, "Preset 5", 0, 0, 0, 0,
        2, 2, 70, 65, -2.5, -1, 0.05, 0.2, 3, 3, 4, 5, 4, 3, 100, 58, 25, 25, 23.5, 23.5, 0, 10, 0)

    _presets = [preset1, preset2, preset3, preset4, preset5]

    sqlite_create.make_presets(_presets)

"""

if __name__ == "__main__":
    user0 = user.User(3, 'scruffy', 'Scruffington', 'scruffe', 20, 40000, 'scruffe@email', True)

    if not user_table.get_user_by_strings(user0.first, user0.last, user0.tag):
        user_table.insert_user(user0)

    print(get_joined())

    close_conn()
