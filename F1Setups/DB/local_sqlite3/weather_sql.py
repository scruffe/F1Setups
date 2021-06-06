import sqlite3


class WeatherSql:
    def __init__(self):
        self.conn = sqlite3.connect('F1Setups/DB/local_sqlite3/data.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS 
                weathers (
                    weather_id integer PRIMARY KEY,
                    weather_name text NOT NULL
                    )""")
        self.conn.commit()

    def insert_weather(self, weather_id, weather_name):
        with self.conn:
            self.c.execute("INSERT INTO weathers VALUES (:id, :name)",
                           {'id': weather_id, 'name': weather_name})
            self.conn.commit()

    def get_weather_name_from_id(self, weather_id):
        self.c.execute("""SELECT weather_name FROM weathers
                    WHERE weather_id=:weather_id;""",
                       {'weather_id': weather_id})
        return self.c.fetchone()

    def get_weather_id_from_name(self, weather_name):
        self.c.execute("""SELECT weather_id FROM weathers
                    WHERE weather_name=:name;""",
                       {'name': weather_name})
        return self.c.fetchone()[0]
