# from tkinter import *
import pathlib

from tkinter import Tk
from tkinter import ttk

from widgets import Widgets
from events import Events
from setup import Setup

from config import Config

from tracks import Tracks


def get_list(d):
    return [*d]


def use_theme():
    root.tk.call('lappend', 'auto_path', str(INSTALL_PATH))
    root.tk.call('package', 'require', config.theme)
    # s.theme_names('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    ttk.Style().theme_use(config.theme)


if __name__ == "__main__":
    INSTALL_PATH = pathlib.Path(__file__).parent.absolute()
    root = Tk()
    root.title('F1 Setup editor')
    root.iconbitmap(str(INSTALL_PATH) + '/pog.ico')

    SetupDir = str(INSTALL_PATH) + "/Setups/"

    config = Config()
    tracks = Tracks(config.sort_tracks)
    widgets = Widgets(root)
    setup = Setup(widgets)

    use_theme()

    event = Events(widgets)
    widgets.set_starting_values()
    widgets.tracks_background_color()
    widgets.toggle_race_sliders(widgets.race_box.get())

    event.show_track_selection()


    #server_postgres.create_table.create_tables()
    root.mainloop()




