import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')
#packages and modules
import pandas as pd

#import other files 
import Read_Load_Database as db

def get_club_data_feature_home():
      
    df = db.get_table('bl1_data_vereine_data_gov')            
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Saison', 'Spieltag'])      
    seasons = df['Saison'].drop_duplicates()
    
    for s in seasons:
        df_season = df[df['Saison']==s]
        vereine = df_season['Heimmannschaft_ID'].drop_duplicates()
        
        for v in vereine:
            df_club = df_season[df_season['Heimmannschaft_ID']==v]
            df_club = df_club.assign(Home_Shot_Feature = 0, Home_Shot_On_Goal_Feature = 0, Home_Fouls_Feature = 0, 
                                     Home_Corner_Feature = 0, Home_Yellowcard_Feature = 0, Home_Redcard_Feature = 0)
            df_club = df_club.sort_values(by = ['Spieltag'])
            df_club.index = range(len(df_club))
            for s in range(1, len(df_club)):
    
                if s == 1:
                    df_club.at[df_club.index[s], 'Home_Shot_Feature'] = df_club.at[df_club.index[s-1], 'Schüsse_Heim']   
                    df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = df_club.at[df_club.index[s-1], 'Torschüsse_Heim'] 
                    df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = df_club.at[df_club.index[s-1], 'Fouls_Heim'] 
                    df_club.at[df_club.index[s], 'Home_Corner_Feature'] = df_club.at[df_club.index[s-1], 'Ecken_Heim'] 
                    df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = df_club.at[df_club.index[s-1], 'Gelbe_Karten_Heim'] 
                    df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = df_club.at[df_club.index[s-1], 'Rote_Karten_Heim'] 
                if s == 2:
                    df_club.at[df_club.index[s], 'Home_Shot_Feature'] = round((df_club.at[df_club.index[s-2], 'Schüsse_Heim'] + df_club.at[df_club.index[s-1], 'Schüsse_Heim'])/2, 2)  
                    df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s-2], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-1], 'Torschüsse_Heim'])/2, 2)
                    df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = round((df_club.at[df_club.index[s-2], 'Fouls_Heim'] + df_club.at[df_club.index[s-1], 'Fouls_Heim'])/2, 2)
                    df_club.at[df_club.index[s], 'Home_Corner_Feature'] = round((df_club.at[df_club.index[s-2], 'Ecken_Heim'] + df_club.at[df_club.index[s-1], 'Ecken_Heim'])/2, 2)
                    df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = round((df_club.at[df_club.index[s-2], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Heim'])/2, 2)
                    df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = round((df_club.at[df_club.index[s-2], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Heim'])/2, 2)
                if s > 2:
                    df_club.at[df_club.index[s], 'Home_Shot_Feature'] = round((df_club.at[df_club.index[s-3], 'Schüsse_Heim'] + df_club.at[df_club.index[s-2], 'Schüsse_Heim'] + df_club.at[df_club.index[s-1], 'Schüsse_Heim']) / 3, 2) 
                    df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s-3], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-2], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-1], 'Torschüsse_Heim']) / 3, 2)
                    df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = round((df_club.at[df_club.index[s-3], 'Fouls_Heim'] + df_club.at[df_club.index[s-2], 'Fouls_Heim'] + df_club.at[df_club.index[s-1], 'Fouls_Heim']) / 3, 2)
                    df_club.at[df_club.index[s], 'Home_Corner_Feature'] = round((df_club.at[df_club.index[s-3], 'Ecken_Heim'] + df_club.at[df_club.index[s-2], 'Ecken_Heim'] + df_club.at[df_club.index[s-1], 'Ecken_Heim']) / 3, 2)
                    df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = round((df_club.at[df_club.index[s-3], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-2], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Heim']) / 3, 2)
                    df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = round((df_club.at[df_club.index[s-3], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-2], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Heim']) / 3, 2)
                
            df_all = df_all.append(df_club)
            
    df_all = df_all.drop_duplicates()
    
    return df_all

def get_club_data_feature_away(df, saison, spieltag):
    
    
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Saison', 'Spieltag'])      
    seasons = df['Saison'].drop_duplicates()
    
    for s in seasons:
        df_season = df[df['Saison']==s]
        vereine = df_season['Auswärtsmannschaft_ID'].drop_duplicates()
        
        for v in vereine:
            df_club = df_season[df_season['Auswärtsmannschaft_ID']==v]
            df_club = df_club.sort_values(by = ['Spieltag'])
            
            df_club = df_club.assign(Away_Shot_Feature = 0, Away_Shot_On_Goal_Feature = 0, Away_Fouls_Feature = 0, 
                                     Away_Corner_Feature = 0, Away_Yellowcard_Feature = 0, Away_Redcard_Feature = 0)
            df_club.index = range(len(df_club))

            for s in range(1, len(df_club)):
    
                if s == 1:
                    df_club.at[df_club.index[s], 'Away_Shot_Feature'] = df_club.at[df_club.index[s-1], 'Schüsse_Auswärts']   
                    df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = df_club.at[df_club.index[s-1], 'Torschüsse_Auswärts'] 
                    df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = df_club.at[df_club.index[s-1], 'Fouls_Auswärts'] 
                    df_club.at[df_club.index[s], 'Away_Corner_Feature'] = df_club.at[df_club.index[s-1], 'Ecken_Auswärts'] 
                    df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = df_club.at[df_club.index[s-1], 'Gelbe_Karten_Auswärts'] 
                    df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = df_club.at[df_club.index[s-1], 'Rote_Karten_Auswärts'] 
                if s == 2:
                    df_club.at[df_club.index[s], 'Away_Shot_Feature'] = round((df_club.at[df_club.index[s-2], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Schüsse_Auswärts'])/2, 2) 
                    df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s-2], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Torschüsse_Auswärts'])/2, 2)
                    df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = round((df_club.at[df_club.index[s-2], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-1], 'Fouls_Auswärts'])/2, 2)
                    df_club.at[df_club.index[s], 'Away_Corner_Feature'] = round((df_club.at[df_club.index[s-2], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-1], 'Ecken_Auswärts'])/2, 2)
                    df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = round((df_club.at[df_club.index[s-2], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Auswärts'])/2, 2)
                    df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = round((df_club.at[df_club.index[s-2], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Auswärts'])/2, 2)
                if s > 2:
                    df_club.at[df_club.index[s], 'Away_Shot_Feature'] = round((df_club.at[df_club.index[s-3], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-2], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Schüsse_Auswärts']) / 3, 2) 
                    df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s-3], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-2], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Torschüsse_Auswärts']) / 3, 2)
                    df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = round((df_club.at[df_club.index[s-3], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-2], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-1], 'Fouls_Auswärts']) / 3, 2)
                    df_club.at[df_club.index[s], 'Away_Corner_Feature'] = round((df_club.at[df_club.index[s-3], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-2], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-1], 'Ecken_Auswärts']) / 3, 2)
                    df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = round((df_club.at[df_club.index[s-3], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-2], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Auswärts']) / 3, 2)
                    df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = round((df_club.at[df_club.index[s-3], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-2], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Auswärts']) / 3, 2)
                
            df_all = df_all.append(df_club)
            
    df_all = df_all.drop_duplicates()
    df_all = df_all[df_all['Saison'] == saison]
    df_all = df_all[df_all['Spieltag'] == spieltag]
    
    return df_all
  


def prepare_upload_home(df):
    df_home = df[['Heimmannschaft_ID', 'Heimmannschaft', 'Saison', 'Spieltag','Home_Shot_Feature', 'Home_Shot_On_Goal_Feature'
                  ,'Home_Fouls_Feature', 'Home_Corner_Feature', 'Home_Yellowcard_Feature', 'Home_Redcard_Feature']]
    df_away = df[['Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Saison', 'Spieltag','Away_Shot_Feature', 'Away_Shot_On_Goal_Feature'
                  ,'Away_Fouls_Feature', 'Away_Corner_Feature', 'Away_Yellowcard_Feature', 'Away_Redcard_Feature']]
    
    df_home = df_home.rename(columns={"Heimmannschaft_ID": "Vereins_ID", "Heimmannschaft": "Verein", "Home_Shot_Feature":"Shot_Feature",
                               "Home_Shot_On_Goal_Feature":"Shot_On_Goal_Feature", "Home_Fouls_Feature":"Fouls_Feature",
                               'Home_Corner_Feature':"Corner_Feature", "Home_Yellowcard_Feature":"Yellowcard_Feature", 
                               "Home_Redcard_Feature":"Redcard_Feature"})
    
    df_away = df_away.rename(columns={"Auswärtsmannschaft_ID": "Vereins_ID", "Auswärtsmannschaft": "Verein", "Away_Shot_Feature":"Shot_Feature",
                               "Away_Shot_On_Goal_Feature":"Shot_On_Goal_Feature", "Away_Fouls_Feature":"Fouls_Feature",
                               'Away_Corner_Feature':"Corner_Feature", "Away_Yellowcard_Feature":"Yellowcard_Feature", 
                               "Away_Redcard_Feature":"Redcard_Feature"})      
    df = df_home.append(df_away)
    #df = df.sort_values(by = ['Saison', 'Spieltag'])   

    return df
      
#df = get_club_data_feature_home()   
#df = get_club_data_feature_away(df)   
#df = prepare_upload_home(df)
   
#db.upload_replace_local_data_to_database(df, 'bl1_features_club_data')
#db.upload_local_data_to_database(df, 'bl1_features_club_data')



def get_club_data_feature_home_forecast(saison):
    
    df = db.get_table('bl1_data_vereine_data_gov')

    df = df[df['Saison']==saison]
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Spieltag'])
    vereine = df['Heimmannschaft_ID'].drop_duplicates()
            
    for v in vereine:
        df_club = df[df['Heimmannschaft_ID']==v]
        df_club = df_club.assign(Home_Shot_Feature = 0, Home_Shot_On_Goal_Feature = 0, Home_Fouls_Feature = 0, 
                                 Home_Corner_Feature = 0, Home_Yellowcard_Feature = 0, Home_Redcard_Feature = 0)
        df_club = df_club.sort_values(by = ['Spieltag'])
        df_club.index = range(len(df_club))
   
        for s in range(1, len(df_club)):

            if s == 1:
                df_club.at[df_club.index[s], 'Home_Shot_Feature'] = df_club.at[df_club.index[s], 'Schüsse_Heim']   
                df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = df_club.at[df_club.index[s], 'Torschüsse_Heim'] 
                df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = df_club.at[df_club.index[s], 'Fouls_Heim'] 
                df_club.at[df_club.index[s], 'Home_Corner_Feature'] = df_club.at[df_club.index[s], 'Ecken_Heim'] 
                df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = df_club.at[df_club.index[s], 'Gelbe_Karten_Heim'] 
                df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = df_club.at[df_club.index[s], 'Rote_Karten_Heim'] 
            if s == 2:
                df_club.at[df_club.index[s], 'Home_Shot_Feature'] = round((df_club.at[df_club.index[s], 'Schüsse_Heim'] + df_club.at[df_club.index[s-1], 'Schüsse_Heim'])/2, 2)  
                df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-1], 'Torschüsse_Heim'])/2, 2)
                df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = round((df_club.at[df_club.index[s], 'Fouls_Heim'] + df_club.at[df_club.index[s-1], 'Fouls_Heim'])/2, 2)
                df_club.at[df_club.index[s], 'Home_Corner_Feature'] = round((df_club.at[df_club.index[s], 'Ecken_Heim'] + df_club.at[df_club.index[s-1], 'Ecken_Heim'])/2, 2)
                df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = round((df_club.at[df_club.index[s], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Heim'])/2, 2)
                df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = round((df_club.at[df_club.index[s], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Heim'])/2, 2)
            if s > 2:
                df_club.at[df_club.index[s], 'Home_Shot_Feature'] = round((df_club.at[df_club.index[s], 'Schüsse_Heim'] + df_club.at[df_club.index[s-2], 'Schüsse_Heim'] + df_club.at[df_club.index[s-1], 'Schüsse_Heim']) / 3, 2) 
                df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-2], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-1], 'Torschüsse_Heim']) / 3, 2)
                df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = round((df_club.at[df_club.index[s], 'Fouls_Heim'] + df_club.at[df_club.index[s-2], 'Fouls_Heim'] + df_club.at[df_club.index[s-1], 'Fouls_Heim']) / 3, 2)
                df_club.at[df_club.index[s], 'Home_Corner_Feature'] = round((df_club.at[df_club.index[s], 'Ecken_Heim'] + df_club.at[df_club.index[s-2], 'Ecken_Heim'] + df_club.at[df_club.index[s-1], 'Ecken_Heim']) / 3, 2)
                df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = round((df_club.at[df_club.index[s], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-2], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Heim']) / 3, 2)
                df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = round((df_club.at[df_club.index[s], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-2], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Heim']) / 3, 2)
        
        df_all = df_all.append(df_club)
  
    df_all = df_all.drop_duplicates()
    
    return df_all

def get_club_data_feature_away_forecast(df, saison, spieltag):
    
    
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Spieltag'])      

    vereine = df['Auswärtsmannschaft_ID'].drop_duplicates()
    
    for v in vereine:
        df_club = df[df['Auswärtsmannschaft_ID']==v]
        df_club = df_club.sort_values(by = ['Spieltag'])
        
        df_club = df_club.assign(Away_Shot_Feature = 0, Away_Shot_On_Goal_Feature = 0, Away_Fouls_Feature = 0, 
                                 Away_Corner_Feature = 0, Away_Yellowcard_Feature = 0, Away_Redcard_Feature = 0)
        df_club.index = range(len(df_club))

        for s in range(1, len(df_club)):

            if s == 1:
                df_club.at[df_club.index[s], 'Away_Shot_Feature'] = df_club.at[df_club.index[s], 'Schüsse_Auswärts']   
                df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = df_club.at[df_club.index[s], 'Torschüsse_Auswärts'] 
                df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = df_club.at[df_club.index[s], 'Fouls_Auswärts'] 
                df_club.at[df_club.index[s], 'Away_Corner_Feature'] = df_club.at[df_club.index[s], 'Ecken_Auswärts'] 
                df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = df_club.at[df_club.index[s], 'Gelbe_Karten_Auswärts'] 
                df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = df_club.at[df_club.index[s], 'Rote_Karten_Auswärts'] 
            if s == 2:
                df_club.at[df_club.index[s], 'Away_Shot_Feature'] = round((df_club.at[df_club.index[s], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Schüsse_Auswärts'])/2, 2) 
                df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Torschüsse_Auswärts'])/2, 2)
                df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = round((df_club.at[df_club.index[s], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-1], 'Fouls_Auswärts'])/2, 2)
                df_club.at[df_club.index[s], 'Away_Corner_Feature'] = round((df_club.at[df_club.index[s], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-1], 'Ecken_Auswärts'])/2, 2)
                df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = round((df_club.at[df_club.index[s], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Auswärts'])/2, 2)
                df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = round((df_club.at[df_club.index[s], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Auswärts'])/2, 2)
            if s > 2:
                df_club.at[df_club.index[s], 'Away_Shot_Feature'] = round((df_club.at[df_club.index[s], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-2], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Schüsse_Auswärts']) / 3, 2) 
                df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-2], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Torschüsse_Auswärts']) / 3, 2)
                df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = round((df_club.at[df_club.index[s], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-2], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-1], 'Fouls_Auswärts']) / 3, 2)
                df_club.at[df_club.index[s], 'Away_Corner_Feature'] = round((df_club.at[df_club.index[s], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-2], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-1], 'Ecken_Auswärts']) / 3, 2)
                df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = round((df_club.at[df_club.index[s], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-2], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Auswärts']) / 3, 2)
                df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = round((df_club.at[df_club.index[s], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-2], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Auswärts']) / 3, 2)
            
        df_all = df_all.append(df_club)
              
    df_all = df_all.drop_duplicates()
    df_all = df_all.assign(Spieltag = lambda x: x['Spieltag']+1)
    df_all = df_all[df_all['Spieltag']!=35]  
    df_all = df_all[df_all['Saison'] == saison]
    df_all = df_all[df_all['Spieltag'] == spieltag]
    
    return df_all
    

def first_gameday_club_data(saison, spieltag):
    #must be changed to ergebnisse
    d = db.get_data_db(2)
    df = d.get_data()
    df = df[df['Saison']==saison]

    vereine = df['Vereins_ID'].drop_duplicates()
    
    df_all = pd.DataFrame()
    #must be changed to variables
    for v in vereine:
        df_club = df[df['Vereins_ID']==v]
        df_club = df_club.assign(L1_Forecast = 0, L2_Forecast = 0, L3_Forecast = 0, L4_Forecast = 0, L5_Forecast = 0)
        df_all = df_all.append(df_club)
        
    df_all = df_all[['Spieltag', 'Saison', 'Vereins_ID', 'Verein', 'L1_Forecast', 'L2_Forecast', 'L3_Forecast', 
                     'L4_Forecast', 'L5_Forecast']]
    return df_all


#df_forecast = get_club_data_feature_home_forecast('2021/22')
#df_forecast = get_club_data_feature_away_forecast(df_forecast, '2021/22', 13)
#df_forecast = prepare_upload_home(df_forecast)

#db.upload_replace_local_data_to_database(df_forecast, 'bl1_features_forecast_club_data')
#db.upload_local_data_to_database(df_forecast, 'bl1_features_forecast_club_data')


def get_club_data_feature_home_pl():
    
    df = db.get_table('pl_data_vereine_data_gov') 
            
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Saison', 'Spieltag'])      
    seasons = df['Saison'].drop_duplicates()
    
    for s in seasons:
        df_season = df[df['Saison']==s]
        vereine = df_season['Heimmannschaft_ID'].drop_duplicates()
        
        for v in vereine:
            df_club = df_season[df_season['Heimmannschaft_ID']==v]
            df_club = df_club.assign(Home_Shot_Feature = 0, Home_Shot_On_Goal_Feature = 0, Home_Fouls_Feature = 0, 
                                     Home_Corner_Feature = 0, Home_Yellowcard_Feature = 0, Home_Redcard_Feature = 0)
            df_club = df_club.sort_values(by = ['Spieltag'])
            df_club.index = range(len(df_club))
            for s in range(1, len(df_club)):
    
                if s == 1:
                    df_club.at[df_club.index[s], 'Home_Shot_Feature'] = df_club.at[df_club.index[s-1], 'Schüsse_Heim']   
                    df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = df_club.at[df_club.index[s-1], 'Torschüsse_Heim'] 
                    df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = df_club.at[df_club.index[s-1], 'Fouls_Heim'] 
                    df_club.at[df_club.index[s], 'Home_Corner_Feature'] = df_club.at[df_club.index[s-1], 'Ecken_Heim'] 
                    df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = df_club.at[df_club.index[s-1], 'Gelbe_Karten_Heim'] 
                    df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = df_club.at[df_club.index[s-1], 'Rote_Karten_Heim'] 
                if s == 2:
                    df_club.at[df_club.index[s], 'Home_Shot_Feature'] = round((df_club.at[df_club.index[s-2], 'Schüsse_Heim'] + df_club.at[df_club.index[s-1], 'Schüsse_Heim'])/2, 2)  
                    df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s-2], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-1], 'Torschüsse_Heim'])/2, 2)
                    df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = round((df_club.at[df_club.index[s-2], 'Fouls_Heim'] + df_club.at[df_club.index[s-1], 'Fouls_Heim'])/2, 2)
                    df_club.at[df_club.index[s], 'Home_Corner_Feature'] = round((df_club.at[df_club.index[s-2], 'Ecken_Heim'] + df_club.at[df_club.index[s-1], 'Ecken_Heim'])/2, 2)
                    df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = round((df_club.at[df_club.index[s-2], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Heim'])/2, 2)
                    df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = round((df_club.at[df_club.index[s-2], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Heim'])/2, 2)
                if s > 2:
                    df_club.at[df_club.index[s], 'Home_Shot_Feature'] = round((df_club.at[df_club.index[s-3], 'Schüsse_Heim'] + df_club.at[df_club.index[s-2], 'Schüsse_Heim'] + df_club.at[df_club.index[s-1], 'Schüsse_Heim']) / 3, 2) 
                    df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s-3], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-2], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-1], 'Torschüsse_Heim']) / 3, 2)
                    df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = round((df_club.at[df_club.index[s-3], 'Fouls_Heim'] + df_club.at[df_club.index[s-2], 'Fouls_Heim'] + df_club.at[df_club.index[s-1], 'Fouls_Heim']) / 3, 2)
                    df_club.at[df_club.index[s], 'Home_Corner_Feature'] = round((df_club.at[df_club.index[s-3], 'Ecken_Heim'] + df_club.at[df_club.index[s-2], 'Ecken_Heim'] + df_club.at[df_club.index[s-1], 'Ecken_Heim']) / 3, 2)
                    df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = round((df_club.at[df_club.index[s-3], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-2], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Heim']) / 3, 2)
                    df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = round((df_club.at[df_club.index[s-3], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-2], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Heim']) / 3, 2)
                
            df_all = df_all.append(df_club)
            
    df_all = df_all.drop_duplicates()
    
    return df_all

def get_club_data_feature_away_pl(df, saison, spieltag):
    
    
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Saison', 'Spieltag'])      
    seasons = df['Saison'].drop_duplicates()
    
    for s in seasons:
        df_season = df[df['Saison']==s]
        vereine = df_season['Auswärtsmannschaft_ID'].drop_duplicates()
        
        for v in vereine:
            df_club = df_season[df_season['Auswärtsmannschaft_ID']==v]
            df_club = df_club.sort_values(by = ['Spieltag'])
            
            df_club = df_club.assign(Away_Shot_Feature = 0, Away_Shot_On_Goal_Feature = 0, Away_Fouls_Feature = 0, 
                                     Away_Corner_Feature = 0, Away_Yellowcard_Feature = 0, Away_Redcard_Feature = 0)
            df_club.index = range(len(df_club))

            for s in range(1, len(df_club)):
    
                if s == 1:
                    df_club.at[df_club.index[s], 'Away_Shot_Feature'] = df_club.at[df_club.index[s-1], 'Schüsse_Auswärts']   
                    df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = df_club.at[df_club.index[s-1], 'Torschüsse_Auswärts'] 
                    df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = df_club.at[df_club.index[s-1], 'Fouls_Auswärts'] 
                    df_club.at[df_club.index[s], 'Away_Corner_Feature'] = df_club.at[df_club.index[s-1], 'Ecken_Auswärts'] 
                    df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = df_club.at[df_club.index[s-1], 'Gelbe_Karten_Auswärts'] 
                    df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = df_club.at[df_club.index[s-1], 'Rote_Karten_Auswärts'] 
                if s == 2:
                    df_club.at[df_club.index[s], 'Away_Shot_Feature'] = round((df_club.at[df_club.index[s-2], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Schüsse_Auswärts'])/2, 2) 
                    df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s-2], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Torschüsse_Auswärts'])/2, 2)
                    df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = round((df_club.at[df_club.index[s-2], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-1], 'Fouls_Auswärts'])/2, 2)
                    df_club.at[df_club.index[s], 'Away_Corner_Feature'] = round((df_club.at[df_club.index[s-2], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-1], 'Ecken_Auswärts'])/2, 2)
                    df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = round((df_club.at[df_club.index[s-2], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Auswärts'])/2, 2)
                    df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = round((df_club.at[df_club.index[s-2], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Auswärts'])/2, 2)
                if s > 2:
                    df_club.at[df_club.index[s], 'Away_Shot_Feature'] = round((df_club.at[df_club.index[s-3], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-2], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Schüsse_Auswärts']) / 3, 2) 
                    df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s-3], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-2], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Torschüsse_Auswärts']) / 3, 2)
                    df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = round((df_club.at[df_club.index[s-3], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-2], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-1], 'Fouls_Auswärts']) / 3, 2)
                    df_club.at[df_club.index[s], 'Away_Corner_Feature'] = round((df_club.at[df_club.index[s-3], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-2], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-1], 'Ecken_Auswärts']) / 3, 2)
                    df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = round((df_club.at[df_club.index[s-3], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-2], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Auswärts']) / 3, 2)
                    df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = round((df_club.at[df_club.index[s-3], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-2], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Auswärts']) / 3, 2)
                
            df_all = df_all.append(df_club)
            
    df_all = df_all.drop_duplicates()
    df_all = df_all[df_all['Saison'] == saison]
    df_all = df_all[df_all['Spieltag'] == spieltag]
    
    return df_all
  


def prepare_upload_home_pl(df):
    df_home = df[['Heimmannschaft_ID', 'Heimmannschaft', 'Saison', 'Spieltag','Home_Shot_Feature', 'Home_Shot_On_Goal_Feature'
                  ,'Home_Fouls_Feature', 'Home_Corner_Feature', 'Home_Yellowcard_Feature', 'Home_Redcard_Feature']]
    df_away = df[['Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Saison', 'Spieltag','Away_Shot_Feature', 'Away_Shot_On_Goal_Feature'
                  ,'Away_Fouls_Feature', 'Away_Corner_Feature', 'Away_Yellowcard_Feature', 'Away_Redcard_Feature']]
    
    df_home = df_home.rename(columns={"Heimmannschaft_ID": "Vereins_ID", "Heimmannschaft": "Verein", "Home_Shot_Feature":"Shot_Feature",
                               "Home_Shot_On_Goal_Feature":"Shot_On_Goal_Feature", "Home_Fouls_Feature":"Fouls_Feature",
                               'Home_Corner_Feature':"Corner_Feature", "Home_Yellowcard_Feature":"Yellowcard_Feature", 
                               "Home_Redcard_Feature":"Redcard_Feature"})
    
    df_away = df_away.rename(columns={"Auswärtsmannschaft_ID": "Vereins_ID", "Auswärtsmannschaft": "Verein", "Away_Shot_Feature":"Shot_Feature",
                               "Away_Shot_On_Goal_Feature":"Shot_On_Goal_Feature", "Away_Fouls_Feature":"Fouls_Feature",
                               'Away_Corner_Feature':"Corner_Feature", "Away_Yellowcard_Feature":"Yellowcard_Feature", 
                               "Away_Redcard_Feature":"Redcard_Feature"})      
    df = df_home.append(df_away)
    df = df.sort_values(by = ['Saison', 'Spieltag'])   

    return df
      
#df = get_club_data_feature_home_pl()   
#df = get_club_data_feature_away_pl(df, '2021/22', 18)   
#df = prepare_upload_home_pl(df)
   
#db.upload_replace_local_data_to_database(df, 'pl_features_club_data')
#db.upload_local_data_to_database(df, 'pl_features_club_data')



def get_club_data_feature_home_forecast_pl(saison):
    
    df = db.get_table('pl_data_vereine_data_gov')

    #df = df[df['Saison']==saison]
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Spieltag'])
    vereine = df['Heimmannschaft_ID'].drop_duplicates()
            
    for v in vereine:
        df_club = df[df['Heimmannschaft_ID']==v]
        df_club = df_club.assign(Home_Shot_Feature = 0, Home_Shot_On_Goal_Feature = 0, Home_Fouls_Feature = 0, 
                                 Home_Corner_Feature = 0, Home_Yellowcard_Feature = 0, Home_Redcard_Feature = 0)
        df_club = df_club.sort_values(by = ['Spieltag'])
        df_club.index = range(len(df_club))
   
        for s in range(1, len(df_club)):

            if s == 1:
                df_club.at[df_club.index[s], 'Home_Shot_Feature'] = df_club.at[df_club.index[s], 'Schüsse_Heim']   
                df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = df_club.at[df_club.index[s], 'Torschüsse_Heim'] 
                df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = df_club.at[df_club.index[s], 'Fouls_Heim'] 
                df_club.at[df_club.index[s], 'Home_Corner_Feature'] = df_club.at[df_club.index[s], 'Ecken_Heim'] 
                df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = df_club.at[df_club.index[s], 'Gelbe_Karten_Heim'] 
                df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = df_club.at[df_club.index[s], 'Rote_Karten_Heim'] 
            if s == 2:
                df_club.at[df_club.index[s], 'Home_Shot_Feature'] = round((df_club.at[df_club.index[s], 'Schüsse_Heim'] + df_club.at[df_club.index[s-1], 'Schüsse_Heim'])/2, 2)  
                df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-1], 'Torschüsse_Heim'])/2, 2)
                df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = round((df_club.at[df_club.index[s], 'Fouls_Heim'] + df_club.at[df_club.index[s-1], 'Fouls_Heim'])/2, 2)
                df_club.at[df_club.index[s], 'Home_Corner_Feature'] = round((df_club.at[df_club.index[s], 'Ecken_Heim'] + df_club.at[df_club.index[s-1], 'Ecken_Heim'])/2, 2)
                df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = round((df_club.at[df_club.index[s], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Heim'])/2, 2)
                df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = round((df_club.at[df_club.index[s], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Heim'])/2, 2)
            if s > 2:
                df_club.at[df_club.index[s], 'Home_Shot_Feature'] = round((df_club.at[df_club.index[s], 'Schüsse_Heim'] + df_club.at[df_club.index[s-2], 'Schüsse_Heim'] + df_club.at[df_club.index[s-1], 'Schüsse_Heim']) / 3, 2) 
                df_club.at[df_club.index[s], 'Home_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-2], 'Torschüsse_Heim'] + df_club.at[df_club.index[s-1], 'Torschüsse_Heim']) / 3, 2)
                df_club.at[df_club.index[s], 'Home_Fouls_Feature'] = round((df_club.at[df_club.index[s], 'Fouls_Heim'] + df_club.at[df_club.index[s-2], 'Fouls_Heim'] + df_club.at[df_club.index[s-1], 'Fouls_Heim']) / 3, 2)
                df_club.at[df_club.index[s], 'Home_Corner_Feature'] = round((df_club.at[df_club.index[s], 'Ecken_Heim'] + df_club.at[df_club.index[s-2], 'Ecken_Heim'] + df_club.at[df_club.index[s-1], 'Ecken_Heim']) / 3, 2)
                df_club.at[df_club.index[s], 'Home_Yellowcard_Feature'] = round((df_club.at[df_club.index[s], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-2], 'Gelbe_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Heim']) / 3, 2)
                df_club.at[df_club.index[s], 'Home_Redcard_Feature'] = round((df_club.at[df_club.index[s], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-2], 'Rote_Karten_Heim'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Heim']) / 3, 2)
        
        df_all = df_all.append(df_club)
  
    df_all = df_all.drop_duplicates()
    
    return df_all

def get_club_data_feature_away_forecast_pl(df, saison, spieltag):
    
    
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Spieltag'])      

    vereine = df['Auswärtsmannschaft_ID'].drop_duplicates()
    
    for v in vereine:
        df_club = df[df['Auswärtsmannschaft_ID']==v]
        df_club = df_club.sort_values(by = ['Spieltag'])
        
        df_club = df_club.assign(Away_Shot_Feature = 0, Away_Shot_On_Goal_Feature = 0, Away_Fouls_Feature = 0, 
                                 Away_Corner_Feature = 0, Away_Yellowcard_Feature = 0, Away_Redcard_Feature = 0)
        df_club.index = range(len(df_club))

        for s in range(1, len(df_club)):

            if s == 1:
                df_club.at[df_club.index[s], 'Away_Shot_Feature'] = df_club.at[df_club.index[s], 'Schüsse_Auswärts']   
                df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = df_club.at[df_club.index[s], 'Torschüsse_Auswärts'] 
                df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = df_club.at[df_club.index[s], 'Fouls_Auswärts'] 
                df_club.at[df_club.index[s], 'Away_Corner_Feature'] = df_club.at[df_club.index[s], 'Ecken_Auswärts'] 
                df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = df_club.at[df_club.index[s], 'Gelbe_Karten_Auswärts'] 
                df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = df_club.at[df_club.index[s], 'Rote_Karten_Auswärts'] 
            if s == 2:
                df_club.at[df_club.index[s], 'Away_Shot_Feature'] = round((df_club.at[df_club.index[s], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Schüsse_Auswärts'])/2, 2) 
                df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Torschüsse_Auswärts'])/2, 2)
                df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = round((df_club.at[df_club.index[s], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-1], 'Fouls_Auswärts'])/2, 2)
                df_club.at[df_club.index[s], 'Away_Corner_Feature'] = round((df_club.at[df_club.index[s], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-1], 'Ecken_Auswärts'])/2, 2)
                df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = round((df_club.at[df_club.index[s], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Auswärts'])/2, 2)
                df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = round((df_club.at[df_club.index[s], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Auswärts'])/2, 2)
            if s > 2:
                df_club.at[df_club.index[s], 'Away_Shot_Feature'] = round((df_club.at[df_club.index[s], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-2], 'Schüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Schüsse_Auswärts']) / 3, 2) 
                df_club.at[df_club.index[s], 'Away_Shot_On_Goal_Feature'] = round((df_club.at[df_club.index[s], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-2], 'Torschüsse_Auswärts'] + df_club.at[df_club.index[s-1], 'Torschüsse_Auswärts']) / 3, 2)
                df_club.at[df_club.index[s], 'Away_Fouls_Feature'] = round((df_club.at[df_club.index[s], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-2], 'Fouls_Auswärts'] + df_club.at[df_club.index[s-1], 'Fouls_Auswärts']) / 3, 2)
                df_club.at[df_club.index[s], 'Away_Corner_Feature'] = round((df_club.at[df_club.index[s], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-2], 'Ecken_Auswärts'] + df_club.at[df_club.index[s-1], 'Ecken_Auswärts']) / 3, 2)
                df_club.at[df_club.index[s], 'Away_Yellowcard_Feature'] = round((df_club.at[df_club.index[s], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-2], 'Gelbe_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Gelbe_Karten_Auswärts']) / 3, 2)
                df_club.at[df_club.index[s], 'Away_Redcard_Feature'] = round((df_club.at[df_club.index[s], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-2], 'Rote_Karten_Auswärts'] + df_club.at[df_club.index[s-1], 'Rote_Karten_Auswärts']) / 3, 2)
            
        df_all = df_all.append(df_club)
              
    df_all = df_all.drop_duplicates()
    df_all = df_all.assign(Spieltag = lambda x: x['Spieltag']+1)
    df_all = df_all[df_all['Spieltag']!=35]  
    df_all = df_all[df_all['Saison'] == saison]
    df_all = df_all[df_all['Spieltag'] == spieltag]
    
    return df_all
    

def first_gameday_club_data_pl(saison, spieltag):
    #must be changed to ergebnisse
    d = db.get_data_db(2)
    df = d.get_data()
    df = df[df['Saison']==saison]

    vereine = df['Vereins_ID'].drop_duplicates()
    
    df_all = pd.DataFrame()
    #must be changed to variables
    for v in vereine:
        df_club = df[df['Vereins_ID']==v]
        df_club = df_club.assign(L1_Forecast = 0, L2_Forecast = 0, L3_Forecast = 0, L4_Forecast = 0, L5_Forecast = 0)
        df_all = df_all.append(df_club)
        
    df_all = df_all[['Spieltag', 'Saison', 'Vereins_ID', 'Verein', 'L1_Forecast', 'L2_Forecast', 'L3_Forecast', 
                     'L4_Forecast', 'L5_Forecast']]
    return df_all

#df_forecast = get_club_data_feature_home_forecast_pl('2021/22')
#df_forecast = get_club_data_feature_away_forecast_pl(df_forecast, '2021/22', 17)
#df_forecast = prepare_upload_home_pl(df_forecast)

#df_forecast = df_forecast.drop_duplicates()
#db.upload_replace_local_data_to_database(df_forecast, 'pl_features_forecast_club_data')
#db.upload_local_data_to_database(df_forecast, 'pl_features_forecast_club_data')