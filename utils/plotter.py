import pylab as pl
from utils import statutils
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib



def findSwapCom(name, players):
    """
    Return the id of the first fight the selected player will take the commander tag

    Parameters
    ----------
    players : list[Player]
        list of the player objects
    name : str
        name of the player that should be commander later in the raid

    Return
    ---------
    separators : int
        id of fight corresponding to the commander changement
    """
    for p in players:
        if p.name == name:
            for fight in range(len(p.commander)):
                if p.commander[fight] == True:
                    return p.fights[fight]
    print("No commander swap found for ", p.name)
    return 0


def plot_all(players, fights):
    """
    Display and save all the different plots

    Parameters
    ----------
    players : list[Player]
        list of the player objects that we want displayed
    fights : list[Fight]
        List containing all the fights meta data
    """
    print("\n\nDISPLAYING PLOTS...\n")
    try:
        separators = [findSwapCom("joch.6823",
                                  players)]  # Replace the name by the second commander of the raid, or remove the line otherwise
    except:
        separators = []
    plot_focus(players, "dmg", fights, ["dps"], separators=separators, title_label="Damages")
    plot_focus(players, "stab", fights, ["stab"], separators=separators, title_label="stab group generation")
    plot_focus(players, "protect", fights, ["protect"], separators=separators, title_label="protect group generation")
    plot_focus(players, "stab_coverage", fights, ["stab"], separators=separators)
    plot_focus(players, "protect_coverage", fights, ["protect"], separators=separators)
    plot_focus(players, "resistance", fights, ["resist"], separators=separators)
    plot_focus(players, "strips", fights, ["strip"], separators=separators)
    plot_focus(players, "cleanses", fights, ["cleanse"], separators=separators)

    plot_focus(players, "dodges", fights, ["melee"], separators=separators,
               title_label="dodges for melee professions")
    plot_focus(players, "evades", fights, ["melee"], separators=separators,
               title_label="attacks evaded for melee professions")
    plot_focus(players, "distance", fights, ["melee"], separators=separators,
               title_label="distance from the lead for melee professions")

    plot_focus(players, "dodges", fights, ["distance"], separators=separators,
               title_label="dodges for distance professions")
    plot_focus(players, "evades", fights, ["distance"], separators=separators,
               title_label="attacks evaded for distance professions")
    plot_focus(players, "distance", fights, ["distance"], separators=separators,
               title_label="distance from the lead for distance professions")
    print_txt_report(players, 'dmg', lambda player: player.dps())
    print_txt_report(players, 'strip', lambda player: player.strip_per_sec())


def print_txt_report(players, title, stat):
    f = open("plots/" + title + ".txt", "w")
    for player in reversed(sorted(players, key=lambda p: float(stat(p)))):
        f.write(player.name + " => " + stat(player) + " " + title + "/s \n")
    f.close()


def plot_focus(players, data, fights, keywords=[], separators=[], title_label=""):

    """
    Display a plot of the selected data for each fight, and its polynomial regression

    Parameters
    ----------
    players : list[Player]
        list of the player objects that we want displayed
    data : str
        name of the attribute we want displayed
    fights : list[Fight]
        List containing all the fights meta data
    keywords : list[str]
        attribute of the profession filtering the player displayed (ex : ["melee","dps"])
    separators : list[int]
        ids of fights corresponding to a commander changement
    title_label : str
        title of the figure, data by default
    """
    #matplotlib.use('Agg')
    if title_label != "":
        figure_name = title_label
    else:
        figure_name = data.upper()

    start_fights = []
    for fight in fights:
        start_fights.append(fight.start)
    xaxis = list(range(len(start_fights)))  # Date of the fights

    colormap = a = pl.cm.tab20  # Choice of the colormap
    colormap = colormap(list(range(len(players))))  # Setup of the colormap

    rawPlots = False
    color = 0
    for p in players:

        # Check if the player is in the fight and checks all keywords
        if p.fights != []:
            flag_kw = 0
            try:
                for kw in keywords:
                    if getattr(p.profession, kw) == False:
                        flag_kw = 1
            except:
                print("Unexpected profession: ", p.name)

            # If the player checks the requirements
            if flag_kw == 0:
                if rawPlots == True:  # Plot without regression
                    pl.figure(figure_name + " raw")
                    pl.plot(p.fights, getattr(p, data), color=colormap[color], label=p.name)

                try:
                    pl.figure(figure_name + " regression")
                    x, y = statutils.polyreg(p.fights, getattr(p, data))  # Regression
                    x = x.transpose()[0]
                    try:
                        # Smooth the curve
                        xnew = np.linspace(x.min(), x.max(), 200)
                        spl = make_interp_spline(x, y, k=3)
                        y_smooth = spl(xnew)
                        pl.plot(xnew, y_smooth, label=p.name, color=colormap[color])
                    except:
                        print("error for player ", p.name, " : not enough fights")
                except:
                    print("Unexpected error : ", data, p.name, p.fights, getattr(p, data))
                color += 1

    pl.figure(figure_name + " regression")
    # TITLE
    if title_label != "":
        pl.title(title_label)
    else:
        pl.title(data.upper())

    # AXIS/LEGEND
    pl.xticks(xaxis, start_fights, rotation=70)
    pl.ylabel(data + " for each fight")
    pl.legend()
    for sep in separators:
        pl.axvline(x=sep, color="black")

    # SAVE THE PLOT
    pl.gcf().set_size_inches(16, 8)
    if title_label != "":
        pl.title(title_label)
        pl.savefig("plots/" + title_label + ".png", bbox_inches='tight', dpi=100)
    else:
        pl.title(data.upper())
        pl.savefig("plots/" + data.upper() + ".png", bbox_inches='tight', dpi=100)
    #pl.show()
