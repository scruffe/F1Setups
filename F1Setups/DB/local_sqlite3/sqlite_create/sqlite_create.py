import sqlite3

from F1Setups.DB.local_sqlite3 import track_sql, user_sql, game_mode_sql, league_sql, team_sql, weather_sql, presets_sql
from F1Setups.DB.local_sqlite3.sqlite_create import league, team, track, game_mode, user

conn = sqlite3.connect('F1Setups/DB/local_sqlite3/data.db')

c = conn.cursor()

track_table = track_sql.TrackSql()
user_table = user_sql.UserSql()
game_mode_table = game_mode_sql.GameModeSql()
league_table = league_sql.LeagueSql()
team_table = team_sql.TeamSql()
weather_table = weather_sql.WeatherSql()


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


def make_league_and_teams(json):
    try:
        league_id = 0
        for _league in json.cars:
            print(_league)
            league_table.insert_league(league.League(league_id, _league))
            team_id = 0
            for _team in json.cars[_league]:
                print(_team)
                team_table.insert_teams(team.Team(league_id, team_id, _team))
                team_id += 1
            league_id += 1
    except sqlite3.IntegrityError:
        pass


def make_tracks(json):
    try:
        country_id = 0
        for country in json.tracks_id:
            print(country)
            track_table.insert_track(track.Track(country_id, country, json.tracks_id[country]))
            country_id += 1
    except sqlite3.IntegrityError:
        pass


def make_game_modes(json):
    try:
        for _game_mode in json.game_modes:
            print(_game_mode)
            game_mode_table.insert_game_mode(game_mode.GameModes(json.game_modes[_game_mode], _game_mode))
    except sqlite3.IntegrityError:
        pass


def make_weathers():
    weathers = ["Wet", "Dry", "Mixed"]
    i = 0
    try:
        for w in weathers:
            print(w)
            weather_table.insert_weather(i, w)
            i += 1
    except sqlite3.IntegrityError:
        pass


def make_presets(_presets):
    try:
        for p in _presets:
            print(p)
            presets_sql.PresetSql().insert_carsetup(p)
    except sqlite3.IntegrityError:
        pass


def close_conn():
    conn.close()


"""

    

    sqlite_create.make_presets(_presets)

"""

if __name__ == "__main__":
    user0 = user.User(3, 'scruffy', 'Scruffington', 'scruffe', 20, 40000, 'scruffe@email', True)

    if not user_table.get_user_by_strings(user0.first, user0.last, user0.tag):
        user_table.insert_user(user0)

    print(get_joined())

    close_conn()
