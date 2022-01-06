from jsondata import Json
from config import Config
from DB.local_sqlite3.track_sql import TrackSql


class Tracks:
    def __init__(self):
        json_data = Json()

        self.config = Config()
        self.tracks_sorted = json_data.tracks_sorted
        self.tracks_season = json_data.tracks_season
        self.tracks_id = json_data.tracks_id

        self.track_sorted_list = list(self.tracks)

    @property
    def track_id(self):
        print(self.config.current_track, TrackSql().get_track_id_by_country(self.config.current_track))
        return TrackSql().get_track_id_by_country(self.config.current_track)  # self.get_list(self.tracks_id).index(self.current_track)

    @property
    def tracks(self):
        if self.config.sort_tracks:
            return self.tracks_sorted
        else:
            return self.tracks_season

    def toggle_track_sort(self, sort_bool):
        if sort_bool:
            self.config.sort_tracks = True
        else:
            self.config.sort_tracks = False
        self.track_sorted_list = list(self.tracks)

    @staticmethod
    def get_list(d):
        return [*d]

    def set_current_track(self, currently_selected_track):
        if len(currently_selected_track) == 1:
            selection_id = int(currently_selected_track[0])
            print(self.track_sorted_list)
            self.config.current_track = self.track_sorted_list[selection_id]
            print("... set current selected track : " + str(self.config.current_track))


