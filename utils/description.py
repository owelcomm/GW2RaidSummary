class Player:
    def __init__(self, name, groupe=0, profession="quaggan"):
        self.name = name
        self.distance = []
        self.fights = []
        self.dmg = []
        self.groupe = groupe
        self.profession = profession
        self.stab = []
        self.power = []
        self.protect = []
        self.resistance = []
        self.commander = []
        self.dodges = []
        self.evades = []
        self.strips = []
        self.cleanses = []


class Profession:
    def __init__(self, name, fightStats, position, boonStats):
        dps, cleanse, strip = fightStats
        protect, stab, resist = boonStats
        melee, distance = position
        self.name = name
        self.dps = dps
        self.cleanse = cleanse
        self.strip = strip
        self.melee = melee
        self.distance = distance
        self.stab = stab
        self.resist = resist
        self.protect = protect


def init_professions():
    """
    Generate the list of used professions

    Returns
    -------
    professions : list[Profession]
        A list of "Profession" objects
    """

    professions = []
    professions.append(Profession("Firebrand", [False, True, False], [True, False], [True, True, True]))
    professions.append(Profession("Dragonhunter", [True, False, False], [False, True], [False, False, False]))
    professions.append(Profession("Guardian", [True, False, False], [True, False], [False, False, False]))
    professions.append(Profession("Spellbreaker", [False, True, True], [True, False], [False, False, True]))
    professions.append(Profession("Herald", [True, False, False], [True, False], [False, False, False]))
    professions.append(Profession("Renegade", [True, False, False], [True, False], [False, False, False]))
    professions.append(Profession("Scourge", [True, False, True], [False, True], [False, False, False]))
    professions.append(Profession("Necromancer", [True, False, True], [False, True], [False, False, False]))
    professions.append(Profession("Reaper", [True, False, True], [True, False], [False, False, False]))
    professions.append(Profession("Tempest", [False, True, False], [False, True], [False, False, False]))
    professions.append(Profession("Weaver", [True, False, False], [False, True], [False, False, False]))
    professions.append(Profession("Elementalist", [True, False, False], [False, True], [False, False, False]))
    professions.append(Profession("Scrapper", [True, True, False], [True, False], [False, False, False]))
    return professions
