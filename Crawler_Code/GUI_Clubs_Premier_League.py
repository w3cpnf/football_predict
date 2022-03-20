import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

import tkinter as tk
import pandas as pd

#import files
import Get_Results as Results 
import Read_Load_Database as db
import Get_Gameplan as gp
import Get_Fifa_Features as ff
import Get_Gamedata as gd
import Get_Gamedata_BL1 as gdbl
import Get_Trainer as trainer
import Get_Club_Value as cv
import Get_Referees as Ref
import Get_Form_Club_Feature as cf
import Get_Football_Data_Gov as f
import Get_Game_Data_Features as d
#define dashboard method and size/height
root = tk.Tk(className = "Data Provider for club level, referees and trainer")
canvas = tk.Canvas(root, height = 900, width = 1200)
canvas.pack()



fifa_entry = tk.Entry()

fifa_label = tk.Label(root, text = 'Fifa Url', font=('calibre', 10, 'bold'))

#define button function 
def get_gameplan():
    #define global dataframe (can be used in other functions)
    global df_gameplan
    df_gameplan = pd.DataFrame()
    #get entries of values in GUI
    spieltag = entry_spieltag.get()
    saison = entry_saison.get()
    gameplan = int(entry_gameplan.get())
    #call class of the file get_gameplan
    f = gp.spielplan_premier_leauge(spieltag, gameplan, saison)
    df = f.get_spielplan()
    #add data to global dataframe
    df_gameplan = df_gameplan.append(df)
    print("done")
   
def check_plan():
    if len(df_gameplan) == 20:
        print("Everythin fine")     
    else:
        print('Issue with getting correct nbr of games')  
        
def upload_gameplan():
    #db.upload_local_db_data(df_gameplan, 8)
    db.upload_local_data_to_database(df_gameplan, 'pl_data_vereine_spielplan')
    print("Data successfuly uploaded")
    
#define button function 
def get_results():
    #define global dataframe (can be used in other functions)
    global df_results
    df_results = pd.DataFrame()
    #get entries of values in GUI
    spieltag = entry_spieltag.get()
    saison = entry_saison.get()
    #call class of the file get_gameplan
    f = Results.get_premierleague_results_class(spieltag, saison)
    df = f.get_results()
    #add data to global dataframe
    df_results = df_results.append(df)
    print("done")
   
def check_results():
    if len(df_results) == 10:
        print("Everythin fine")     
    else:
        print(len(df_results))
        print('Issue with getting correct nbr of games')  
        
def upload_results():
    db.upload_local_data_to_database(df_results, 'pl_staging_ergebnisse')
    print("Data successfuly uploaded")

def get_results_cat():
    #define global dataframe (can be used in other functions)
    global df_categorization
    df_categorization = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    print(saison)
    print(spieltag)
    f = Results.categorisation_premier_league(saison, spieltag)
    df = f.categorisation_premier_league()
    #add data to global dataframe
    df_categorization = df_categorization.append(df)
    print("done")
   
def check_results_cat():
    if len(df_categorization) == 20:
        print("Everythin fine")     
    else:
        print('Issue with getting correct nbr of games')  
        
def upload_results_cat():
    db.upload_local_data_to_database(df_categorization, 'pl_data_ergebnisse_kategorisiert')
    print("Data successfuly uploaded")    
   
    
#Get coming matches
def get_coming_matches():
    #define global dataframe (can be used in other functions)
    global df_comming_matches
    df_comming_matches = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get()) 
    saison = entry_saison.get()
    #call class of the file get_gameplan
    f = Results.coming_matchday_premier_league(spieltag, saison)
    df = f.get_coming_matchday()
    #add data to global dataframe
    df_comming_matches = df_comming_matches.append(df)
    print("done")
    
    
def check_coming_matches():
    
    if len(df_comming_matches) == 10:
        print('everything is fine')
    else:
        print('Issue with getting correct nbr of games')  
        print(df_comming_matches)

def upload_coming_matches():
    db.upload_local_data_to_database(df_comming_matches, 'pl_staging_vereine_kommende_spieltag')
    print("Data successfuly uploaded")
  
#Get Fifa Features 
def get_fifa_data():
    #define global dataframe (can be used in other functions)
    global df_fifa_data
    df_fifa_data = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())   
    url = fifa_entry.get()
    saison = entry_saison.get()
    #call class of the file get_gameplan
    f = ff.pl_fifa_features(saison, spieltag, url)
    df = f.pl_get_fifa_features()
    #add data to global dataframe
    df_fifa_data = df_fifa_data.append(df)
    print("done")
    
def check_fifa_data():
    
    if len(df_fifa_data) == 20:
        print(df_fifa_data)
    else:
        print('Issue with getting correct nbr of games')  

def upload_fifa_upload():
    db.upload_local_data_to_database(df_fifa_data, 'pl_staging_vereine_fifa_features')
    #db.upload_local_db_data(df_fifa_data, 4)
    print("Data successfuly uploaded")
    
def get_formfeature():
    #define global dataframe (can be used in other functions)
    global df_form
    df_form = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = cf.get_form_pl(saison, spieltag)
    #add data to global dataframe
    df_form = df_form.append(df)
    print("done") 

def check_formfeatures():
    if len(df_form)==20:
        print("Everything fine")
    else:
        print("Problem")
        print(df_form)
        
def upload_formfeatures():
    db.upload_local_data_to_database(df_form, 'pl_features_club_form')
    print("Data successfuly uploaded")
          
def get_formfeature_forecast():
    #define global dataframe (can be used in other functions)
    global df_form_forecast
    df_form_forecast = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = cf.get_form_forcast_pl(saison, spieltag)
    #add data to global dataframe
    df_form_forecast = df_form_forecast.append(df)
    print("done") 

def check_formfeatures_forecast():
    if len(df_form_forecast)==20:
        print("Everything fine")
    else:
        print("Problem")
        print(df_form_forecast)
        
def upload_formfeatures_forecast():
    db.upload_local_data_to_database(df_form_forecast, 'pl_features_forecast_club_form')
    print("Data successfuly uploaded") 
    
def get_staging_football_gov():

    global df_staging_football_gov
    df_staging_football_gov = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())   
    saison = entry_saison.get()
    df = f.get_staging_football_pl(spieltag, saison)

    df_staging_football_gov = df_staging_football_gov.append(df)

    print("done")  

def check_staging_football_gov():
    
    if len(df_staging_football_gov) == 10:
        print("Everything Fine!")
    else:
        print("Issue with:")
        print(" ")
        print(df_staging_football_gov) 
        
def upload_staging_football_gov():
    db.upload_local_data_to_database(df_staging_football_gov, 'pl_staging_football_uk')
    print("Data successfuly uploaded")    
    
def get_data_gov():
    #define global dataframe (can be used in other functions)
    global df_data_gov
    df_data_gov = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = f.get_data_pl(saison, spieltag)
    #add data to global dataframe
    df_data_gov = df_data_gov.append(df)
    print("done") 

def check_data_gov():
    if len(df_data_gov)==10:
        print("Everything fine")
    else:
        print("Problem")
        print(df_data_gov)
        
def upload_data_gov():
    db.upload_local_data_to_database(df_data_gov, 'pl_data_vereine_data_gov')
    print("Data successfuly uploaded") 
    
def get_data_odds_gov():
    #define global dataframe (can be used in other functions)
    global df_data_odds
    df_data_odds = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = f.get_odds_pl(saison, spieltag)
    #add data to global dataframe
    df_data_odds = df_data_odds.append(df)
    print("done") 

def check_data_odds_gov():
    if len(df_data_odds)==10:
        print("Everything fine")
    else:
        print("Problem")
        print(df_data_odds)
        
def upload_data_odds_gov():
    db.upload_local_data_to_database(df_data_odds, 'pl_data_vereine_bookmaker_odds')
    print("Data successfuly uploaded")      

def get_data_features():

    global df_data_features
    df_data_features = pd.DataFrame()

    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()

    df = d.get_club_data_feature_home_pl()
    df = d.get_club_data_feature_away_pl(df, saison, spieltag)
    df = d.prepare_upload_home_pl(df)
    df_data_features = df_data_features.append(df)
    print("done") 

def check_data_features():
    if len(df_data_features)==20:
        print("Everything fine")
    else:
        print("Problem")
        print(df_data_features)
        
def upload_data_features():
    db.upload_local_data_to_database(df_data_features, 'pl_features_club_data')
    print("Data successfuly uploaded")      
   
    
def get_data_features_forecast():

    global df_data_features_forecast
    df_data_features_forecast = pd.DataFrame()

    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()

    df = d.get_club_data_feature_home_forecast_pl(saison)
    df = d.get_club_data_feature_away_forecast_pl(df, saison, spieltag)
    print(df)
    df = d.prepare_upload_home_pl(df)
    print(df)
    df_data_features_forecast = df_data_features_forecast.append(df)
    print("done") 


def check_data_features_forecast():
    if len(df_data_features_forecast)==20:
        print("Everything fine")
    else:
        print("Problem")
        print(df_data_features_forecast)
      
        
def upload_data_features_forecast():
    db.upload_local_data_to_database(df_data_features_forecast, 'pl_features_forecast_club_data')
    print("Data successfuly uploaded")  
    
#trainer
def get_trainer():
    #define global dataframe (can be used in other functions)
    global df_trainer
    df_trainer = pd.DataFrame()
    #get entries of values in GUI
    #spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = trainer.get_trainer_premier_league(saison)
    df_trainer = df_trainer.append(df)
    print(df_trainer)
    
def new_trainer():
    #define global dataframe (can be used in other functions)
    global df_new_trainer
    df_new_trainer = pd.DataFrame()
    #get entries of values in GUI
    #spieltag = int(entry_spieltag.get())
    #saison = entry_saison.get()
    #call class of the file get_gameplan
    df = trainer.new_trainer(df_trainer)
    #add data to global dataframe
    
    df_new_trainer = df_new_trainer.append(df)
    print("done") 

def get_trainer_matchday():
    #define global dataframe (can be used in other functions)
    global df_trainer_matchday
    df_trainer_matchday = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = trainer.get_plan_premier_league(df_trainer, spieltag, saison)
    #add data to global dataframe
    df_trainer_matchday = df_trainer_matchday.append(df)
    print("done") 
    
def check_trainer():
    print(df_trainer_matchday)

def check_new_trainer():
    print(df_new_trainer)
        
def upload_trainer():
    db.upload_local_data_to_database(df_trainer_matchday, 'pl_data_trainer_spiele')
    #db.upload_local_db_data(df_trainer_matchday, 15)
    print("Data successfuly uploaded")    

def upload_new_trainer():
    db.upload_local_data_to_database(df_new_trainer, 'master_trainer_id')
    #db.upload_local_db_data(df_new_trainer, 18)
    print("Data successfuly uploaded")    


def get_club_value():
    #define global dataframe (can be used in other functions)
    global df_club_value
    df_club_value = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    f = cv.club_value_premier_league(spieltag, saison)
    df = f.get_club_value()
    #add data to global dataframe
    df_club_value = df_club_value.append(df)
    print("done") 

def check_club_value():
    if len(df_club_value)==20:
       print("Everything is fine")     
    else:
        print(df_club_value)
        print("Problem")
        
def upload_club_value():
    db.upload_local_data_to_database(df_club_value, 'pl_data_vereine_kader_wert')
    print("Data successfuly uploaded")       
    
#define buttons, entries and labels    
entry_saison = tk.Entry()
entry_spieltag = tk.Entry()
entry_gameplan = tk.Entry()
fifa_entry = tk.Entry()

headliner_label = tk.Label(root, text = 'Data Provider for club level, referees and trainer', font=('calibre', 14, 'bold')) 
saison_label = tk.Label(root, text = 'Season', font=('calibre', 10, 'bold')) 
spieltag_label = tk.Label(root, text = 'Matchday', font=('calibre', 10, 'bold'))
gameplan_label = tk.Label(root, text = 'Schedule', font=('calibre', 10, 'bold'))
fifa_label = tk.Label(root, text = 'Fifa Url', font=('calibre', 10, 'bold'))

#comments
gameplan_comment = tk.Label(root, text = 'Spieltag, Saison'+ '\n' + 'and Gameplan', font=('calibre', 8)) 
results_comment = tk.Label(root, text = 'Season and Machtday', font=('calibre', 8)) 
schedule_comment = tk.Label(root, text = 'Schedule: 1 = 1 ' + '\n' + '2(16,20) 21(14,20) 22(12,20) 23(8,20) 24(10,10)' + '\n' + '3(14,18,20); 31(12,18,20); 32(16,18,20); 33(2,16,20); 34(2,12,20)' + '\n' + ' 4 = 4 Matchdays', font=('calibre', 8)) 
categorisation_comment = tk.Label(root, text = 'Season and Matchday', font=('calibre', 8)) 
coming_matches_comment = tk.Label(root, text = 'Only matchdays in the future can be taken', font=('calibre', 8)) 
referees_comment = tk.Label(root, text = 'Only matchday needed ' + '\n' + 'Results + Coming Matchday must be updated', font=('calibre', 8)) 
bundesliga_data_comment = tk.Label(root, text = 'last matchday needed and results up to date ' + '\n' + 'Update must be in between the matchdays ' + '\n' + ' otherwise Data issues', font=('calibre', 8))
google_comment = tk.Label(root, text = 'Only matchday needed ' + '\n' + 'Results must be updated before', font=('calibre', 8)) 
club_value_comment = tk.Label(root, text = 'Only matchday needed' + '\n' + 'Should be updated one time per week', font=('calibre', 8)) 
trainer_comment = tk.Label(root, text = 'No matchday or Season needed' + '\n' + 'but matchday needs get trainer before', font=('calibre', 8)) 
fifa_label.place(relx = 0.2, rely = 0.12, relwidth = 0.1, relheight = 0.1)
fifa_entry.place(relx = 0.3, rely = 0.16, relwidth = 0.3, relheight = 0.02) 

#gameplan
button_plan = tk.Button(root, text = 'Match Schedule',command = get_gameplan)
button_plan.pack()
button_plan_check = tk.Button(root, text = 'Check Schedule',command = check_plan)
button_plan_check.pack()
button_plan_upload = tk.Button(root, text = 'Upload Gameplan',command = upload_gameplan)
button_plan_upload.pack()

#Results
button_results = tk.Button(root, text = 'Results',command = get_results)
button_results.pack()
button_results_check = tk.Button(root, text = 'Check Results',command = check_results)
button_results_check.pack()
button_results_upload = tk.Button(root, text = 'Upload Results',command = upload_results)
button_results_upload.pack()

#Categorization
button_cat = tk.Button(root, text = 'Categorization',command = get_results_cat)
button_cat.pack()
button_cat_check = tk.Button(root, text = 'Check Categorization',command = check_results_cat)
button_cat_check.pack()
button_cat_upload = tk.Button(root, text = 'Upload Categorization',command = upload_results_cat)
button_cat_upload.pack()

#Coming Matchdays
button_coming = tk.Button(root, text = 'Coming Matchdays',command = get_coming_matches)
button_coming.pack()
button_coming_check = tk.Button(root, text = 'Check Matchdays',command = check_coming_matches)
button_coming_check.pack()
button_coming_upload = tk.Button(root, text = 'Upload Matchdays',command = upload_coming_matches)
button_coming_upload.pack()

#Coming Matchdays
button_fifa = tk.Button(root, text = 'Fifa Data',command = get_fifa_data)
button_fifa.pack()
button_fifa_check = tk.Button(root, text = 'Check Fifa Data',command = check_fifa_data)
button_fifa_check.pack()
button_fifa_upload = tk.Button(root, text = 'Upload Fifa Data',command = upload_fifa_upload)
button_fifa_upload.pack()

#form features 
button_club_form = tk.Button(root, text = 'Get Club Form', command = get_formfeature)
button_club_form.pack()
button_club_form_check = tk.Button(root, text = 'Check Club Form', command = check_formfeatures)
button_club_form_check.pack()
button_club_form_upload = tk.Button(root, text = 'Upload Club Form', command = upload_formfeatures)
button_club_form_upload.pack()

#form features forecast
button_club_Forecast = tk.Button(root, text = 'Get Form Forecast', command = get_formfeature_forecast)
button_club_Forecast.pack()
button_club_Forecast_check = tk.Button(root, text = 'Check Form Forecast', command = check_formfeatures_forecast)
button_club_Forecast_check.pack()
button_club_Forecast_upload = tk.Button(root, text = 'Upload Form Forecast', command = upload_formfeatures_forecast)
button_club_Forecast_upload.pack()

#game data from data gov
button_bundesliga_game_data = tk.Button(root, text = 'bl1_staging_football_uk', command = get_staging_football_gov)
button_bundesliga_game_data.pack()
button_bundesliga_game_data_check = tk.Button(root, text = 'Check bl1_staging_football_uk', command = check_staging_football_gov)
button_bundesliga_game_data_check.pack()
button_bundesliga_game_data_upload = tk.Button(root, text = 'Upload bl1_staging_football_uk', command = upload_staging_football_gov)
button_bundesliga_game_data_upload.pack()

#form data gov
button_data_gov = tk.Button(root, text = 'pl_data_vereine_data_gov', command = get_data_gov)
button_data_gov.pack()
button_data_gov_check = tk.Button(root, text = 'Check', command = check_data_gov)
button_data_gov_check.pack()
button_data_gov_upload = tk.Button(root, text = 'Upload', command = upload_data_gov)
button_data_gov_upload.pack()

#odds data gov
button_data_odds = tk.Button(root, text = 'pl_data_vereine_bookmaker_odds', command = get_data_odds_gov)
button_data_odds.pack()
button_data_odds_check = tk.Button(root, text = 'Check', command = check_data_odds_gov)
button_data_odds_check.pack()
button_data_odds_upload = tk.Button(root, text = 'Upload', command = upload_data_odds_gov)
button_data_odds_upload.pack()


#odds data features
button_data_features = tk.Button(root, text = 'pl_features_club_data', command = get_data_features)
button_data_features.pack()
button_data_features_check = tk.Button(root, text = 'Check', command = check_data_features)
button_data_features_check.pack()
button_data_features_upload = tk.Button(root, text = 'Upload', command = upload_data_features)
button_data_features_upload.pack()


#odds data features forecast
button_data_features_forecast = tk.Button(root, text = 'pl_features_forecast_club_data', command = get_data_features_forecast)
button_data_features_forecast.pack()
button_data_features_forecast_check = tk.Button(root, text = 'Check', command = check_data_features_forecast)
button_data_features_forecast_check.pack()
button_data_features_forecast_upload = tk.Button(root, text = 'Upload', command = upload_data_features_forecast)
button_data_features_forecast_upload.pack()

#get trainer
button_trainer = tk.Button(root, text = 'Get Trainer', command = get_trainer)
button_trainer.pack()
button_new_trainer = tk.Button(root, text = 'Get New Trainer', command = new_trainer)
button_new_trainer.pack()
button_check_button_new_trainer = tk.Button(root, text = 'Check New Trainer', command = check_new_trainer)
button_check_button_new_trainer.pack()
button_check_trainer = tk.Button(root, text = 'Check Trainer', command = check_trainer)
button_check_trainer.pack()
button_new_trainer_upload = tk.Button(root, text = 'Upload New Trainer', command = upload_new_trainer)
button_new_trainer_upload.pack()
button_trainer_upload = tk.Button(root, text = 'Upload Trainer Per Matchday', command = upload_trainer)
button_trainer_upload.pack()
button_trainer_matchday = tk.Button(root, text = 'Get trainer per Matchday', command = get_trainer_matchday)
button_trainer_matchday.pack()

#club value 
button_club_value = tk.Button(root, text = 'Get Club Value', command = get_club_value)
button_club_value.pack()
button_club_value_day_check = tk.Button(root, text = 'Check Club Value', command = check_club_value)
button_club_value_day_check.pack()
button_club_value_upload = tk.Button(root, text = 'Upload Club Value', command = upload_club_value)
button_club_value_upload.pack()
#place buttons, entries and labels
headliner_label.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.1) 

saison_label.place(relx = 0.05, rely = 0.06, relwidth = 0.1, relheight = 0.1) 
entry_saison.place(relx = 0.15, rely = 0.1, relwidth = 0.05, relheight = 0.02)

schedule_comment.place(relx = 0.35, rely = 0.06, relwidth = 0.25, relheight = 0.1) 
gameplan_label.place(relx = 0.2, rely = 0.06, relwidth = 0.1, relheight = 0.1) 
entry_gameplan.place(relx = 0.3, rely = 0.1, relwidth = 0.05, relheight = 0.02)

spieltag_label.place(relx = 0.05, rely = 0.12, relwidth = 0.1, relheight = 0.1) 
entry_spieltag.place(relx = 0.15, rely = 0.16, relwidth = 0.05, relheight = 0.02)

fifa_label.place(relx = 0.2, rely = 0.12, relwidth = 0.1, relheight = 0.1)
fifa_entry.place(relx = 0.3, rely = 0.16, relwidth = 0.3, relheight = 0.02) 


#first row
#*******************************************************
gameplan_comment.place(relx = 0.05, rely = 0.2, relwidth = 0.1, relheight = 0.05)
button_plan.place(relx = 0.05, rely = 0.25, relwidth = 0.1, relheight = 0.05)
button_plan_check.place(relx = 0.05, rely = 0.3, relwidth = 0.1, relheight = 0.05)
button_plan_upload.place(relx = 0.05, rely = 0.35, relwidth = 0.1, relheight = 0.05)

button_results.place(relx = 0.15, rely = 0.25, relwidth = 0.1, relheight = 0.05)
button_results_check.place(relx = 0.15, rely = 0.3, relwidth = 0.1, relheight = 0.05)
button_results_upload.place(relx = 0.15, rely = 0.35, relwidth = 0.1, relheight = 0.05)

button_cat.place(relx = 0.25, rely = 0.25, relwidth = 0.1, relheight = 0.05)
button_cat_check.place(relx = 0.25, rely = 0.3, relwidth = 0.1, relheight = 0.05)
button_cat_upload.place(relx = 0.25, rely = 0.35, relwidth = 0.1, relheight = 0.05)

button_coming.place(relx = 0.35, rely =  0.25, relwidth = 0.1, relheight = 0.05)
button_coming_check.place(relx = 0.35, rely =0.3, relwidth =0.1, relheight = 0.05)
button_coming_upload.place(relx = 0.35, rely = 0.35, relwidth = 0.1, relheight = 0.05)

button_fifa.place(relx = 0.45, rely =  0.25, relwidth = 0.1, relheight = 0.05)
button_fifa_check.place(relx = 0.45, rely =  0.3, relwidth = 0.1, relheight = 0.05)
button_fifa_upload.place(relx = 0.45, rely =  0.35, relwidth = 0.1, relheight = 0.05)

button_club_form.place(relx = 0.55, rely =  0.25, relwidth = 0.1, relheight = 0.05)
button_club_form_check.place(relx = 0.55, rely =  0.3, relwidth = 0.1, relheight = 0.05)
button_club_form_upload.place(relx = 0.55, rely =  0.35, relwidth = 0.1, relheight = 0.05)

button_club_Forecast.place(relx = 0.65, rely =  0.25, relwidth = 0.1, relheight = 0.05)
button_club_Forecast_check.place(relx = 0.65, rely =  0.3, relwidth = 0.1, relheight = 0.05)
button_club_Forecast_upload.place(relx = 0.65, rely =  0.35, relwidth = 0.1, relheight = 0.05)

button_club_value.place(relx = 0.75, rely =  0.25, relwidth = 0.1, relheight = 0.05)
button_club_value_day_check.place(relx = 0.75, rely =  0.3, relwidth = 0.1, relheight = 0.05)
button_club_value_upload.place(relx = 0.75, rely =  0.35, relwidth = 0.1, relheight = 0.05)
#second row
#*******************************************************

button_bundesliga_game_data.place(relx = 0.05, rely = 0.45, relwidth = 0.15, relheight = 0.05)
button_bundesliga_game_data_check.place(relx = 0.05, rely = 0.5, relwidth =  0.15, relheight = 0.05)
button_bundesliga_game_data_upload.place(relx = 0.05, rely = 0.55, relwidth =  0.15, relheight = 0.05)

button_data_gov.place(relx = 0.2, rely = 0.45, relwidth = 0.15, relheight = 0.05)
button_data_gov_check.place(relx = 0.2, rely = 0.5, relwidth =  0.15, relheight = 0.05)
button_data_gov_upload.place(relx = 0.2, rely = 0.55, relwidth =  0.15, relheight = 0.05)

button_data_odds.place(relx = 0.35, rely = 0.45, relwidth = 0.15, relheight = 0.05)
button_data_odds_check.place(relx = 0.35, rely = 0.5, relwidth =  0.15, relheight = 0.05)
button_data_odds_upload.place(relx = 0.35, rely = 0.55, relwidth =  0.15, relheight = 0.05)

button_data_features.place(relx = 0.5, rely = 0.45, relwidth = 0.15, relheight = 0.05)
button_data_features_check.place(relx = 0.5, rely = 0.5, relwidth =  0.15, relheight = 0.05)
button_data_features_upload.place(relx = 0.5, rely = 0.55, relwidth =  0.15, relheight = 0.05)#

button_data_features_forecast.place(relx = 0.65, rely = 0.45, relwidth = 0.15, relheight = 0.05)
button_data_features_forecast_check.place(relx = 0.65, rely = 0.5, relwidth =  0.15, relheight = 0.05)
button_data_features_forecast_upload.place(relx = 0.65, rely = 0.55, relwidth =  0.15, relheight = 0.05)


#third row
#*******************************************************
trainer_comment.place(relx = 0.1, rely = 0.69, relwidth = 0.2, relheight = 0.05)
button_trainer.place(relx = 0.05, rely = 0.75, relwidth = 0.15, relheight = 0.05)
button_new_trainer.place(relx =  0.05, rely = 0.8, relwidth = 0.15, relheight = 0.05)
button_check_button_new_trainer.place(relx =   0.05, rely = 0.85, relwidth = 0.15, relheight = 0.05)
button_new_trainer_upload.place(relx =  0.05, rely = 0.9, relwidth = 0.15, relheight = 0.05)

button_trainer_matchday.place(relx =  0.2, rely = 0.75, relwidth = 0.15, relheight = 0.05)
button_check_trainer.place(relx =  0.2, rely = 0.8, relwidth = 0.15, relheight = 0.05)
button_trainer_upload.place(relx =  0.2, rely = 0.85, relwidth = 0.15, relheight = 0.05)

root.mainloop()
