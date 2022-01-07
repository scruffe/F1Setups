from os import path
from tkinter import filedialog
from tracks import Tracks
from pathlib import Path
from DB.local_sqlite3.local_sqlite3 import LocalSqlite3

INSTALL_PATH = Path(__file__).parent.absolute()


class Update:
    def __init__(self, widgets, setup):
        self.widgets = widgets
        self.local_sqlite = LocalSqlite3()
        self.setup = setup

    def populate_db_from_setups_dir(self):
        """previous version 1.62 and before used individual .bin files to save setups"""
        setup_dir = filedialog.askdirectory(initialdir=INSTALL_PATH, title="Select setup directory")
        """find files in dir, check if its already in db, load file from dir, write to db"""
        for league in list(self.widgets.raceSettings):
            p = setup_dir + "/" + league
            if path.isdir(p):
                for team in self.widgets.raceSettings[league]:
                    team_path = p + "/" + team
                    if path.isdir(team_path):
                        for weather in list(self.widgets.weatherTypes):
                            weather_path = team_path + "/" + weather
                            if path.isdir(weather_path):
                                for game_mode in self.widgets.game_modes:
                                    game_mode_path = weather_path + "/" + game_mode
                                    if path.isdir(game_mode_path):
                                        for country in Tracks().tracks:
                                            file_path = game_mode_path + "/" + country + ".bin"
                                            if path.isfile(file_path):
                                                print(file_path)
                                                ids = self.local_sqlite.get_ids(league,
                                                                                country,
                                                                                weather,
                                                                                game_mode,
                                                                                team)
                                                try:
                                                    setup_db = self.local_sqlite.setups.get_setup_by_ids(*ids)
                                                    setup_id = setup_db[0][0]
                                                    print(setup_id, "is already in database")
                                                except IndexError:

                                                    self.widgets.sliders = self.setup.unpack_setup(file_path)
                                                    self.setup.load_setup_file(file_path)
                                                    car_setup = self.widgets.create_car_setup_from_widgets()
                                                    car_setup.league_id = ids[0]
                                                    car_setup.track_id = ids[1]
                                                    car_setup.weather_id = ids[2]
                                                    car_setup.game_mode_id = ids[3]
                                                    car_setup.team_id = ids[4]
                                                    print(car_setup.values)
                                                    self.local_sqlite.save_setup_to_db(car_setup)
                                                    print("added to database")
