#!/usr/bin/python
#    Der Datenspeicher ist dafür zuständig, die Beziehung zwischen den 
#    Layern und der Harris-Matrix zu speichern
#    Einmal sollen die ausgewählten Knoten zurückgegeben werden
#    Einmal sollen die ausgewählten Layer zurückgegeben werden

import xml.dom.minidom as dom


def _knotenAuslesen(knoten):
    return eval("%s('%s')" % (knoten.getAttribute("typ"), knoten.firstChild.data.strip())) 

   
def _erstelleEintrag(schluessel, wert):
    tag_eintrag = dom.Element("eintrag")
    tag_schluessel = dom.Element("schluessel")
    tag_wert = dom.Element("wert")
        
    tag_schluessel.setAttribute("typ", type(schluessel).__name__)
    tag_wert.setAttribute("type", type(wert).__name__)
        
    text = dom.Text()
    text.data = str(schluessel)
    tag_schluessel.appendChild(text)
     
    text = dom.Text()
    text.data = str(wert)
    tag_schluessel.appendChild(text)
        
    tag_eintrag.appendChild(tag_schluessel)
    tag_eintrag.appendChild(tag_wert)
    return tag_eintrag

    
def ladeDict(dateiname): 
    dict = {} 
    baum = dom.parse(dateiname)

    for eintrag in baum.firstChild.childNodes: 
        if eintrag.nodeName == "eintrag": 
            schluessel = wert = None

            for knoten in eintrag.childNodes: 
                if knoten.nodeName == "schluessel": 
                    schluessel = _knoten_auslesen(knoten) 
                elif knoten.nodeName == "wert": 
                    wert = _knoten_auslesen(knoten)

            dict[schluessel] = wert 
    return dict    

def ladeKnoten(dict, knotenId):    
    schluessel = dict._knoten_auslesen(knoten)
    if schluessel == knotenId:    
        return schluessel

def schreibeDict(dict, dateiname): 
    baum = dom.Document() 
    tag_dict = dom.Element("dictionary") 
    baum.appendChild(tag_dict)

    for schluessel, wert in dict.iteritems(): 
        tag_eintrag = _erstelle_eintrag(schluessel, wert) 
        tag_dict.appendChild(tag_eintrag)

f = open(dateiname, "w") 
baum.writexml(f, "", "\t", "\n") 
f.close()
    