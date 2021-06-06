class League:
    def __init__(self, league_id, name):
        self.league_id = league_id
        self.name = name

    def __repr__(self):
        return "League('{}', '{}')".format(self.name, self.league_id)