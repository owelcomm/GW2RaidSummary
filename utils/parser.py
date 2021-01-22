# -*- coding: utf-8 -*-

import ast
from bs4 import BeautifulSoup
import codecs
import glob, os
from utils import description


def parse(logs_folder, players, professions):
    """
    Update the players list, using all the html files in the log directory

    Parameters
    ----------
    logs_folder : str
        Directory containing the html files
    players : list of Player objects
        List containing all the players to be updated
    professions : list[Profession]
        A list of "Profession" objects

    Returns
    -------
    fights : list[Fight]
        List containing all the fights meta data
    dict
        A debug variable containing the fight data of the last html file

    """
    root = os.getcwd()
    id_fight = 0  # Current file analysed
    fights = []
    os.chdir(logs_folder)
    print("\n\nPARSING...\n")
    for file in glob.glob("*.html"):
        fight, debug_variable = parse_fight(file, players, id_fight, professions)
        fights.append(fight)
        id_fight += 1
        print("file " + str(id_fight) + " in " + str(
            len(glob.glob("*.html"))) + " files")  # Debug print, showing the current file being parsed

    os.chdir(root)
    return fights, debug_variable


def parse_fight(file, players, id_fight, professions):
    """
    Update the players using one single fight file

    Parameters
    ----------
    file : str
        file containing the fight data
    id_fight : int
        the index of the fight (ids in a directory being "1, 2, 3, ...")
    players : list[Player]
        List containing all the players to be updated
    professions : list[Profession]
        A list of "Profession" objects

    Returns
    -------
    fight : Fight
        fight object containing the fight meta data
    temp
        A debug variable containing the fight data


    Comments
    -------
    Html file structure :

        html file
          ├── 0 : ...
          ├── 1 : ...
          ├──  ...
          ├── 14 : ...
          ├── 15 : fight data
          │         ├── targets : ...
          │         ├── players
          │         │      ├── player #1
          │         │      │      ├── group
          │         │      │      ├── acc
          │         │      │      ├── profession
          │         │      │      ├── ...
          │         │      │      └── details : ...
          │         │      ├── player #2 : ...
          │         │      ├── ...
          │         │      └── player #n : ...
          │         ├── enemies : ...
          │         ├── phases
          │         │      └── phases
          │         │            ├── name
          │         │            ├── duration
          │         │            ├── ...
          │         │            ├── dmgStats
          │         │            │     ├──  player #1
          │         │            │     │      ├── 0: ???
          │         │            │     │      ├── 1: ???
          │         │            │     │      ├── ...
          │         │            │     │      └── 20 : av. dist to the commander
          │         │            │     ├──  player #2 : ...
          │         │            │     ├──    ...
          │         │            │     └──  player #n : ...
          │         │            ├──defStats
          │         │            │     ├──  player #1
          │         │            │     │      ├── 0 : damage taken
          │         │            │     │      ├── 1 : barrier
          │         │            │     │      ├── 2 : attacks blocked
          │         │            │     │      ├── 3 : invu
          │         │            │     │      ├── 4 : interrupted
          │         │            │     │      ├── 5 : evades
          │         │            │     │      ├── 6 : dodge
          │         │            │     │      ├── 7 : ...
          │         │            │     ├──    ...
          │         │            │     └──  player #n : ...
          │         │            ├──supportStats
          │         │            │     ├──  player #1
          │         │            │     │      ├── 0 : cleanse
          │         │            │     │      ├── 1 : ...
          │         │            │     │      ├── 2 : ...
          │         │            │     │      ├── 3 : ...
          │         │            │     │      ├── 4 : strips
          │         │            │     │      ├── 5 : ...
          │         │            │     │      ├── 6 : resurrect
          │         │            │     │      ├── 7 : ...
          │         │            │     ├──    ...
          │         │            │     └──  player #n : ...
          │         │            ├── ...
          │         │            ├── boonStats (coverage)
          │         │            │     ├──  player #1
          │         │            │     │      ├── 0 : power
          │         │            │     │      ├── 1 : fury
          │         │            │     │      ├── 2 : quickness
          │         │            │     │      ├── 3 : alacrity
          │         │            │     │      ├── 4 : protection
          │         │            │     │      ├── 5 : regen
          │         │            │     │      ├── 6 : vigor
          │         │            │     │      ├── 7 : aegis
          │         │            │     │      ├── 8 : stability
          │         │            │     │      ├── 9 : swiftness
          │         │            │     │      ├── 10 : retaliation
          │         │            │     │      └── 11 : resistance
          │         │            │     ├──    ...
          │         │            │     └──  player #n : ...
          │         │            ├── boonGenGroupStats (generation)
          │         │            │     ├──  player #1
          │         │            │     │      ├── 0 : power
          │         │            │     │      ├── 1 : fury
          │         │            │     │      ├── 2 : quickness
          │         │            │     │      ├── 3 : alacrity
          │         │            │     │      ├── 4 : protection
          │         │            │     │      ├── 5 : regen
          │         │            │     │      ├── 6 : vigor
          │         │            │     │      ├── 7 : aegis
          │         │            │     │      ├── 8 : stability
          │         │            │     │      ├── 9 : swiftness
          │         │            │     │      ├── 10 : retaliation
          │         │            │     │      └── 11 : resistance
          │         │            │     ├──    ...
          │         │            │     └──  player #n : ...
          │         │            ├── ...
          │         │            ├── dpsStatsTargets
          │         │            │     ├──  player #1
          │         │            │     │      ├── 0 : damage
          │         │            │     │      ├── 1 : power damage
          │         │            │     │      └── 2 : condi damage
          │         │            │     ├──    ...
          │         │            │     └──  player #n : ...
          │         │            ├── ...
          │         │            └── playerActiveTimes
          │         ├── boons : ...
          │         ├── encounterStart : str
          │         ├── ...
          │         └── uploadLinks : ...
          ├── 16 : ...
          ├── ...
          └── 51 : ...



    """

    f = codecs.open(file, 'r', 'utf-8')
    document = BeautifulSoup(f.read(), "lxml")
    f.close()
    sections = document.findAll()
    logs = sections[15]
    txt = logs.get_text()
    txt = txt.replace("null", "None")
    txt = txt.replace("true", "True")
    txt = txt.replace("false", "False")
    txt = txt[txt.find("{"):txt.find(";")]
    temp = ast.literal_eval(txt) #Transform the dictionnory in the html file into an actual variable
    play = temp["players"]
    playL = []
    for i in play:
        playL.append(i['acc'])
    phases = temp["phases"]

    start = temp['encounterStart']
    start = start[start.find(" ") + 1: start.find(" +")]
    fight = description.Fight(start)

    dmgstats = phases[0]["dmgStats"]
    defstats = phases[0]["defStats"]
    supstats = phases[0]["supportStats"]
    boons = phases[0]["boonGenActiveGroupStats"]
    boonscoverage = phases[0]["boonStats"]
    dmg = phases[0]["dpsStatsTargets"]

    for player in players:
        if player.name in playL:
            p_index = playL.index(player.name)
            if dmgstats[p_index][20] < 1500 and len(boons[p_index]["data"]) == 12:
                for prof in professions:
                    if play[p_index]['profession'] == prof.name:
                        player.profession = prof

                player.distance.append(dmgstats[p_index][20])
                player.evades.append(defstats[p_index][5])
                player.dodges.append(defstats[p_index][6])
                player.cleanses.append(supstats[p_index][0])
                player.strips.append(supstats[p_index][4])
                player.fights.append(id_fight)
                player.groupe = play[p_index]['group']
                player.dmg.append(dmg[p_index][0][0])
                player.commander.append(play[p_index]['isCommander'])
                player.add_fight_data(phases[0]['duration'], dmg[p_index][0][0], supstats[p_index][4], supstats[p_index][0])

                getattr(player, "power").append(boons[p_index]["data"][0][0])
                getattr(player, "stab").append(boons[p_index]["data"][8][0])
                getattr(player, "protect").append(boons[p_index]["data"][4][0])
                getattr(player, "resistance").append(boons[p_index]["data"][11][0])

                try:
                    getattr(player, "stab_coverage").append(boonscoverage[p_index]["data"][8][1])
                except:
                    getattr(player, "stab_coverage").append(0)
                try:
                    getattr(player, "protect_coverage").append(boonscoverage[p_index]["data"][4][0])
                except:
                    getattr(player, "protect_coverage").append(0)
    if len(boons[p_index]["data"]) != 12:
        print("fight #", id_fight, " excluded, not enough boon generated")

    return fight, temp
