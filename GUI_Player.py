import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

import tkinter as tk
import pandas as pd

import Get_Kader as k
import Read_Load_Database as db 
import Get_Kicker as kicker
import Get_Ligainsider as l
import Get_Ligainsider_Url as l_url
import Get_Ligainsider_Data as ld
import Get_Injuries as injuries
import Get_System_Team as s
import Get_Master_Spieler_Config as ms

#define dashboard method and size/height
root = tk.Tk(className = "Data Provider for player")
canvas = tk.Canvas(root, height = 900, width = 1200)
canvas.pack()

#comments
get_player_comment = tk.Label(root, text = 'Club nbr from 1-18'+ '\n' + 'and Saison', font=('calibre', 8)) 
new_player_comment = tk.Label(root, text = 'Dataframe from clubs'+ '\n' + 'and Saison', font=('calibre', 8)) 
kader_comment = tk.Label(root, text = 'Dataframe from clubs'+ '\n' + 'season, transferwindow', font=('calibre', 8)) 
player_worth_comment = tk.Label(root, text = 'Dataframe from clubs', font=('calibre', 8)) 
get_url_comment = tk.Label(root, text = 'Club nbr and saison', font=('calibre', 8)) 

get_injuries_comment = tk.Label(root, text = 'Needs Club nbr from 1-18'+ '\n' + 'saison, and transferwindow', font=('calibre', 8)) 
get_injuries_comment_data = tk.Label(root, text = 'Needs Club nbr from 1-18'+ '\n' + 'saison, and transferwindow', font=('calibre', 8))
get_perf_index_comment = tk.Label(root, text = 'Needs URL of recent matchday', font=('calibre', 8))

get_ligainsider_comment = tk.Label(root, text = 'Needs Club nbr from 1-18'+ '\n' + 'saison, saison_1', font=('calibre', 8))
get_ligainsider_comment_data = tk.Label(root, text = 'Needs Club nbr from 1-18'+ '\n' + 'saison', font=('calibre', 8))

get_kicker_comment_data = tk.Label(root, text = 'Needs ClubNbr, saison, Saison_kicker'+ '\n' + 'Spieltag, Transferfenster', font=('calibre', 8))
get_system_comment_data = tk.Label(root, text = 'Needs ClubNbr, saison'+ '\n' + 'Saison_kicker, Spieltag', font=('calibre', 8))

get_palyer_matchday_comment_data = tk.Label(root, text = 'Needs ClubNbr, saison'+ '\n' + 'Transferwindow', font=('calibre', 8))

headliner_label = tk.Label(root, text = 'Data Provider for player', font=('calibre', 14, 'bold')) 
headliner_label.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.1) 

#entries
entry_spieltag = tk.Entry()
club_nbr_entry = tk.Entry()
transferfenster_entry = tk.Entry()
saison_entry = tk.Entry()
url_entry = tk.Entry()
saison_entry_1 = tk.Entry()


#labels
saison_label = tk.Label(root, text = 'Season', font=('calibre', 10, 'bold')) 
spieltag_label = tk.Label(root, text = 'Gameday', font=('calibre', 10, 'bold'))
club_label = tk.Label(root, text = 'Club_Nbr (1 to 18)', font=('calibre', 10, 'bold'))
transferfenster_label = tk.Label(root, text = 'Transferfenster', font=('calibre', 10, 'bold'))
url_label = tk.Label(root, text = 'Perf URL', font=('calibre', 10, 'bold'))


#placement of labels and entries
url_label.place(relx = 0.05, rely = 0.2, relwidth = 0.1, relheight = 0.1)
url_entry.place(relx = 0.16, rely = 0.24, relwidth = 0.3, relheight = 0.02)

club_label.place(relx =  0.25, rely = 0.12, relwidth = 0.1, relheight = 0.1)
club_nbr_entry.place(relx = 0.37, rely = 0.16, relwidth = 0.05, relheight = 0.02)

saison_label.place(relx = 0.55, rely = 0.24, relwidth = 0.1, relheight = 0.02)
saison_entry.place(relx = 0.65, rely = 0.24, relwidth = 0.05, relheight = 0.02)

spieltag_label.place(relx = 0.05, rely = 0.12, relwidth = 0.1, relheight = 0.1) 
entry_spieltag.place(relx = 0.15, rely = 0.16, relwidth = 0.05, relheight = 0.02)

transferfenster_label.place(relx = 0.55, rely = 0.16, relwidth = 0.1, relheight = 0.02)
transferfenster_entry.place(relx = 0.65, rely = 0.16, relwidth = 0.05, relheight = 0.02)





def get_all_players():
    #define global dataframe (can be used in other functions)
    global df_all_players
    df_all_players = pd.DataFrame()
    club = int(club_nbr_entry.get())
    saison = saison_entry.get()
    #call class of the file get_gameplan
    df = k.get_kader(club, saison)
    #add data to global dataframe
    df_all_players = df_all_players.append(df)
    
    print("done")
    
    
def get_new_players():
    #define global dataframe (can be used in other functions)
    global df_new_players
    df_new_players = pd.DataFrame()
    #call class of the file get_gameplan
    df = k.get_new_player(df_all_players)
    #add data to global dataframe
    df_new_players = df_new_players.append(df)
    print("done")   
    
    
def upload_new_player():
    db.upload_local_data_to_database(df_new_players, 'master_spieler_id')
    print("Data successfuly uploaded")
    
    
def get_kader():
    #define global dataframe (can be used in other functions)
    global df_kader
    df_kader = pd.DataFrame()
    saison = saison_entry.get()
    timewindow = int(transferfenster_entry.get())
    #call class of the file get_gameplan
    df = k.get_kader_club(df_all_players, saison, timewindow)
    df_kader = df_kader.append(df)
    
    print("done")  


def upload_kader():
    db.upload_local_data_to_database(df_kader, 'bl1_staging_spieler_kader')
    print("Data successfuly uploaded")


def get_wert_alter():
    #define global dataframe (can be used in other functions)
    global df_wert_alter
    df_wert_alter = pd.DataFrame()
    saison = saison_entry.get()
    club = int(club_nbr_entry.get())
    #call class of the file get_gameplan
    df = k.get_Wert_Alter(df_all_players, saison, club)
    df_wert_alter = df_wert_alter.append(df)

    print("done")  


def upload_spieler_wert_alter():
    db.upload_local_data_to_database(df_wert_alter, 'bl1_data_spieler_wert_alter')
    #db.upload_local_db_data(df_wert_alter, 7)
    print("Data successfuly uploaded")


def get_ligainsider_url():
    global df_url
    saison = saison_entry.get()

    club = int(club_nbr_entry.get())
    
    df_url = l_url.get_url_via_google(saison, club)
    print("Done")

def upload_ligainsider_url():
    db.upload_local_db_data(df_url, 11)    
    print("Data successfuly uploaded")

def get_injuries_players():
    #define global dataframe (can be used in other functions)
    global df_injuries_players
    df_injuries_players = pd.DataFrame()   
    saison = saison_entry.get()
    timewindow = int(transferfenster_entry.get())
    club = int(club_nbr_entry.get())
    
    #call class 
    df = injuries.get_verletzungen(saison, timewindow, club)
    #add data to global dataframe
    df_injuries_players = df_injuries_players.append(df)
    print("done")   
    
def prepare_injuries_players():
    global df_injuries
    df_injuries = injuries.prep_ver_upload(df_injuries_players)
        
def upload_injuries_players():
    db.upload_local_db_data(df_injuries, 23)
    print("Data successfuly uploaded")

def get_injuries_players_data():
    #define global dataframe (can be used in other functions)
    global df_injuries_players_data
    df_injuries_players_data = pd.DataFrame()   
    saison = saison_entry.get()
    timewindow = int(transferfenster_entry.get())
    club = int(club_nbr_entry.get())
    #call class 
    df = injuries.get_injuries_data_format(saison, timewindow, club)
    #add data to global dataframe
    df_injuries_players_data = df_injuries_players_data.append(df)
    print("done")   

def upload_injuries_players_data():
    db.upload_local_db_data(df_injuries_players_data, 27)
    print("Data successfuly uploaded")

def get_ligainsider_players():
    #define global dataframe (can be used in other functions)
    global df_ligainsider_players
    df_ligainsider_players = pd.DataFrame()   
    #call class 
    #saison_1 = saison_entry_1.get()
    saison = saison_entry.get()
    club = int(club_nbr_entry.get())
    spieltag = int(entry_spieltag.get())
    
    df = ld.get_bundesliga_player_daten(saison, club, spieltag)
    
    #add data to global dataframe
    df_ligainsider_players = df_ligainsider_players.append(df)
    print("done")   

def upload_ligainsider_players():
    db.upload_local_db_data(df_ligainsider_players, 22)
    print("Data successfuly uploaded")

def get_data_ligainsider_players():
    #define global dataframe (can be used in other functions)
    global df_ligainsider_data_players
    df_ligainsider_data_players = pd.DataFrame()   
    #call class 
    saison = saison_entry.get()
    club = int(club_nbr_entry.get())
    spieltag = int(entry_spieltag.get())
    df = ld.get_data_ligainsider(saison, club, spieltag)
    #add data to global dataframe
    df_ligainsider_data_players = df_ligainsider_data_players.append(df)
    print("done")   

def upload_data_ligainsider_players():
    db.upload_local_db_data(df_ligainsider_data_players, 28)
    print("Data successfuly uploaded")

def get_kicker_players():
    #define global dataframe (can be used in other functions)
    global df_kicker_players
    df_kicker_players = pd.DataFrame()
    #get entries
    saison = saison_entry.get()
    spieltag = int(entry_spieltag.get())
    club = int(club_nbr_entry.get())

    #call class 
    df = kicker.get_kicker(spieltag, saison, club)
    
    #add data to global dataframe
    df_kicker_players = df_kicker_players.append(df)
    print("done")   
    

def upload_kicker_players():
    db.upload_local_db_data(df_kicker_players, 9)
    print("Data successfuly uploaded")
    
    
def get_perf_players():
    #define global dataframe (can be used in other functions)
    global df_perf_players
    df_perf_players = pd.DataFrame()
    #get entries
    spieltag = int(entry_spieltag.get())
    saison = saison_entry.get()
    url = url_entry.get()
    #call class 
    df = l.get_perf_index(spieltag, url, saison)
    #add data to global dataframe
    df_perf_players = df_perf_players.append(df)
    print("done")   
    
def check_perf_players():
    print(len(df_perf_players))
    print(df_perf_players)
    
def upload_perf_players():
    db.upload_local_data_to_database(df_perf_players, 'bl1_data_spieler_performance')
    print("Data successfuly uploaded")
       
    
def get_system():
    #define global dataframe (can be used in other functions)
    global df_system
    df_system = pd.DataFrame()   
    #call class 
    df = s.get_system_aufstellung()
    #add data to global dataframe
    df_system = df_system.append(df)
    print("done")   
     
def upload_system():
    db.upload_local_db_data(df_system, 24)
    
    
def get_player_per_gamedata():
    #define global dataframe (can be used in other functions)
    global df_player_gamedata
    df_player_gamedata = pd.DataFrame()  
    saison = saison_entry.get()
    club = int(club_nbr_entry.get())
    timewindow = int(transferfenster_entry.get())
    #call class 
    df = ms.get_player_config(club, saison, timewindow)
    #add data to global dataframe
    df_player_gamedata = df_player_gamedata.append(df)
    print("done")   
     
def upload_player_per_gamedata():
    db.upload_local_data_to_database(df_player_gamedata, 'bl1_master_spieler_config') 
    print("Data succesfully uploaded")
    
    
#kader 
button_get_all_players = tk.Button(root, text = 'Get all players',command = get_all_players)
button_get_all_players.pack()
button_new_player = tk.Button(root, text = 'Get new players',command = get_new_players)
button_new_player.pack()
button_upload_new_players= tk.Button(root, text = 'Upload new players',command = upload_new_player)
button_upload_new_players.pack()

button_get_kader= tk.Button(root, text = 'Get team',command = get_kader)
button_get_kader.pack()
button_upload_kader = tk.Button(root, text = 'Upload team',command = upload_kader)
button_upload_kader.pack()

button_get_worth_age= tk.Button(root, text = 'Get worth and age',command = get_wert_alter)
button_get_worth_age.pack()
button_upload_worth_age = tk.Button(root, text = 'Upload worth and age',command = upload_spieler_wert_alter)
button_upload_worth_age.pack()

#kicker 
button_get_kicker = tk.Button(root, text = 'Get Kicker information',command = get_kicker_players)
button_get_kicker.pack()
button_upload_kicker = tk.Button(root, text = 'Upload Kicker information',command = upload_kicker_players)
button_upload_kicker.pack()

#perf
button_get_perf_index = tk.Button(root, text = 'Get Perf Index',command = get_perf_players)
button_get_perf_index.pack()
button_upload_perf_index = tk.Button(root, text = 'Upload Perf Index',command = upload_perf_players)
button_upload_perf_index.pack()

#url
button_ligainsider_url = tk.Button(root, text = 'Get Url Ligainsider',command = get_ligainsider_url)
button_ligainsider_url.pack()
button_upload_ligainsider_url = tk.Button(root, text = 'Upload Url Ligainsider',command = upload_ligainsider_url)
button_upload_ligainsider_url.pack()


#perf
button_get_ligainsider= tk.Button(root, text = 'Get Player Data',command = get_ligainsider_players)
button_get_ligainsider.pack()
button_upload_ligainsider = tk.Button(root, text = 'Upload Player Data',command = upload_ligainsider_players)
button_upload_ligainsider.pack()

button_get_data_ligainsider= tk.Button(root, text = 'Transform To Player Data',command = get_data_ligainsider_players)
button_get_data_ligainsider.pack()
button_upload_data_ligainsider = tk.Button(root, text = 'Upload Tranformed Player Data',command = upload_data_ligainsider_players)
button_upload_data_ligainsider.pack()

#injuries
button_get_injuries= tk.Button(root, text = 'Get Injuries staging',command = get_injuries_players)
button_get_injuries.pack()
button_prepare_injuries = tk.Button(root, text = 'Prepare Injuries staging',command = prepare_injuries_players)
button_prepare_injuries.pack()
button_upload_injuries = tk.Button(root, text = 'Upload Injuries staging',command = upload_injuries_players)
button_upload_injuries.pack()
button_get_injuries_data= tk.Button(root, text = 'Get Injuries data',command = get_injuries_players_data)
button_get_injuries.pack()
button_upload_injuries_data = tk.Button(root, text = 'Upload Injuries data',command = upload_injuries_players_data)
button_upload_injuries_data.pack()

#System
button_get_system = tk.Button(root, text = 'Get System Data',command = get_system)
button_get_system.pack()
button_upload_system = tk.Button(root, text = 'Upload System Data',command = upload_system)
button_upload_system.pack()

#Player for club per gameday
button_player_gameday = tk.Button(root, text = 'Get Player Per Gameday',command = get_player_per_gamedata)
button_player_gameday.pack()
button_player_gameday_upload = tk.Button(root, text = 'Upload Player Per Gameday',command = upload_player_per_gamedata)
button_player_gameday_upload.pack()


get_player_comment.place(relx = -0.03, rely = 0.3, relwidth = 0.3, relheight = 0.05)
button_get_all_players.place(relx = 0.05, rely = 0.35, relwidth = 0.14, relheight = 0.05)

new_player_comment.place(relx = 0.2, rely = 0.3, relwidth = 0.14, relheight = 0.05)
button_new_player.place(relx = 0.2, rely = 0.35, relwidth = 0.14, relheight = 0.05)
button_upload_new_players.place(relx = 0.2, rely = 0.4, relwidth = 0.14, relheight = 0.05)

kader_comment.place(relx = 0.32, rely = 0.3, relwidth = 0.2, relheight = 0.05)
button_get_kader.place(relx = 0.35, rely = 0.35, relwidth = 0.14, relheight = 0.05)
button_upload_kader.place(relx = 0.35, rely = 0.4, relwidth = 0.14, relheight = 0.05)

player_worth_comment.place(relx = 0.48, rely = 0.3, relwidth = 0.2, relheight = 0.05)
button_get_worth_age.place(relx = 0.5, rely = 0.35, relwidth = 0.14, relheight = 0.05)
button_upload_worth_age.place(relx = 0.5, rely = 0.4, relwidth = 0.14, relheight = 0.05)

get_url_comment.place(relx = 0.63, rely = 0.3, relwidth = 0.2, relheight = 0.05)
button_ligainsider_url.place(relx = 0.65, rely = 0.35, relwidth = 0.14, relheight = 0.05)
button_upload_ligainsider_url.place(relx = 0.65, rely = 0.4, relwidth = 0.14, relheight = 0.05)

get_injuries_comment.place(relx = 0.0, rely = 0.5, relwidth = 0.2, relheight = 0.05)
button_get_injuries.place(relx = 0.05, rely = 0.55, relwidth = 0.14, relheight = 0.05)
button_prepare_injuries.place(relx = 0.05, rely = 0.6, relwidth = 0.14, relheight = 0.05)
button_upload_injuries.place(relx = 0.05, rely = 0.65, relwidth = 0.14, relheight = 0.05)

get_injuries_comment_data.place(relx = 0.17, rely = 0.5, relwidth = 0.2, relheight = 0.05)
button_get_injuries_data.place(relx =0.2, rely = 0.55, relwidth = 0.14, relheight = 0.05)
button_upload_injuries_data.place(relx =0.2, rely = 0.6, relwidth = 0.14, relheight = 0.05)

get_perf_index_comment.place(relx = 0.32, rely = 0.5, relwidth = 0.2, relheight = 0.05)
button_get_perf_index.place(relx = 0.35, rely = 0.55, relwidth = 0.14, relheight = 0.05)
button_upload_perf_index.place(relx = 0.35, rely = 0.6, relwidth = 0.14, relheight = 0.05)

get_ligainsider_comment.place(relx = 0.48, rely = 0.5, relwidth = 0.2, relheight = 0.05)
button_get_ligainsider.place(relx = 0.5, rely = 0.55, relwidth = 0.14, relheight = 0.05)
button_upload_ligainsider.place(relx = 0.5, rely = 0.6, relwidth = 0.14, relheight = 0.05)

get_ligainsider_comment_data.place(relx = 0.62, rely = 0.5, relwidth = 0.2, relheight = 0.05)
button_get_data_ligainsider.place(relx = 0.65, rely = 0.55, relwidth = 0.14, relheight = 0.05)
button_upload_data_ligainsider.place(relx = 0.65, rely = 0.6, relwidth = 0.14, relheight = 0.05)

get_kicker_comment_data.place(relx = 0.02, rely = 0.75, relwidth = 0.2, relheight = 0.05)
button_get_kicker.place(relx = 0.05, rely = 0.8, relwidth = 0.14, relheight = 0.05)
button_upload_kicker.place(relx = 0.05, rely = 0.85, relwidth = 0.14, relheight = 0.05)

get_system_comment_data.place(relx = 0.17, rely = 0.75, relwidth = 0.2, relheight = 0.05)
button_get_system.place(relx = 0.2, rely = 0.8, relwidth = 0.14, relheight = 0.05)
button_upload_system.place(relx = 0.2, rely = 0.85, relwidth = 0.14, relheight = 0.05)

get_palyer_matchday_comment_data.place(relx = 0.47, rely = 0.75, relwidth = 0.2, relheight = 0.05)
button_player_gameday.place(relx = 0.5, rely = 0.8, relwidth = 0.14, relheight = 0.05)
button_player_gameday_upload.place(relx = 0.5, rely = 0.85, relwidth = 0.14, relheight = 0.05)
root.mainloop()




