import os
os.chdir('D:/Projects/Football/Prediction_Code')


import pandas as pd
from pandastable import Table
#import pandas as pd

import Get_RandomForest_Prediction as rp
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
values_n = StringVar()
values_criterion = StringVar()
values_prediction_length = StringVar()

variables.set("Gegner_ID Kaderwert_Differenz Kaderwert_Per_Spieler_Differenz Abwehrdifferenz Gesamtdiffferenz \
            Angriffdifferenz Mittelfelddifferenz Heimangriff_Abwehr_Differenz Auswärtsangriff_Abwehr_Differenz \
            Auswärtsangriff_Abwehr_Differenz Trainer_ID Trainer_Gegner_ID B365H B365D B365A L1 L2 L3 L4 \
            GegnerL1 GegnerL2 GegnerL3 GegnerL4 GegnerL5")

#index_ = [100, 500, 1000, 2000, 5000, 10000]
values_spieltag.set("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34")
values_saisons.set("2019/20 2020/21 2021/22")
values_vereins_id.set("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18")
values_n.set("1 2 3 4 5 6")
values_criterion.set("gini entropy")
values_prediction_length.set("1 2 3 4 5 10 15 18 20 25 30 34")

lstbox_saison = Listbox(frame, listvariable=values_saisons, selectmode=MULTIPLE, exportselection=0, width=10, height=10)
lstbox_saison.grid(column=1, row=1, columnspan=1)

lstbox_spieltage = Listbox(frame, listvariable=values_spieltag, selectmode=MULTIPLE, exportselection=0, width=5, height=10)
lstbox_spieltage.grid(column=2, row=1, columnspan=1)

lstbox_vereins_id = Listbox(frame, listvariable=values_vereins_id, selectmode=MULTIPLE, exportselection=0, width=5, height=10)
lstbox_vereins_id.grid(column=3, row=1, columnspan=1)

lstbox_variables = Listbox(frame, listvariable=variables, selectmode=MULTIPLE, exportselection=0, width=40, height=10)
lstbox_variables.grid(column=4, row=1, columnspan=1)

lstbox_n = Listbox(frame, listvariable=values_n, selectmode=MULTIPLE, exportselection=0, width=10, height=10)
lstbox_n.grid(column=5, row=1, columnspan=1)

lstbox_criterion = Listbox(frame, listvariable=values_criterion, selectmode=MULTIPLE, exportselection=0, width=10, height=10)
lstbox_criterion.grid(column=6, row=1, columnspan=1)

lstbox_prediction_length = Listbox(frame, listvariable=values_prediction_length, selectmode=MULTIPLE, exportselection=0, width=10, height=10)
lstbox_prediction_length.grid(column=7, row=1, columnspan=1)

def select_variables():
    
    variables_list = list()
    spieltag = list()
    saison_list = list()
    vereins_id_list = list()
    n_list = list()
    criterion_list = list()
    prediction_length_list = list()

    selection_variables = lstbox_variables.curselection()
    selection_spieltag = lstbox_spieltage.curselection()
    selection_saison = lstbox_saison.curselection()
    selection_vereins_id = lstbox_vereins_id.curselection()
    selection_n = lstbox_n.curselection()
    selection_criterion = lstbox_criterion.curselection()
    selection_length_list = lstbox_prediction_length.curselection()
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

    for n in selection_n:
        entry_n = lstbox_n.get(n)
        n_list.append(entry_n)   

    for c in selection_criterion:
        entry_criterion = lstbox_criterion.get(c)
        criterion_list.append(entry_criterion)  

    for p in selection_length_list:
        entry_length = lstbox_prediction_length.get(p)
        prediction_length_list.append(entry_length)  
        
    for var in variables_list:
        values.append(var)


    f = db.get_data_db(3)
    df = f.get_data()

    df = df[df['Heimmannschaft_ID']==int(vereins_id_list[0])]
    df_seasons_before = df[df['Saison'] < saison_list[0]]
    df_season_chosen = df[df['Saison'] == saison_list[0]]
    
    df_season_chosen = df_season_chosen[df_season_chosen['Spieltag']<=int(spieltag[0])]
    df_analyse = df_seasons_before.append(df_season_chosen, ignore_index = True)
    df_analyse = df_analyse.sort_values(by = ['Saison', 'Spieltag'])
    
    df_results = df_analyse[['Spiel_Ausgang']]
    df_analyse = df_analyse[values]
    
    if int(entry_n[0])==1:
        n_ = 100
    if int(entry_n[0])==2:
        n_ = 500
    if int(entry_n[0])==3:
        n_ = 1000
    if int(entry_n[0])==4:
        n_ = 2000
    if int(entry_n[0])==5:
        n_ = 5000
    if int(entry_n[0])==6:
        n_ = 10000
      
    criterion = criterion_list[0]
    length = int(prediction_length_list[0])
    
    X_train = df_analyse.iloc[:,:].values[:-length]
    X_test = df_analyse.iloc[:,:].values[-length:]
    y_train = df_results.iloc[:,:].values[:-length].ravel()
    y_test = df_results.iloc[:,:].values[-length:].ravel()

    rp.random_forest_score(X_train, X_test, y_train, y_test, n_, criterion)


btn = ttk.Button(frame, text="Test Selection", command=select_variables)
btn.grid(column=1, row=2)

label_season = Label(frame, text="Seasons")
label_season.grid(column=1, row=0)
label_spieltag = Label(frame, text="Matchdays")
label_spieltag.grid(column=2, row=0)
label_clubs = Label(frame, text="Clubs")
label_clubs.grid(column=3, row=0)
label_variables = Label(frame, text="Variables")
label_variables.grid(column=4, row=0)
label_n = Label(frame, text="Tree Nodes")
label_n.grid(column=5, row=0)
label_criterion = Label(frame, text="Criterion")
label_criterion.grid(column=6, row=0)
label_length = Label(frame, text="Test Set Length")
label_length.grid(column=7, row=0)
main.mainloop()