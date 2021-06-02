import sqlite3

from track import Track
from game_mode import GameModes
from league import League
from team import Team
from user import User

from jsondata import Json
from sql import *

conn = sqlite3.connect('data.db')

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


def make_league_and_teams():
    try:
        league_id = 0
        for league in json.cars:
            league_table.insert_league(League(league_id, league))
            team_id = 0
            for team in json.cars[league]:
                team_table.insert_teams(Team(league_id, team_id, team))
                team_id += 1
            league_id += 1
    except sqlite3.IntegrityError:
        pass


def make_tracks():
    try:
        country_id = 0
        for country in json.tracks_id:
            track_table.insert_track(Track(country_id, country, json.tracks_id[country]))
            country_id += 1
    except sqlite3.IntegrityError:
        pass


def make_game_modes():
    try:
        for game_mode in json.game_modes:
            game_mode_table.insert_game_mode(GameModes(json.game_modes[game_mode], game_mode))
    except sqlite3.IntegrityError:
        pass


def make_weathers():
    try:
        weather_table.insert_weather(0, "Wet")
        weather_table.insert_weather(1, "Dry")
        weather_table.insert_weather(2, "Mixed")
    except sqlite3.IntegrityError:
        pass


def make_presets():
    try:
        pass

    except sqlite3.IntegrityError:
        pass

def close_conn():
    conn.close()


if __name__ == "__main__":
    user0 = User(3, 'scruffy', 'Scruffington', 'scruffe', 20, 40000, 'scruffe@email', True)

    if not user_table.get_user_by_strs(user0.first, user0.last, user0.tag):
        user_table.insert_user(user0)

    json = Json()

    print(get_joined())

    close_conn()
