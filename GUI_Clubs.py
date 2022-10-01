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
import Get_Trainer as trainer
import Get_Club_Value as cv
import Get_Referees as Ref
import Get_Form_Club_Feature as cf
import Get_Recent_Gameday_Quotes as q
import Get_Football_Data_Gov as f
import Get_Game_Data_Features as d

#define dashboard method and size/height
root = tk.Tk(className = "Data Provider for club level, referees and trainer")
canvas = tk.Canvas(root, height = 900, width = 1200)
canvas.pack()

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
    f = gp.spielplan(spieltag, gameplan, saison)
    df = f.get_spielplan()
    #add data to global dataframe
    df_gameplan = df_gameplan.append(df)
    print("done")
   
    
def upload_gameplan():
    #db.upload_local_db_data(df_gameplan, 8)
    db.upload_local_data_to_database(df_gameplan, 'bl1_data_vereine_spielplan')
    print("Data successfuly uploaded")
    
def check_plan():
    if len(df_gameplan) == 18:
        print("Everythin fine")
    else:
        print('Issue with getting correct nbr of games')  

    
#result function    
def get_results():
    #define global dataframe (can be used in other functions)
    global df_erg
    df_erg = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    f = Results.get_results_class(spieltag,saison)
    #add data to global dataframe
    df = f.get_results()
    df_erg = df_erg.append(df)
    print("done")
    
    
def check_results():
    if len(df_erg) == 9:
        print("Everything is fine")
    else:
        print('Issue with getting correct nbr of games')
        print(df_erg)

        
        
def upload_results():
   #db.upload_local_db_data(df_erg, 1)
    db.upload_local_data_to_database(df_erg, 'bl1_staging_ergebnisse')
    print("Data successfuly uploaded")
  
    

def get_categorisation():
    #define global dataframe (can be used in other functions)
    global df_erg_cat
    df_erg_cat = pd.DataFrame()

    #call class of the file get_gameplan
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    
    f = Results.categorisation(saison, spieltag)
    df = f.categorisation()
    #add data to global dataframe
    df_erg_cat = df_erg_cat.append(df)
    print("done")
    
def check_categorisation():
    if len(df_erg_cat) == 18:
        print(df_erg_cat)
    else:
        print('Issue with getting correct nbr of games')  

def upload_categorisation():
    db.upload_local_data_to_database(df_erg_cat, 'bl1_data_ergebnisse_kategorisiert')
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
    f = Results.coming_matchday(spieltag, saison)
    df = f.get_coming_matchday()
    #add data to global dataframe
    df_comming_matches = df_comming_matches.append(df)
    print("done")
    
    
def check_coming_matches():
    
    if len(df_comming_matches) == 9:
        print(df_comming_matches)
    else:
        print('Issue with getting correct nbr of games')  

def upload_coming_matches():
    db.upload_local_db_data(df_comming_matches, 18)
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
    f = ff.fifa_features(saison, spieltag, url)
    df = f.get_fifa_features()
    #add data to global dataframe
    df_fifa_data = df_fifa_data.append(df)
    print("done")
    
def check_fifa_data():
    
    if len(df_fifa_data) == 18:
        print(df_fifa_data)
    else:
        print('Issue with getting correct nbr of games')  

def upload_fifa_upload():
    db.upload_local_data_to_database(df_fifa_data, 'bl1_staging_vereine_fifa_features')
    #db.upload_local_db_data(df_fifa_data, 4)
    print("Data successfuly uploaded")
    
#Get Game Data
def get_game_data_google():
    #define global dataframe (can be used in other functions)
    global df_game_data_google
    df_game_data_google = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get()) 
    saison = entry_saison.get()
    #call class of the file get_gameplan
    f =gd.game_data(spieltag, saison)
    df = f.get_game_data()
    #add data to global dataframe
    df_game_data_google = df_game_data_google.append(df)

    print(df_game_data_google)
    print("done")  

def check_game_data():
    
    if len(df_game_data_google) == 18:
        print(df_game_data_google)
    else:
        print('Issue with getting correct nbr of games') 
        
def upload_check_game_data():
    db.upload_local_db_data(df_game_data_google, 5)
    print("Data successfuly uploaded")    


def get_staging_football_gov():

    global df_staging_football_gov
    df_staging_football_gov = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())   
    saison = entry_saison.get()
    df = f.get_staging_football(spieltag, saison)

    df_staging_football_gov = df_staging_football_gov.append(df)

    print("done")  

def check_staging_football_gov():
    
    if len(df_staging_football_gov) == 9:
        print("Everything Fine!")
    else:
        print("Issue with:")
        print(" ")
        print(df_staging_football_gov) 
        
def upload_staging_football_gov():
    db.upload_local_data_to_database(df_staging_football_gov, 'bl1_staging_football_uk')
    print("Data successfuly uploaded")    
    

#coming match day 
def get_comming_match_day():
    #define global dataframe (can be used in other functions)
    global df_coming_match_day
    df_coming_match_day = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    f = Results.coming_matchday(spieltag,saison)
    #add data to global dataframe
    df = f.get_coming_matchday()
    df_coming_match_day = df_coming_match_day.append(df)
    print("done")
    
    
def check_comming_match_day():
    if len(df_coming_match_day) == 9:
        print(df_coming_match_day)
    else:
        print('Issue with getting correct nbr of games')
        
def upload_comming_match_day():
    db.upload_local_db_data(df_coming_match_day, 18)
    print("Data successfuly uploaded")
  

#trainer
def get_trainer():
    #define global dataframe (can be used in other functions)
    global df_trainer
    df_trainer = pd.DataFrame()
    #get entries of values in GUI
    #spieltag = int(entry_spieltag.get())
    #saison = entry_saison.get()
    #call class of the file get_gameplan
    df = trainer.get_trainer()
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
    df = trainer.get_plan(df_trainer, spieltag, saison)
    #add data to global dataframe
    df_trainer_matchday = df_trainer_matchday.append(df)
    print("done") 
    
def check_trainer():
    print(df_trainer_matchday)

def check_new_trainer():
    print(df_new_trainer)
        
def upload_trainer():
    db.upload_local_data_to_database(df_trainer_matchday, 'bl1_data_trainer_spiele')
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
    f = cv.club_value(spieltag, saison)
    df = f.get_club_value()
    #add data to global dataframe
    df_club_value = df_club_value.append(df)
    print("done") 

def check_club_value():
    if len(df_club_value)==18:
       print("Everything is fine")     
    else:
        print(df_club_value)
        print("Problem")
        
    
def upload_club_value():
    db.upload_local_data_to_database(df_club_value, 'bl1_data_vereine_kader_wert')
    print("Data successfuly uploaded")        

def get_referees():
    #define global dataframe (can be used in other functions)
    global df_referees
    df_referees = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = Ref.get_referees(spieltag, saison)
    #add data to global dataframe
    df_referees = df_referees.append(df)
    print("done") 

def check_referees():
    if len(df_referees)==9:
        print("Everything fine")
    else:
        print("Problem")
        print(df_referees)
def upload_referees():
    db.upload_local_db_data(df_referees, 25)
    print("Data successfuly uploaded")  
    
def get_formfeature():
    #define global dataframe (can be used in other functions)
    global df_form
    df_form = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = cf.get_form(saison, spieltag)
    #add data to global dataframe
    df_form = df_form.append(df)
    print("done") 

def check_formfeatures():
    if len(df_form)==18:
        print("Everything fine")
    else:
        print("Problem")
        print(df_form)
        
def upload_formfeatures():
    db.upload_local_data_to_database(df_form, 'bl1_features_club_form')
    print("Data successfuly uploaded")
          
def get_formfeature_forecast():
    #define global dataframe (can be used in other functions)
    global df_form_forecast
    df_form_forecast = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = cf.get_form_forcast(saison, spieltag)
    #add data to global dataframe
    df_form_forecast = df_form_forecast.append(df)
    print("done") 

def check_formfeatures_forecast():
    if len(df_form_forecast)==18:
        print("Everything fine")
    else:
        print("Problem")
        print(df_form_forecast)
def upload_formfeatures_forecast():
    db.upload_local_data_to_database(df_form_forecast, 'bl1_features_forecast_club_form')
    print("Data successfuly uploaded") 
    
    
def get_recent_odds():
    #define global dataframe (can be used in other functions)
    global df_quoten
    df_quoten = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = q.get_recent_odds(spieltag, saison)
    #add data to global dataframe
    df_quoten = df_quoten.append(df)
    print("done") 

def check_recent_odds():
    if len(df_quoten)==18:
        print("Everything fine")
    else:
        print("Problem")
        print(df_quoten)
        
def upload_recent_odds():
    db.upload_local_data_to_database(df_quoten, 'bl1_features_odds')
    print("Data successfuly uploaded") 
    
def get_data_gov():
    #define global dataframe (can be used in other functions)
    global df_data_gov
    df_data_gov = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = f.get_data(saison, spieltag)
    #add data to global dataframe
    df_data_gov = df_data_gov.append(df)
    print("done") 

def check_data_gov():
    if len(df_data_gov)==9:
        print("Everything fine")
    else:
        print("Problem")
        print(df_data_gov)
        
def upload_data_gov():
    db.upload_local_data_to_database(df_data_gov, 'bl1_data_vereine_data_gov')
    print("Data successfuly uploaded") 
   
def get_data_odds_gov():
    #define global dataframe (can be used in other functions)
    global df_data_odds
    df_data_odds = pd.DataFrame()
    #get entries of values in GUI
    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()
    #call class of the file get_gameplan
    df = f.get_odds(saison, spieltag)
    #add data to global dataframe
    df_data_odds = df_data_odds.append(df)
    print("done") 

def check_data_odds_gov():
    if len(df_data_odds)==9:
        print("Everything fine")
    else:
        print("Problem")
        print(df_data_odds)
        
def upload_data_odds_gov():
    db.upload_local_data_to_database(df_data_odds, 'bl1_data_vereine_bookmaker_odds')
    print("Data successfuly uploaded")      

def get_data_features():

    global df_data_features
    df_data_features = pd.DataFrame()

    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()

    df = d.get_club_data_feature_home()
    df = d.get_club_data_feature_away(df, saison, spieltag)
    df = d.prepare_upload_home(df)
    df_data_features = df_data_features.append(df)
    print("done") 

def check_data_features():
    if len(df_data_features)==18:
        print("Everything fine")
    else:
        print("Problem")
        print(df_data_features)
        
def upload_data_features():
    db.upload_local_data_to_database(df_data_features, 'bl1_features_club_data')
    print("Data successfuly uploaded")      
   
    
def get_data_features_forecast():

    global df_data_features_forecast
    df_data_features_forecast = pd.DataFrame()

    spieltag = int(entry_spieltag.get())
    saison = entry_saison.get()

    df = d.get_club_data_feature_home_forecast(saison)
    df = d.get_club_data_feature_away_forecast(df, saison, spieltag)
    print(df)
    df = d.prepare_upload_home(df)
    print(df)
    df_data_features_forecast = df_data_features_forecast.append(df)
    print("done") 


def check_data_features_forecast():
    if len(df_data_features_forecast)==18:
        print("Everything fine")
    else:
        print("Problem")
        print(df_data_features_forecast)
      
        
def upload_data_features_forecast():
    db.upload_local_data_to_database(df_data_features_forecast, 'bl1_features_forecast_club_data')
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
gameplan_comment = tk.Label(root, text = 'matchday, Season'+ '\n' + 'and Gameplan', font=('calibre', 8)) 
results_comment = tk.Label(root, text = 'Season'+ '\n' + 'Machtday', font=('calibre', 8)) 
schedule_comment = tk.Label(root, text = 'Schedule: 1 = 1 Matchdays'+ '\n' + '2 = 2 and 3 = 3 and 4 = 4 Matchdays', font=('calibre', 8)) 
categorisation_comment = tk.Label(root, text = 'Season'+ '\n' + 'Matchday', font=('calibre', 8)) 
coming_matches_comment = tk.Label(root, text = 'Only future'+ '\n' + 'matchday', font=('calibre', 8)) 
referees_comment = tk.Label(root, text = 'matchday' + '\n' + 'Results Coming Matchday' + '\n' + ' updated', font=('calibre', 8)) 
bundesliga_data_comment = tk.Label(root, text = 'Saison/Spieltag and download recent csv' + '\n' + 'http://www.football-data.co.uk/germanym.php')
google_comment = tk.Label(root, text = 'matchday' + '\n' + 'Results', font=('calibre', 8)) 
#club_value_comment = tk.Label(root, text = 'Only matchday needed' + '\n' + 'Should be updated one time per week', font=('calibre', 8)) 
trainer_comment = tk.Label(root, text = 'No matchday or Season needed' + '\n' + 'but matchday needs get trainer before', font=('calibre', 8)) 

#gameplan
button_plan = tk.Button(root, text = 'Match Schedule',command = get_gameplan)
button_plan.pack()
button_plan_check = tk.Button(root, text = 'Check Schedule',command = check_plan)
button_plan_check.pack()
button_plan_upload = tk.Button(root, text = 'Upload Gameplan',command = upload_gameplan)
button_plan_upload.pack()


#Results
button_results = tk.Button(root, text = 'Results of Matchday',command = get_results)
button_results.pack()
button_results_check = tk.Button(root, text = 'Check Results',command = check_results)
button_results_check.pack()
button_results_upload = tk.Button(root, text = 'Upload Results',command = upload_results)
button_results_upload.pack()
button_cat = tk.Button(root, text = 'Categorisation',command = get_categorisation)
button_cat.pack()
button_cat_check = tk.Button(root, text = 'Check Categorisation',command = check_categorisation)
button_cat_check.pack()
button_cat_upload = tk.Button(root, text = 'Upload Categorisation',command = upload_categorisation)
button_cat_upload.pack()

#next games
button_next_game = tk.Button(root, text = 'Next Gameday',command = get_coming_matches)
button_next_game.pack()
button_next_game_check = tk.Button(root, text = 'Check Gameday',command = check_coming_matches)
button_next_game_check.pack()
button_next_game_upload = tk.Button(root, text = 'Upload Gameday',command = upload_coming_matches)
button_next_game_upload.pack()

#Referees
button_Referees = tk.Button(root, text = 'Get Referees', command = get_referees)
button_Referees.pack()
button_Referees_check = tk.Button(root, text = 'Check Referees', command = check_referees)
button_Referees_check.pack()
button_Referees_upload = tk.Button(root, text = 'Upload Referees', command = upload_referees)
button_Referees_upload.pack()

#fifa
button_fifa_game = tk.Button(root, text = 'Fifa Data', command = get_fifa_data)
button_fifa_game.pack()
button_fifa_game_check = tk.Button(root, text = 'Check Fifa Data', command = check_fifa_data)
button_fifa_game_check.pack()
button_fifa_game_upload = tk.Button(root, text = 'Upload Fifa Data', command = upload_fifa_upload)
button_fifa_game_upload.pack()

#game data from google search
button_google_game_data = tk.Button(root, text = 'Google Game Data', command = get_game_data_google)
button_google_game_data.pack()
button_google_game_data_check = tk.Button(root, text = 'Check Data', command = check_game_data)
button_google_game_data_check.pack()
button_google_game_data_upload = tk.Button(root, text = 'Upload Data', command = upload_check_game_data)
button_google_game_data_upload.pack()

#game data from data gov
button_bundesliga_game_data = tk.Button(root, text = 'bl1_staging_football_uk', command = get_staging_football_gov)
button_bundesliga_game_data.pack()
button_bundesliga_game_data_check = tk.Button(root, text = 'Check bl1_staging_football_uk', command = check_staging_football_gov)
button_bundesliga_game_data_check.pack()
button_bundesliga_game_data_upload = tk.Button(root, text = 'Upload bl1_staging_football_uk', command = upload_staging_football_gov)
button_bundesliga_game_data_upload.pack()


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

#form features 
button_club_form = tk.Button(root, text = 'Get Club Form', command = get_formfeature)
button_club_form.pack()
button_club_form_check = tk.Button(root, text = 'Check Club Form', command = check_formfeatures)
button_club_form_check.pack()
button_club_form_upload = tk.Button(root, text = 'Upload Club Form', command = upload_formfeatures)
button_club_form_upload.pack()

#form features forecast
button_club_Forecast = tk.Button(root, text = 'Get Club Form Forecast', command = get_formfeature_forecast)
button_club_Forecast.pack()
button_club_Forecast_check = tk.Button(root, text = 'Check Club Form Forecast', command = check_formfeatures_forecast)
button_club_Forecast_check.pack()
button_club_Forecast_upload = tk.Button(root, text = 'Upload Club Form Forecast', command = upload_formfeatures_forecast)
button_club_Forecast_upload.pack()

#form odds 
button_club_odds = tk.Button(root, text = 'Get Recent Odds', command = get_recent_odds)
button_club_odds.pack()
button_club_odds_check = tk.Button(root, text = 'Check Recent Odds', command = check_recent_odds)
button_club_odds_check.pack()
button_club_odds_upload = tk.Button(root, text = 'Upload Recent Odds', command = upload_recent_odds)
button_club_odds_upload.pack()

#form data gov
button_data_gov = tk.Button(root, text = 'bl1_data_vereine_data_gov', command = get_data_gov)
button_data_gov.pack()
button_data_gov_check = tk.Button(root, text = 'Check', command = check_data_gov)
button_data_gov_check.pack()
button_data_gov_upload = tk.Button(root, text = 'Upload', command = upload_data_gov)
button_data_gov_upload.pack()

#odds data gov
button_data_odds = tk.Button(root, text = 'bl1_data_vereine_bookmaker_odds', command = get_data_odds_gov)
button_data_odds.pack()
button_data_odds_check = tk.Button(root, text = 'Check', command = check_data_odds_gov)
button_data_odds_check.pack()
button_data_odds_upload = tk.Button(root, text = 'Upload', command = upload_data_odds_gov)
button_data_odds_upload.pack()


#odds data features
button_data_features = tk.Button(root, text = 'bl1_features_club_data', command = get_data_features)
button_data_features.pack()
button_data_features_check = tk.Button(root, text = 'Check', command = check_data_features)
button_data_features_check.pack()
button_data_features_upload = tk.Button(root, text = 'Upload', command = upload_data_features)
button_data_features_upload.pack()


#odds data features forecast
button_data_features_forecast = tk.Button(root, text = 'bl1_features_forecast_club_data', command = get_data_features_forecast)
button_data_features_forecast.pack()
button_data_features_forecast_check = tk.Button(root, text = 'Check', command = check_data_features_forecast)
button_data_features_forecast_check.pack()
button_data_features_forecast_upload = tk.Button(root, text = 'Upload', command = upload_data_features_forecast)
button_data_features_forecast_upload.pack()


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

results_comment.place(relx = 0.15, rely = 0.2, relwidth = 0.1, relheight = 0.05)
button_results.place(relx = 0.15, rely = 0.25, relwidth = 0.1, relheight = 0.05)
button_results_check.place(relx = 0.15, rely = 0.3, relwidth = 0.1, relheight = 0.05)
button_results_upload.place(relx = 0.15, rely = 0.35, relwidth = 0.1, relheight = 0.05)

categorisation_comment.place(relx = 0.25, rely = 0.2, relwidth = 0.1, relheight = 0.05)
button_cat.place(relx = 0.25, rely = 0.25, relwidth = 0.1, relheight = 0.05)
button_cat_check.place(relx = 0.25, rely = 0.3, relwidth = 0.1, relheight = 0.05)
button_cat_upload.place(relx = 0.25, rely = 0.35, relwidth = 0.1, relheight = 0.05)

coming_matches_comment.place(relx = 0.35, rely = 0.2, relwidth = 0.1, relheight = 0.05)
button_next_game.place(relx = 0.35, rely =  0.25, relwidth = 0.1, relheight = 0.05)
button_next_game_check.place(relx = 0.35, rely =0.3, relwidth =0.1, relheight = 0.05)
button_next_game_upload.place(relx = 0.35, rely = 0.35, relwidth = 0.1, relheight = 0.05)

referees_comment.place(relx = 0.45, rely = 0.19, relwidth = 0.12, relheight = 0.06)
button_Referees.place(relx = 0.45, rely =  0.25, relwidth = 0.1, relheight = 0.05)
button_Referees_check.place(relx = 0.45, rely = 0.3, relwidth =0.1, relheight = 0.05)
button_Referees_upload.place(relx = 0.45, rely = 0.35, relwidth = 0.1, relheight = 0.05)

#club_value_comment.place(relx = 0.4, rely = 0.43, relwidth = 0.2, relheight = 0.05)
button_club_value.place(relx =  0.55, rely = 0.25, relwidth = 0.1, relheight = 0.05)
button_club_value_day_check.place(relx = 0.55, rely = 0.3, relwidth = 0.1, relheight = 0.05)
button_club_value_upload.place(relx =  0.55, rely = 0.35, relwidth = 0.1, relheight = 0.05)

button_fifa_game.place(relx = 0.65, rely = 0.25, relwidth = 0.1, relheight = 0.05)
button_fifa_game_check.place(relx = 0.65, rely = 0.3, relwidth = 0.1, relheight = 0.05)
button_fifa_game_upload.place(relx = 0.65, rely = 0.35, relwidth = 0.1, relheight = 0.05)

google_comment.place(relx = 0.75, rely = 0.2, relwidth = 0.1, relheight = 0.05)
button_google_game_data.place(relx = 0.75, rely = 0.25, relwidth = 0.1, relheight = 0.05)
button_google_game_data_check.place(relx = 0.75, rely = 0.3, relwidth = 0.1, relheight = 0.05)
button_google_game_data_upload.place(relx = 0.75, rely = 0.35, relwidth = 0.1, relheight = 0.05)



#second row
#*******************************************************
bundesliga_data_comment.place(relx = 0.01, rely = 0.43, relwidth = 0.25, relheight = 0.05)
button_bundesliga_game_data.place(relx = 0.05, rely = 0.5, relwidth = 0.15, relheight = 0.05)
button_bundesliga_game_data_check.place(relx = 0.05, rely = 0.55, relwidth =  0.15, relheight = 0.05)
button_bundesliga_game_data_upload.place(relx = 0.05, rely = 0.6, relwidth =  0.15, relheight = 0.05)

button_data_gov.place(relx = 0.2, rely = 0.5, relwidth = 0.15, relheight = 0.05)
button_data_gov_check.place(relx = 0.2, rely = 0.55, relwidth =  0.15, relheight = 0.05)
button_data_gov_upload.place(relx = 0.2, rely = 0.6, relwidth =  0.15, relheight = 0.05)

button_data_odds.place(relx = 0.35, rely = 0.5, relwidth = 0.15, relheight = 0.05)
button_data_odds_check.place(relx = 0.35, rely = 0.55, relwidth =  0.15, relheight = 0.05)
button_data_odds_upload.place(relx = 0.35, rely = 0.6, relwidth =  0.15, relheight = 0.05)

button_data_features.place(relx = 0.5, rely = 0.5, relwidth = 0.15, relheight = 0.05)
button_data_features_check.place(relx = 0.5, rely = 0.55, relwidth =  0.15, relheight = 0.05)
button_data_features_upload.place(relx = 0.5, rely = 0.6, relwidth =  0.15, relheight = 0.05)#

button_data_features_forecast.place(relx = 0.65, rely = 0.5, relwidth = 0.15, relheight = 0.05)
button_data_features_forecast_check.place(relx = 0.65, rely = 0.55, relwidth =  0.15, relheight = 0.05)
button_data_features_forecast_upload.place(relx = 0.65, rely = 0.6, relwidth =  0.15, relheight = 0.05)



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

button_club_form.place(relx =  0.35, rely = 0.75, relwidth = 0.15, relheight = 0.05)
button_club_form_check.place(relx =   0.35, rely = 0.8, relwidth = 0.15, relheight = 0.05)
button_club_form_upload.place(relx =  0.35, rely = 0.85, relwidth = 0.15, relheight = 0.05)

button_club_Forecast.place(relx =  0.5, rely = 0.75, relwidth = 0.15, relheight = 0.05)
button_club_Forecast_check.place(relx =  0.5, rely = 0.8, relwidth = 0.15, relheight = 0.05)
button_club_Forecast_upload.place(relx =  0.5, rely = 0.85, relwidth = 0.15, relheight = 0.05)

button_club_odds.place(relx =  0.65, rely = 0.75, relwidth = 0.15, relheight = 0.05)
button_club_odds_check.place(relx =  0.65, rely = 0.8, relwidth = 0.15, relheight = 0.05)
button_club_odds_upload.place(relx =  0.65, rely = 0.85, relwidth = 0.15, relheight = 0.05)
root.mainloop()
