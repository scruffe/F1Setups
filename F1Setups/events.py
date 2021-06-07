from DB.local_sqlite3 import presets_sql
from DB.local_sqlite3.local_sqlite3 import LocalSqlite3
from config import Config
from tracks import Tracks


class Events:
    def __init__(self, widgets):
        self.db = LocalSqlite3()
        self.tracks = Tracks()
        self.widgets = widgets
        self.config = Config()
        self.setup = widgets.setup

        self.track_box = widgets.track_box
        self.race_box = widgets.race_box
        self.cars_box = widgets.cars_box
        self.weather_box = widgets.weather_box
        self.preset_box = widgets.preset_box
        self.game_mode_box = widgets.game_mode_box

        #self.sort_tracks_box = widgets.sort_tracks_box

        self.sliders = widgets.sliders

        self.bind_events()

    def bind_events(self):
        self.track_box.bind('<ButtonRelease>', self.show_track_selection)
        self.race_box.bind("<<ComboboxSelected>>", self.race_box_event)
        self.cars_box.bind("<<ComboboxSelected>>", self.box_event)
        self.weather_box.bind("<<ComboboxSelected>>", self.box_event)
        self.preset_box.bind("<<ComboboxSelected>>", self.preset_box_event)
        self.game_mode_box.bind("<<ComboboxSelected>>", self.box_event)
        for slider in self.widgets.sliders:
            slider.bind("<ButtonRelease-1>", self.slider_event)

    def show_track_selection(self, *args):
        self.tracks.set_current_track(self.widgets.track_box.curselection())
        self.select_track(self.tracks.current_track)

    def race_box_event(self, *args):
        race = self.race_box.get()
        self.widgets.toggle_race_sliders(race)
        self.config.dump("race_box", race)
        self.cars_box['values'] = self.widgets.raceSettings[race]
        self.cars_box.current(0)
        self.box_event()

    def box_event(self, *args):
        self.config.dump("weather_box", self.weather_box.get())
        self.config.dump("game_mode_box", self.game_mode_box.get())
        self.config.dump("cars_box", self.cars_box.get())
        self.keep_track_selection_highlighted()
        self.show_track_selection()

    def slider_event(self, *args):
        auto_use = self.config.auto_use_changes
        auto_save = self.config.auto_save_changes
        if auto_use and auto_save:
            self.widgets.use_save_cmd()
        elif auto_use:
            self.setup.use_setup()
        elif auto_save:
            self.widgets.save_cmd()

    def preset_box_event(self, *args):
        self.keep_track_selection_highlighted()
        nr = str(self.preset_box.current() + 1)

        self.widgets.sliders = (True, *presets_sql.PresetSql().get_preset_by_id(nr))

        self.widgets.status_message.set(" Loaded (" + self.preset_box.get() + ")")
        self.widgets.preset_box.set("Load Preset")

    def keep_track_selection_highlighted(self):
        track_list = self.tracks.track_sorted_list
        self.track_box.selection_set(track_list.index(self.tracks.current_track))

    def select_track(self, country):
        """select the file to open, unpack the file, update sliders, if autoUse is checked;  write to workshop file"""
        league = self.race_box.get()
        team = self.cars_box.get()
        weather = self.weather_box.get()
        game_mode = self.game_mode_box.get()

        ids = self.db.get_ids(league,
                              country,
                              weather,
                              game_mode,
                              team)
        setup_db = self.db.setups.get_setup_by_ids(*ids)

        try:
            self.widgets.sliders = (True, *self.db.setups.get_setup_by_setup_id(setup_db[0][0]))
        except IndexError:
            """ if its not in db """
            print("file not in db")
            ids = self.db.get_ids(league,
                                  country,
                                  weather,
                                  "Invitational",
                                  "All Cars")
            setup_db = self.db.setups.get_setup_by_ids(*ids)

            try:
                self.widgets.sliders = (True, *self.db.setups.get_setup_by_setup_id(setup_db[0][0]))
            except IndexError:
                self.widgets.sliders = (True, *presets_sql.PresetSql().get_preset_by_id(3))

        if self.config.auto_use_track:
            self.setup.use_setup()

        self.widgets.status_message.set(
            " %s | %s | (%s) %s [%s]" % (
                league, team, country, self.tracks.tracks[country], self.widgets.weatherTypes[weather]))
