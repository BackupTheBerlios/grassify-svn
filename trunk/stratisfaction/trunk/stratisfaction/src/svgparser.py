#!/usr/bin/python

# svgparser.py

import xml.dom.minidom as dom

def __init__(self):
    pass

def lade_svg(dateiname): 
    d = {} 
    baum = dom.parse(dateiname)

    for eintrag in  baum.documentElement.getElementsByTagName("g"): 
        if eintrag.getAttribute("class") == "node":
            schluessel = wert = None

            for knoten in eintrag.childNodes: 
                if knoten.nodeName == "title": 
                    schluessel = knoten.firstChild.data.strip()
                    #print schluessel
                elif knoten.nodeName == "polygon": 
                    werte = knoten.getAttribute("points").rsplit(" ")
                    punkteX = set()
                    punkteY = set()
                    punkte = []
                    for koordinaten in werte:
                        koordinate = koordinaten.rsplit(" ")        
                        [x,y] = koordinate[0].rsplit(",")                        
                        if x.find(".") > -1:
                            [vorkommax,nachkommax] = x.rsplit(".")
                        else:
                            vorkommax = x
                        if y.find(".") > -1:
                            [vorkommay,nachkommay] = y.rsplit(".")
                        else:
                            vorkommay = y
                        punkte.append([vorkommax,vorkommay])
            d[schluessel] = punkte
    #printMoped(d)
    return d
    
def printMoped(sukamare):
    for key in sukamare:
        print key + ": " + sukamare[key][2][1]

#def main():
#    lade_svg("matrix.svg")
#    
#main()
