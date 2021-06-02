import json
import os
import winreg
import re
import webbrowser
from tkinter import filedialog, messagebox, ttk


class Config:
    def __init__(self, root, install_path):
        self.root = root
        self.INSTALL_PATH = install_path

        self.config = self.load()
        self._steam_path = self.config['steam_path']
        self._workshop_dir = self.config['workshop_dir']
        self._workshop_file = ""
        self._sort_tracks = self.config['sort_tracks']
        self._auto_use_changes = self.config['auto_use_changes']
        self._auto_save_changes = self.config['auto_save_changes']
        self._auto_use_track = self.config['auto_use_track']

        self.theme = self.config['theme']
        self.default_setups = self.config['default_setups']
        self.race = self.config['race_box']
        self.cars = self.config['cars_box']
        self.weather = self.config['weather_box']
        self.game_mode = self.config['game_mode_box']

        self.f1_2020_steamID = "1080110"
        self.scruffe_f1_workshop_id = "2403338074"
        self.scruffe_f2_workshop_id = "2404403390"
        self.scruffe_classic_workshop_id = "2404433709"

    @staticmethod
    def load():
        with open('config.json') as f:
            config_f = json.load(f)
        f.close()
        return config_f

    def dump(self, key, value):
        self.config[key] = value
        with open("config.json", "w") as f:
            json.dump(self.config, f, indent=4)
        f.close()

    @staticmethod
    def subscribe(workshop_file, workshop_race_id):
        if not os.path.isfile(workshop_file):
            url = "https://steamcommunity.com/sharedfiles/filedetails/?id=" + workshop_race_id
            messagebox.showerror(
                "error",
                "Not Subscribed to steam workshop, Subscribe to: " + url)
            webbrowser.open_new(url)

    def use_theme(self):
        self.root.tk.call('lappend', 'auto_path', str(self.INSTALL_PATH))
        self.root.tk.call('package', 'require', self.theme)
        # s.theme_names('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        ttk.Style().theme_use(self.theme)

    @property
    def steam_path(self):
        return self._steam_path

    @steam_path.setter
    def steam_path(self, path):
        if path is None:
            try:
                hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                      r"SOFTWARE\WOW6432Node\Valve\Steam")  # <PyHKEY:0x0000000000000094>
                path = winreg.QueryValueEx(hkey, "InstallPath")
                winreg.CloseKey(hkey)
                path = path[0]
            except OSError:
                messagebox.showerror("error", "Can't find steam Install directory, select steam install dir")
                path = filedialog.askdirectory()
        self._steam_path = path
        self.dump('steam_path', path)

    @property
    def workshop_dir(self):
        return self._workshop_dir

    @workshop_dir.setter
    def workshop_dir(self, path):
        if path is None:
            if not os.path.isdir(self.steam_path):
                self.steam_path = None
            steam_path = self.steam_path
            library_folders = steam_path + r"\steamapps\libraryfolders.vdf"
            with open(library_folders) as f:
                libraries = [steam_path]
                lf = f.read()
                libraries.extend([fn.replace("\\\\", "\\") for fn in
                                  re.findall(r'^\s*"\d*"\s*"([^"]*)"', lf, re.MULTILINE)])
                for library in libraries:
                    appmanifest = library + r"\steamapps\appmanifest_" + self.f1_2020_steamID + ".ACF"
                    if os.path.isfile(appmanifest):
                        with open(appmanifest) as ff:
                            ff.read()
                            path = library + "/steamapps/workshop/content/" + self.f1_2020_steamID
                        ff.close()
            f.close()
        self._workshop_dir = path
        self.dump('workshop_dir', path)

    @property
    def workshop_file(self):
        return self._workshop_file

    @workshop_file.setter
    def workshop_file(self, workshop_race_id):
        if not os.path.isdir(self.workshop_dir):
            self.workshop_dir = None
        self._workshop_file = self._workshop_dir + "/" + workshop_race_id + "/ugcitemcontent.bin"
        self.subscribe(self._workshop_file, workshop_race_id)

    def get_workshop_race_id(self, race):
        race_id = self.scruffe_f1_workshop_id
        if race == "classic":
            race_id = self.scruffe_classic_workshop_id
        elif race == "F2 2019" or race == "F2 2020":
            race_id = self.scruffe_f2_workshop_id
        return race_id

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
