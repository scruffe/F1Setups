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
        print("uploading: ", car_setup.info)
        """car_setup = (1, 0, " save name test", 1, 2, 11, 0,
                     5, 7, 50, 60, -3, -1, 0, 0, 3, 3, 2, 5, 9, 11, 100, 50, 21, 21, 20, 20, 0, 5, 0)
        """
        self.server.insert_setup(description, downloads, user_id, car_setup.setup)
        pass

    def download(self, _id):
        """        downloads car setup from server        """
        _id = _id[0][0]

        print(_id)
        self.server.update_downloads(_id)
        downloaded_car_setup = self.server.get_setup_from_id(_id)
        # Convert String to Tuple
        car_setup = eval(downloaded_car_setup[4])
        car_setup = CarSetup(*car_setup)
        print("downloaded: ", car_setup.info)
        # check if setup is already in db?
        # if yes update?
        local_sqlite = setup_sql.SetupSql()
        local_car = local_sqlite.get_setup_by_ids(
            car_setup.league_id, car_setup.track_id, car_setup.weather_id,
            car_setup.game_mode_id, car_setup.team_id)
        print(local_sqlite.get_setup_by_ids(
            car_setup.league_id, car_setup.track_id, car_setup.weather_id,
            car_setup.game_mode_id, car_setup.team_id))

        if local_car is not None:
            print(local_car[0][0])
            car_setup.setup_id = local_car[0][0]
            local_sqlite.update_setup_values_on_setup_id(car_setup)
            print("updating values: ", car_setup.info)
        else:

            local_sqlite.insert_setup(car_setup)
            print("inserting: ", car_setup.info )

    def search(self):
        pass
