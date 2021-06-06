from DB.server_postgres import *
from carsetup import CarSetup
from DB.local_sqlite3 import setup_sql


class Commands:
    def __init__(self):
        self.server = server_postgres.ServerPostgres()
        pass

    def sort(self):
        """ sort """
        pass

    def upload(self, car_setup):
        """        uploads setup to online database        """
        description = "placeholder"
        downloads = 0
        user_id = 0  # my user id
        print(car_setup.setup)
        """car_setup = (1, 0, " save name test", 1, 2, 11, 0,
                     5, 7, 50, 60, -3, -1, 0, 0, 3, 3, 2, 5, 9, 11, 100, 50, 21, 21, 20, 20, 0, 5, 0)
        """
        self.server.insert_setup(description, downloads, user_id, car_setup.setup)
        pass

    def download(self, _id):
        """        downloads car setup from server        """
        print(_id)
        downloaded_car_setup = self.server.get_setup_from_id(_id[0][0])
        car_setup = CarSetup(downloaded_car_setup[4])
        print(car_setup)
        setup_sql.SetupSql().insert_setup(car_setup)


        # downloads++
        pass

    def search(self):
        pass
