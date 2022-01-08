import sqlite3


class TeamSql:
    def __init__(self):
        self.conn = sqlite3.connect('F1Setups/DB/local_sqlite3/data.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS 
                teams (
                    league_id integer,
                    team_id integer,
                    team_name text NOT NULL
                    )""")
        self.conn.commit()

    def insert_teams(self, team):
        with self.conn:
            self.c.execute("INSERT INTO teams VALUES (:league_id, :team_id, :name)",
                           {'league_id': team.league_id, 'team_id': team.team_id, 'name': team.name})
            self.conn.commit()

    def get_teams(self):
        self.c.execute("""SELECT * FROM teams 
                """)
        return self.c.fetchall()

    def get_team_name_from_ids(self, team_id, league_id):
        self.c.execute("""SELECT team_name FROM teams
                    WHERE 
                        team_id=:team_id AND
                        league_id=:league_id
                    ;""",
                       {'team_id': team_id,
                        'league_id': league_id})
        return self.c.fetchone()

    def get_team_id(self, team_name, league_id):
        self.c.execute("""SELECT team_id FROM teams
                    WHERE 
                        team_name=:team_name AND
                        league_id=:league_id
                    ;""",
                       {'team_name': team_name,
                        'league_id': league_id})
        return self.c.fetchone()[0]
