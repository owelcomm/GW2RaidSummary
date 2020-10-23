import pylab as pl
from utils import statutils
import numpy as np
from scipy.interpolate import make_interp_spline


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
    separators = []
    separators = [findSwapCom("joch.6823",
                              players)]  # Replace the name by the second commander of the raid, or remove the line otherwise
    plot_focus(players, "dmg", fights, ["dps"], separators=separators)
    plot_focus(players, "stab_coverage", fights, ["stab"], separators=separators)
    plot_focus(players, "protect_coverage", fights, ["protect"], separators=separators)
    # plot_focus(players, "resistance", fights, ["resist"],separators=separators)
    # plot_focus(players, "strips", fights, ["strip"],separators=separators)
    # plot_focus(players, "cleanses", fights, ["cleanse"],separators=separators)
    # plot_focus(players, "dodges", fights, ["melee"],separators=separators, title_label="dodges for melee professions")
    # plot_focus(players, "evades", fights, ["melee"],separators=separators, title_label="attacks evaded for melee professions")
    # plot_focus(players, "distance", fights, ["melee"],separators=separators, title_label="distance from the lead for melee professions")
    # plot_focus(players, "dodges", fights, ["distance"],separators=separators, title_label="dodges for distance professions")
    # plot_focus(players, "evades", fights, ["distance"],separators=separators, title_label="attacks evaded for distance professions")
    # plot_focus(players, "distance", fights, ["distance"],separators=separators, title_label="distance from the lead for distance professions")


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

    start_fights=[]
    for fight in fights:
        start_fights.append(fight.start)
    xaxis = list(range(len(start_fights)))

    colormap = a=pl.cm.tab20
    colormap = colormap(list(range(len(players))))

    rawPlots = False
    if rawPlots == True:
        pl.figure()
        color=0
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
                if flag_kw == 0:
                    pl.plot(p.fights, getattr(p, data), color= colormap[color], label=p.name)
                    color+=1
                    pass

        if title_label != "":
            pl.title(title_label)
        else:
            pl.title(data.upper())
        pl.xticks(xaxis, start_fights, rotation=70)
        pl.ylabel(data + " for each fight")
        pl.legend()
        for sep in separators:
            pl.axvline(x=sep, color="black")

    pl.figure()
    color=0
    for p in players:
        # Check if the player is in the fight and checks all keywords
        if p.fights != []:
            flag_kw = 0
            for kw in keywords:
                if getattr(p.profession, kw) == False:
                    flag_kw = 1

            if flag_kw == 0:
                try:
                    x, y = statutils.polyreg(p.fights, getattr(p, data))
                    x = x.transpose()[0]
                    try:
                        xnew = np.linspace(x.min(), x.max(), 200)
                        spl = make_interp_spline(x, y, k=3)
                        y_smooth = spl(xnew)
                        pl.plot(xnew, y_smooth, label=p.name, color= colormap[color])
                        color+=1
                    except:
                        print("error for player ", p.name, " : not enough fights")
                except:
                    print("Unexpected error : ", data, p.name, p.fights, getattr(p, data))
    pl.xticks(xaxis, start_fights, rotation=70)
    pl.ylabel("smoothed curve of " + data)
    pl.legend()
    for sep in separators:
        pl.axvline(x=sep, color="black")
    pl.gcf().set_size_inches(16, 8)
    if title_label != "":
        pl.title(title_label)
        pl.savefig("plots/" + title_label + ".png", bbox_inches='tight', dpi=100)
    else:
        pl.title(data.upper())
        pl.savefig("plots/" + data.upper() + ".png", bbox_inches='tight', dpi=100)
    pl.show()
