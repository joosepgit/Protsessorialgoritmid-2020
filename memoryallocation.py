#!/usr/bin/env python3
# vim: set fileencoding=utf8 :
# Näiteprogramm protsessoriaja planeerijate visualiseerimiseks
# algne autor Sten-Oliver Salumaa
# refaktoreerinud ja muidu muutnud Meelis Roos
# OS2020 2. kodutöö lahenduse teinud Joosep Tavits

from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox
from copy import *
from random import *


def puhasta():
    tahvel.delete('all')

# joonistab tahvlile protsesse kujutavad ristkülikud numbrite ja protsesside nimedega
def joonista(jarjend, valjund, nimi):
    puhasta()
    tähed = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    värvid = {"A": "green", "B": "red", "C": "orange", "D": "steel blue", "E": "yellow", "F": "purple",
              "G": "spring green", "H": "tomato", "I": "cyan", "J": "khaki", "-": "light grey"}
    tahvel.create_text(45, 10, text=nimi.replace("_", " "), anchor=NW)
    tahvel.create_text(20, 30, text="Etapp", anchor=NW)
    tahvel.create_text(70, 30, text="Lisatud\nprotsess", anchor=NW)
    for i in range(50):
        tahvel.create_text(135 + i * 20, 35, text=str(i), anchor=NW)
    for i in range(len(jarjend)):
        tahvel.create_text(70, 70 + i * 20,
                           text=tähed[i] + " (" + str(jarjend[i][0]) + ", " + str(jarjend[i][1]) + ")", anchor=NW)
    for i in range(len(valjund)):
        tahvel.create_text(20, 70 + i * 20, text=str(i + 1), anchor=NW)
    for i in range(len(valjund)):
        for j in range(50):
            try:
                tahvel.create_rectangle(130 + j * 20, 70 + i * 20, 150 + j * 20, 90 + i * 20,
                                        fill=värvid[valjund[i][j]])
                tahvel.create_text(137 + j * 20, 73 + i * 20, text=valjund[i][j], anchor=NW)
            except:
                tahvel.create_rectangle(130, 100 + i * 20, 150 + 49 * 20, 120 + i * 20, fill='black')
                tahvel.create_text(137 + 22 * 20, 103 + i * 20, text="Protsess ei mahu mällu", anchor=NW, fill='white')
                raise StopIteration

# teeb järjendist kahetasemelise listi, mida on mugavam töödelda
def massiiviks(input_jarjend):
    valjund = []
    jupid = input_jarjend.split(";")
    for i in range(len(jupid)):
        hakkliha = jupid[i].split(",")
        saabumine = int(hakkliha[0])
        kestus = int(hakkliha[1])
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
            return massiiviks(predef1)
    else:
        return massiiviks(predef1)

#Jarjendi elemendid tuple kujul: {mälumaht (positiivne täisarv)} ; {kestus sammudes (positiivne täisarv)}
# 0 - suurus
# 1 - kestvus
# 2 - tähis
# 3 - protsess("p") või auk("a")
# 4 - kuna ta lõpetab
def firstFit(jarjend):
    tahed = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    tulemus = []
    rida = [[50, 10, "-", "h", 10]]
    info = list()
    pikkus = len(jarjend)
    for j in range(pikkus):
        info += [[jarjend[j][0], jarjend[j][1], tahed[j], "p", 10]]
    for i in range(10):
        for e in range(len(rida)):
            if rida[e][4] == i:
                rida[e][1] = 10
                rida[e][2] = "-"
                rida[e][3] = "h"
                rida[e][4] = 10
        nullindeksid = []
        oliauk = False
        for asi in range(len(rida)):
            if rida[asi][3] == "h":
                if oliauk and i < pikkus:
                    rida[asi][0] += copy(rida[asi-1][0])
                    rida[asi-1][0] = 0
                    nullindeksid.append(asi-1)
                oliauk = True
            else:
                oliauk = False
        for n in nullindeksid:
            del rida[n]
            for v in range(len(nullindeksid)):
                nullindeksid[v] -= 1
        koht = -1
        for element in range(len(rida)):
            if i < pikkus:
                if rida[element][3] == "h" and info[i][0] <= rida[element][0]:
                    koht = copy(element)
                    info[i][4] = copy(info[i][1]+i)
                    rida[koht][0] -= copy(info[i][0])
                    rida.insert(koht, copy(info[i]))
                    break
            else:
                koht = i
        if koht == -1:
            rida = [[0,0,"error", "error", 0]]
        tulemus_rida = []
        for k in range(len(rida)):
            for l in range(rida[k][0]):
                tulemus_rida.append(rida[k][2])
        tulemus.append(tulemus_rida)
    return tulemus


def lastFit(jarjend):
    tahed = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    tulemus = []
    rida = [[50, 10, "-", "h", 10]]
    info = list()
    pikkus = len(jarjend)
    for j in range(pikkus):
        info += [[jarjend[j][0], jarjend[j][1], tahed[j], "p", 10]]
    for i in range(10):
        for e in range(len(rida)):
            if rida[e][4] == i:
                rida[e][1] = 10
                rida[e][2] = "-"
                rida[e][3] = "h"
                rida[e][4] = 10
        nullindeksid = []
        oliauk = False
        for asi in range(len(rida)):
            if rida[asi][3] == "h":
                if oliauk and i < pikkus:
                    rida[asi][0] += copy(rida[asi-1][0])
                    rida[asi-1][0] = 0
                    nullindeksid.append(asi-1)
                oliauk = True
            else:
                oliauk = False
        for n in nullindeksid:
            del rida[n]
            for v in range(len(nullindeksid)):
                nullindeksid[v] -= 1
        koht = -1
        for element in range(len(rida)):
            if i < pikkus and rida[element][3] == "h" and info[i][0] <= rida[element][0]:
                koht = copy(element)
        if i < pikkus:
            if info[i][0] <= rida[koht][0]:
                info[i][4] = copy(info[i][1]+i)
                rida[koht][0] -= copy(info[i][0])
                rida.insert(koht, copy(info[i]))
        else:
            koht = i
        if koht == -1:
            rida = [[0,0,"error", "error", 0]]
        tulemus_rida = []
        for k in range(len(rida)):
            for l in range(rida[k][0]):
                tulemus_rida.append(rida[k][2])
        tulemus.append(tulemus_rida)
    return tulemus

def worstFit(jarjend):
    tahed = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    tulemus = []
    rida = [[50, 10, "-", "h", 10]]
    info = list()
    pikkus = len(jarjend)
    for j in range(pikkus):
        info += [[jarjend[j][0], jarjend[j][1], tahed[j], "p", 10]]
    for i in range(10):
        for e in range(len(rida)):
            if rida[e][4] == i:
                rida[e][1] = 10
                rida[e][2] = "-"
                rida[e][3] = "h"
                rida[e][4] = 10
        nullindeksid = []
        oliauk = False
        for asi in range(len(rida)):
            if rida[asi][3] == "h":
                if oliauk and i < pikkus:
                    rida[asi][0] += copy(rida[asi-1][0])
                    rida[asi-1][0] = 0
                    nullindeksid.append(asi-1)
                oliauk = True
            else:
                oliauk = False
        for n in nullindeksid:
            del rida[n]
            for v in range(len(nullindeksid)):
                nullindeksid[v] -= 1
        vabad = {}
        koht = -1
        for element in range(len(rida)):
            if i < pikkus and rida[element][3] == "h" and info[i][0] <= rida[element][0]:
                vabad[element] = rida[element][0]
        if len(vabad) > 0:
            koht = max(vabad, key=vabad.get)
        if i < pikkus and info[i][0] <= rida[koht][0]:
            info[i][4] = copy(info[i][1]+i)
            rida[koht][0] -= copy(info[i][0])
            rida.insert(koht, copy(info[i]))
        if i < pikkus and koht == -1:
            rida = [[0,0,"error", "error", 0]]
        tulemus_rida = []
        for k in range(len(rida)):
            for l in range(rida[k][0]):
                tulemus_rida.append(rida[k][2])
        tulemus.append(tulemus_rida)
    return tulemus

def bestFit(jarjend):
    tahed = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    tulemus = []
    rida = [[50, 10, "-", "h", 10]]
    info = list()
    pikkus = len(jarjend)
    for j in range(pikkus):
        info += [[jarjend[j][0], jarjend[j][1], tahed[j], "p", 10]]
    for i in range(10):
        for e in range(len(rida)):
            if rida[e][4] == i:
                rida[e][1] = 10
                rida[e][2] = "-"
                rida[e][3] = "h"
                rida[e][4] = 10
        nullindeksid = []
        oliauk = False
        for asi in range(len(rida)):
            if rida[asi][3] == "h":
                if oliauk and i < pikkus:
                    rida[asi][0] += copy(rida[asi-1][0])
                    rida[asi-1][0] = 0
                    nullindeksid.append(asi-1)
                oliauk = True
            else:
                oliauk = False
        for n in nullindeksid:
            del rida[n]
            for v in range(len(nullindeksid)):
                nullindeksid[v] -= 1
        vabad = {}
        koht = -1
        for element in range(len(rida)):
            if i < pikkus and rida[element][3] == "h" and info[i][0] <= rida[element][0]:
                vabad[element] = rida[element][0]
        if len(vabad) > 0:
            koht = min(vabad, key=vabad.get)
        if i < pikkus and info[i][0] <= rida[koht][0]:
            info[i][4] = copy(info[i][1]+i)
            rida[koht][0] -= copy(info[i][0])
            rida.insert(koht, copy(info[i]))
        if i < pikkus and koht == -1:
            rida = [[0,0,"error", "error", 0]]
        tulemus_rida = []
        for k in range(len(rida)):
            for l in range(rida[k][0]):
                tulemus_rida.append(rida[k][2])
        tulemus.append(tulemus_rida)
    return tulemus


def randomFit(jarjend):
    tahed = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    tulemus = []
    rida = [[50, 10, "-", "h", 10]]
    info = list()
    pikkus = len(jarjend)
    for j in range(pikkus):
        info += [[jarjend[j][0], jarjend[j][1], tahed[j], "p", 10]]
    for i in range(10):
        for e in range(len(rida)):
            if rida[e][4] == i:
                rida[e][1] = 10
                rida[e][2] = "-"
                rida[e][3] = "h"
                rida[e][4] = 10
        nullindeksid = []
        oliauk = False
        for asi in range(len(rida)):
            if rida[asi][3] == "h":
                if oliauk and i < pikkus:
                    rida[asi][0] += copy(rida[asi-1][0])
                    rida[asi-1][0] = 0
                    nullindeksid.append(asi-1)
                oliauk = True
            else:
                oliauk = False
        for n in nullindeksid:
            del rida[n]
            for v in range(len(nullindeksid)):
                nullindeksid[v] -= 1
        vabad = {}
        koht = -1
        for element in range(len(rida)):
            if i < pikkus and rida[element][3] == "h" and info[i][0] <= rida[element][0]:
                vabad[element] = rida[element][0]
        if len(vabad) > 0:
            koht = choice(list(vabad.keys()))
        if i < pikkus and info[i][0] <= rida[koht][0]:
            info[i][4] = copy(info[i][1]+i)
            rida[koht][0] -= copy(info[i][0])
            rida.insert(koht, copy(info[i]))
        if i < pikkus and koht == -1:
            rida = [[0,0,"error", "error", 0]]
        tulemus_rida = []
        for k in range(len(rida)):
            for l in range(rida[k][0]):
                tulemus_rida.append(rida[k][2])
        tulemus.append(tulemus_rida)
    return tulemus


def get_key(val, dict):
    for key, value in dict.items():
        if val == value:
            return key

    return "key doesn't exist"

def kasuvalija(jarjend, algoritm):
    if algoritm == "First_Fit":
        return firstFit(jarjend)
    elif algoritm == "Last_Fit":
        return lastFit(jarjend)
    elif algoritm == "Best_Fit":
        return bestFit(jarjend)
    elif algoritm == "Worst_Fit":
        return worstFit(jarjend)
    elif algoritm == "Random_Fit":
        return randomFit(jarjend)

def jooksuta_algoritmi(algoritm):
    jarjend = massiiviMeister()
    valjund = kasuvalija(jarjend, algoritm)
    joonista(jarjend, valjund, algoritm)


predef1 = "3,5;12,9;4,7;15,2;1,7;6,3;11,8;10,4;2,7;4,1"
predef2 = "8,1;6,3;12,4;15,5;4,9;42,2;6,1;8,5"
predef3 = "1,8;35,4;3,6;4,2;1,4;3,3;1,2;5,1;50,1"
firstFit(massiiviks(predef3))

# GUI
raam = Tk()
raam.title("Planeerimisalgoritmid")
raam.resizable(False, False)
raam.geometry("1200x550")

var = IntVar()
var.set(1)
Radiobutton(raam, text="Esimene", variable=var, value=1).place(x=10,y=40)
Radiobutton(raam, text="Teine", variable=var, value=2).place(x=10,y=70)
Radiobutton(raam, text="Kolmas", variable=var, value=3).place(x=10,y=100)
Radiobutton(raam, text="Enda oma", variable=var, value=4).place(x=10,y=130)

silt_vali = ttk.Label(raam, text="Vali või sisesta kuni kümneelemendiline järjend kujul 1,10;4,2;12,3;13,2")
silt_vali.place(x=10, y=10)

silt1 = ttk.Label(raam, text=predef1)
silt1.place(x=120, y=40)

silt2 = ttk.Label(raam, text=predef2)
silt2.place(x=120, y=70)

silt3 = ttk.Label(raam, text=predef3)
silt3.place(x=120, y=100)

silt_run = ttk.Label(raam, text="Algoritmi käivitamiseks klõpsa nupule")
silt_run.place(x=10, y=160)

#silt_tahvel = ttk.Label(raam, text="Käsil olevad protsessid:")
#silt_tahvel.place(x=450, y=10)

kasutaja_jarjend = ttk.Entry(raam)
kasutaja_jarjend.place(x=120, y=130, height=25, width=240)

tahvel = Canvas(raam, width=1200, height=350, background="white")
tahvel.place(x=0, y=220)

First_Fit_nupp = ttk.Button(raam, text="First-Fit", command = lambda : jooksuta_algoritmi("First_Fit"))
First_Fit_nupp.place(x=10, y=190,height=25, width=80)

Last_Fit_nupp = ttk.Button(raam, text="Last-Fit", command = lambda : jooksuta_algoritmi("Last_Fit"))
Last_Fit_nupp.place(x=100, y=190,height=25, width=80)

Best_Fit_nupp = ttk.Button(raam, text="Best-Fit", command = lambda : jooksuta_algoritmi("Best_Fit"))
Best_Fit_nupp.place(x=370, y=190,height=25, width=80)

Worst_Fit_nupp = ttk.Button(raam, text="Worst-Fit", command = lambda : jooksuta_algoritmi("Worst_Fit"))
Worst_Fit_nupp.place(x=190, y=190,height=25, width=80)

Random_Fit_nupp = ttk.Button(raam, text="Random-Fit", command = lambda : jooksuta_algoritmi("Random_Fit"))
Random_Fit_nupp.place(x=280, y=190,height=25, width=80)

puhasta_nupp = ttk.Button(raam, text="Puhasta väljund", command = lambda : puhasta() )
puhasta_nupp.place(x=500, y=190,height=25, width=130)

#text = Text(raam, width=25, height=9)
#text.place(x=450, y=30)

raam.mainloop()
