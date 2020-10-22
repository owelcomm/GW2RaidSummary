import pylab as pl
from utils import statutils
import numpy as np
from scipy.interpolate import make_interp_spline

def findSwapCom(name,players):
    for p in players :
        if p.name == name :
            for fight in range(len(p.commander)):
                if p.commander[fight]==True:
                    return p.fights[fight]
    print("No commander swap found for ",p.name)
    return 0

def plot_all(players):
    print("\n\nDISPLAYING PLOTS...\n")
    separators=[]
    separators = [findSwapCom("joch.6823",players)] # Replace the name by the second commander of the raid, or remove the line otherwise
    plot_focus(players, "dmg", ["dps"],separators)
    plot_focus(players, "stab", ["stab"],separators)
    plot_focus(players, "protect", ["protect"],separators)
    plot_focus(players, "resistance", ["resist"],separators)


def plot_focus(players, data, keywords, separators=[]):
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
    separators : list[int]
        ids of fights corresponding to a commander changement
    """

    rawPlots=True
    if rawPlots==True:
        pl.figure()
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
                    pl.plot(p.fights, getattr(p, data),label=p.name)
                    pass

        pl.title(data.upper())
        pl.xlabel("#fights")
        pl.ylabel(data + " for each fight")
        pl.legend()
        for sep in separators:
            pl.axvline(x=sep,color="black")

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
    for sep in separators:
        pl.axvline(x=sep,color="black")

    pl.show()
