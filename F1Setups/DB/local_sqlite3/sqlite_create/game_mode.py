class GameModes:
    """Game modes like Time trail, multiplayer"""
    def __init__(self, _id, name):
        self.id = _id
        self.name = name

    def __repr__(self):
        return "GameMode('{}', '{}')".format(self.name, self.id)
