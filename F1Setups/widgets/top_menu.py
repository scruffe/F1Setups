from tkinter import Menu, BooleanVar
# from community import community
from F1Setups.config.config import Config


class TopMenu:
    """create menu bar"""

    def __init__(self, widgets, root):
        self.widgets = widgets

        menubar = Menu(root)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Use", command=self.widgets.use_cmd)
        file_menu.add_command(label="Save", command=self.widgets.save_cmd)
        file_menu.add_separator()
        file_menu.add_command(label="Import", command=self.widgets.open_cmd)
        file_menu.add_command(label="Export as...", command=self.widgets.save_as_cmd)
        file_menu.add_separator()
        file_menu.add_command(label="Open Community",  # command=community.Community,
                              state="disabled")
        file_menu.add_command(label="Upload to Community", command=self.widgets.upload,
                              state="disabled")
        file_menu.add_separator()

        file_menu.add_command(label="Exit", command=root.quit)

        menubar.add_cascade(label="File", menu=file_menu)

        community_menu = Menu(menubar, tearoff=0)

        community_menu.add_command(label="Open community",  # command=community.Community
                                   )
        community_menu.add_command(label="Upload to Community", command=self.widgets.upload)

        menubar.add_cascade(label="Community", menu=community_menu,
                            state="disabled")

        self.order_tracks = BooleanVar()
        self.auto_use_changes = BooleanVar()
        self.auto_save_changes = BooleanVar()
        self.auto_use_track = BooleanVar()

        self.settings_menu = Menu(menubar, tearoff=0)
        self.settings_menu.add_command(label="import previous setups",
                                       command=self.widgets.update.populate_db_from_setups_dir)
        self.settings_menu.add_separator()

        self.settings_menu.add_checkbutton(label='Order Tracks',
                                           variable=self.order_tracks,
                                           command=lambda: self.widgets.toggle_track_list_order(
                                               self.order_tracks.get()))
        self.settings_menu.add_checkbutton(label="Auto Use Changes",
                                           variable=self.auto_use_changes,
                                           command=lambda: self.update_auto_use(
                                               self.auto_use_changes.get()))
        self.settings_menu.add_checkbutton(label="Auto Save Changes",
                                           variable=self.auto_save_changes,
                                           command=lambda: self.update_auto_save(
                                               self.auto_save_changes.get()))
        self.settings_menu.add_checkbutton(label="Auto Use track",
                                           variable=self.auto_use_track,
                                           command=lambda: self.update_auto_use_track(
                                               self.auto_use_track.get()))

        menubar.add_cascade(label="Settings", menu=self.settings_menu)

        donate_menu = Menu(menubar, tearoff=0)
        donate_menu.add_command(label="Tip Scruffe", command=lambda: self.widgets.open_url("https://paypal.me/valar"))
        menubar.add_cascade(label="Donate", menu=donate_menu)

        root.config(menu=menubar)

    @staticmethod
    def update_auto_use(b: bool):
        Config().auto_use_changes = b

    @staticmethod
    def update_auto_save(b: bool):
        Config().auto_save_changes = b

    @staticmethod
    def update_auto_use_track(b: bool):
        Config().auto_use_track = b

    def set_starting_values(self):
        config = Config()
        if config.sort_tracks:
            self.settings_menu.invoke(2)
        if config.auto_use_changes:
            self.settings_menu.invoke(3)
        if config.auto_save_changes:
            self.settings_menu.invoke(4)
        if config.auto_use_track:
            self.settings_menu.invoke(5)
