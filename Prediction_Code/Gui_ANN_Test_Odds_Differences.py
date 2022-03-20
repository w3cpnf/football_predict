import os
os.chdir('D:/Projects/Football/Prediction_Code')
#https://mljar.com/blog/feature-importance-in-random-forest/

import pandas as pd
from pandastable import Table
#import pandas as pd

import Get_ANN as ann
import My_Tools_Prediction as t
import Read_Load_Prediction as db

from tkinter import *
from tkinter import ttk

main = Tk()
main.title("Parameter Choice")
main.geometry("+40+60")
frame = ttk.Frame(main, padding=(120, 120, 200, 200))
frame.grid(column=0, row=0, sticky=(N, S, E, W))


frame.grid_columnconfigure(4, minsize=250) 

variables = StringVar()
values_spieltag = StringVar()
values_saisons = StringVar()
values_vereins_id = StringVar()
values_smaller_bigger = StringVar()

variables.set("Gegner_ID Kaderwert_Differenz Kaderwert_Per_Spieler_Differenz Abwehrdifferenz Gesamtdiffferenz \
            Angriffdifferenz Mittelfelddifferenz Heimangriff_Abwehr_Differenz Auswärtsangriff_Abwehr_Differenz \
            Auswärtsangriff_Abwehr_Differenz Trainer_ID Trainer_Gegner_ID B365H B365D B365A L1 L2 L3 L4 GegnerL1 GegnerL2 GegnerL3 \
            GegnerL4 GegnerL5")
            
values_spieltag.set("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34")
values_saisons.set("2019/20 2020/21 2021/22")
values_vereins_id.set("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 29 31")
values_smaller_bigger.set("1 2")

lstbox_saison = Listbox(frame, listvariable=values_saisons, selectmode=MULTIPLE, exportselection=0, width=10, height=10)
lstbox_saison.grid(column=2, row=1, columnspan=1)

lstbox_spieltage = Listbox(frame, listvariable=values_spieltag, selectmode=MULTIPLE, exportselection=0, width=5, height=10)
lstbox_spieltage.grid(column=4, row=1, columnspan=1)

lstbox_vereins_id = Listbox(frame, listvariable=values_vereins_id, selectmode=MULTIPLE, exportselection=0, width=5, height=10)
lstbox_vereins_id.grid(column=1, row=1, columnspan=1)

lstbox_variables = Listbox(frame, listvariable=variables, selectmode=MULTIPLE, exportselection=0, width=40, height=10)
lstbox_variables.grid(column=5, row=1, columnspan=1)

lstbox_smaller_bigger = Listbox(frame, listvariable=values_smaller_bigger, selectmode=MULTIPLE, exportselection=0, width=10, height=10)
lstbox_smaller_bigger.grid(column=3, row=1, columnspan=1)

def select_variables():
    variables_list = list()
    spieltag = list()
    saison_list = list()
    vereins_id_list = list()
    bigger_smaller_list = list()
    total_list = list()
    
    selection_variables = lstbox_variables.curselection()
    selection_spieltag = lstbox_spieltage.curselection()
    selection_saison = lstbox_saison.curselection()
    selection_vereins_id = lstbox_vereins_id.curselection()
    selection_bigger_smaller = lstbox_smaller_bigger.curselection()
    values = []
    
    for saison in selection_saison:
        entry_saison = lstbox_saison.get(saison)
        saison_list.append(entry_saison)

        
    for s in selection_spieltag:
        entry_spieltag = lstbox_spieltage.get(s)
        spieltag.append(entry_spieltag)

        
    for i in selection_variables:
        entry_variables = lstbox_variables.get(i)
        variables_list.append(entry_variables)

        
    for vid in selection_vereins_id:
        entry_vereins_id = lstbox_vereins_id.get(vid)
        vereins_id_list.append(entry_vereins_id)      

    for bg in selection_bigger_smaller:
        entry_bigger_smaller = lstbox_smaller_bigger.get(bg)
        bigger_smaller_list.append(entry_bigger_smaller)   
        
    for var in variables_list:
        values.append(var)


    f = db.get_data_db(1)
    df = f.get_data()
    df = df[df['Heimmannschaft_ID'] == int(vereins_id_list[0])]
    df_seasons_before = df[df['Saison'] < saison_list[0]]
    df_season_analysed = df[df['Saison'] == saison_list[0]]
    
    if int(bigger_smaller_list[0])==1:
        df_spieltag_seasons_analysed = df_season_analysed[df_season_analysed['Spieltag'] <= int(spieltag[0])]
    if int(bigger_smaller_list[0])==2:
        df_spieltag_seasons_analysed = df_season_analysed[df_season_analysed['Spieltag'] >= int(spieltag[0])]
        
    all_left_spieltage = df_spieltag_seasons_analysed['Spieltag'].drop_duplicates()

    for spieltag_left in all_left_spieltage:

        df_spieltag_lef = df_spieltag_seasons_analysed[df_spieltag_seasons_analysed['Spieltag']<=spieltag_left]
        df_analyse = df_seasons_before.append(df_spieltag_lef, ignore_index = True)
        df_analyse = df_analyse.sort_values(by = ['Saison', 'Spieltag'])
        df_results = df_analyse[['Spiel_Ausgang']]
        df_variables = df_analyse[values]
        
        df_odds = df_season_analysed[df_season_analysed['Spieltag']==spieltag_left]
        print(df_odds.columns)
        home_odds = df_odds['B365H'].iloc[0]
        draw_odds = df_odds['B365D'].iloc[0]
        away_odds = df_odds['B365A'].iloc[0]

        total = ann.ann_for_tool(df_results, df_variables, home_odds, draw_odds, away_odds)
        total_list.append(total)
    print(total_list)
    print(sum(total_list))
    print("Done")
btn = ttk.Button(frame, text="Test Selection", command=select_variables)
btn.grid(column=1, row=2)

label_season = Label(frame, text="Seasons")
label_season.grid(column=2, row=0)
label_spieltag = Label(frame, text="Matchdays")
label_spieltag.grid(column=4, row=0)
label_clubs = Label(frame, text="Clubs")
label_clubs.grid(column=1, row=0)
label_variables = Label(frame, text="Variables")
label_variables.grid(column=5, row=0)
label_smaller_bigger = Label(frame, text="1 smaller 2 bigger")
label_smaller_bigger.grid(column=3, row=0)
main.mainloop()