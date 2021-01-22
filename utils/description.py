class Player:
    def __init__(self, name, groupe=0, profession="quaggan"):
        self.name = name
        self.distance = []
        self.fights = []
        self.dmg = []
        self.groupe = groupe
        self.profession = profession
        self.stab = []
        self.stab_coverage = []
        self.power = []
        self.protect = []
        self.protect_coverage = []
        self.resistance = []
        self.commander = []
        self.dodges = []
        self.evades = []
        self.strips = []
        self.cleanses = []
        self.fights_data = []

    def add_fight_data(self, duration_ms, dmg, strip):
        self.fights_data.append(PlayerFightData(duration_ms // 1000, dmg, strip))

    def dps(self):
        if len(self.fights_data) == 0:
            return "0"
        dps = 0
        for fight_data in self.fights_data:
            dps += fight_data.dps()

        return "{:.2f}".format(dps / len(self.fights_data))

    def strip_per_sec(self):
        if len(self.fights_data) == 0:
            return "0"
        sps = 0
        for fight_data in self.fights_data:
            sps += fight_data.strip_per_sec()

        return "{:.2f}".format(sps / len(self.fights_data))


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


class PlayerFightData:
    def __init__(self, fight_time, dmg, strip):
        self.fight_time = fight_time
        self.dmg = dmg
        self.strip = strip

    def _compute_stat_per_sec(self, func):
        if self.fight_time == 0:
            return 0
        return func(self) / self.fight_time

    def dps(self):
        return self._compute_stat_per_sec(lambda a: a.dmg)

    def strip_per_sec(self):
        return self._compute_stat_per_sec(lambda a: a.strip)


class Fight:
    def __init__(self, start):
        self.start = start


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
    professions.append(Profession("Berserker", [True, False, False], [True, False], [False, False, False]))
    professions.append(Profession("Herald", [True, False, False], [False, True], [False, False, False]))
    professions.append(Profession("Renegade", [True, False, False], [True, False], [False, False, False]))
    professions.append(Profession("Scourge", [True, False, True], [False, True], [False, False, False]))
    professions.append(Profession("Necromancer", [True, False, True], [False, True], [False, False, False]))
    professions.append(Profession("Reaper", [True, False, True], [True, False], [False, False, False]))
    professions.append(Profession("Tempest", [False, True, False], [False, True], [False, False, False]))
    professions.append(Profession("Weaver", [True, False, False], [False, True], [False, False, False]))
    professions.append(Profession("Elementalist", [True, False, False], [False, True], [False, False, False]))
    professions.append(Profession("Scrapper", [True, True, False], [True, False], [False, False, False]))
    return professions
