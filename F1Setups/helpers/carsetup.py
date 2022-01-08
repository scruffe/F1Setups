class CarSetup:
    """ a car setup for the f1 series"""

    def __init__(self,
                 setup_id=0,
                 league_id=0,
                 save_name='',
                 team_id=0,
                 track_id=0,
                 game_mode_id=0,
                 weather_id=1,
                 front_wing=0,
                 rear_wing=0,
                 on_throttle=0,
                 off_throttle=0,
                 front_camber=0,
                 rear_camber=0,
                 front_toe=0,
                 rear_toe=0,
                 front_suspension=0,
                 rear_suspension=0,
                 front_suspension_height=0,
                 rear_suspension_height=0,
                 front_antiroll_bar=0,
                 rear_antiroll_bar=0,
                 brake_pressure=0,
                 brake_bias=0,
                 front_right_tyre_pressure=0,
                 front_left_tyre_pressure=0,
                 rear_right_tyre_pressure=0,
                 rear_left_tyre_pressure=0,
                 ballast=0,
                 fuel_load=0,
                 ramp_differential=0):
        self.setup_id = setup_id
        self.league_id = league_id

        self.save_name = save_name
        self.team_id = team_id
        self.track_id = track_id
        self.game_mode_id = game_mode_id
        self.weather_id = weather_id

        self.front_wing = front_wing
        self.rear_wing = rear_wing
        self.on_throttle = on_throttle
        self.off_throttle = off_throttle
        self.front_camber = front_camber
        self.rear_camber = rear_camber
        self.front_toe = front_toe
        self.rear_toe = rear_toe
        self.front_suspension = front_suspension
        self.rear_suspension = rear_suspension
        self.front_suspension_height = front_suspension_height
        self.rear_suspension_height = rear_suspension_height
        self.front_antiroll_bar = front_antiroll_bar
        self.rear_antiroll_bar = rear_antiroll_bar
        self.brake_pressure = brake_pressure
        self.brake_bias = brake_bias
        self.front_right_tyre_pressure = front_right_tyre_pressure
        self.front_left_tyre_pressure = front_left_tyre_pressure
        self.rear_right_tyre_pressure = rear_right_tyre_pressure
        self.rear_left_tyre_pressure = rear_left_tyre_pressure
        self.ballast = ballast
        self.fuel_load = fuel_load
        self.ramp_differential = ramp_differential

    @property
    def info(self):
        return[
            self.setup_id,
            self.league_id,
            self.track_id,
            self.weather_id,
            self.game_mode_id,
            self.team_id,
            self.save_name
        ]

    @property
    def values(self):
        return (
            self.front_wing,
            self.rear_wing,
            self.on_throttle,
            self.off_throttle,
            self.front_camber,
            self.rear_camber,
            self.front_toe,
            self.rear_toe,
            self.front_suspension,
            self.rear_suspension,
            self.front_suspension_height,
            self.rear_suspension_height,
            self.front_antiroll_bar,
            self.rear_antiroll_bar,
            self.brake_pressure,
            self.brake_bias,
            self.front_right_tyre_pressure,
            self.front_left_tyre_pressure,
            self.rear_right_tyre_pressure,
            self.rear_left_tyre_pressure,
            self.ballast,
            self.fuel_load,
            self.ramp_differential
        )

    @property
    def setup(self):
        return (
            self.setup_id,
            self.league_id,
            self.save_name,
            self.team_id,
            self.track_id,
            self.game_mode_id,
            self.weather_id,
            self.front_wing,
            self.rear_wing,
            self.on_throttle,
            self.off_throttle,
            self.front_camber,
            self.rear_camber,
            self.front_toe,
            self.rear_toe,
            self.front_suspension,
            self.rear_suspension,
            self.front_suspension_height,
            self.rear_suspension_height,
            self.front_antiroll_bar,
            self.rear_antiroll_bar,
            self.brake_pressure,
            self.brake_bias,
            self.front_right_tyre_pressure,
            self.front_left_tyre_pressure,
            self.rear_right_tyre_pressure,
            self.rear_left_tyre_pressure,
            self.ballast,
            self.fuel_load,
            self.ramp_differential)

    def __repr__(self):
        return "reply: Car Setup info(id: '{}', name: '{}', track id:'{}',  weather:{})".format(
            self.setup_id, self.save_name, self.track_id, self.weather_id)
