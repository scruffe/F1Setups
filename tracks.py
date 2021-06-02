class Tracks:
    def __init__(self, json_data, sort_tracks=True):

        self.current_track = "Australia"
        self.tracks_sorted = json_data.tracks_sorted
        self.tracks_season = json_data.tracks_season
        self.tracks_id = json_data.tracks_id

        self.sort_tracks = sort_tracks
        self.track_sorted_list = list(self.tracks)

    @property
    def track_id(self):
        return self.get_list(self.tracks_id).index(self.current_track)

    @property
    def tracks(self):
        if self.sort_tracks:
            return self.tracks_sorted
        else:
            return self.tracks_season

    @staticmethod
    def get_list(d):
        return [*d]

    def set_current_track(self, currently_selected_track):
        if len(currently_selected_track) == 1:
            idx = int(currently_selected_track[0])
            self.current_track = self.track_sorted_list[idx]

    def toggle_track_sort(self, sort_bool):
        if sort_bool:
            self.sort_tracks = True
        else:
            self.sort_tracks = False
        self.track_sorted_list = list(self.tracks)
