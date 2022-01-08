import sqlite3


class UserSql:
    def __init__(self):
        self.conn = sqlite3.connect('F1Setups/DB/local_sqlite3/data.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS 
                users (
                    user_id int PRIMARY KEY,
                    first text,
                    last text,
                    tag text,
                    uploads int,
                    credit int,
                    email text,
                    premium bool
                    )""")
        self.conn.commit()

    def insert_user(self, user):
        with self.conn:
            self.c.execute(
                "INSERT INTO users VALUES (:user_id, :first, :last, :tag, :uploads, :credit, :email, :premium)",
                {'user_id': user.id,
                 'first': user.first,
                 'last': user.last,
                 'tag': user.tag,
                 'uploads': user.uploads,
                 'credit': user.credit,
                 'email': user.email,
                 'premium': user.premium
                 })
            self.conn.commit()

    def get_user_from_id(self, user_id):
        self.c.execute("""SELECT * FROM users
                    WHERE user_id=:user_id;""",
                       {'user_id': user_id})
        return self.c.fetchone()

    def get_user_by_strings(self, first, last, tag):
        self.c.execute("""
                SELECT 
                    user_id,
                    first,
                    last,
                    tag
                FROM users
                WHERE
                    first=:first AND
                    last=:last AND
                    tag=:tag;
                """, {
            'first': first,
            'last': last,
            'tag': tag
        })
        return self.c.fetchone()
