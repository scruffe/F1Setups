from tkinter import ttk, N, W, E, S, StringVar, Listbox, END
from tkinter.ttk import Combobox
import webbrowser

from DB.local_sqlite3 import league_sql, track_sql

from carsetup import CarSetup
from community import commands
from grid_widgets import GridWidgets
from make_scale import MakeScale
from slidercounter import SliderCounter
from jsondata import Json
from DB.local_sqlite3.local_sqlite3 import LocalSqlite3
from setup import Setup
from update import Update
from events import Events
from tracks import Tracks
from config import Config
from top_menu import TopMenu


class Widgets:
    def __init__(self, root):
        self.setup = Setup(self)
        json_data = Json()
        self.update = Update(self, self.setup)
        self.db = LocalSqlite3()
        self.tracks = Tracks()
        self.config = Config()

        self.top_menu = TopMenu(self, root)

        self.preset_setups = json_data.preset_setups
        self.game_modes = json_data.game_modes
        self.weatherTypes = json_data.weather
        self.cars = ('All Cars', '')
        self.raceSettings = json_data.cars

        self.c = ttk.Frame(root, padding=(5, 5, 12, 0))
        self.c.grid(column=0, row=0, sticky=(N, W, E, S))
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        self.bg = "#33393b"  # backgroundcolor
        self.fg = "white"  # forgroundcolor

        self.status_message = StringVar()

        self.tracks_sorted = StringVar(value=self.tracks.track_sorted_list)

        self.sliderFrame = ttk.LabelFrame(
            self.c,
            text="Setup",
            labelanchor='nw',
            padding=5)

        self.track_box = Listbox(
            self.c,
            listvariable=self.tracks_sorted,
            height=len(self.tracks.track_sorted_list),
            bg=self.bg,
            fg=self.fg,
            highlightcolor="black",
            selectbackground="darkred",
            selectforeground="white")
        self.track_box.selection_clear(1, last=None)

        self.race_box = self.create_combobox(list(self.raceSettings))
        self.cars_box = self.create_combobox(self.cars)
        self.weather_box = self.create_combobox(list(self.weatherTypes))
        self.preset_box = self.create_combobox(list(self.preset_setups.values()))
        self.game_mode_box = self.create_combobox(list(self.game_modes))

        """
        self.sort_tracks_box = self.create_checkbox(
            'Order Tracks', self.sort_tracks, lambda: self.toggle_track_list(self.sort_tracks.get()))
        self.auto_use_changes_box = self.create_checkbox(
            'Auto Use Changes', self.auto_use_changes, lambda: self.update_auto_use(self.auto_use_changes.get()))
        self.auto_save_changes_box = self.create_checkbox(
            'Auto Save Changes',
            self.auto_save_changes,
            lambda: self.update_auto_save(self.auto_save_changes.get()))
        self.auto_use_track_box = self.create_checkbox(
            'Auto Use track', self.auto_use_track,
            lambda: self.update_auto_use_track(self.auto_use_track.get()))
        """

        # self.upload_button = self.create_button("Upload", self.upload)
        # self.community_button = self.create_button("Community", community.Community)
        # self.import_setups = self.create_button("import previous setups", self.update.populate_db_from_setups_dir)
        self.useButton = self.create_button("Use", self.use_cmd)
        # self.useSaveButton = self.create_button("Save & Use", self.use_save_cmd)
        # self.saveButton = self.create_button("Save", self.save_cmd)
        # self.saveAsButton = self.create_button("Save As", self.save_as_cmd)
        # self.openButton = self.create_button("Open", self.open_cmd)
        # self.tipBtn = self.create_button("Tip Scruffe",
        #                                  lambda: self.open_url("https://paypal.me/valar"))
        self.status_bar = ttk.Label(
            self.c,
            textvariable=self.status_message,
            anchor=W)

        scales = MakeScale(self.sliderFrame)
        self.front_wing_Scale = scales.make("Front wing")
        self.rear_wing_Scale = scales.make("Rear wing")
        self.on_throttle_Scale = scales.make("On throttle", from_=50, to=100)
        self.off_throttle_Scale = scales.make("Off throttle", from_=50, to=100)
        self.front_camber_Scale = scales.make("Front camber", step=0.1, offset=-3.5)
        self.rear_camber_Scale = scales.make("Rear camber", step=0.1, offset=-2)
        self.front_toe_Scale = scales.make("Front toe", step=0.01, offset=0.05, res=2)
        self.rear_toe_Scale = scales.make("Rear toe", step=0.03, offset=0.20, res=2)  # there is an offset
        self.front_suspension_Scale = scales.make("Front suspension")
        self.rear_suspension_Scale = scales.make("Rear suspension")
        self.front_antiroll_bar_Scale = scales.make("Front antiroll bar")
        self.rear_antiroll_bar_Scale = scales.make("Rear antiroll bar")
        self.front_suspension_height_Scale = scales.make("Front suspension height")
        self.rear_suspension_height_Scale = scales.make("Rear suspension height")
        self.brake_pressure_Scale = scales.make("Brake pressure", from_=50, to=100)
        self.brake_bias_Scale = scales.make("Brake bias", from_=70, to=50)
        self.front_right_tyre_pressure_Scale = scales.make("Front right tyre pressure", step=.4, offset=21)  # , 0.4)
        self.front_left_tyre_pressure_Scale = scales.make("Front left tyre pressure", step=.4, offset=21)
        self.rear_right_tyre_pressure_Scale = scales.make("Rear right tyre pressure", step=.4, offset=19.5)
        self.rear_left_tyre_pressure_Scale = scales.make("Rear left tyre pressure", step=.4, offset=19.5)
        self.ballast_Scale = scales.make("Ballast")
        self.ramp_differential_Scale = scales.make("Ramp differential", from_=50, to=70)
        self.fuel_load_Scale = scales.make("Fuel load", from_=5, to=110)
        self.grid()

    @property
    def boxes(self):
        return [self.track_box,
                self.race_box,
                self.cars_box,
                self.weather_box,
                self.game_mode_box,
                self.preset_box]


    """@property
    def check_boxes(self):
        return [self.sort_tracks_box,
                self.auto_use_changes_box,
                self.auto_save_changes_box,
                self.auto_use_track_box,
                # self.import_setups
                ]"""

    @property
    def league_id(self):
        return self.race_box.get()

    @property
    def team_id(self):
        """returns the ingame f1game team_id"""
        team_ids = [  # https://forums.codemasters.com/topic/50942-f1-2020-udp-specification/
            "Mercedes",
            "Ferrari",
            "Red Bull",
            "Williams",
            "Racing Point",
            "Renault",
            "AlphaTauri",
            "Haas",
            "McLaren",
            "Alfa Romeo",

            "McLaren 1988",
            "McLaren 1991",
            "Williams 1992",
            "Ferrari 1995",
            "Williams 1996",
            "McLaren 1998",
            "Ferrari 2002",
            "Ferrari 2004",
            "Renault 2006",
            "Ferrari 2007",

            "McLaren 2008",
            "Red Bull 2010",
            "Ferrari 1976",

            "ART Grand Prix",
            "Campos Vexatec Racing",
            "Carlin",
            "Charouz Racing System",
            "Dams",
            "Uni-Virtuosi Racing",  # changed russiantime
            "MP Motorsport",

            "Pertamina",  #
            "McLaren 1990",
            "Trident",
            "BWT HWA Racelab",
            "McLaren 1976",
            "Lotus 1972",
            "Ferrari 1979",
            "McLaren 1982",
            "Williams 2003",
            "Brawn 2009",

            "Lotus 1978",
            "F1 Generic car",
            "Art GP ’19",
            "Campos ’19",
            "Carlin ’19",
            "Sauber Junior Charouz ’19",
            "Dams '19",
            "Uni-Virtuosi ‘19",
            "MP Motorsport ‘19",
            "Prema ’19",

            "Trident ’19",
            "Arden ’19",
            "Benetton 1994",
            "Benetton 1995",
            "Ferrari 2000",
            "Jordan 1991",
            "All Cars",
            "My Team"]  # 255
        """
        f2 does not comply with udp specification some examples:
        
        69 =multiplayer
        76= mpmotersport
        77 perta
        78 trident
        79 bwt
        80 hitech
        
        81 jordan91
        82 benet
        """

        team = self.cars_box.get()
        if team == "All Cars":
            return 41  # multiplayer car
        return team_ids.index(team)

    @property
    def track_id(self):
        return self.tracks.current_track

    @property
    def game_mode_id(self):
        return self.game_modes[self.game_mode_box.get()]

    @property
    def weather_id(self):
        if self.weather_box.get() == "Wet":
            return 0
        return 1

    @property
    def sliders(self):
        """list of sliders"""
        return [
            self.front_wing_Scale,
            self.rear_wing_Scale,
            self.on_throttle_Scale,
            self.off_throttle_Scale,
            self.front_camber_Scale,
            self.rear_camber_Scale,
            self.front_toe_Scale,
            self.rear_toe_Scale,
            self.front_suspension_Scale,
            self.rear_suspension_Scale,
            self.front_suspension_height_Scale,
            self.rear_suspension_height_Scale,
            self.front_antiroll_bar_Scale,
            self.rear_antiroll_bar_Scale,
            self.brake_pressure_Scale,
            self.brake_bias_Scale,
            self.front_right_tyre_pressure_Scale,
            self.front_left_tyre_pressure_Scale,
            self.rear_right_tyre_pressure_Scale,
            self.rear_left_tyre_pressure_Scale,
            self.ballast_Scale,
            self.fuel_load_Scale,
            self.ramp_differential_Scale]

    @sliders.setter
    def sliders(self, unpacked_setup):
        """syntax, bool(from database or .bin file) + car setup"""
        if unpacked_setup[0] is True:
            i = 8
            for slider in self.sliders:
                if slider.offset != 1:
                    value = unpacked_setup[i]
                    p = round(value - slider.offset, slider.res)
                    product = round(p / slider.step, slider.res) + 1
                    slider.set(product)
                else:
                    slider.set(unpacked_setup[i])
                i += 1
            print('loaded from db', unpacked_setup)
        else:
            create_slider = SliderCounter(unpacked_setup)
            for slider in self.sliders:
                create_slider.set_slider_value(slider)

    def create_combobox(self, _values):
        return Combobox(
            self.c,
            justify="center",
            values=_values,
            state='readonly')

    def create_checkbox(self, text, variable, command=None):
        return ttk.Checkbutton(
            self.c,
            text=text,
            variable=variable,
            command=command)

    def create_checkbutton(self, txt, var, cmd):
        return ttk.Checkbutton(
            self.c,
            text=txt,
            variable=var,
            command=lambda: cmd)

    def create_button(self, text, command=None):
        return ttk.Button(
            self.c,
            text=text,
            command=command)

    def grid(self):
        self.sliderFrame.grid(
            row=0,
            rowspan=15,
            column=2,
            columnspan=5)

        box_grid = GridWidgets()
        for box in self.boxes:
            box_grid.grid_box(box)

        check_box_grid = GridWidgets(startrow=8, padx=10)


        """for check_box in self.check_boxes:
            check_box_grid.grid_box(check_box)"""

        buttons = GridWidgets(startrow=check_box_grid.row, increment_horizontal=True)

        buttons.grid_box(self.useButton, columnspan=2)
        # buttons.grid_box(self.saveButton)
        # buttons.grid_box(self.saveAsButton)
        # buttons.grid_box(self.openButton)
        # buttons.grid_box(self.tipBtn, columnspan=2)
        # buttons.grid_box(self.community_button)
        # buttons.grid_box(self.upload_button)

        status = GridWidgets(startrow=(buttons.row + 16))
        status.grid_box(self.status_bar, columnspan=7)

        self.c.grid_columnconfigure(0, weight=1)
        self.c.grid_rowconfigure(11, weight=1)

    def use_cmd(self):
        self.setup.use_setup()
        self.status_message.set("Using current setup")

    def open_cmd(self):
        try:
            path = self.setup.open_setup()
            self.status_message.set(" Opened (" + str(path) + ")")
        except FileNotFoundError:
            self.status_message.set(" Can't find file)")

    def use_save_cmd(self):
        self.setup.use_setup()
        self.save_cmd()

    def save_cmd(self):
        car_setup = self.create_car_setup_from_widgets()
        self.setup.save_setup(car_setup)
        self.status_message.set("Saved")

    def save_as_cmd(self):
        try:
            path = self.setup.save_as_setup()
            self.status_message.set("Saved: " + path)
        except FileNotFoundError:
            self.status_message.set("File not found")

    def upload(self):
        car_setup = self.create_car_setup_from_widgets()
        print(car_setup.info)
        commands.Commands().upload(car_setup)

    def toggle_track_list(self, sort_bool):
        """sort track list based on calendar or Alphabet"""
        # save new value to config file
        self.config.sort_tracks = sort_bool

        # update track list
        self.tracks.toggle_track_sort(sort_bool)
        self.track_box.delete(0, END)
        self.track_box.insert(END, *self.tracks.track_sorted_list)

        # redo background color
        self.tracks_background_color()

        # show the previous selected track
        Events(self).box_event()

    def tracks_background_color(self):
        for i in range(0, len(self.tracks.track_sorted_list), 2):
            self.track_box.itemconfigure(i, background='#576366', fg=self.fg)

    def set_starting_values(self):
        """set widgets default values"""
        self.track_box.selection_set(0)
        self.race_box.set(self.config.race)
        self.cars_box['values'] = self.raceSettings[self.config.race]
        self.cars_box.set(self.config.cars)
        self.weather_box.set(self.config.weather)
        self.game_mode_box.set(self.config.game_mode)
        self.preset_box.set("Load Preset")
        self.status_message.set('')
        self.top_menu.set_starting_values()

    def toggle_race_sliders(self, race):
        on_throttle = 'enabled'
        off_throttle = 'enabled'
        brake_pressure = 'enabled'
        fuel_load = 'enabled'
        ballast = 'enabled'
        ramp_differential = 'enabled'

        if race == 'F1 2020' or race == 'classic':
            ramp_differential = 'disabled'
            if race == 'F1 2020':
                ballast = 'disabled'

        elif race == 'F2 2020' or race == 'F2 2019':
            on_throttle = 'disabled'
            off_throttle = 'disabled'
            brake_pressure = 'disabled'
            fuel_load = 'disabled'

        self.on_throttle_Scale.config(state=on_throttle)
        self.off_throttle_Scale.config(state=off_throttle)
        self.brake_pressure_Scale.config(state=brake_pressure)
        self.fuel_load_Scale.config(state=fuel_load)
        self.ballast_Scale.config(state=ballast)
        self.ramp_differential_Scale.config(state=ramp_differential)

    def create_car_setup_from_widgets(self):
        league_id = league_sql.LeagueSql().get_id_from_name(self.league_id)
        car_setup = CarSetup(
            league_id=league_id,
            save_name=" save name test",
            team_id=self.db.teams.get_team_id(self.cars_box.get(), league_id),
            track_id=track_sql.TrackSql().get_track_id_by_country(self.track_id),
            game_mode_id=self.game_mode_id,
            weather_id=self.weather_id,

            front_wing=self.front_wing_Scale.get(),
            rear_wing=self.rear_wing_Scale.get(),
            on_throttle=self.on_throttle_Scale.get(),
            off_throttle=self.off_throttle_Scale.get(),
            front_camber=self.front_camber_Scale.get(),
            rear_camber=self.rear_camber_Scale.get(),
            front_toe=self.front_toe_Scale.get(),
            rear_toe=self.rear_toe_Scale.get(),
            front_suspension=self.front_suspension_Scale.get(),
            rear_suspension=self.rear_suspension_Scale.get(),
            front_suspension_height=self.front_suspension_height_Scale.get(),
            rear_suspension_height=self.rear_suspension_height_Scale.get(),
            front_antiroll_bar=self.front_antiroll_bar_Scale.get(),
            rear_antiroll_bar=self.rear_antiroll_bar_Scale.get(),
            brake_pressure=self.brake_pressure_Scale.get(),
            brake_bias=self.brake_bias_Scale.get(),
            front_right_tyre_pressure=self.front_right_tyre_pressure_Scale.get(),
            front_left_tyre_pressure=self.front_left_tyre_pressure_Scale.get(),
            rear_right_tyre_pressure=self.rear_right_tyre_pressure_Scale.get(),
            rear_left_tyre_pressure=self.rear_left_tyre_pressure_Scale.get(),
            ballast=self.ballast_Scale.get(),
            fuel_load=self.fuel_load_Scale.get(),
            ramp_differential=self.ramp_differential_Scale.get()
        )
        return car_setup

    @staticmethod
    def open_url(url):
        webbrowser.open_new(url)
