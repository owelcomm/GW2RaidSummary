class Player:
    def __init__(self, name, groupe=0, profession="quaggan"):
        self.name = name
        self.dist = []
        self.fights = []
        self.dmg = []
        self.groupe = groupe
        self.profession = profession
        self.stab = []
        self.power = []
        self.protec = []
        self.resistance = []


class Profession:
    def __init__(self, name, dps, cleanse, strip, melee, FB):
        self.name = name
        self.dps = dps
        self.cleanse = cleanse
        self.strip = strip
        self.melee = melee
        self.FB = FB


def init_professions():
    """
    Generate the list of used professions

    Returns
    -------
    professions : list[Profession]
        A list of "Profession" objects
    """

    professions = []
    professions.append(Profession("Firebrand", False, True, False, True, True))
    professions.append(Profession("Dragonhunter", True, False, False, False, False))
    professions.append(Profession("Guardian", True, False, False, True, False))
    professions.append(Profession("Spellbreaker", False, True, True, True, False))
    professions.append(Profession("Herald", True, False, False, True, False))
    professions.append(Profession("Renegade", True, False, False, True, False))
    professions.append(Profession("Scourge", True, False, True, False, False))
    professions.append(Profession("Necromancer", True, False, True, False, False))
    professions.append(Profession("Reaper", True, False, True, True, False))
    professions.append(Profession("Tempest", False, True, False, False, False))
    professions.append(Profession("Weaver", True, False, False, False, False))
    professions.append(Profession("Elementalist", True, False, False, False, False))
    professions.append(Profession("Scrapper", True, True, False, True, False))
    return professions
