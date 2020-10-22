import pylab as pl
from utils import statutils
import numpy as np
from scipy.interpolate import make_interp_spline


def plot_all(players):
    print("\n\nDISPLAYING PLOTS...\n")
    plot_focus(players, "dmg", ["dps"])
    plot_focus(players, "stab", ["stab"])
    plot_focus(players, "protect", ["protect"])
    plot_focus(players, "resistance", ["resist"])


def plot_focus(players, data, keywords):
    """
    Display a plot of the selected data for each fight, and its polynomial regression

    Parameters
    ----------
    players : list[Player]
        list of the player objects that we want displayed
    data : str
        name of the attribute we want displayed
    keywords : list[str]
        attribute of the profession filtering the player displayed (ex : ["melee","dps"])
    """

    legends = []
    #pl.figure()
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
                # pl.plot(p.fights, getattr(p, data))
                legends.append(p.name)

    # pl.title(data.upper())
    # pl.xlabel("#fights")
    # pl.ylabel(data + " for each fight")
    # pl.legend(legends)

    pl.figure()
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
                        pl.plot(xnew, y_smooth,label=p.name)
                    except:
                        print("error for player ", p.name, " : not enough fights")
                except:
                    print("Unexpected error : ", data, p.name, p.fights, getattr(p, data))

    pl.title(data.upper())
    pl.xlabel("#fights")
    pl.ylabel("smoothed curve of " + data)
    pl.legend()

    pl.show()
