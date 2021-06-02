import sqlite3


class GameModeSql:
    def __init__(self):
        self.conn = sqlite3.connect('./data.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS 
                game_modes (
                    game_mode_id integer PRIMARY KEY,
                    game_mode_name text NOT NULL
                    )""")
        self.conn.commit()

    def insert_game_mode(self, game_mode):
        with self.conn:
            self.c.execute("INSERT INTO game_modes VALUES (:id, :name)",
                           {'id': game_mode.id, 'name': game_mode.name})
            self.conn.commit()

    def get_game_modes(self):
        self.c.execute("""SELECT * FROM game_modes 
                """)
        return self.c.fetchall()

    def get_game_modes_from_name(self, game_mode_name):
        self.c.execute("""SELECT * FROM game_modes 
                        WHERE game_mode_name=:game_mode_name;""",
                       {'game_mode_name': game_mode_name})
        return self.c.fetchall()

    def get_game_mode_id_from_name(self, game_mode_name):
        self.c.execute("""SELECT game_mode_id FROM game_modes
                    WHERE game_mode_name=:game_mode_name;""",
                       {'game_mode_name': game_mode_name})
        return self.c.fetchone()[0]
