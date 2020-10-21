import ast
from bs4 import BeautifulSoup
import codecs
import glob, os


def parse(logs_folder, players):
    """
    Update the players list, using all the html files in the log directory

    Parameters
    ----------
    logs_folder : str
        Directory containing the html files
    players : list of Player objects
        List containing all the players to be updated

    Returns
    -------
    dict
        A debug variable containing the fight data of the last html file

    """

    id_fight = 0  # Current file analysed
    os.chdir(logs_folder)
    for file in glob.glob("*.html"):
        debug_variable = parse_fight(file, players, id_fight)
        id_fight += 1
        print("file " + str(id_fight) + " in " + str(
            len(glob.glob("*.html"))) + " files")  # Debug print, showing the current file being parsed
    return debug_variable


def parse_fight(file, players, id_fight):
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
    for p in players:
        if p.name in playL:
            p_index = playL.index(p.name)
            if dmgstats[p_index][20] < 1500:
                p.dist.append(dmgstats[p_index][20])
                p.fights.append(id_fight)
            p.groupe = play[p_index]['group']
            p.classe = play[p_index]['profession']

    return temp
