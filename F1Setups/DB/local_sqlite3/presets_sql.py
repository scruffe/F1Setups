import sqlite3


class PresetSql:
    def __init__(self):
        self.conn = sqlite3.connect('DB/local_sqlite3/data.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS 
                presets (
                
                    setup_id    INTEGER PRIMARY KEY
                                NOT NULL,
                    league_id int,
                
                    save_name text,
                    team_id integer,
                    track_id integer,
                    game_mode_id integer,
                    weather_id integer,
                                    
                    front_wing integer,
                    rear_wing integer,
                    on_throttle integer,
                    off_throttle integer,
                    front_camber int,
                    rear_camber int,
                    front_toe int,
                    rear_toe int,
                    front_suspension int,
                    rear_suspension int,
                    front_suspension_height int,
                    rear_suspension_height int,
                    front_antiroll_bar int,
                    rear_antiroll_bar int,
                    brake_pressure int,
                    brake_bias int,
                    front_right_tyre_pressure int,
                    front_left_tyre_pressure int,
                    rear_right_tyre_pressure int,
                    rear_left_tyre_pressure int,
                    ballast int,
                    fuel_load int,
                    ramp_differential int
                    )""")
        self.conn.commit()

    def insert_carsetup(self, setup):
        with self.conn:
            self.c.execute("""INSERT INTO presets (
                        save_name,

                        front_wing,
                        rear_wing,
                        on_throttle,
                        off_throttle,
                        front_camber,
                        rear_camber,
                        front_toe,
                        rear_toe,
                        front_suspension,
                        rear_suspension,
                        front_suspension_height,
                        rear_suspension_height,
                        front_antiroll_bar,
                        rear_antiroll_bar,
                        brake_pressure,
                        brake_bias,
                        front_right_tyre_pressure,
                        front_left_tyre_pressure,
                        rear_right_tyre_pressure,
                        rear_left_tyre_pressure,
                        ballast,
                        fuel_load,
                        ramp_differential
                    )
                    VALUES (

                        :save_name,

                        :front_wing,
                        :rear_wing,
                        :on_throttle,
                        :off_throttle,
                        :front_camber,
                        :rear_camber,
                        :front_toe,
                        :rear_toe,
                        :front_suspension,
                        :rear_suspension,
                        :front_suspension_height,
                        :rear_suspension_height,
                        :front_antiroll_bar,
                        :rear_antiroll_bar,
                        :brake_pressure,
                        :brake_bias,
                        :front_right_tyre_pressure,
                        :front_left_tyre_pressure,
                        :rear_right_tyre_pressure,
                        :rear_left_tyre_pressure,
                        :ballast,
                        :fuel_load,
                        :ramp_differential)""",
                           {
                               'save_name': setup.save_name,

                               'front_wing': setup.front_wing,
                               'rear_wing': setup.rear_wing,
                               'on_throttle': setup.on_throttle,
                               'off_throttle': setup.off_throttle,
                               'front_camber': setup.front_camber,
                               'rear_camber': setup.rear_camber,
                               'front_toe': setup.front_toe,
                               'rear_toe': setup.rear_toe,
                               'front_suspension': setup.front_suspension,
                               'rear_suspension': setup.rear_suspension,
                               'front_suspension_height': setup.front_suspension_height,
                               'rear_suspension_height': setup.rear_suspension_height,
                               'front_antiroll_bar': setup.front_antiroll_bar,
                               'rear_antiroll_bar': setup.rear_antiroll_bar,
                               'brake_pressure': setup.brake_pressure,
                               'brake_bias': setup.brake_bias,
                               'front_right_tyre_pressure': setup.front_right_tyre_pressure,
                               'front_left_tyre_pressure': setup.front_left_tyre_pressure,
                               'rear_right_tyre_pressure': setup.rear_right_tyre_pressure,
                               'rear_left_tyre_pressure': setup.rear_left_tyre_pressure,
                               'ballast': setup.ballast,
                               'fuel_load': setup.fuel_load,
                               'ramp_differential': setup.ramp_differential})
            self.conn.commit()

    def get_preset_by_id(self, _id):
        self.c.execute("""SELECT * FROM presets WHERE setup_id = :id""",
                       {'id': _id})
        return self.c.fetchone()

    def get_preset_by_name(self, save_name):
        self.c.execute("""SELECT * FROM presets WHERE save_name = :save_name""",
                       {'save_name': save_name})
        return self.c.fetchone()

    def delete_presets_data(self):
        with self.conn:
            self.c.execute("DELETE FROM presets;")
            self.conn.commit()
