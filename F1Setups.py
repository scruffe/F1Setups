# from tkinter import *
import os
import pathlib
import struct
import webbrowser
from tkinter import Tk, ttk, HORIZONTAL, messagebox, filedialog, DoubleVar, \
    IntVar, StringVar, BooleanVar, N, W, E, S, Listbox, END
from tkinter.ttk import Combobox

from jsondata import Json
from config import Config
from tracks import Tracks

from carsetup import CarSetup

import community
import grid_widgets

from sql_db import SqlDB
from sql import *
import testing

INSTALL_PATH = pathlib.Path(__file__).parent.absolute()
root = Tk()
root.title('F1 Setup editor')
root.iconbitmap(str(INSTALL_PATH) + '/pog.ico')

SetupDir = str(INSTALL_PATH) + "/Setups/"


# precision limiter
# https://stackoverflow.com/questions/54186639/tkinter-control-ttk-scales-increment-as-with-tk-scale-and-a-tk-doublevar
class Limiter(ttk.Scale):
    """ ttk.Scale subclass that limits the precision of values. """

    def __init__(self, *args, **kwargs):
        self.precision = kwargs.pop('precision')  # Remove non-std kwarg.
        self.offset = kwargs.pop('offset')
        self.res = kwargs.pop('res')
        self.step = kwargs.pop('step')

        self.chain = kwargs.pop('command', lambda *a: None)  # Save if present.
        super(Limiter, self).__init__(*args, command=self._value_changed, **kwargs)

    def get(self, x=None, y=None):
        """Get the current value of the value option, or the value
        corresponding to the coordinates x, y if they are specified.

        x and y are pixel coordinates relative to the scale widget
        origin."""
        if self.offset != 1:  # offset has to do with sliders being 10 steps
            value = self.tk.call(self._w, 'get', x, y)

            m = round(value * self.step, self.res)
            return round(self.offset + m - self.step, self.res)

        return self.tk.call(self._w, 'get', x, y)

    def _value_changed(self, new_value):
        new_value = round(float(new_value), self.precision)
        if self.precision == 0:
            self.winfo_toplevel().globalsetvar(self.cget('variable'), (int(new_value)))
        else:
            self.winfo_toplevel().globalsetvar(self.cget('variable'), new_value)
        self.chain(new_value)  # Call user specified function.


class SliderCounter:  # reads corresponding slider value in setup file and sets a slider to that value

    def __init__(self, unpacked_setup):
        self.setup = unpacked_setup
        self.x = 41

    def set_slider_value(self, scale):
        self.x += 3

        if scale.offset != 1:
            self.set_slider_with_offset(scale)
        else:
            scale.set(self.setup[self.x])

    # Translates the 10 steps in sliders to actual values for/from the setup files
    def set_slider_with_offset(self, scale):
        value = self.setup[self.x]
        p = round(value - scale.offset, scale.res)
        product = round(p / scale.step, scale.res) + 1
        scale.set(product)


class MakeScale:
    def __init__(self, frame, step=0.0, offset=1.0, res=1):
        self.row_i = 1
        self.column = 2
        self.rowspan = 1
        self.sticky = 'NSEW'
        self.frame = frame
        self.text = ""

        self.from_ = 1
        self.to = 11
        self.step = step
        self.offset = offset
        self.res = res

        self.input_var = IntVar()

    def create_separator(self):
        ttk.Separator(self.frame).grid(row=self.row_i)

    def create_empty_space(self):
        ttk.Label(self.frame, anchor=W).grid(row=self.row_i)
        self.row_i += 1

    def create_scale(self):
        scale = Limiter(
            self.frame,
            from_=self.from_,
            to=self.to,
            orient=HORIZONTAL,
            length=200,
            variable=self.input_var,
            precision=0,
            step=self.step,
            offset=self.offset,
            res=self.res
        )
        scale.grid(
            row=self.row_i,
            column=self.column + 1,
            columnspan=2,
            rowspan=self.rowspan,
            sticky=self.sticky)
        return scale

    def set_offset(self, label):
        var = self.input_var
        step = self.step
        res = self.res
        offset = self.offset

        def update_other_label(*args):
            value = var.get()
            multiplier = round(value * step, res)
            product = round(offset + multiplier - step, res)

            input_var_mult.set(product)

        self.input_var.trace_add("write", update_other_label)
        input_var_mult = DoubleVar()

        label.config(textvariable=input_var_mult)

    def create_text_label(self):
        txt = ttk.Label(
            self.frame,
            text=self.text,
            anchor=W)
        txt.grid(
            row=self.row_i,
            column=self.column,
            columnspan=1,
            rowspan=self.rowspan,
            sticky=self.sticky)

    def create_value_label(self):
        scale_nr = ttk.Label(
            self.frame,
            textvariable=self.input_var,
            anchor=E,
            width=5)
        scale_nr.grid(
            row=self.row_i,
            column=self.column + 4,
            columnspan=1,
            rowspan=self.rowspan,
            sticky=self.sticky)

        return scale_nr

    def make(self, text, from_=1, to=11, step=0.0, offset=1.0, res=1):
        self.input_var = IntVar()

        self.from_ = from_
        self.to = to
        self.text = text
        self.step = step
        self.offset = offset
        self.res = res

        if (self.row_i % 3) == 0:  # create empty space every 2 sliders
            self.create_empty_space()

        self.create_separator()
        scale = self.create_scale()
        self.create_text_label()
        scale_nr = self.create_value_label()

        if step != 0:
            self.set_offset(scale_nr)

        self.row_i += 1
        return scale


class Widgets:
    def __init__(self, settings):
        self.settings = settings
        self.update = Update()
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

        self.sort_tracks = BooleanVar()
        self.auto_use_track = BooleanVar()
        self.auto_save_changes = BooleanVar()
        self.auto_use_changes = BooleanVar()
        self.tracks_sorted = StringVar(value=tracks.track_sorted_list)
        self.setup = setup

        self.sliderFrame = ttk.LabelFrame(
            self.c,
            text="Setup",
            labelanchor='nw',
            padding=5)
        self.track_box = Listbox(
            self.c,
            listvariable=self.tracks_sorted,
            height=len(tracks.track_sorted_list),
            bg=self.bg,
            fg=self.fg,
            highlightcolor="black",
            selectbackground="darkred",
            selectforeground="white")
        self.race_box = Combobox(
            self.c,
            justify="center",
            values=list(self.raceSettings),
            state='readonly')  # state= 'readonly' , 'disabled'
        self.cars_box = Combobox(
            self.c,
            justify="center",
            values=self.cars,
            state='readonly')
        self.weather_box = Combobox(
            self.c,
            justify="center",
            values=list(self.weatherTypes),
            state='readonly')

        self.preset_box = Combobox(
            self.c,
            justify="center",
            values=list(self.preset_setups.values()),
            state='readonly')
        self.game_mode_box = Combobox(
            self.c,
            justify="center",
            values=list(self.game_modes),
            state='readonly')

        self.status_bar = ttk.Label(
            self.c,
            textvariable=self.status_message,
            anchor=W)

        self.sort_tracks_box = ttk.Checkbutton(
            self.c,
            text='Order Tracks',
            variable=self.sort_tracks,
            command=lambda: self.toggle_track_list(self.sort_tracks.get()))

        self.auto_use_changes_box = ttk.Checkbutton(
            self.c,
            text='Auto Use Changes',
            variable=self.auto_use_changes,
            command=lambda: self.update_auto_use(self.auto_use_changes.get()))

        self.auto_save_changes_box = ttk.Checkbutton(
            self.c,
            text='Auto Save Changes',
            variable=self.auto_save_changes,
            command=lambda: self.update_auto_save(self.auto_save_changes.get()))

        self.auto_use_track_box = ttk.Checkbutton(
            self.c,
            text='Auto Use track',
            variable=self.auto_use_track,
            command=lambda: self.update_auto_use_track(self.auto_use_track.get()))

        self.community_button = ttk.Button(
            self.c,
            text="Community",
            command=community.CommunityWidget
        )

        self.import_setups = ttk.Button(
            self.c,
            text="import previous setups",
            command=self.update.populate_db_from_setups_dir
        )

        self.useButton = ttk.Button(
            self.c,
            text="Use",
            command=self.setup.use_setup
        )
        self.useSaveButton = ttk.Button(
            self.c,
            text="Save & Use",
            command=self.setup.use_save_setup
        )
        self.saveButton = ttk.Button(
            self.c,
            text="Save",
            command=self.setup.save_setup
        )
        self.saveAsButton = ttk.Button(
            self.c,
            text="Save As",
            command=self.setup.save_as_setup
        )
        self.openButton = ttk.Button(
            self.c,
            text="Open",
            command=self.setup.open_setup
        )

        # create tipURL widget
        self.tipBtn = ttk.Button(
            self.c,
            text="Tip Scruffe",
            command=lambda: open_url("https://paypal.me/valar")
        )

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

        self.track_box.selection_clear(1, last=None)
        self.grid()

    def grid(self):
        self.sliderFrame.grid(
            row=0,
            rowspan=15,
            column=2,
            columnspan=5)

        box = grid_widgets.GridWidgets()

        box.grid_box(self.track_box, rowspan=3)
        box.grid_box(self.race_box)
        box.grid_box(self.cars_box)
        box.grid_box(self.weather_box)
        box.grid_box(self.game_mode_box)
        box.grid_box(self.preset_box)

        check_box = grid_widgets.GridWidgets(startrow=8, padx=10)
        check_box.grid_box(self.sort_tracks_box)
        check_box.grid_box(self.auto_use_changes_box)
        check_box.grid_box(self.auto_save_changes_box)
        check_box.grid_box(self.auto_use_track_box)
        check_box.grid_box(self.import_setups)

        buttons = grid_widgets.GridWidgets(startrow=check_box.row, increment_horizontal=True)
        buttons.grid_box(self.useButton, columnspan=2)
        buttons.grid_box(self.saveButton)
        buttons.grid_box(self.saveAsButton)
        buttons.grid_box(self.openButton)
        buttons.grid_box(self.tipBtn, columnspan=2)
        buttons.grid_box(self.community_button)

        status = grid_widgets.GridWidgets(startrow=(buttons.row + 1))
        status.grid_box(self.status_bar, columnspan=7)

        self.c.grid_columnconfigure(0, weight=1)
        self.c.grid_rowconfigure(11, weight=1)

    def toggle_track_list(self, sort_bool):
        self.settings.sort_tracks = sort_bool
        tracks.toggle_track_sort(sort_bool)
        self.track_box.delete(0, END)
        self.track_box.insert(END, *tracks.track_sorted_list)
        self.tracks_background_color()
        event.box_event()

    def tracks_background_color(self):
        for i in range(0, len(tracks.track_sorted_list), 2):
            self.track_box.itemconfigure(i, background='#576366', fg=self.fg)

    def update_auto_use(self, b):
        self.settings.auto_use_changes = b

    def update_auto_save(self, b):
        self.settings.auto_save_changes = b

    def update_auto_use_track(self, b):
        self.settings.auto_use_track = b

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

    def set_starting_values(self):
        self.track_box.selection_set(0)
        self.race_box.set(self.settings.race)
        self.cars_box['values'] = self.raceSettings[self.settings.race]
        self.cars_box.set(self.settings.cars)
        self.weather_box.set(self.settings.weather)
        self.game_mode_box.set(self.settings.game_mode)
        self.preset_box.set("Load Preset")
        if self.settings.sort_tracks:
            self.sort_tracks_box.invoke()
        if self.settings.auto_use_changes:
            self.auto_use_changes_box.invoke()
        if self.settings.auto_save_changes:
            self.auto_save_changes_box.invoke()
        if self.settings.auto_use_track:
            self.auto_use_track_box.invoke()
        self.status_message.set('')

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
        return tracks.current_track

    @property
    def game_mode_id(self):
        return self.game_modes[self.game_mode_box.get()]

    @property
    def weather_id(self):
        if self.weather_box.get() == "Wet":
            return 0
        return 1

    def create_car_setup(self):
        league_id = league_sql.LeagueSql().get_id_from_name(self.league_id)
        car_setup = CarSetup(
            league_id=league_id,
            save_name=" save name test",
            team_id=db.teams.get_team_id(self.cars_box.get(), league_id),
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


class Events:
    def __init__(self, settings):
        self.widgets = widgets
        self.settings = settings
        self.setup = setup

        self.track_box = widgets.track_box
        self.race_box = widgets.race_box
        self.cars_box = widgets.cars_box
        self.weather_box = widgets.weather_box
        self.preset_box = widgets.preset_box
        self.game_mode_box = widgets.game_mode_box

        self.sort_tracks_box = widgets.sort_tracks_box

        self.sliders = widgets.sliders

        self.bind_events()

    def bind_events(self):
        self.track_box.bind('<ButtonRelease>', self.show_track_selection)
        self.race_box.bind("<<ComboboxSelected>>", self.race_box_event)
        self.cars_box.bind("<<ComboboxSelected>>", self.box_event)
        self.weather_box.bind("<<ComboboxSelected>>", self.box_event)
        self.preset_box.bind("<<ComboboxSelected>>", self.preset_box_event)
        self.game_mode_box.bind("<<ComboboxSelected>>", self.box_event)
        for slider in widgets.sliders:
            slider.bind("<ButtonRelease-1>", self.slider_event)

    def show_track_selection(self, *args):
        tracks.set_current_track(widgets.track_box.curselection())
        self.select_track(tracks.current_track)

    def race_box_event(self, *args):
        race = self.race_box.get()
        widgets.toggle_race_sliders(race)
        self.settings.dump("race_box", race)
        self.cars_box['values'] = widgets.raceSettings[race]
        self.cars_box.current(0)
        self.box_event()

    def box_event(self, *args):
        self.settings.dump("weather_box", self.weather_box.get())
        self.settings.dump("game_mode_box", self.game_mode_box.get())
        self.settings.dump("cars_box", self.cars_box.get())
        self.keep_track_selection_highlighted()
        self.show_track_selection()

    def slider_event(self, *args):
        auto_use = self.settings.auto_use_changes
        auto_save = self.settings.auto_save_changes
        if auto_use and auto_save:
            self.setup.use_save_setup()
        elif auto_use:
            self.setup.use_setup()
        elif auto_save:
            self.setup.save_setup()

    def preset_box_event(self, *args):
        self.keep_track_selection_highlighted()
        nr = str(self.preset_box.current() + 1)
        path = SetupDir + "Presets/Preset " + nr + ".bin"
        self.setup.load_setup_file(path)

        widgets.status_message.set(" Loaded (" + self.preset_box.get() + ")")
        widgets.preset_box.set("Load Preset")

    def keep_track_selection_highlighted(self):
        track_list = tracks.track_sorted_list
        self.track_box.selection_set(track_list.index(tracks.current_track))

    # select the file to open, unpack the file, update sliders, if autoUse is checked;  write to workshopfile
    def select_track(self, country):
        league = self.race_box.get()
        team = self.cars_box.get()
        weather = self.weather_box.get()
        game_mode = self.game_mode_box.get()

        ids = db.get_ids(league,
                         country,
                         weather,
                         game_mode,
                         team)
        setup_db = db.setups.get_setup_by_ids(*ids)

        try:
            widgets.sliders = (True, *db.setups.get_setup_by_setup_id(setup_db[0][0]))
        except IndexError:
            """ if its not in db """
            print("file not in db")
            ids = db.get_ids(league,
                             country,
                             weather,
                             "Invitational",
                             "All Cars")
            setup_db = db.setups.get_setup_by_ids(*ids)

            try:
                widgets.sliders = (True, *db.setups.get_setup_by_setup_id(setup_db[0][0]))
            except IndexError:
                preset_file_path = SetupDir + "Presets/Preset 3.bin"
                setup.load_setup_file(preset_file_path)

        if config.auto_use_track:
            setup.use_setup()

        widgets.status_message.set(
            " %s | %s | (%s) %s [%s]" % (
                league, team, country, tracks.tracks[country], widgets.weatherTypes[weather]))


class Setup:
    def __init__(self):
        # self.max_length_save_name = 128

        self.header = 'F1CS'
        self.versions = 'versionsi32'
        self.save_name_length = 'save_names128'
        self.save_name = 'All setups | scruffe'
        self.team_id = 'team_idui16'
        self.track_id = 'track_idui08'
        self.game_mode_id = 'game_mode_idsi32'
        self.weather_bool = 'weather_typebool'
        self.timestamp = 'timestampui64'
        self.game_setup_mode = 'game_setup_modeui08'
        self.fw = 'front_wingfp32'
        self.rw = 'rear_wingfp32'
        self.ot = 'on_throttlefp32'
        self.oft = 'off_throttlefp32'
        self.fc = 'front_camberfp32'
        self.rc = 'rear_camberfp32'
        self.ft = 'front_toefp32'
        self.rt = 'rear_toefp32'
        self.fs = 'front_suspensionfp32'
        self.rs = 'rear_suspensionfp32'
        self.fsh = 'front_suspension_heightfp32'
        self.rsh = 'rear_suspension_heightfp32'
        self.fab = 'front_antiroll_barfp32'
        self.rab = 'rear_antiroll_barfp32'
        self.bp = 'brake_pressurefp32'
        self.bb = 'brake_biasfp32'
        self.frtp = 'front_right_tyre_pressurefp32'
        self.fltp = 'front_left_tyre_pressurefp32'
        self.rrtp = 'rear_right_tyre_pressurefp32'
        self.rltp = 'rear_left_tyre_pressurefp32'
        self.b = 'ballastfp32'
        self.fl = 'fuel_loadfp32'
        self.rd = 'ramp_differentialfp32'
        self.footer = 'published_file_idui64'

        self.size = len(self.save_name)  # default size 20

    @property
    def packing_format(self):
        # ui08  |Unsigned 8-bit integer
        # i08   |Signed 8-bit integer
        # fp32  |Floating point (32-bit)

        # self.size = len(self.save_name)
        fmt = \
            f'<' \
            f'{len(self.header)}s5l1b' \
            f'{len(self.versions)}sfb' \
            f'{len(self.save_name_length)}sb' \
            f'{self.size}sb' \
            f'{len(self.team_id)}s3b' \
            f'{len(self.track_id)}s2b' \
            f'{len(self.game_mode_id)}s5b' \
            f'{len(self.weather_bool)}s2b' \
            f'{len(self.timestamp)}s9b' \
            f'{len(self.game_setup_mode)}s2b' \
            f'{len(self.fw)}sfb' \
            f'{len(self.rw)}sfb' \
            f'{len(self.ot)}sfb' \
            f'{len(self.oft)}sfb' \
            f'{len(self.fc)}sfb' \
            f'{len(self.rc)}sfb' \
            f'{len(self.ft)}sfb' \
            f'{len(self.rt)}sfb' \
            f'{len(self.fs)}sfb' \
            f'{len(self.rs)}sfb' \
            f'{len(self.fsh)}sfb' \
            f'{len(self.rsh)}sfb ' \
            f'{len(self.fab)}sfb ' \
            f'{len(self.rab)}sfb ' \
            f'{len(self.bp)}sfb ' \
            f'{len(self.bb)}sfb ' \
            f'{len(self.frtp)}sfb ' \
            f'{len(self.fltp)}sfb ' \
            f'{len(self.rrtp)}sfb ' \
            f'{len(self.rltp)}sfb ' \
            f'{len(self.b)}sfb ' \
            f'{len(self.fl)}sfb ' \
            f'{len(self.rd)}sfb ' \
            f'{len(self.footer)}s8B'
        return fmt

    def set_file_size(self, filename):
        # all information in the setup is static except for the length of the save name
        if os.path.isfile(filename):
            min_size = 748
            file_size = os.path.getsize(filename)
            name_size = file_size - min_size
            self.size = name_size
        else:
            self.size = 20  # preset save_name size

    def pack_setup(self):

        # syntax:  b'string', values (based on packing format), check value
        # all vars have a check value at the end,
        # Remove them and the game crashes. ¯\_(ツ)_/¯
        def b(s):
            return bytes(s, 'utf-8')

        self.save_name = 'All setups | scruffe'
        self.size = len(self.save_name)

        # self.setupStructPackingFormat = self.get_packing_format()
        packed_setup = struct.pack(
            self.packing_format,
            b(self.header), 0, 1, 0, 32, 0, 7,
            # \x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x07
            b(self.versions), 0, 9,  # \x00\x00\x00\x00\t
            b(self.save_name_length), self.size,  # \x14      probably string length of next name
            b(self.save_name), 7,  # \x07
            b(self.team_id), widgets.team_id, 0, 8,  # \x00\x00\x08
            b(self.track_id), tracks.track_id, 12,  # \x03\x0c
            b(self.game_mode_id), widgets.game_mode_id, 0, 0, 0, 12,
            # \x05\x00\x00\x00 \x0c
            b(self.weather_bool), widgets.weather_id, 9,  # \x01\t
            b(self.timestamp), 19, 14, 5, 95, 0, 0, 0, 0, 15,  # \x13\x0e\x05_\x00\x00\x00\x00\x0f
            b(self.game_setup_mode), 0, 10,  # \x00\n
            b(self.fw), widgets.front_wing_Scale.get(), 9,
            b(self.rw), widgets.rear_wing_Scale.get(), 11,
            b(self.ot), widgets.on_throttle_Scale.get(), 12,
            b(self.oft), widgets.off_throttle_Scale.get(), 12,
            b(self.fc), widgets.front_camber_Scale.get(), 11,
            b(self.rc), widgets.rear_camber_Scale.get(), 9,
            b(self.ft), widgets.front_toe_Scale.get(), 8,
            b(self.rt), widgets.rear_toe_Scale.get(), 16,
            b(self.fs), widgets.front_suspension_Scale.get(), 15,
            b(self.rs), widgets.rear_suspension_Scale.get(), 23,
            b(self.fsh), widgets.front_suspension_height_Scale.get(), 22,
            b(self.rsh), widgets.rear_suspension_height_Scale.get(), 18,
            b(self.fab), widgets.front_antiroll_bar_Scale.get(), 17,
            b(self.rab), widgets.rear_antiroll_bar_Scale.get(), 14,
            b(self.bp), widgets.brake_pressure_Scale.get(), 10,
            b(self.bb), widgets.brake_bias_Scale.get(), 25,
            b(self.frtp), widgets.front_right_tyre_pressure_Scale.get(), 24,
            b(self.fltp), widgets.front_left_tyre_pressure_Scale.get(), 24,
            b(self.rrtp), widgets.rear_right_tyre_pressure_Scale.get(), 23,
            b(self.rltp), widgets.rear_left_tyre_pressure_Scale.get(), 7,
            b(self.b), widgets.ballast_Scale.get(), 9,
            b(self.fl), widgets.fuel_load_Scale.get(), 17,
            b(self.rd), widgets.ramp_differential_Scale.get(), 17,
            b(self.footer), 31, 174, 162, 128, 0, 0, 0, 0
            # b'published_file_idui64\x1f\xae\xa2\x80\x00\x00\x00\x00'
        )

        return packed_setup

    def write_setup(self, filename):
        self.set_file_size(filename)
        packed_setup = self.pack_setup()
        with open(filename, 'wb') as file:
            file.write(packed_setup)
        file.close()

    def use_setup(self):
        config.workshop_file = config.get_workshop_race_id(widgets.race_box.get())
        self.write_setup(config.workshop_file)
        widgets.status_message.set("Using current setup")

    def save_setup(self):
        car_setup = widgets.create_car_setup()
        print(car_setup.setup_id, car_setup.team_id)
        db.save_setup_to_db(car_setup)
        testing.commit_conn()

        # self.write_setup(root.filename)
        widgets.status_message.set("Saved")

    def use_save_setup(self):
        self.use_setup()
        self.save_setup()

    def save_as_setup(self):
        asked_filename = filedialog.asksaveasfilename(initialdir=INSTALL_PATH, title="Select file",
                                                      defaultextension=".bin",
                                                      filetypes=(("bin files", "*.bin"), ("all files", "*.*")))
        self.write_setup(asked_filename)
        widgets.status_message.set("Saved: " + asked_filename)

    def unpack_setup(self, path):
        try:
            self.set_file_size(path)
            setup_file = open(path, "rb")
            unpacked_setup = struct.unpack(self.packing_format, setup_file.read())
            setup_file.close()
            return unpacked_setup
        except struct.error:
            messagebox.showerror("error", "can't open")

    def open_setup(self):
        root.filename = filedialog.askopenfilename(initialdir=INSTALL_PATH, title="Select setup file",
                                                   filetypes=(("bin files", "*.bin"), ("all files", "*.*")))
        self.load_setup_file(root.filename)
        widgets.status_message.set(" Opened (" + root.filename + ")")

    def load_setup_file(self, path):
        widgets.sliders = self.unpack_setup(path)
        if config.auto_use_track:
            self.use_setup()

    @staticmethod
    def check_dir(path):
        access_rights = 0o755
        if not os.path.isdir(path):
            try:
                os.makedirs(path, access_rights)
            except OSError:
                print("Creation of the directory %s failed" % path)


class Update:

    def populate_db_from_setups_dir(self):
        """previous version 1.62 and before used individual .bin files to save setups"""
        setup_dir = filedialog.askdirectory(initialdir=INSTALL_PATH, title="Select setup directory")
        """find files in dir, check if its already in db, load file from dir, write to db"""
        for league in list(widgets.raceSettings):
            path = setup_dir + "/" + league
            if os.path.isdir(path):
                for team in widgets.raceSettings[league]:
                    team_path = path + "/" + team
                    if os.path.isdir(team_path):
                        for weather in list(widgets.weatherTypes):
                            weather_path = team_path + "/" + weather
                            if os.path.isdir(weather_path):
                                for game_mode in widgets.game_modes:
                                    game_mode_path = weather_path + "/" + game_mode
                                    if os.path.isdir(game_mode_path):
                                        for country in tracks.tracks:
                                            file_path = game_mode_path + "/" + country + ".bin"
                                            if os.path.isfile(file_path):
                                                print(file_path)
                                                db = SqlDB()
                                                ids = db.get_ids(league,
                                                                 country,
                                                                 weather,
                                                                 game_mode,
                                                                 team)
                                                try:
                                                    setup_db = db.setups.get_setup_by_ids(*ids)
                                                    setup_id = setup_db[0][0]
                                                    print(setup_id, "is already in database")
                                                except IndexError:

                                                    widgets.sliders = setup.unpack_setup(file_path)
                                                    setup.load_setup_file(file_path)
                                                    car_setup = widgets.create_car_setup()
                                                    car_setup.league_id = ids[0]
                                                    car_setup.track_id = ids[1]
                                                    car_setup.weather_id = ids[2]
                                                    car_setup.game_mode_id = ids[3]
                                                    car_setup.team_id = ids[4]
                                                    print(car_setup.values)
                                                    db.save_setup_to_db(car_setup)
                                                    print("added to database")


def open_url(url):
    webbrowser.open_new(url)


def get_list(d):
    return [*d]


if __name__ == "__main__":
    json_data = Json()
    db = SqlDB()
    config = Config(root, INSTALL_PATH)
    tracks = Tracks(json_data, config.sort_tracks)
    setup = Setup()
    widgets = Widgets(config)

    config.use_theme()

    widgets.grid()
    event = Events(config)
    widgets.set_starting_values()
    widgets.tracks_background_color()
    widgets.toggle_race_sliders(widgets.race_box.get())

    event.show_track_selection()




root.mainloop()
