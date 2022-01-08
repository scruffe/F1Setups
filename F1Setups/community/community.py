import tkinter
import tkinter.ttk

from .commands import *

from F1Setups.widgets.grid_widgets import GridWidgets
from F1Setups.DB.server_postgres import *
from F1Setups.DB.local_sqlite3 import *


class Community:
    def __init__(self):
        self.grid_widgets = GridWidgets()
        self.window = tkinter.Tk()
        self.window.title('Community')

        self.cmd = Commands()

        self.download_button = None
        self.search_button = None

        self.create_buttons()
        self.buttons = [self.search_button, self.download_button]

        self.track = None
        self.uploaded_by = None
        self.downloads = None
        self.date_uploaded = None

        self.treeview = None
        self.create_treeview()

        self.x = 0

        self.insert_treeview()
        self.grid()

    def create_buttons(self):
        self.search_button = tkinter.Button(
            self.window,
            text="Search",

            command=self.cmd.search)
        self.download_button = tkinter.Button(
            self.window,
            text="Download",
            command=self.download)

    def create_treeview(self):
        self.treeview = tkinter.ttk.Treeview(self.window)
        columns = ("Track", "Weather", "Team", "Description", 'Downloads', 'Uploaded by')
        self.treeview['columns'] = columns
        self.treeview.column('#0', width=0, stretch=tkinter.NO)
        self.treeview.heading('#0', text='', anchor=tkinter.CENTER)

        for col in columns:
            self._create_treeview(col)
            self.treeview.heading(col, text=col, command=lambda _col=col:
            self.treeview_sort_column(self.treeview, _col, False))

    def _create_treeview(self, name):
        self.treeview.column(name, anchor=tkinter.CENTER, width=80)
        self.treeview.heading(name, text=name, anchor=tkinter.CENTER)

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def grid(self):
        box1 = self.grid_widgets.GridWidgets(increment_horizontal=True)
        box1.grid_box(self.treeview)

        box2 = self.grid_widgets.GridWidgets(startrow=(box1.row + 1), increment_horizontal=True)
        for button in self.buttons:
            box2.grid_box(button, rowspan=3)

    def insert_treeview(self):
        for entry in server_postgres.ServerPostgres().get_setups():
            print("inserting: ", entry)
            _id = entry[0]
            description = entry[1]
            downloads = entry[2]
            user_id = entry[3]
            car_setup = entry[4]

            # Convert String to Tuple
            car_setup = eval(car_setup)

            league_id = car_setup[1]
            team_id = car_setup[3]
            track_id = car_setup[4]
            weather_id = car_setup[6]

            team = team_sql.TeamSql().get_team_name_from_ids(team_id, league_id)
            weather = weather_sql.WeatherSql().get_weather_name_from_id(weather_id)
            track = track_sql.TrackSql().get_track_country_by_id(track_id)
            self._insert_treeview(track[0], weather, team[0], description, downloads, user_id)

    def _insert_treeview(self, track, weather, team, description, downloads, uploaded_by):
        self.x += 1
        self.treeview.insert(parent='', index=self.x, iid=self.x, text='',
                             values=(track, weather, team, description, downloads, uploaded_by))

    def select_treeview(self):
        return self.treeview.selection()

    def download(self):
        for select in self.select_treeview():
            self.cmd.download(select)


if __name__ == "__main__":
    Community()
