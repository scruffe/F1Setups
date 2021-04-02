# from tkinter import *
import json
import os
import pathlib
import re
import struct
import webbrowser
import winreg
from tkinter import Tk, HORIZONTAL, messagebox, filedialog, DoubleVar, \
    IntVar, StringVar, BooleanVar, N, W, E, S, Listbox
from tkinter import ttk
from tkinter.ttk import Combobox

F1SetupPath = pathlib.Path(__file__).parent.absolute()
root = Tk()
root.title('F1 Setup editor')
root.iconbitmap(str(F1SetupPath) + '/pog.ico')

with open('config.json') as json_file:
    config = json.load(json_file)
json_file.close()

with open('tracks.json', encoding='utf-8') as json_file:
    tracks = json.load(json_file)
json_file.close()

theme = config['theme']
s = ttk.Style()  # s.theme_names('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
root.tk.call('lappend', 'auto_path', str(F1SetupPath))
root.tk.call('package', 'require', 'awdark')
s.theme_use(theme)

SetupDir = str(F1SetupPath) + "/Setups/"

setupStructPackingFormat = '<4s5l1b 11sfb 13sb 20sb 11s3b 12s2b 16s5b 16s2b 13s9b 19s2b ' \
                           '14sfb 13sfb 15sfb 16sfb 16sfb 15sfb 13sfb 12sfb 20sfb 19sfb ' \
                           '27sfb 26sfb 22sfb 21sfb 18sfb 14sfb 29sfb 28sfb 28sfb 27sfb 11sfb 13sfb 21sfb 21s8B '

tipURL = "https://paypal.me/valar"

f1_2020_steamID = "1080110"
scruffe_f1_workshop_id = "2403338074"  # f2 2404403390        2404433709
scruffe_f2_workshop_id = "2404403390"
scruffe_classic_workshop_id = "2404433709"
scruffe_WorkshopUrl = "https://steamcommunity.com/sharedfiles/filedetails/?id=" + scruffe_f1_workshop_id

bg = "#33393b"  # backgroundcolor
fg = "white"  # forgroundcolor

countrynames = list(tracks)

cnames = StringVar(value=countrynames)

raceSettings = {'F1 2020': ["All Cars",
                            "Ferrari",
                            "Renault",
                            "Red Bull",
                            "McLaren",
                            "Mercedes",
                            "AlphaTauri",
                            "Williams",
                            "Racing Point",
                            "Alfa Romeo",
                            "Haas"],
                'F2 2020': ["All Cars",
                            "Dams",
                            "Uni-Virtuosi Racing",
                            "ART Grand Prix",
                            "Carlin",
                            "Campos Vexatec Racing",
                            "Charouz Racing System",
                            "MP Motorsport",
                            "BWT HWA Racelab",
                            "Pertamina",  #
                            "Trident",
                            "Hitech Grand Prix"],  #
                'F2 2019': ["All Cars",
                            "Dams '19",
                            "Uni-Virtuosi ‘19",
                            "Art GP ’19",
                            "Carlin ’19",
                            "Campos ’19",
                            "Sauber Junior Charouz ’19",
                            "MP Motorsport ‘19",
                            "Arden ’19",
                            "Prema ’19",
                            "Trident ’19"],
                'classic': ["All Cars",
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

                            "McLaren 1990",

                            "McLaren 1976",
                            "Lotus 1972",
                            "Ferrari 1979",
                            "McLaren 1982",
                            "Williams 2003",
                            "Brawn 2009",

                            "Lotus 1978",

                            "Benetton 1994",
                            "Benetton 1995",
                            "Ferrari 2000",
                            "Jordan 1991",
                            ]
                }

weatherTypes = {'Dry': 'Dry setup', 'Wet': 'Wet setup', 'Mixed': 'Mixed setup'}

cars = ('All Cars', '')
preset_setups = {
    'Preset 1': 'Maximum Downforce',
    'Preset 2': 'Increased Downforce',
    'Preset 3': 'Balanced/Default',
    'Preset 4': 'Increased Topspeed',
    'Preset 5': 'Maximum Topspeed'}

game_modes = {
    "Weekly Event": 0,
    "Grand Prix": 3,  # 6
    "Time Trial": 5,
    "Multiplayer": 7,  # 8, 15
    "Invitational": 11,
    "Invitational Event": 12,
    "Career": 13,  # 17
    "Online Championship": 14
}

# weather = StringVar()
statusmsg = StringVar()
autoUseChanges = BooleanVar()
autoSaveChanges = BooleanVar()
autoUse = BooleanVar()


# precision limiter
# https://stackoverflow.com/questions/54186639/tkinter-control-ttk-scales-increment-as-with-tk-scale-and-a-tk-doublevar
class Limiter(ttk.Scale):
    """ ttk.Scale sublass that limits the precision of values. """

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
            return round(self.offset + m, self.res)

        return self.tk.call(self._w, 'get', x, y)

    def _value_changed(self, new_value):
        new_value = round(float(new_value), self.precision)
        if self.precision == 0:
            self.winfo_toplevel().globalsetvar(self.cget('variable'), (int(new_value)))
        else:
            self.winfo_toplevel().globalsetvar(self.cget('variable'), new_value)
        self.chain(new_value)  # Call user specified function.


class Track:
    def __init__(self):
        self.current_track = ""
        self.tracks_season = {
            "Australia": "Melbourne Grand Prix Circuit",
            "France": "Circuit Paul Ricard",
            "China": "Shanghai International Circuit",
            "Bahrain": "Bahrain International Circuit",
            "Spain": "Circuit de Barcelona-Catalunya",
            "Monaco": "Circuit de Monaco",
            "Canada": "Circuit Gilles-Villeneuve",
            "Britain": "Silverstone Circuit",
            "Hockenheim": "ITS NOT EVEN SHIPPED",
            "Hungary": "Hungaroring",
            "Belgium": "Circuit De Spa-Francorchamps",
            "Italy": "Autodromo Nazionale Monza",
            "Singapore": "Marina Bay Street Circuit",
            "Japan": "Suzuka International Racing Course",
            "Abu Dhabi": "Yas Marina Circuit",
            "USA": "Circuit of The Americas",
            "Brazil": "Autódromo José Carlos Pace",
            "Austria": "Spielberg",
            "Russia": "Sochi Autodrom",
            "México": "Autódromo Hermanos Rodríguez",
            "Azerbaijan": "Baku City Circuit",
            "Bahrain Short": "Bahrain International Circuit (Short)",
            "Britain Short": "Silverstone Circuit (Short)",
            "USA Short": "Circuit of The Americas (Short)",
            "Japan Short": "Suzuka International Racing Course (Short)",
            "Vietnam": "Hanoi Circuit",
            "The Netherlands": "Circuit Zandvoort"
        }

    def set_current_track(self):
        idxs = track_box.curselection()
        if len(idxs) == 1:
            idx = int(idxs[0])
            self.current_track = countrynames[idx]

    def get_current_track(self):
        return self.current_track

    def get_track_id(self):
        return get_list(self.tracks_season).index(self.current_track)


class SliderCounter:  # reads corresponding slider value in setup file and sets a slider to that value

    def __init__(self, setup):
        self.x = 41
        self.setup = setup

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
        product = round(p / scale.step, scale.res)
        scale.set(product)


track = Track()


def set_config(key, value):
    config[key] = value
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    json_file.close()


def set_steam_path():
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                              r"SOFTWARE\WOW6432Node\Valve\Steam")  # <PyHKEY:0x0000000000000094>
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
        steam_path = steam_path[0]
        winreg.CloseKey(hkey)
    except OSError:
        messagebox.showerror("error", "Can't find steam Install directory")
        steam_path = filedialog.askdirectory()  # manual entry
    set_config('steam_path', steam_path)


def get_steam_path():
    if not os.path.isdir(config['steam_path']):
        set_steam_path()
    return config['steam_path']


def set_workshop_dir():
    steam_path = get_steam_path()
    library_folders = steam_path + r"\steamapps\libraryfolders.vdf"
    with open(library_folders) as f:
        libraries = [steam_path]
        lf = f.read()
        libraries.extend([fn.replace("\\\\", "\\") for fn in
                          re.findall(r'^\s*"\d*"\s*"([^"]*)"', lf, re.MULTILINE)])
        for library in libraries:
            appmanifest = library + r"\steamapps\appmanifest_" + f1_2020_steamID + ".ACF"
            if os.path.isfile(appmanifest):
                with open(appmanifest) as ff:
                    ff.read()
                    workshop = library + "/steamapps/workshop/content/" + f1_2020_steamID
                    if os.path.isdir(workshop):
                        set_config('WorkshopFile', workshop)
                    else:
                        not_subscribed(scruffe_WorkshopUrl)
                ff.close()
    f.close()


def not_subscribed(url):
    messagebox.showerror("error",
                         "Not Subscribed to steam workshop, Subscribe to: " + url)
    open_url(url)


def get_workshop_dir(race):
    if not os.path.isdir(config['WorkshopFile']):
        set_workshop_dir()

    workshop_id = scruffe_f1_workshop_id

    if race == "classic":
        workshop_id = scruffe_classic_workshop_id
    elif race == "F2 2019" or race == "F2 2020":
        workshop_id = scruffe_f2_workshop_id
    f = config['WorkshopFile'] + "/" + workshop_id + "/ugcitemcontent.bin"
    if not os.path.isfile(f):
        url = "https://steamcommunity.com/sharedfiles/filedetails/?id=" + workshop_id
        not_subscribed(url)
    return f


def open_url(url):
    webbrowser.open_new(url)


def toggle_race_sliders():
    race = race_box.get()
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

    on_throttle_Scale.config(state=on_throttle)
    off_throttle_Scale.config(state=off_throttle)
    brake_pressure_Scale.config(state=brake_pressure)
    fuel_load_Scale.config(state=fuel_load)
    ballast_Scale.config(state=ballast)
    ramp_differential_Scale.config(state=ramp_differential)


def set_sliders(setup):
    instance = SliderCounter(setup)

    sliders = [
        front_wing_Scale,
        rear_wing_Scale,
        on_throttle_Scale,
        off_throttle_Scale,

        front_camber_Scale,
        rear_camber_Scale,
        front_toe_Scale,
        rear_toe_Scale,

        front_suspension_Scale,
        rear_suspension_Scale,
        front_suspension_height_Scale,
        rear_suspension_height_Scale,
        front_antiroll_bar_Scale,
        rear_antiroll_bar_Scale,
        brake_pressure_Scale,
        brake_bias_Scale,

        front_right_tyre_pressure_Scale,
        front_left_tyre_pressure_Scale,
        rear_right_tyre_pressure_Scale,
        rear_left_tyre_pressure_Scale,

        ballast_Scale,
        fuel_load_Scale,
        ramp_differential_Scale
    ]

    for slider in sliders:
        instance.set_slider_value(slider)


def get_list(d):
    return [*d]


def get_game_mode_id():
    if game_mode_box.get() == "Game mode":
        return 8
    return get_list(game_modes).index(game_mode_box.get())


def get_weather_id():
    if weather_box.get() == "Wet":
        return 0
    return 1


def get_team_id():
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

    team = cars_box.get()
    if team == "All Cars":
        return 41  # multiplayer car
    return team_ids.index(team)


def pack_setup():
    # ui08  |Unsigned 8-bit integer
    # i08   |Signed 8-bit integer
    # fp32   |Floating point (32-bit)

    # game mode id
    # all vars have a check value at the end, i have no idea what they do. Remove them and the game crashes. ¯\_(ツ)_/¯
    setup = struct.pack(setupStructPackingFormat,
                        b'F1CS', 0, 1, 0, 32, 0, 7,
                        # \x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x07
                        b'versionsi32', 0, 9,  # \x00\x00\x00\x00\t
                        b'save_names128', 20,  # \x14      probably string length of next name
                        b'All setups | scruffe', 7,  # \x07
                        b'team_idui16', get_team_id(), 0, 8,  # \x00\x00\x08
                        b'track_idui08', track.get_track_id(), 12,  # \x03\x0c
                        b'game_mode_idsi32', get_game_mode_id(), 0, 0, 0, 12,  # \x05\x00\x00\x00 \x0c
                        b'weather_typebool', get_weather_id(), 9,  # \x01\t
                        b'timestampui64', 19, 14, 5, 95, 0, 0, 0, 0, 15,  # \x13\x0e\x05_\x00\x00\x00\x00\x0f
                        b'game_setup_modeui08', 0, 10,  # \x00\n
                        b'front_wingfp32', front_wing_Scale.get(), 9,
                        b'rear_wingfp32', rear_wing_Scale.get(), 11,
                        b'on_throttlefp32', on_throttle_Scale.get(), 12,
                        b'off_throttlefp32', off_throttle_Scale.get(), 12,
                        b'front_camberfp32', front_camber_Scale.get(), 11,
                        b'rear_camberfp32', rear_camber_Scale.get(), 9,
                        b'front_toefp32', front_toe_Scale.get(), 8,
                        b'rear_toefp32', rear_toe_Scale.get(), 16,
                        b'front_suspensionfp32', front_suspension_Scale.get(), 15,
                        b'rear_suspensionfp32', rear_suspension_Scale.get(), 23,
                        b'front_suspension_heightfp32', front_suspension_height_Scale.get(), 22,
                        b'rear_suspension_heightfp32', rear_suspension_height_Scale.get(), 18,
                        b'front_antiroll_barfp32', front_antiroll_bar_Scale.get(), 17,
                        b'rear_antiroll_barfp32', rear_antiroll_bar_Scale.get(), 14,
                        b'brake_pressurefp32', brake_pressure_Scale.get(), 10,
                        b'brake_biasfp32', brake_bias_Scale.get(), 25,
                        b'front_right_tyre_pressurefp32', front_right_tyre_pressure_Scale.get(), 24,
                        b'front_left_tyre_pressurefp32', front_left_tyre_pressure_Scale.get(), 24,
                        b'rear_right_tyre_pressurefp32', rear_right_tyre_pressure_Scale.get(), 23,
                        b'rear_left_tyre_pressurefp32', rear_left_tyre_pressure_Scale.get(), 7,
                        b'ballastfp32', ballast_Scale.get(), 9,
                        b'fuel_loadfp32', fuel_load_Scale.get(), 17,
                        b'ramp_differentialfp32', ramp_differential_Scale.get(), 17,
                        b'published_file_idui64', 31, 174, 162, 128, 0, 0, 0, 0
                        # b'published_file_idui64\x1f\xae\xa2\x80\x00\x00\x00\x00'
                        )
    return setup


def write_setup(filename):
    setup = pack_setup()
    with open(filename, 'wb') as file:
        file.write(setup)
    file.close()


def use_setup():
    race = race_box.get()
    workshop_file = get_workshop_dir(race)
    write_setup(workshop_file)
    statusmsg.set("Using current setup")


def save_setup():
    write_setup(root.filename)
    statusmsg.set("Saved as: " + root.filename)


def use_save_setup():
    use_setup()
    save_setup()


def save_as_setup():
    asked_filename = filedialog.asksaveasfilename(initialdir=F1SetupPath, title="Select file",
                                                  filetypes=(("bin files", "*.bin"), ("all files", "*.*")))
    write_setup(asked_filename)
    statusmsg.set("Saved: " + asked_filename)


def open_setup():
    try:
        root.filename = filedialog.askopenfilename(initialdir=F1SetupPath, title="Select file",
                                                   filetypes=(("bin files", "*.bin"), ("all files", "*.*")))
        setup_file = open(root.filename, "rb")
        setup = struct.unpack(setupStructPackingFormat, setup_file.read())
        statusmsg.set(" Opened (" + root.filename + ")")
        set_sliders(setup)
    except OSError:
        messagebox.showerror("error", "can't open")


def load_setup_file(path):
    f = open(path, "rb")
    setup = struct.unpack(setupStructPackingFormat, f.read())
    f.close()
    set_sliders(setup)
    if autoUse.get():
        use_setup()


def make_dir(path):
    access_rights = 0o755
    if not os.path.isdir(path):
        try:
            os.makedirs(path, access_rights)
        except OSError:
            print("Creation of the directory %s failed" % path)


def make_file():
    race = race_box.get()
    car = cars_box.get()
    weather = weather_box.get()
    game_mode = game_mode_box.get()
    track_name = track.get_current_track()
    default_setups = config['defaultsetups']

    make_dir(SetupDir + race + '/' + car + '/' + weather + '/' + game_mode + '/')
    if default_setups == "Preset":
        preset_file = SetupDir + "Presets/Preset 3.bin"
    else:
        f = SetupDir + race + '/' + default_setups + '/' + weather + '/' + game_mode + '/' + track_name + ".bin"
        if os.path.isfile(f):
            preset_file = f
        elif os.path.isfile(SetupDir + race + '/' + default_setups + '/' + weather + '/Multiplayer/' + track_name + ".bin"):
            preset_file = SetupDir + race + '/' + default_setups + '/' + weather + '/Multiplayer/' + track_name + ".bin"
        elif os.path.isfile(SetupDir + race + '/' + default_setups + '/Dry/Multiplayer/' + track_name + ".bin"):
            preset_file = SetupDir + race + '/' + default_setups + '/Dry/Multiplayer/' + track_name + ".bin"
        elif os.path.isfile(SetupDir + 'F1 2020/' + default_setups + '/Dry/Multiplayer/' + track_name + ".bin"):
            preset_file = SetupDir + 'F1 2020/' + default_setups + '/Dry/Multiplayer/' + track_name + ".bin"
        else:
            preset_file = SetupDir + "Presets/Preset 3.bin"

    load_setup_file(preset_file)
    write_setup(root.filename)


# select the file to open, unpack the file, update sliders, if autoUse is checked;  write to workshopfile
def select_track(country):
    race = race_box.get()
    car = cars_box.get()
    weather = weather_box.get()
    game_mode = game_mode_box.get()
    root.filename = SetupDir + race + '/' + car + '/' + weather + '/' + game_mode + '/' + country + ".bin"

    if not os.path.isfile(root.filename):
        make_file()

    load_setup_file(root.filename)
    statusmsg.set(" %s | %s | (%s) %s [%s]" % (race, car, country, tracks[country], weatherTypes[weather]))


def highlight_track():  # keep the trackname highlighted when you lose focus
    track_box.selection_set(get_list(tracks).index(track.get_current_track()))


# Create and grid the outer content frame
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N, W, E, S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

sliderFrame = ttk.LabelFrame(
    c,
    text="Setup",
    labelanchor='nw',
    padding=5
)
sliderFrame.grid(
    row=0,
    rowspan=15,
    column=2,
    columnspan=5)

# create widgets
track_box = Listbox(
    c,
    listvariable=cnames,
    height=len(countrynames),
    bg=bg,
    fg=fg,
    highlightcolor="black",
    selectbackground="darkred",
    selectforeground="white")
track_box.selection_clear(1, last=None)
race_box = Combobox(
    c,
    justify="center",
    values=list(raceSettings),
    state='readonly')  # state= 'readonly' , 'disabled'
cars_box = Combobox(
    c,
    justify="center",
    values=cars,
    state='readonly')
weather_box = Combobox(
    c,
    justify="center",
    values=list(weatherTypes),
    state='readonly')

preset_box = Combobox(
    c,
    justify="center",
    values=list(preset_setups.values()),
    state='readonly')
game_mode_box = Combobox(
    c,
    justify="center",
    values=list(game_modes),
    state='readonly')

status_bar = ttk.Label(
    c,
    textvariable=statusmsg,
    anchor=W)

autoUseChangesBox = ttk.Checkbutton(
    c,
    text='Auto Use Changes',
    variable=autoUseChanges,
    onvalue=True,
    offvalue=False,
    command=lambda: set_config('autoUseChanges', autoUseChanges.get()))
autoSaveChangesBox = ttk.Checkbutton(
    c,
    text='Auto Save Changes',
    variable=autoSaveChanges,
    onvalue=True,
    offvalue=False,
    command=lambda: set_config('autoSaveChanges', autoSaveChanges.get()))
autoUseTrackBox = ttk.Checkbutton(
    c,
    text='Auto Use track',
    variable=autoUse,
    onvalue=True,
    offvalue=False,
    command=lambda: set_config('autoUseButton', autoUse.get()))

useButton = ttk.Button(
    c,
    text="Use",
    command=use_setup
)
useSaveButton = ttk.Button(
    c,
    text="Save & Use",
    command=use_save_setup
)
saveButton = ttk.Button(
    c,
    text="Save",
    command=save_setup
)
saveAsButton = ttk.Button(
    c,
    text="Save As",
    command=save_as_setup
)
openButton = ttk.Button(
    c,
    text="Open",
    command=open_setup
)

# create tipURL widget
tipBtn = ttk.Button(
    c,
    text="Tip Scruffe",
    command=lambda: open_url(tipURL)
)


class MakeScale:
    def __init__(self, step=0.0, offset=1.0, res=1):
        self.row_i = 1
        self.column = 2
        self.rowspan = 1
        self.sticky = 'NSEW'
        self.frame = sliderFrame
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
            sliderFrame,
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
            sliderFrame,
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


scales = MakeScale()
front_wing_Scale = scales.make("Front wing")
rear_wing_Scale = scales.make("Rear wing")

on_throttle_Scale = scales.make("On throttle", from_=50, to=100)
off_throttle_Scale = scales.make("Off throttle", from_=50, to=100)

front_camber_Scale = scales.make("Front camber", step=0.1, offset=-3.5)
rear_camber_Scale = scales.make("Rear camber", step=0.1, offset=-2)
front_toe_Scale = scales.make("Front toe", step=0.01, offset=0.05, res=2)
rear_toe_Scale = scales.make("Rear toe", step=0.03, offset=0.20, res=2)  # there is an offset

front_suspension_Scale = scales.make("Front suspension")
rear_suspension_Scale = scales.make("Rear suspension")
front_antiroll_bar_Scale = scales.make("Front antiroll bar")
rear_antiroll_bar_Scale = scales.make("Rear antiroll bar")

front_suspension_height_Scale = scales.make("Front suspension height")
rear_suspension_height_Scale = scales.make("Rear suspension height")
brake_pressure_Scale = scales.make("Brake pressure", from_=50, to=100)
brake_bias_Scale = scales.make("Brake bias", from_=70, to=50)
front_right_tyre_pressure_Scale = scales.make("Front right tyre pressure", step=.4, offset=21)  # , 0.4)
front_left_tyre_pressure_Scale = scales.make("Front left tyre pressure", step=.4, offset=21)
rear_right_tyre_pressure_Scale = scales.make("Rear right tyre pressure", step=.4, offset=19.5)
rear_left_tyre_pressure_Scale = scales.make("Rear left tyre pressure", step=.4, offset=19.5)

ballast_Scale = scales.make("Ballast")
ramp_differential_Scale = scales.make("Ramp differential", from_=50, to=70)
fuel_load_Scale = scales.make("Fuel load", from_=5, to=110)


class GridWidgets:
    def __init__(self, startrow=0, increment_horizontal=False, sticky=(E, W), padx=0):
        self.row = startrow
        self.column = 0
        self.increment_horizontal = increment_horizontal
        self.sticky = sticky
        self.padx = padx

    def grid_box(self, box, rowspan=1, columnspan=1):
        box.grid(
            column=self.column,
            row=self.row,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=self.sticky,
            padx=self.padx
        )
        if self.increment_horizontal:
            self.column += columnspan
        else:
            self.row += rowspan

    def get_row(self):
        return self.row


instance = GridWidgets()

instance.grid_box(track_box, rowspan=3)
instance.grid_box(race_box)
instance.grid_box(cars_box)
instance.grid_box(weather_box)
instance.grid_box(game_mode_box)
instance.grid_box(preset_box)

check_box = GridWidgets(startrow=12, padx=10)
check_box.grid_box(autoUseChangesBox)
check_box.grid_box(autoSaveChangesBox)
check_box.grid_box(autoUseTrackBox)

buttons = GridWidgets(startrow=check_box.get_row(), increment_horizontal=True)
buttons.grid_box(useButton, columnspan=2)
buttons.grid_box(saveButton)
buttons.grid_box(saveAsButton)
buttons.grid_box(openButton)
buttons.grid_box(tipBtn, columnspan=2)

status = GridWidgets(startrow=(buttons.get_row() + 1))
status.grid_box(status_bar, columnspan=7)

c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(11, weight=1)


def tracks_background_color():
    for i in range(0, len(countrynames), 2):
        track_box.itemconfigure(i, background='#576366', fg=fg)


# Called when the selection in the listbox changes; figure out
# which country is currently selected, and then lookup its country
# code, and from that, its population.  Update the status message
# with the new population.  As well, clear the message about the
# weather being sent, so it doesn't stick around after we start doing
# other things.

def show_track_selection(*args):
    track.set_current_track()
    select_track(track.get_current_track())


def race_box_event(*args):
    race = race_box.get()
    toggle_race_sliders()
    set_config("race_box", race)
    cars_box['values'] = raceSettings[race]
    cars_box.current(0)
    box_event()


def box_event(*args):
    set_config("weather_box", weather_box.get())
    set_config("game_mode_box", game_mode_box.get())
    set_config("cars_box", cars_box.get())
    track_list = get_list(tracks)
    track_box.selection_set(track_list.index(track.get_current_track()))


def slider_event(*args):
    auto_use_changes = config['autoUseChanges']
    auto_save_changes = config['autoSaveChanges']
    if auto_use_changes and auto_save_changes:
        use_save_setup()
        return
    if auto_use_changes:
        use_setup()
    if auto_save_changes:
        save_setup()


def preset_box_event(*args):
    nr = str(preset_box.current() + 1)
    path = SetupDir + "Presets/Preset " + nr + ".bin"
    load_setup_file(path)

    statusmsg.set(" Loaded (" + preset_box.get() + ")")
    preset_box.set("Load Preset")


track_box.bind('<<ListboxSelect>>', show_track_selection)
race_box.bind("<<ComboboxSelected>>", race_box_event)
cars_box.bind("<<ComboboxSelected>>", box_event)
weather_box.bind("<<ComboboxSelected>>", box_event)
preset_box.bind("<<ComboboxSelected>>", preset_box_event)
game_mode_box.bind("<<ComboboxSelected>>", box_event)

front_wing_Scale.bind("<ButtonRelease-1>", slider_event)
rear_wing_Scale.bind("<ButtonRelease-1>", slider_event)
on_throttle_Scale.bind("<ButtonRelease-1>", slider_event)
off_throttle_Scale.bind("<ButtonRelease-1>", slider_event)
front_camber_Scale.bind("<ButtonRelease-1>", slider_event)
rear_camber_Scale.bind("<ButtonRelease-1>", slider_event)
front_toe_Scale.bind("<ButtonRelease-1>", slider_event)
rear_toe_Scale.bind("<ButtonRelease-1>", slider_event)
front_suspension_Scale.bind("<ButtonRelease-1>", slider_event)
rear_suspension_Scale.bind("<ButtonRelease-1>", slider_event)
front_antiroll_bar_Scale.bind("<ButtonRelease-1>", slider_event)
rear_antiroll_bar_Scale.bind("<ButtonRelease-1>", slider_event)

front_suspension_height_Scale.bind("<ButtonRelease-1>", slider_event)
rear_suspension_height_Scale.bind("<ButtonRelease-1>", slider_event)
brake_pressure_Scale.bind("<ButtonRelease-1>", slider_event)
brake_bias_Scale.bind("<ButtonRelease-1>", slider_event)
front_right_tyre_pressure_Scale.bind("<ButtonRelease-1>", slider_event)
front_left_tyre_pressure_Scale.bind("<ButtonRelease-1>", slider_event)
rear_right_tyre_pressure_Scale.bind("<ButtonRelease-1>", slider_event)
rear_left_tyre_pressure_Scale.bind("<ButtonRelease-1>", slider_event)
ballast_Scale.bind("<ButtonRelease-1>", slider_event)
fuel_load_Scale.bind("<ButtonRelease-1>", slider_event)
ramp_differential_Scale.bind("<ButtonRelease-1>", slider_event)

# Set the starting state of the interface, including selecting the
# default weather to send, and clearing the messages.  Select the first
# country in the list; because the <<ListboxSelect>> events are only
# fired when users makes a change, we explicitly call showTrackselection.
# weather.set('Dry')
statusmsg.set('')
track_box.selection_set(0)

if config['autoUseChanges']:
    autoUseChangesBox.invoke()
if config['autoSaveChanges']:
    autoSaveChangesBox.invoke()
if config['autoUseButton']:
    autoUseTrackBox.invoke()

race_box.set(config['race_box'])
cars_box['values'] = raceSettings[race_box.get()]

cars_box.set(config['cars_box'])
weather_box.set(config['weather_box'])
game_mode_box.set(config['game_mode_box'])
preset_box.set("Load Preset")


if __name__ == "__main__":
    tracks_background_color()
    # create sliders
    toggle_race_sliders()

    # Load track
    show_track_selection()

root.mainloop()
