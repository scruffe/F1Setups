import tkinter
from json import load, dump
from os import path
import winreg
import re
import webbrowser
from tkinter import filedialog, messagebox
import pathlib


class Config:
    def __init__(self):
        self.INSTALL_PATH = pathlib.Path(__file__).parent.absolute()

        self.config = self.load()
        self._steam_path = self.config['steam_path']
        self._workshop_dir = self.config['workshop_dir']
        self._2020_workshop_dir = self.config['2020_workshop_dir']
        self._workshop_file = ""
        self._current_track = self.config['current_track']
        self._sort_tracks = self.config['sort_tracks']
        self._auto_use_changes = self.config['auto_use_changes']
        self._auto_save_changes = self.config['auto_save_changes']
        self._auto_use_track = self.config['auto_use_track']
        self._order_tracks = self.config['order_tracks']

        self.theme = self.config['theme']
        self.default_setups = self.config['default_setups']
        self._race = self.config['race']
        self.cars = self.config['cars_box']
        self.weather = self.config['weather_box']
        self.game_mode = self.config['game_mode_box']

        self.f1_2021_steamID = "1134570"
        self.f1_2020_steamID = "1080110"

        self.scruffe_f1_21_workshop_id = "2710709065"
        self.scruffe_f1_20_workshop_id = "2403338074"

        self.scruffe_f2_21_workshop_id = "2712074261"
        self.scruffe_f2_20_workshop_id = "2404403390"

        self.scruffe_classic_20_workshop_id = "2404433709"

        self._install_db = self.config["install_db"]

    @staticmethod
    def load():
        with open('F1Setups/config/config.json') as f:
            config_f = load(f)
        f.close()
        return config_f

    def dump(self, key, value):
        self.config[key] = value
        with open("F1Setups/config/config.json", "w") as f:
            dump(self.config, f, indent=4)
        f.close()

    @staticmethod
    def subscribe(workshop_file, workshop_race_id):
        if not path.isfile(workshop_file):
            url = "https://steamcommunity.com/sharedfiles/filedetails/?id=" + workshop_race_id
            if messagebox.askokcancel(
                    "error",
                    "Not Subscribed to steam workshop, Subscribe to: " + url + "\n Subscribe?"):
                webbrowser.open_new(url)

    @property
    def steam_path(self):
        return self._steam_path

    @steam_path.setter
    def steam_path(self, _path):
        if _path is None:
            try:
                hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                      r"SOFTWARE\WOW6432Node\Valve\Steam")  # <PyHKEY:0x0000000000000094>
                _path = winreg.QueryValueEx(hkey, "InstallPath")
                winreg.CloseKey(hkey)
                _path = _path[0]
            except OSError:
                messagebox.showerror("error", "Can't find steam Install directory, select steam install dir")
                _path = filedialog.askdirectory()
        self._steam_path = _path
        self.dump('steam_path', _path)

    @property
    def workshop_dir(self):
        race = Config().race
        if race == "F1 2021" or race == "F2 2021":
            workshop_dir = self._workshop_dir
        else:
            workshop_dir = self._2020_workshop_dir
        return workshop_dir

    @workshop_dir.setter
    def workshop_dir(self, _path):
        if _path is None or path == "":
            if not path.isdir(self.steam_path):
                self.steam_path = None
            steam_path = self.steam_path
            library_folders = steam_path + r"\steamapps\libraryfolders.vdf"

            """"read the file and find the libraries"""
            with open(library_folders) as f:
                library_file = f.read()
                pattern = re.compile(
                    r'"path"[\s]+"(.+)"')  # {"path"+ spaces (1-more) +"+ Any Character Except \n (1-more)+"}
                matches = pattern.finditer(library_file)
                for library in matches:
                    lib_path = library.group(1)
                    print(lib_path)

                    """check every library for an app manifest with the game"""
                    def check_appmanifest(steam_id):
                        appmanifest = lib_path + r"\steamapps\appmanifest_" + steam_id + ".ACF"
                        if path.isfile(appmanifest):
                            with open(appmanifest) as ff:
                                ff.read()
                                return lib_path + "/steamapps/workshop/content/" + steam_id

                    _path = check_appmanifest(self.f1_2021_steamID)
                    self._2020_workshop_dir = check_appmanifest(self.f1_2020_steamID)

        def ask_user_steam_library(p, string, steam_id):
            if p is None or p == "":
                p = tkinter.filedialog.askdirectory(
                    title=f"select {string} SteamLibrary folder, eg D:/SteamLibrary") + "/steamapps/workshop/content/"
                if path.isdir(p + steam_id):
                    return p + steam_id
                else:
                    messagebox.showerror("Error", f"Cant find {string} SteamLibrary")

        _path = ask_user_steam_library(_path, "F1 2021", self.f1_2021_steamID)
        self._2020_workshop_dir = ask_user_steam_library(self._2020_workshop_dir, "F1 2020", self.f1_2020_steamID)

        self._workshop_dir = _path
        self.dump('workshop_dir', _path)
        self.dump('2020_workshop_dir', self._2020_workshop_dir)

    @property
    def workshop_file(self):
        return self._workshop_file

    @workshop_file.setter
    def workshop_file(self, args):
        workshop_path = args[0]
        race_id = args[1]
        if workshop_path is None or workshop_path == "":
            self.workshop_dir = None
            workshop_path = self.workshop_dir
        self._workshop_file = workshop_path + "/" + race_id + "/ugcitemcontent.bin"
        if not path.isdir(workshop_path):
            messagebox.showerror("error", "Cant find game workshop dir")
        elif not path.isfile(self._workshop_file):
            self.subscribe(self._workshop_file, race_id)

    def get_workshop_race_id(self, race):
        if race == "F1 2021":
            _path = self._workshop_dir
            race_id = self.scruffe_f1_21_workshop_id
        elif race == "F2 2021":
            _path = self._workshop_dir
            race_id = self.scruffe_f2_21_workshop_id
        elif race == "F1 2020":
            _path = self._2020_workshop_dir
            race_id = self.scruffe_f1_20_workshop_id
        elif race == "classic":
            _path = self._2020_workshop_dir
            race_id = self.scruffe_classic_20_workshop_id
        elif race == "F2 2019" or race == "F2 2020":
            _path = self._2020_workshop_dir
            race_id = self.scruffe_f2_20_workshop_id
        return _path, race_id

    @property
    def sort_tracks(self):
        return self._sort_tracks

    @sort_tracks.setter
    def sort_tracks(self, value):
        self._sort_tracks = value
        self.dump('sort_tracks', value)

    @property
    def auto_use_changes(self):
        return self._auto_use_changes

    @auto_use_changes.setter
    def auto_use_changes(self, value):
        self._auto_use_changes = value
        self.dump('auto_use_changes', value)

    @property
    def auto_save_changes(self):
        return self._auto_save_changes

    @auto_save_changes.setter
    def auto_save_changes(self, value):
        self._auto_save_changes = value
        self.dump('auto_save_changes', value)

    @property
    def auto_use_track(self):
        return self._auto_use_track

    @auto_use_track.setter
    def auto_use_track(self, value):
        self._auto_use_track = value
        self.dump('auto_use_track', value)

    @property
    def order_tracks(self):
        return self._order_tracks

    @order_tracks.setter
    def order_tracks(self, v):
        self._order_tracks = v
        self.dump('order_tracks', v)

    @property
    def current_track(self):
        return self._current_track

    @current_track.setter
    def current_track(self, v: str):
        self._current_track = v
        self.dump('current_track', v)

    @property
    def install_db(self):
        return self._install_db

    @install_db.setter
    def install_db(self, v: str):
        self._install_db = v
        self.dump('install_db', v)

    @property
    def race(self):
        return self._race

    @race.setter
    def race(self, v: str):
        self._race = v
        self.dump('race', v)
