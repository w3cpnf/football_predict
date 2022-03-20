import os
os.chdir('D:/Projects/Football/Prediction_Code')


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
 
variables.set("Gegner_ID Kaderwert_Differenz Kaderwert_Per_Spieler_Differenz Abwehrdifferenz Gesamtdiffferenz \
            Angriffdifferenz Mittelfelddifferenz Heimangriff_Abwehr_Differenz Auswärtsangriff_Abwehr_Differenz \
            Auswärtsangriff_Abwehr_Differenz Trainer_ID Gegner_Trainer_ID B365H B365A B365D HeimSystem AuswärtsSystem \
            L1 L2 L3 L4 L5  GegnerL1 GegnerL2 GegnerL3 GegnerL4 GegnerL5")
            
values_spieltag.set("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34")
values_saisons.set("2019/20 2020/21 2021/22")
values_vereins_id.set("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 26 29 31")

lstbox_saison = Listbox(frame, listvariable=values_saisons, selectmode=MULTIPLE, exportselection=0, width=10, height=10)
lstbox_saison.grid(column=1, row=1, columnspan=1)

lstbox_spieltage = Listbox(frame, listvariable=values_spieltag, selectmode=MULTIPLE, exportselection=0, width=5, height=10)
lstbox_spieltage.grid(column=2, row=1, columnspan=1)

lstbox_vereins_id = Listbox(frame, listvariable=values_vereins_id, selectmode=MULTIPLE, exportselection=0, width=5, height=10)
lstbox_vereins_id.grid(column=3, row=1, columnspan=1)

lstbox_variables = Listbox(frame, listvariable=variables, selectmode=MULTIPLE, exportselection=0, width=40, height=10)
lstbox_variables.grid(column=4, row=1, columnspan=1)



def select_variables():
    
    variables_list = list()
    spieltag = list()
    saison_list = list()
    vereins_id_list = list()
    
    selection_variables = lstbox_variables.curselection()
    selection_spieltag = lstbox_spieltage.curselection()
    selection_saison = lstbox_saison.curselection()
    selection_vereins_id = lstbox_vereins_id.curselection()
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

        
    for var in variables_list:
        values.append(var)


    f1 = db.get_data_db(12)
    df1 = f1.get_data()

    f2 = db.get_data_db(13)
    df2 = f2.get_data()

    df = df1.merge(df2, on = ['Saison', 'Spieltag', 'Heimmannschaft', 'Heimmannschaft_ID', 'Gegner_ID'])
    df = df.sort_values(['Saison', 'Spieltag'])


    df = df[df['Heimmannschaft_ID']==int(vereins_id_list[0])]
    df_seasons_before = df[df['Saison'] < saison_list[0]]
    df_season_chosen = df[df['Saison'] == saison_list[0]]
    
    df_season_chosen = df_season_chosen[df_season_chosen['Spieltag']<int(spieltag[0])]
    df_analyse = df_seasons_before.append(df_season_chosen, ignore_index = True)
    
    df_analyse = df_analyse.sort_values(by = ['Saison', 'Spieltag'])
    
    results = df_analyse[['Spiel_Ausgang']].values
    variables = df_analyse[values].values

    f_1 = db.get_data_db(2)
    df_forecast = f_1.get_data()
    
    df_forecast = df_forecast[df_forecast['Saison']==saison_list[0]]
    df_forecast = df_forecast[df_forecast['Spieltag']==int(spieltag[0])]
    df_forecast = df_forecast[df_forecast['Heimmannschaft_ID']==int(vereins_id_list[0])]
    
    home_team = df_forecast['Heimmannschaft'].iloc[0]
    away_team = df_forecast['Gegner'].iloc[0]
    #away_team_id = df_forecast['Gegner_ID'].iloc[0]
    
    # if 'Gegner_ID' in values:
    #     df_gegner = df_analyse[df_analyse['Gegner_ID']==away_team_id]
    #     df_gegner['Gegner_ID'] = 1
    #     df_not_gegner = df_analyse[df_analyse['Gegner_ID']!=away_team_id]
    #     df_not_gegner['Gegner_ID'] = 0    
    #     df_analyse = df_gegner.append(df_not_gegner)  
        
    #df_forecast['Gegner_ID'] = 1          
    forecast = df_forecast[values].values
    ann.get_best_ann(forecast, variables, results, home_team, away_team)


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


main.mainloop()