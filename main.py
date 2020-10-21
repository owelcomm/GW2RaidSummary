from utils import parser
from utils import player
from utils import plotter

if __name__ == "__main__":
    # Parameters :
    player_list = "players.txt"
    logs_folder = "logs"

    # Reading the participating player file
    with open(player_list) as f:
        players_names = f.readlines()
    players_names = [x.strip() for x in players_names]

    # Instantiating the player objects in a player list
    players = []
    for i in players_names:
        players.append(player.Player(i))

    # Reading and parsing the logs
    debug_variable = parser.parse(logs_folder, players)

    # Display of the graphs
    plotter.harry_plotter(players, "dist")

    # Debug for further console testing
    p = debug_variable['players']
    p = p[0]
    phases = debug_variable["phases"]
    dmg = phases[0]["dmgStats"]
