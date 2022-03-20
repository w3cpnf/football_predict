import os
os.chdir('D:/Projects/Football/Database/DQ_Code')

import tkinter as tk
#import pandas as pd

import DQ_Players as dq

#define dashboard method and size/height
root = tk.Tk(className = "DQ check for Players")
canvas = tk.Canvas(root, height = 900, width = 1200)
canvas.pack()

def kader_check():
    dq.check_kader()

def worth_age_check():
    dq.check_age_worth()
    
def url_check():
    dq.check_url()
    
def mapping_player_master_check():
    dq.check_master_player_config()

def player_staging_daten_check():
    dq.check_player_staging_daten()

def player_data_daten_check():
    dq.check_player_data_daten()

def player_kicker_check():
    dq.check_kicker_daten()

def player_kader_duplicate_check_dashboard():
    dq.player_kader_duplicate_check()
    
def player_mapping_config_duplicate_check_dashboard():
    dq.player_mapping_config_duplicate_check()
    
def player_staging_daten_duplicate_check_dashboard():
    dq.player_staging_daten_duplicate_check()
    
def player_data_daten_duplicate_check_dashboard():
    dq.player_data_daten_duplicate_check()

def kicker_duplicate_check_dashboard():
    dq.kicker_duplicate_check()
    
def master_player_check():
    dq.check_master_player()   

def performance_check():
    dq.check_perf_daten()

def startelf_check():
    dq.check_perf_daten()
    
def injuries_check():
    dq.check_injuries_daten()
    
def injuries_staging_check():
    dq.check_injuries_staging()
    
#headline
headliner_label = tk.Label(root, text = 'DQ check for Players', font=('calibre', 14, 'bold')) 
headliner_label.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.1) 

#kader
button_kader_check = tk.Button(root, text = 'bl1_staging_spieler_kader',command = kader_check)
button_kader_check.pack()
button_kader_check.place(relx = 0.1, rely = 0.2, relwidth = 0.2, relheight = 0.05)

#worth_age
button_kader_check = tk.Button(root, text = 'bl1_data_spieler_wert_alter',command = worth_age_check)
button_kader_check.pack()
button_kader_check.place(relx = 0.1, rely = 0.25, relwidth = 0.2, relheight = 0.05)

#url
button_kader_check = tk.Button(root, text = 'bl1_mapping_ligainsider',command = url_check)
button_kader_check.pack()
button_kader_check.place(relx = 0.1, rely = 0.3, relwidth = 0.2, relheight = 0.05)

#master_player_check
button_kader_check = tk.Button(root, text = 'master_spieler_id',command = master_player_check)
button_kader_check.pack()
button_kader_check.place(relx = 0.1, rely = 0.35, relwidth = 0.2, relheight = 0.05)

#config_check 
button_master_player_config_check = tk.Button(root, text = 'bl1_master_spieler_config',command = mapping_player_master_check)
button_master_player_config_check.pack()
button_master_player_config_check.place(relx = 0.1, rely = 0.4, relwidth = 0.2, relheight = 0.05)

#check staging data
button_staging_player_data_duplicate_check = tk.Button(root, text = 'bl1_staging_spieler_daten',command = player_staging_daten_check)
button_staging_player_data_duplicate_check.pack()
button_staging_player_data_duplicate_check.place(relx = 0.1, rely = 0.45, relwidth = 0.2, relheight = 0.05)

#check data player
button_data_player_data_check = tk.Button(root, text = 'bl1_data_spieler_daten',command = player_data_daten_check)
button_data_player_data_check.pack()
button_data_player_data_check.place(relx = 0.1, rely = 0.5, relwidth = 0.2, relheight = 0.05)#

#Kicker
button_kicker_check = tk.Button(root, text = 'bl1_data_spieler_kicker_position',command = player_kicker_check)
button_kicker_check.pack()
button_kicker_check.place(relx = 0.1, rely = 0.55, relwidth = 0.2, relheight = 0.05)

#Performance
button_kicker_check = tk.Button(root, text = 'bl1_data_spieler_performance',command = performance_check)
button_kicker_check.pack()
button_kicker_check.place(relx = 0.1, rely = 0.6, relwidth = 0.2, relheight = 0.05)

#startelf
button_kicker_check = tk.Button(root, text = 'bl1_data_spieler_startelf_system',command = startelf_check)
button_kicker_check.pack()
button_kicker_check.place(relx = 0.1, rely = 0.65, relwidth = 0.2, relheight = 0.05)

#injuries
button_injuries_check = tk.Button(root, text = 'bl1_data_spieler_verletzt',command = injuries_check)
button_injuries_check.pack()
button_injuries_check.place(relx = 0.1, rely = 0.7, relwidth = 0.2, relheight = 0.05)

#injuries staging
button_injuries_staging_check = tk.Button(root, text = 'bl1_staging_spieler_verletzt',command = injuries_staging_check)
button_injuries_staging_check.pack()
button_injuries_staging_check.place(relx = 0.1, rely = 0.75, relwidth = 0.2, relheight = 0.05)

#Duplicate check Config
button_master_player_config_duplicate_check = tk.Button(root, text = 'bl1_master_spieler_config Duplicate Check',command = player_mapping_config_duplicate_check_dashboard)
button_master_player_config_duplicate_check.pack()
button_master_player_config_duplicate_check.place(relx = 0.35, rely = 0.2, relwidth = 0.2, relheight = 0.05)

#Duplicate check Kader
button_kader_check_duplicate = tk.Button(root, text = 'bl1_staging_spieler_kader Duplicate Check',command = player_kader_duplicate_check_dashboard)
button_kader_check_duplicate.pack()
button_kader_check_duplicate.place(relx = 0.35, rely = 0.25, relwidth = 0.2, relheight = 0.05)

#Duplicate check staging data
button_staging_player_data_duplicate_check = tk.Button(root, text = 'bl1_staging_spieler_daten Duplicate Check',command = player_staging_daten_duplicate_check_dashboard)
button_staging_player_data_duplicate_check.pack()
button_staging_player_data_duplicate_check.place(relx = 0.35, rely = 0.3, relwidth = 0.2, relheight = 0.05)

root.mainloop()