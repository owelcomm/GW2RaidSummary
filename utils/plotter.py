import pylab as pl
from utils import statutils


def harry_plotter(players, data):
    """
    Display a plot of the selected data for each fight, and its polynomial regression

    Parameters
    ----------
    players : list[Player]
        list of the player objects that we want displayed
    data : str
        name of the attribute we want displayed
    """

    legends = []
    pl.figure()
    for p in players:
        if p.fights != []:
            pl.plot(p.fights, getattr(p, data))
            legends.append(p.name)
    pl.xlabel("n-ième fight")
    pl.ylabel(data)
    pl.legend(legends)

    pl.figure()
    for p in players:
        if p.fights != []:
            x, y = statutils.polyreg(p.fights, getattr(p, data))
            pl.plot(x, y)
    pl.xlabel("n-ième fight")
    pl.ylabel("distance moyenne par rapport au lead")
    pl.legend(legends)

    pl.show()


def temp_func():
    pass
    # elif subgroup == "classe":
    #     pl.figure()
    #     classes = {}
    #     for p in players:
    #         if not (p.classe in groups.keys):
    #             groups[p.classe] = [p]
    #         else:
    #             groups[p.classe].append(p)
    #     for i in []:
    #         pass
    #     pl.xlabel("n-ième fight")
    #     pl.ylabel("distance moyenne par rapport au lead")
    # else:
    #     pass
    #
    # pl.show()
