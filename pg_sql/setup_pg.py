#!/usr/bin/python

import psycopg2
from pg_config import config


class SetupPG:
    @staticmethod
    def insert_setup(setup_name):
        """ insert a new vendor into the vendors table """
        sql = """INSERT INTO setups(setup_name)
                 VALUES(%s) RETURNING setup_name;"""
        conn = None
        vendor_id = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (setup_name,))
            vendor_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return vendor_id

    @staticmethod
    def get_setups():
        sql = """SELECT * FROM setups """
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            return data

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


if __name__ == '__main__':
    pg = SetupPG()

    pg.insert_setup("australia super fast")

    print(pg.get_setups())
