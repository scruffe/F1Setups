import os
import struct
from tkinter import filedialog, messagebox
from DB.local_sqlite3.local_sqlite3 import LocalSqlite3
import pathlib
from tracks import Tracks
from config import Config

INSTALL_PATH = pathlib.Path(__file__).parent.absolute()


class Setup:
    def __init__(self, widgets):
        # self.max_length_save_name = 128
        self.tracks = Tracks()
        self.widgets = widgets
        self.config = Config()
        self.db = LocalSqlite3()

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
        """all information in the setup is static except for the length of the save name"""
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
            b(self.team_id), self.widgets.team_id, 0, 8,  # \x00\x00\x08
            b(self.track_id), self.tracks.track_id, 12,  # \x03\x0c
            b(self.game_mode_id), self.widgets.game_mode_id, 0, 0, 0, 12,
            # \x05\x00\x00\x00 \x0c
            b(self.weather_bool), self.widgets.weather_id, 9,  # \x01\t
            b(self.timestamp), 19, 14, 5, 95, 0, 0, 0, 0, 15,  # \x13\x0e\x05_\x00\x00\x00\x00\x0f
            b(self.game_setup_mode), 0, 10,  # \x00\n
            b(self.fw), self.widgets.front_wing_Scale.get(), 9,
            b(self.rw), self.widgets.rear_wing_Scale.get(), 11,
            b(self.ot), self.widgets.on_throttle_Scale.get(), 12,
            b(self.oft), self.widgets.off_throttle_Scale.get(), 12,
            b(self.fc), self.widgets.front_camber_Scale.get(), 11,
            b(self.rc), self.widgets.rear_camber_Scale.get(), 9,
            b(self.ft), self.widgets.front_toe_Scale.get(), 8,
            b(self.rt), self.widgets.rear_toe_Scale.get(), 16,
            b(self.fs), self.widgets.front_suspension_Scale.get(), 15,
            b(self.rs), self.widgets.rear_suspension_Scale.get(), 23,
            b(self.fsh), self.widgets.front_suspension_height_Scale.get(), 22,
            b(self.rsh), self.widgets.rear_suspension_height_Scale.get(), 18,
            b(self.fab), self.widgets.front_antiroll_bar_Scale.get(), 17,
            b(self.rab), self.widgets.rear_antiroll_bar_Scale.get(), 14,
            b(self.bp), self.widgets.brake_pressure_Scale.get(), 10,
            b(self.bb), self.widgets.brake_bias_Scale.get(), 25,
            b(self.frtp), self.widgets.front_right_tyre_pressure_Scale.get(), 24,
            b(self.fltp), self.widgets.front_left_tyre_pressure_Scale.get(), 24,
            b(self.rrtp), self.widgets.rear_right_tyre_pressure_Scale.get(), 23,
            b(self.rltp), self.widgets.rear_left_tyre_pressure_Scale.get(), 7,
            b(self.b), self.widgets.ballast_Scale.get(), 9,
            b(self.fl), self.widgets.fuel_load_Scale.get(), 17,
            b(self.rd), self.widgets.ramp_differential_Scale.get(), 17,
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
        self.config.workshop_file = self.config.get_workshop_race_id(self.widgets.race_box.get())
        self.write_setup(self.config.workshop_file)
        self.widgets.status_message.set("Using current setup")

    def save_setup(self, car_setup):
        print(car_setup.setup_id, car_setup.team_id)
        self.db.save_setup_to_db(car_setup)


    def save_as_setup(self):
        path = filedialog.asksaveasfilename(initialdir=INSTALL_PATH, title="Select file",
                                                      defaultextension=".bin",
                                                      filetypes=(("bin files", "*.bin"), ("all files", "*.*")))
        self.write_setup(path)
        return path

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
        path = filedialog.askopenfilename(initialdir=INSTALL_PATH, title="Select setup file",
                                          filetypes=(("bin files", "*.bin"), ("all files", "*.*")))
        self.load_setup_file(path)
        return path

    def load_setup_file(self, path):
        self.widgets.sliders = self.unpack_setup(path)
        if self.config.auto_use_track:
            self.use_setup()

    @staticmethod
    def check_dir(path):
        access_rights = 0o755
        if not os.path.isdir(path):
            try:
                os.makedirs(path, access_rights)
            except OSError:
                print("Creation of the directory %s failed" % path)
