class Player:
    def __init__(self, name, groupe=0, classe="quaggan"):
        self.name = name
        self.dist = []
        self.fights = []
        self.dmg = []
        self.groupe = groupe
        self.classe = classe
