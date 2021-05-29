# -*- coding: utf-8 -*-
#1. Caricare tutti i dati del file in un dataframe e visualizzarli in un oggetto opportuno
#2. Dato il nome di un gioco, visualizzare tutte le informazioni relative a quel gioco
#3. Modificare il punto precedente in modo che sia possibile visualizzare le informazioni dei giochi
#successivi o precedenti con due bottoni “Next” e “Prev”
#4. Dato il nome di un gioco, visualizzare la percentuale di vendita nei quattro mercati
#5. Visualizzare i giochi appartenenti ad una certa piattaforma: permettere all’utente di inserire (o di
#scegliere) la piattaforma
#6. Visualizzare il numero totale di giochi venduti in ogni mercato
#7. Visualizzare il grafico del punto 4 con un grafico a torta
#8. Visualizzare il grafico del punto 5 con un grafico a barre orizzontali
#9. Data una stringa, visualizzare i giochi che hanno quella stringa nel nome

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import os.path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

df = pd.read_csv("C:/Users/ismai/Downloads/gamesSales.txt", sep='|')
df["percent"] = (df['NA_Sales'] / df['NA_Sales'].sum()) * 100
df["percent2"] = (df['EU_Sales'] / df['EU_Sales'].sum()) * 100
df["percent3"] = (df['JP_Sales'] / df['JP_Sales'].sum()) * 100
df["percent4"] = (df['Other_Sales'] / df['Other_Sales'].sum()) * 100

pd.options.display.max_rows = 8
sg.theme('DarkBlue')


fig = plt.figure(figsize=(500, 100), dpi=400)
ax = fig.add_subplot(1, 1, 1)

labels = df['Name']
values = df['percent']

x = np.arange(len(values))
width = 0.2 # the width of the bars

fig, ax = plt.subplots()

ind = np.arange(len(labels))


ax.barh(ind, df["percent"],color='red', align='center')
ax.barh(ind, df["percent2"],color='green', align='center')
ax.barh(ind, df["percent3"],color='blue', align='center')
ax.barh(ind, df["percent4"],color='orange', align='center')
ax.set(yticks=ind + width, yticklabels=df["percent2"], ylim=[2*width - 1, len(df)])
ax.set_yticks(ind)
ax.set_yticklabels(labels)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Performance')


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

fig = plt.gcf() # if using Pyplot then get the figure from the plot
fig.set_size_inches(9,12)
figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

# ------------------------------- Beginning of GUI CODE -------------------------------

file_list_column = [
    [sg.Text(""),
     sg.Output(size=(80,20)),
     ],
]

# For now will only show the name of the file that was chosen
menu_column = [
    [sg.Text("MENU",size=(30, 1), font='Lucida',justification='left')],
    [sg.Button('visualizzare data frame')],
    [sg.InputText(key='key'),sg.Button('cerca gioco')],
    [sg.Button('prev'),sg.Button('next')],
    [sg.InputText(key='key1'),sg.Button('cerca percentuale vendita del gioco')],
    [sg.Combo(['Wii', "NES", "GB","X360","SNES","DS","3DS","PS4","PS2","2060","N64","XB","GBA","PC"], key='key2'),sg.Button('visualizza giochi')],
    [sg.Button('visualizzare totale vendite')],
    [sg.Button('visualizzare grafico a torta')],
    [sg.Button('visualizzare grafico a barre')],
    [sg.InputText(key='key3'),sg.Button('cerca nome')],
    [sg.Button('Exit')],
]

# ----- Full layout -----
layout = [
    [sg.Column(file_list_column),
     sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-'),
     sg.VSeperator(),
     sg.Column(menu_column),]
]

window = sg.Window("giochi", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif  event == 'visualizzare data frame':
        print(df)
    elif  event == 'cerca gioco':
        print(df.loc[df['Name'] == values.get("key")],"\n")
    elif  event == 'prev':
        condition = df[df["Name"]== values.get("key")].index.values
        indice = condition[0]
        print(df.iloc[indice-1])
    elif  event == 'next':
        condition = df[df["Name"]== values.get("key")].index.values
        indice = condition[0]
        print(df.iloc[indice+1])
    elif  event == 'cerca percentuale vendita del gioco':
        c = df.loc[df['Name'] == values.get("key1")]
        perc = c[["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]] / df[["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]].sum() * 100
        print(perc)
    elif  event == 'visualizza giochi':
        b = df.loc[df['Platform'] == values.get("key2")]
        print(b["Name"])
    elif  event == 'visualizzare totale vendite':
        print(df[["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]].sum())
    elif event == 'visualizzare grafico a barre':
        fig_photo = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    elif event =="cerca nome":
        print(df.loc[df['Name'].str.contains(values.get("key3"), case=False)])
window.refresh()
window.close()



window.refresh()
window.close()