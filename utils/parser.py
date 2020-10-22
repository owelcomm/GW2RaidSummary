import ast
from bs4 import BeautifulSoup
import codecs
import glob, os


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
    dict
        A debug variable containing the fight data of the last html file

    """
    root = os.getcwd()
    id_fight = 0  # Current file analysed
    os.chdir(logs_folder)
    print("\n\nPARSING...\n")
    for file in glob.glob("*.html"):
        debug_variable = parse_fight(file, players, id_fight, professions)
        id_fight += 1
        print("file " + str(id_fight) + " in " + str(
            len(glob.glob("*.html"))) + " files")  # Debug print, showing the current file being parsed

    os.chdir(root)
    return debug_variable


def append_boon(player,boon,boon_list,boon_id):
    """
    Update the player's selected boon list, and fill it with 0 if no possible

    Parameters
    ----------
    player : Player
    boon : str
        selected boon
    boon_list : list[float]
        List from the html file containing all boon data from the player
    boon_id : int
        position of the selected boon in the boon list
    """
    try :
        getattr(player,boon).append(boon_list[boon_id][0])
    except:
        getattr(player, boon).append(0)


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
          │         │            ├── boonGenGroupStats
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
    temp = ast.literal_eval(txt)
    play = temp["players"]
    playL = []
    for i in play:
        playL.append(i['acc'])
    phases = temp["phases"]
    dmgstats = phases[0]["dmgStats"]
    defstats = phases[0]["defStats"]
    supstats = phases[0]["supportStats"]
    boons = phases[0]["boonGenActiveGroupStats"]
    dmg = phases[0]["dpsStatsTargets"]
    for p in players:
        if p.name in playL:
            p_index = playL.index(p.name)
            if dmgstats[p_index][20] < 1500 and len(boons[p_index]["data"])==12:
                for prof in professions:
                    if play[p_index]['profession'] == prof.name:
                        p.profession = prof

                p.distance.append(dmgstats[p_index][20])
                p.evades.append(defstats[p_index][5])
                p.dodges.append(defstats[p_index][6])
                p.cleanses.append(supstats[p_index][0])
                p.strips.append(supstats[p_index][4])
                p.fights.append(id_fight)
                p.groupe = play[p_index]['group']
                p.dmg.append(dmg[p_index][0][0])
                p.commander.append(play[p_index]['isCommander'])

                getattr(p, "power").append(boons[p_index]["data"][0][0])
                getattr(p, "stab").append(boons[p_index]["data"][8][0])
                getattr(p, "protect").append(boons[p_index]["data"][4][0])
                getattr(p, "resistance").append(boons[p_index]["data"][11][0])
    if len(boons[p_index]["data"])!=12:
        print("fight #",id_fight," excluded, not enough boon generated")


    return temp
