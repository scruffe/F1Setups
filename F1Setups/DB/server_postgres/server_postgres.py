#!/usr/bin/python

import psycopg2
from .config_pg import config


class ServerPostgres:
    def exec(self, sql, one=False, *args):
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, args)
            if one:
                data = cur.fetchone()
            else:
                data = cur.fetchall()
            conn.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def insert_setup(self, setup_name, downloads, user_id, setup):
        """ insert a new vendor into the vendors table """
        sql = """INSERT INTO setups(
                setup_name,
                downloads,
                user_id,
                setup
                )
                 VALUES(
                    %s,%s,%s, ROW %s
                    ) RETURNING setup_id;"""

        return (self.exec(sql, True, (setup_name, downloads, user_id, setup)))[0]

    def get_setups(self):
        sql = """SELECT * FROM setups """
        return self.exec(sql)

    def get_setup_from_id(self, setup_id):
        sql = """SELECT * FROM setups WHERE setup_id=%s"""
        return self.exec(sql, True, setup_id)


if __name__ == '__main__':
    pg = ServerPostgres()

    pg.insert_setup('super fast', 0, 1, (
        1, 0, " save name test", 0, 0, 11, 1,
        5, 7, 50, 60, -3, -1, 0, 0, 3, 3, 2, 5, 9, 11, 100, 50, 21, 21, 20, 20, 0, 5, 0))

    print(pg.get_setups())
