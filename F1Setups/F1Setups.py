from pathlib import Path
from tkinter import Tk
from tkinter.ttk import Style

from F1Setups.helpers.carsetup import CarSetup
from F1Setups.widgets.widgets import Widgets
from F1Setups.config.config import Config
from F1Setups.DB.local_sqlite3.sqlite_create import sqlite_create
from F1Setups.data.jsondata import Json

INSTALL_PATH = Path(__file__).parent.absolute()
root = Tk()
root.title('F1 Setup editor')
root.iconbitmap(str(INSTALL_PATH) + '/pog.ico')
SetupDir = str(INSTALL_PATH) + "/Setups/"


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


config = Config()
if config.install_db:
    create_local_db()
    config.install_db = False
use_theme()
Widgets(root).set_starting_values()



root.mainloop()
