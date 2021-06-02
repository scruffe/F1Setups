import sqlite3


class LeagueSql:
    def __init__(self):
        self.conn = sqlite3.connect('./data.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS 
                leagues (
                    league_id integer PRIMARY KEY,
                    league_name text NOT NULL
                    )""")
        self.conn.commit()

    def insert_league(self, league):
        with self.conn:
            self.c.execute("INSERT INTO leagues VALUES (:league_id, :name)",
                      {'league_id': league.league_id, 'name': league.name})
        self.conn.commit()

    def get_leagues(self):
        self.c.execute("""SELECT * FROM leagues 
                """)
        return self.c.fetchall()

    def get_id_from_name(self, name):
        self.c.execute("""SELECT league_id FROM leagues WHERE league_name = :name
                """, {'name': name})
        return self.c.fetchone()[0]
