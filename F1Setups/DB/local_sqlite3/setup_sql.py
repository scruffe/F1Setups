import sqlite3


class SetupSql:
    def __init__(self):
        self.conn = sqlite3.connect('DB/local_sqlite3/data.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS 
                setups (
                    setup_id    INTEGER PRIMARY KEY ASC AUTOINCREMENT
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
                    ramp_differential int,
                    
                    FOREIGN KEY (league_id)
                       REFERENCES leagues (league_id),
                    FOREIGN KEY (team_id)
                       REFERENCES teams (team_id),
                    FOREIGN KEY (track_id)
                       REFERENCES tracks (track_id), 
                    FOREIGN KEY (game_mode_id)
                       REFERENCES game_modes (game_mode_id) 
                    )""")
        self.conn.commit()

    def insert_setup(self, setup):
        with self.conn:
            self.c.execute("""INSERT INTO setups (
                        league_id,
                        
                        save_name,
                        team_id,
                        track_id,
                        game_mode_id,
                        weather_id,

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
                        :league_id,
                        
                        :save_name,
                        :team_id,
                        :track_id,
                        :game_mode_id,
                        :weather_id,

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

                               'league_id': setup.league_id,

                               'save_name': setup.save_name,
                               'team_id': setup.team_id,
                               'track_id': setup.track_id,
                               'game_mode_id': setup.game_mode_id,
                               'weather_id': setup.weather_id,

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

    def update_setup_values_on_setup_id(self, setup):
        with self.conn:
            self.c.execute("""
                        UPDATE setups 
                        SET     
                            save_name                 = :save_name,
                                       
                            front_wing                = :front_wing,               
                            rear_wing                 = :rear_wing,                
                            on_throttle               = :on_throttle,              
                            off_throttle              = :off_throttle,             
                            front_camber              = :front_camber,             
                            rear_camber               = :rear_camber,              
                            front_toe                 = :front_toe,                
                            rear_toe                  = :rear_toe,                 
                            front_suspension          = :front_suspension,         
                            rear_suspension           = :rear_suspension,          
                            front_suspension_height   = :front_suspension_height,  
                            rear_suspension_height    = :rear_suspension_height,   
                            front_antiroll_bar        = :front_antiroll_bar,       
                            rear_antiroll_bar         = :rear_antiroll_bar,        
                            brake_pressure            = :brake_pressure,           
                            brake_bias                = :brake_bias,               
                            front_right_tyre_pressure = :front_right_tyre_pressure,
                            front_left_tyre_pressure  = :front_left_tyre_pressure, 
                            rear_right_tyre_pressure  = :rear_right_tyre_pressure, 
                            rear_left_tyre_pressure   = :rear_left_tyre_pressure,  
                            ballast                   = :ballast,                  
                            fuel_load                 = :fuel_load,                
                            ramp_differential         = :ramp_differential 
                        WHERE
                            setups.setup_id=:setup_id """,
                           {
                               'setup_id': setup.setup_id,

                               'save_name': setup.save_name,
                               'team_id': setup.team_id,
                               'track_id': setup.track_id,
                               'game_mode_id': setup.game_mode_id,
                               'weather_id': setup.weather_id,

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

    def get_setups(self):
        self.c.execute("""SELECT * FROM setups 
                    """)
        return self.c.fetchall()

    def get_setup_by_setup_id(self, setup_id):
        self.c.execute("""SELECT * FROM setups WHERE setup_id = :id""",
                       {'id': setup_id})
        return self.c.fetchone()

    def get_setup_by_ids(self, league_id, track_id, weather_id=1, game_mode_id=7, team_id=0):
        self.c.execute("""
                SELECT 
                    setup_id,
                    track_country,
                    track_name,
                    league_name,
                    weather_name,
                    game_mode_name
                FROM setups
                LEFT JOIN tracks
                    ON setups.track_id = tracks.track_id
                LEFT JOIN leagues
                    ON setups.league_id = leagues.league_id
                LEFT JOIN weathers
                    ON setups.weather_id = weathers.weather_id
                LEFT JOIN game_modes
                    ON setups.game_mode_id = game_modes.game_mode_id
                WHERE
                    setups.league_id=:league AND
                    setups.track_id=:track AND
                    setups.weather_id=:weather AND
                    setups.game_mode_id=:game_mode AND
                    setups.team_id=:team;
                """, {
            'league': league_id,
            'track': track_id,
            'weather': weather_id,
            'game_mode': game_mode_id,
            'team': team_id
        })
        return self.c.fetchall()

    def delete_setups_data(self):
        with self.conn:
            self.c.execute("DELETE FROM setups;")
            self.conn.commit()
