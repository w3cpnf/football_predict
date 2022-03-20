import os
os.chdir('D:/Projects/Football/Database/DQ_Code')

import pandas as pd
import mysql
import mysql.connector

today = pd.Timestamp.date(pd.Timestamp.today())

def connection(query):

    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd="...",
        database = '...'
    )
    
    df = pd.read_sql(query, con = mydb) 
    
    return df

def check_duplicates_staging():
    table_list_gamedays = ['bl1_staging_ergebnisse', 'bl1_staging_football_uk', 'bl1_staging_vereine_fifa_features', 
                           'bl1_staging_vereine_kommende_spieltag']    
    
    for table in table_list_gamedays:
        query = 'select * from ' + table
        
        df = connection(query) 
        print(table)
        saisons = df['Saison'].drop_duplicates()    
        for s in saisons:
            df_s = df[df['Saison']==s]
            if len(df_s.drop_duplicates())==len(df_s):
                print('***************')
                print("No duplicates in saison ")
                print(s)
                print('***************')
            else:
                print('***************')
                print("DUPLICATES saison")
                print(s)  
                print('***************')

def check_duplicates_data():
    table_list_gamedays = ['bl1_data_ergebnisse_kategorisiert', 'bl1_data_trainer_spiele', 'bl1_data_vereine_bookmaker_odds',
                           'bl1_data_vereine_data_gov', 'bl1_data_vereine_kader_wert', 'bl1_data_vereine_spielplan', 
                           'bl1_data_vereine_spielsystem']    
    
    for table in table_list_gamedays:
        query = 'select * from ' + table
        
        df = connection(query) 
        print(table)
        saisons = df['Saison'].drop_duplicates()    
        for s in saisons:
            df_s = df[df['Saison']==s]
            if len(df_s.drop_duplicates())==len(df_s):
                print('***************')
                print("No duplicates in saison ")
                print(s)
                print('***************')
            else:
                print('***************')
                print("DUPLICATES saison")
                print(s)  
                print('***************')
                
def check_duplicates_features():
    table_list_gamedays = ['bl1_features_club_data', 'bl1_features_club_form',
                           'bl1_features_forecast_club_data', 'bl1_features_forecast_club_form', 'bl1_features_odds']    
    
    for table in table_list_gamedays:
        query = 'select * from ' + table
        
        df = connection(query) 
        print(table)
        saisons = df['Saison'].drop_duplicates()    
        for s in saisons:
            df_s = df[df['Saison']==s]
            if len(df_s.drop_duplicates())==len(df_s):
                print('***************')
                print("No duplicates in saison ")
                print(s)
                print('***************')
            else:
                print('***************')
                print("DUPLICATES saison")
                print(s)  
                print('***************')
                
                
def check_matchdays():
    
    table_list_gamedays = ['bl1_data_ergebnisse_kategorisiert', 'bl1_data_trainer_spiele', 'bl1_data_vereine_bookmaker_odds',
                           'bl1_data_vereine_data_gov', 'bl1_data_vereine_kader_wert', 'bl1_data_vereine_spielplan', 
                           'bl1_data_vereine_spielsystem', 'bl1_features_club_data', 'bl1_features_club_form',
                           'bl1_features_forecast_club_data', 'bl1_features_forecast_club_form', 'bl1_features_odds', 
                           'bl1_staging_ergebnisse', 'bl1_staging_football_uk', 'bl1_staging_vereine_fifa_features', 
                           'bl1_staging_vereine_kommende_spieltag'] 
    
    for table in table_list_gamedays:
        query = 'select saison, count(distinct spieltag) from ' + table + ' group by saison'
        
        df = connection(query)   
        print('***************')
        print(table)
        print(df)
        print('***************')

def check_clubs():
    
    table_list_club_nbr = ['bl1_data_ergebnisse_kategorisiert', 'bl1_data_trainer_spiele',
                           'bl1_data_vereine_kader_wert', 'bl1_data_vereine_spielplan', 
                           'bl1_data_vereine_spielsystem', 'bl1_features_club_data', 'bl1_features_club_form',
                           'bl1_features_forecast_club_data', 'bl1_features_forecast_club_form',
                           'bl1_staging_vereine_fifa_features']    
    
    for table in table_list_club_nbr:
        query = 'select saison, spieltag, count(distinct vereins_id) as Clubs_Nbr from ' + table + ' group by saison, spieltag having count(distinct vereins_id) != 20 order by saison, spieltag'
        
        df = connection(query)    
        print('***************')
        print(table)
        if len(df)==0:
            print("Everything fine")
        else:
            print(df)
        print('***************')
        
def check_clubs_home_id():
    
    table_list_club_nbr_homeid = ['bl1_data_vereine_bookmaker_odds','bl1_data_vereine_data_gov', 'bl1_features_odds', 
                           'bl1_staging_ergebnisse', 'bl1_staging_football_uk', 
                           'bl1_staging_vereine_kommende_spieltag']    
    
    for table in table_list_club_nbr_homeid:
        query = 'select saison, spieltag, count(distinct Heimmannschaft_ID) as Clubs_Nbr from ' + table + ' group by saison, spieltag having count(distinct Heimmannschaft_ID) != 10 order by saison, spieltag'
        
        df = connection(query) 
        print('***************')
        print(table)
        if len(df)==0:
            print("Everything fine")
        else:
            print(df)
        print('***************')
        