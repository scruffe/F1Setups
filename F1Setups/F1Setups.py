from pathlib import Path
from tkinter import Tk
from tkinter.ttk import Style

from carsetup import CarSetup
from widgets.widgets import Widgets
from widgets.events import Events
from setup import Setup
from config import Config
from tracks import Tracks
from DB.local_sqlite3.sqlite_create import sqlite_create
from jsondata import Json


def get_list(d):
    return [*d]


def use_theme():
    root.tk.call('lappend', 'auto_path', str(INSTALL_PATH))
    root.tk.call('package', 'require', config.theme)
    # s.theme_names('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    Style().theme_use(config.theme)


def create_local_db():
    sqlite_create.make_league_and_teams(Json())
    sqlite_create.make_tracks(Json())
    sqlite_create.make_game_modes(Json())
    sqlite_create.make_weathers()
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


if __name__ == "__main__":



    INSTALL_PATH = Path(__file__).parent.absolute()
    root = Tk()
    root.title('F1 Setup editor')
    root.iconbitmap(str(INSTALL_PATH) + '/pog.ico')

    SetupDir = str(INSTALL_PATH) + "/Setups/"

    config = Config()

    if config.install_db:
        create_local_db()
        config.install_db = False

    tracks = Tracks()
    widgets = Widgets(root)
    setup = Setup(widgets)

    use_theme()

    event = Events(widgets)
    widgets.set_starting_values()
    widgets.tracks_background_color()
    widgets.toggle_race_sliders(widgets.race_box.get())

    event.show_track_selection()

    """"run this first time to populate db"""
    # server_postgres.create_table.create_tables()

    root.mainloop()




