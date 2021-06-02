import sqlite3

conn = sqlite3.connect('data.db')

c = conn.cursor()


def commit_conn():
    conn.commit()


def close_conn():
    conn.close()


def create_view():
    c.execute("""CREATE VIEW v_setups AS 
    SELECT
        setups.setup_id,
        setups.save_name,
        tracks.track_name AS track,
        leagues.league_name AS league,
        weathers.weather_name AS weather,
        game_modes.game_mode_name AS game_mode
        
    FROM
        setups
        left  JOIN tracks ON setups.track_id = tracks.track_id
        left  JOIN leagues ON setups.league_id = leagues.league_id
        left  JOIN weathers ON setups.weather_id = weathers.weather_id
        left  JOIN game_modes ON setups.game_mode_id = game_modes.game_mode_id
    """)


if __name__ == "__main__":
    c.execute("drop table setups")
    """
    setup_table = setup_sql.SetupSql()
    track_table = track_sql.TrackSql()
    print(setup_table.get_setup_by_strs('F1 2020', 'Canada', 'Dry'))
    car = CarSetup()
    car.save_name = 'my name'
    car.front_wing = 10
    car.track_id = track_table.get_track_id_by_country('Canada')
    if not setup_table.get_setup_by_ids(car.league_id, car.track_id, car.weather_id, car.game_mode_id):
        setup_table.insert_setup(car)

    newcar = CarSetup(*setup_table.get_setup_by_setup_id(1))

    newcar.front_wing = 3
    newcar.rear_wing = 5
    setup_table.update_setup_values(newcar)
    print(setup_table.get_setup_by_strs('F1 2020', 'Canada', 'Dry'))
    """


    close_conn()
