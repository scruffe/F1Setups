#!/usr/bin/python

import psycopg2
from .config_pg import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (

        """
        CREATE TABLE IF NOT EXISTS setups (
            setup_id    SERIAL      PRIMARY KEY,
            setup_name  VARCHAR     NOT NULL,
            downloads   SERIAL,
            user_id     SERIAL      NOT NULL,
            car_setup   car_setup   NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id serial PRIMARY KEY,
            username VARCHAR ( 50 ) UNIQUE NOT NULL,
            password VARCHAR ( 50 ) NOT NULL,
            email VARCHAR ( 255 ) UNIQUE NOT NULL,
            created_on TIMESTAMP NOT NULL,
            last_login TIMESTAMP 
        )
        """)
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

sql = """
        CREATE TYPE car_setup AS (
            setup_id                    integer,
            league_id                   integer,
            save_name                   text,
            team_id                     integer,
            track_id                    integer,
            game_mode_id                integer,
            weather_id                  integer,
            front_wing                  integer,
            rear_wing                   integer,
            on_throttle                 integer,
            off_throttle                integer,
            front_camber                integer,
            rear_camber                 integer,
            front_toe                   integer,
            rear_toe                    integer,
            front_suspension            integer,
            rear_suspension             integer,
            front_suspension_height     integer,
            rear_suspension_height      integer,
            front_antiroll_bar          integer,
            rear_antiroll_bar           integer,
            brake_pressure              integer,
            brake_bias                  integer,
            front_right_tyre_pressure   integer,
            front_left_tyre_pressure    integer,
            rear_right_tyre_pressure    integer,
            rear_left_tyre_pressure     integer,
            ballast                     integer,
            fuel_load                   integer,
            ramp_differential           integer
        );
        """
if __name__ == '__main__':
    create_tables()
