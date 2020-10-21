from __future__ import division, unicode_literals 
import codecs
from bs4 import BeautifulSoup
import glob, os
import ast 
from pylab import *
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class player:
    def __init__(self,name, groupe=0, classe="quaggan"):
        self.name = name
        self.dist = []
        self.fights = []
        self.dmg = []
        self.groupe=groupe
        self.classe=classe

def findtruc(d,v):
    for k in d.keys():
        try:
            if v in str(d[k]):
                print(k)
                findtruc(d[k])
        except:
            pass

def parse(file,players,id_fight):
    f=codecs.open(file, 'r', 'utf-8')
    document= BeautifulSoup(f.read(), "lxml")
    f.close()
    sections=document.findAll()
    logs = sections[15]
    txt = logs.get_text()
    txt=txt.replace("null","None")
    txt=txt.replace("true","True")
    txt=txt.replace("false","False")
    txt=txt[txt.find("{"):txt.find(";")]
    temp = ast.literal_eval(txt) 
    play = temp["players"]
    playL=[]
    for i in play:
        playL.append(i['acc'])
    phases = temp["phases"]
    dmgstats = phases[0]["dmgStats"]
    for p in players:
        if p.name in playL:
            p_index = playL.index(p.name)
            if dmgstats[p_index][20]<1500:
                p.dist.append(dmgstats[p_index][20])
                p.fights.append(id_fight)
            p.groupe = play[p_index]['group']
            p.classe = play[p_index]['profession']

    return temp

def polyreg(x,y):
    x=np.array(x)
    y=np.array(y)
    x=x[:, np.newaxis]
    polynomial_features= PolynomialFeatures(degree=3)
    x_poly = polynomial_features.fit_transform(x)
    model = LinearRegression()
    model.fit(x_poly, y)
    LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None,normalize=False)
    y_poly_pred = model.predict(x_poly)
    return (x,y_poly_pred)

def harry_plotter(players,data,subgroup):
    if subgroup == "all":
        legends=[]
        figure()
        for p in players:
            if p.fights!=[]:
                plot(p.fights, p.dist)
                legends.append(p.name)
        xlabel("n-ième fight")
        ylabel("distance moyenne par rapport au lead")
        legend(legends)

        figure()
        for p in players:
            if p.fights!=[]:
                x,y=polyreg(p.fights,p.dist)
                plot(x,y)
        xlabel("n-ième fight")
        ylabel("distance moyenne par rapport au lead")
        legend(legends)
        
    elif subgroup == "classe":
        figure()
        classes={}
        for p in players:
            if not(p.classe in groups.keys):
                groups[p.classe]=[p]
            else:
                groups[p.classe].append(p)
        for i in []:
            pass

        xlabel("n-ième fight")
        ylabel("distance moyenne par rapport au lead")
    else:
        pass


players_names=['Tourson.8143',
         'Floyd.2164',
         'Keyro.6159',
         'zylion.6327',
         'Unnamed.7395',
         'Nurofen.1398',
         'Pascal COEUR.9760',
         'lodykas.8279',
         'mathusalem.6871',
         'jerrybud.8470',
         'Albatros.6593',
         'Fauve.7498',
         'corsi.1965',
         'rowell.1298',
         'Minacotrion Desthi.4152',
         'elenia syrany.9748',
         'Thepat.1437']

##players_names=['Keyro.6159',
##         'zylion.6327',
##         'Unnamed.7395',
##         'lodykas.8279',
##         'Nurofen.1398',
##         'rowell.1298']

players=[]
for i in players_names:
    players.append(player(i))

id_fight=0
os.chdir("logs2")
i=0
for file in glob.glob("*.html"):
    t=parse(file,players,id_fight)
    id_fight+=1
    i+=1
    print("file " + str(i) + " in " + str(len(glob.glob("*.html"))) + " files")

harry_plotter(players,"yes","all")

#debug
p=t['players']
p=p[0]
phases = t["phases"]
dmg = phases[0]["dmgStats"]
show()
