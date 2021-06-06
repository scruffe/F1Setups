import sqlite3


class TrackSql:
    def __init__(self):
        self.conn = sqlite3.connect('F1Setups/DB/local_sqlite3/data.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS 
                tracks (
                    track_id integer PRIMARY KEY,
                    track_country text NOT NULL,
                    track_name text
                    )""")
        self.conn.commit()

    def insert_track(self, tr):
        with self.conn:
            self.c.execute("INSERT INTO tracks VALUES (:id, :country, :name)",
                           {'id': tr.track_id, 'country': tr.country, 'name': tr.name})
            self.conn.commit()

    def get_tracks(self):
        self.c.execute("""SELECT * FROM tracks 
                """)
        return self.c.fetchall()

    def get_track_country_by_id(self, track_id):
        self.c.execute("""SELECT track_country FROM tracks WHERE track_id = :track_id
                """, {'track_id': track_id})
        return self.c.fetchone()

    def get_track_id_by_country(self, country):
        self.c.execute("""SELECT track_id FROM tracks WHERE track_country = :country
                """, {'country': country})
        return self.c.fetchone()[0]
