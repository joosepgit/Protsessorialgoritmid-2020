#!/usr/bin/env python3
# vim: set fileencoding=utf8 :
# OS2020 3. kodutöö lahenduse teinud Joosep Tavits

from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox
from copy import *
from random import *


def puhasta():
    tahvel.delete('all')
    arvutused = Canvas(raam, width=430, height=170)
    arvutused.place(x=600, y=30)
# joonistab tahvlile protsesse kujutavad ristkülikud numbrite ja protsesside nimedega
def joonista(jarjend, valjund):
    puhasta()
    arvutused = Canvas(raam, width=430, height=170)
    arvutused.place(x=600, y=30)
    värvid = {"A": "green", "B": "red", "C": "orange", "D": "steel blue", "E": "yellow", "F": "purple",
              "G": "spring green", "H": "tomato", "I": "cyan", "J": "khaki", "": "light grey"}
    for i in range(len(valjund[0])):
        tahvel.create_text(75 + i * 20, 15, text=str(i+1), anchor=NW)
    for i in range(len(jarjend)):
        tahvel.create_text(15, 40 + i * 30,
                           text="Samm " + str(i+1), anchor=NW)
    pikkus = (len(valjund))
    if pikkus < len(jarjend):
        pikkus = len(jarjend)
    for i in range(pikkus):
        for j in range(len(valjund[0])):
            try:
                tahvel.create_rectangle(70 + j * 20, 40 + i * 30, 90 + j * 20, 60 + i * 30,
                                    fill=värvid[valjund[i][j]])
                tahvel.create_text(77 + j * 20, 43 + i * 30, text=valjund[i][j], anchor=NW)
            except:
                tahvel.create_rectangle(70, 40 + i * 30, 1030, 60 + i * 30, fill='black')
                tahvel.create_text(77 + 22 * 20, 43 + i * 30, text="Uue faili jaoks ei jätku ruumi!", anchor=NW, fill='white')
                math = arvutaVajalik(valjund[i-1])
                allesfrag = ttk.Label(arvutused, text="Allesjäänud failidest on fragmenteerunud " + str(math[0]) + "%.")
                allesfrag.place(x=0, y=0)
                fragala = ttk.Label(arvutused,
                                    text="Fragmenteerunud failidele kuulub " + str(math[1]) + "% kasutatud ruumist.")
                fragala.place(x=0, y=(allesfrag.winfo_vrootwidth()//100)+3)
                raise StopIteration
    math = arvutaVajalik(valjund[len(valjund) - 1])
    allesfrag = ttk.Label(arvutused, text="Allesjäänud failidest on fragmenteerunud " + str(math[0]) + "%.")
    allesfrag.place(x=0, y=0)
    fragala = ttk.Label(arvutused, text="Fragmenteerunud failidele kuulub " + str(math[1]) + "% kasutatud ruumist.")
    fragala.place(x=0, y=(allesfrag.winfo_vrootwidth()//100)+3)


# teeb järjendist kahetasemelise listi, mida on mugavam töödelda
def massiiviks(input_jarjend):
    valjund = []
    jupid = input_jarjend.split(";")
    for i in range(len(jupid)):
        hakkliha = jupid[i].split(",")
        saabumine = str(hakkliha[0])
        kestus = str(hakkliha[1])
        valjund.append([saabumine, kestus])
    return valjund

# otsustab, millist järjendit teha kahetasemeliseks massiiviks
def massiiviMeister():
    jarjend = []
    if var.get() == 1:
        return massiiviks(predef1)
    elif var.get() == 2:
        return massiiviks(predef2)
    elif var.get() == 3:
        return massiiviks(predef3)
    elif var.get() == 4:
        try:
            return massiiviks(kasutaja_jarjend.get())
        except:
            messagebox.showerror(title="Viga sisendis", message="Vigane kasutaja muster!")
            puhasta()
            return None
    else:
        messagebox.showerror(title="Viga sisendis", message="Vigane kasutaja muster!")
        return None

def visualiseeriPaigutus(jarjend):
    tulemus = []
    rida = [['48', ""]]
    pikkus = len(jarjend)
    for i in range(pikkus):
        if jarjend[i][1] != "-":
            jarjend[i][1] = int(jarjend[i][1].strip("+"))
            rida[len(rida)-1][0] = int(rida[len(rida)-1][0]) - int(jarjend[i][1])
            for j in range(len(rida)):
                if rida[j][1] == '':
                    if int(rida[j][0]) <= int(jarjend[i][1]):
                        if j == len(rida)-1 and jarjend[i][1] != 0:
                            rida.insert(j, [jarjend[i][1], jarjend[i][0]])
                        else:
                            rida[j][1] = jarjend[i][0]
                    elif jarjend[i][1] != 0:
                        rida.insert(j, [jarjend[i][1], jarjend[i][0]])
                        rida[j+1][0] -= jarjend[i][1]
                    jarjend[i][1] = int(jarjend[i][1]) - int(rida[j][0])
        elif jarjend[i][1] == "-":
            length = len(rida)
            for e in range(length):
                if rida[e][1] == jarjend[i][0]:
                    rida[e][1] = ""
        lugeja = 0
        for o in range(len(rida)):
            if o != len(rida)-1:
                lugeja += rida[o][0]
        if lugeja > 48:
            break
        rida[len(rida)-1][0] = 48 - lugeja
        tulemus_rida = []
        for k in range(len(rida)):
            for l in range(int(rida[k][0])):
                tulemus_rida.append(rida[k][1])
        tulemus.append(tulemus_rida)
    return tulemus

def arvutaVajalik(rida):
    praegune = None
    esinemisi = dict()
    fragmenteerumine = dict()
    for elem in rida:
        if elem != "":
            fragmenteerumine[elem] = 0
            esinemisi[elem] = 0
    for elem in rida:
        if elem != "":
            esinemisi[elem] += 1
            if praegune != elem:
                fragmenteerumine[elem] += 1
                praegune = elem
    fragmenteerunud = 0
    terviklikud = 0
    for key, val in fragmenteerumine.items():
        if val > 1:
            fragmenteerunud += 1
        else:
            terviklikud += 1
    fragplokke = 0
    tervplokke = 0
    for key, val in esinemisi.items():
        if fragmenteerumine[key] > 1:
            fragplokke += esinemisi[key]
        else:
            tervplokke += esinemisi[key]
    allesfrag = round(((fragmenteerunud/(fragmenteerunud+terviklikud))*100), 2)
    fragala = round(((fragplokke/(fragplokke+tervplokke))*100), 2)
    return allesfrag, fragala

def kasuvalija(jarjend):
    return visualiseeriPaigutus(jarjend)

def jooksuta_algoritmi():
    jarjend = massiiviMeister()
    valjund = kasuvalija(jarjend)
    joonista(jarjend, valjund)


predef1 = "A,2;B,3;A,-;C,4;B,+3;D,5;E,15;C,-;F,5"
predef2 = "A,4;B,3;C,6;D,5;C,+2;B,-;E,5;A,-;F,10"
predef3 = "A,2;B,3;C,4;D,5;B,-;E,7;D,-;E,+3;F,10"

# GUI
raam = Tk()
raam.title("Planeerimisalgoritmid")
raam.resizable(False, False)
raam.geometry("1050x560")

var = IntVar()
var.set(1)
Radiobutton(raam, text="Esimene", variable=var, value=1).place(x=10,y=40)
Radiobutton(raam, text="Teine", variable=var, value=2).place(x=10,y=70)
Radiobutton(raam, text="Kolmas", variable=var, value=3).place(x=10,y=100)
Radiobutton(raam, text="Enda oma", variable=var, value=4).place(x=10,y=130)

silt_vali = ttk.Label(raam, text="Vali või sisesta järjend (kujul A,2;B,3;A,-;C,4;B,+2). Max 10 faili.")
silt_vali.place(x=10, y=10)

silt1 = ttk.Label(raam, text=predef1)
silt1.place(x=120, y=40)

silt2 = ttk.Label(raam, text=predef2)
silt2.place(x=120, y=70)

silt3 = ttk.Label(raam, text=predef3)
silt3.place(x=120, y=100)

silt_run = ttk.Label(raam, text="Algoritmi käivitamiseks klõpsa nupule")
silt_run.place(x=10, y=160)

silt_tahvel = ttk.Label(raam, text="Arvutused:")
silt_tahvel.place(x=600, y=10)

kasutaja_jarjend = ttk.Entry(raam)
kasutaja_jarjend.place(x=120, y=130, height=25, width=240)

tahvel = Canvas(raam, width=1200, height=350, background="white")
tahvel.place(x=0, y=220)

kaivita_nupp = ttk.Button(raam, text="Käivita", command = lambda : jooksuta_algoritmi())
kaivita_nupp.place(x=10, y=190,height=25, width=80)

puhasta_nupp = ttk.Button(raam, text="Puhasta väljund", command = lambda : puhasta() )
puhasta_nupp.place(x=100, y=190,height=25, width=130)

arvutused = Canvas(raam, width=430, height=170)
arvutused.place(x=600, y=30)

raam.mainloop()
