import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')
#packages and modules
import pandas as pd

#import other files 
import Read_Load_Database as db



def get_form(saison, spieltag):
    
  
    df = db.get_table('bl1_data_ergebnisse_kategorisiert')
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Saison', 'Spieltag'])      
    seasons = df['Saison'].drop_duplicates()
    
    for s in seasons:
        df_season = df[df['Saison']==s]
        vereine = df_season['Vereins_ID'].drop_duplicates()
        
        for v in vereine:
            df_club = df_season[df_season['Vereins_ID']==v]
            results = df_club['Spiel_Ausgang']
            df_club = df_club.assign(L1=results.values, L2=results.values, L3=results.values, L4 = results, L5 = results)
            df_club['L1'] = df_club['L1'].shift(1)
            df_club['L2'] = df_club['L2'].shift(2)
            df_club['L3'] = df_club['L3'].shift(3)
            df_club['L4'] = df_club['L4'].shift(4)
            df_club['L5'] = df_club['L5'].shift(5)
            
            df_club = df_club.fillna(0)
            
            df_all = df_all.append(df_club)
    df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Heim', 'Saison', 'L1', 'L2', 'L3', 'L4', 'L5']]  
    df_all = df_all[df_all['Saison']==saison]  
    df_all = df_all[df_all['Spieltag']==spieltag] 
    df_all = df_all.drop_duplicates()
    
    return df_all


def get_form_home(df):
    
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Saison', 'Spieltag'])      
    seasons = df['Saison'].drop_duplicates()
    
    for s in seasons:
        df_season = df[df['Saison']==s]
        vereine = df_season['Vereins_ID'].drop_duplicates()
        
        for v in vereine:
            df_club = df_season[df_season['Vereins_ID']==v]
            df_club_home = df_club[df_club['Heim']==1]
            df_club_home.index = range(len(df_club_home))
            results = df_club_home['Spiel_Ausgang']
            df_club_home = df_club_home.assign(HL1=results.values, HL2=results.values, HL3=results.values, HL4 = results, HL5 = results)
            df_club_home['HL1'] = df_club_home['HL1'].shift(1)
            df_club_home['HL2'] = df_club_home['HL2'].shift(2)
            df_club_home['HL3'] = df_club_home['HL3'].shift(3)
            df_club_home['HL4'] = df_club_home['HL4'].shift(4)
            df_club_home['HL5'] = df_club_home['HL5'].shift(5)
            df_club_home = df_club_home.fillna(0)
            df_club_home = df_club_home[['Spieltag', 'Saison', 'Vereins_ID', 'Verein', 'Heim', 'HL1', 'HL2', 
                             'HL3', 'HL4', 'HL5']]
            df_all = df_all.append(df_club_home)
    
    return df_all


def get_form_away(df):
    
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Saison', 'Spieltag'])      
    seasons = df['Saison'].drop_duplicates()
    
    for s in seasons:
        df_season = df[df['Saison']==s]
        vereine = df_season['Vereins_ID'].drop_duplicates()
        
        for v in vereine:
            df_club = df_season[df_season['Vereins_ID']==v]
            df_club_away = df_club[df_club['Heim']==0]
            df_club_away.index = range(len(df_club_away))
            results_away = df_club_away['Spiel_Ausgang']
            df_club_away = df_club_away.assign(AL1=results_away.values, AL2=results_away.values,
                                               AL3=results_away.values,
                                               AL4 = results_away.values, AL5 = results_away.values)
            df_club_away['AL1'] = df_club_away['AL1'].shift(1)
            df_club_away['AL2'] = df_club_away['AL2'].shift(2)
            df_club_away['AL3'] = df_club_away['AL3'].shift(3)
            df_club_away['AL4'] = df_club_away['AL4'].shift(4)
            df_club_away['AL5'] = df_club_away['AL5'].shift(5)
            df_club_away = df_club_away.fillna(0)
            df_club_away = df_club_away[['Spieltag', 'Saison', 'Vereins_ID', 'Verein', 'Heim',
                     'AL1', 'AL2', 'AL3', 'AL4', 'AL5']] 
            df_all = df_all.append(df_club_away)
    
    return df_all


#need to check how to handle 1 +1 Saison

def get_form_forcast(saison, spieltag):
    
    df = db.get_table('bl1_data_ergebnisse_kategorisiert')    
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Saison', 'Spieltag'])      
    seasons = df['Saison'].drop_duplicates()
    
    for s in seasons:
        df_season = df[df['Saison']==s]
        vereine = df_season['Vereins_ID'].drop_duplicates()
        
        for v in vereine:
            df_club = df_season[df_season['Vereins_ID']==v]
            results = df_club['Spiel_Ausgang']
            df_club = df_club.assign(L1_Forecast=results.values, L2_Forecast=results.values,
                                     L3_Forecast=results.values, L4_Forecast = results, L5_Forecast = results)

            df_club['L1_Forecast'] = df_club['L1_Forecast']
            df_club['L2_Forecast'] = df_club['L2_Forecast'].shift(1)
            df_club['L3_Forecast'] = df_club['L3_Forecast'].shift(2)
            df_club['L4_Forecast'] = df_club['L4_Forecast'].shift(3)
            df_club['L5_Forecast'] = df_club['L5_Forecast'].shift(4)
            df_club = df_club.fillna(0)
            df_club = df_club.assign(Spieltag = lambda x: x['Spieltag']+1)
            df_club = df_club[df_club['Spieltag']!=35]

            df_all = df_all.append(df_club)
            
    
    df_all = df_all[['Spieltag', 'Saison', 'Vereins_ID', 'Verein', 'L1_Forecast', 'L2_Forecast', 'L3_Forecast', 
                     'L4_Forecast', 'L5_Forecast']]
    
    df_all = df_all[df_all['Saison']==saison]  
    df_all = df_all[df_all['Spieltag']==spieltag] 
    df_all = df_all.drop_duplicates()
    
    return df_all

#df_form = get_form('2021/22', 8)

#df_form_forecast = get_form_forcast('2021/22', 8)
#df_form_forecast = df_form_forecast.drop_duplicates()

#df_form_home = get_form_home(df)
#df_form_home = df_form_home.drop_duplicates()
#df_form_away = get_form_away(df)
#df_form_away = df_form_away.drop_duplicates()


#db.upload_replace_local_data_to_database(df_form_home, 'bl1_features_club_home_form')
#db.upload_replace_local_data_to_database(df_form_away, 'bl1_features_club_away_form')
#db.upload_replace_local_data_to_database(df_form, 'bl1_features_club_form')
#db.upload_local_data_to_database(df_form_forecast, 'bl1_features_forecast_club_form')


def first_gameday(saison, spieltag):
    df = db.get_table('bl1_data_vereine_spielplan') 
    df = df[df['Saison']==saison]

    vereine = df['Vereins_ID'].drop_duplicates()
    
    df_all = pd.DataFrame()
    
    for v in vereine:
        df_club = df[df['Vereins_ID']==v]
        df_club = df_club.assign(L1_Forecast = 0, L2_Forecast = 0, L3_Forecast = 0, L4_Forecast = 0, L5_Forecast = 0)
        df_all = df_all.append(df_club)
        
    df_all = df_all[['Spieltag', 'Saison', 'Vereins_ID', 'Verein', 'L1_Forecast', 'L2_Forecast', 'L3_Forecast', 
                     'L4_Forecast', 'L5_Forecast']]
    return df_all

#df = first_gameday('2021/22', 1)
#db.upload_replace_local_data_to_database(df, 'bl1_features_forecast_club_form')




#*******************************************************************************
#*******************************************************************************


def get_form_pl(saison, spieltag):
    
    df = db.get_table('pl_data_ergebnisse_kategorisiert')    
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Saison', 'Spieltag'])      
    seasons = df['Saison'].drop_duplicates()
    
    for s in seasons:
        df_season = df[df['Saison']==s]
        vereine = df_season['Vereins_ID'].drop_duplicates()
        
        for v in vereine:
            df_club = df_season[df_season['Vereins_ID']==v]
            results = df_club['Spiel_Ausgang']
            df_club = df_club.assign(L1=results.values, L2=results.values, L3=results.values, L4 = results, L5 = results)
            df_club['L1'] = df_club['L1'].shift(1)
            df_club['L2'] = df_club['L2'].shift(2)
            df_club['L3'] = df_club['L3'].shift(3)
            df_club['L4'] = df_club['L4'].shift(4)
            df_club['L5'] = df_club['L5'].shift(5)
            
            df_club = df_club.fillna(0)
            
            df_all = df_all.append(df_club)
    df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Heim', 'Saison', 'L1', 'L2', 'L3', 'L4', 'L5']]  
    df_all = df_all[df_all['Saison']==saison]  
    df_all = df_all[df_all['Spieltag']==spieltag] 
    df_all = df_all.drop_duplicates()
    
    return df_all


def get_form_forcast_pl(saison, spieltag):
    
    df = db.get_table('pl_data_ergebnisse_kategorisiert')       
    df_all = pd.DataFrame()
    df = df.sort_values(by = ['Saison', 'Spieltag'])      
    seasons = df['Saison'].drop_duplicates()
    
    for s in seasons:
        df_season = df[df['Saison']==s]
        vereine = df_season['Vereins_ID'].drop_duplicates()
        
        for v in vereine:
            df_club = df_season[df_season['Vereins_ID']==v]
            results = df_club['Spiel_Ausgang']
            df_club = df_club.assign(L1_Forecast=results.values, L2_Forecast=results.values,
                                     L3_Forecast=results.values, L4_Forecast = results, L5_Forecast = results)

            df_club['L1_Forecast'] = df_club['L1_Forecast']
            df_club['L2_Forecast'] = df_club['L2_Forecast'].shift(1)
            df_club['L3_Forecast'] = df_club['L3_Forecast'].shift(2)
            df_club['L4_Forecast'] = df_club['L4_Forecast'].shift(3)
            df_club['L5_Forecast'] = df_club['L5_Forecast'].shift(4)
            df_club = df_club.fillna(0)
            df_club = df_club.assign(Spieltag = lambda x: x['Spieltag']+1)
            df_club = df_club[df_club['Spieltag']!=35]

            df_all = df_all.append(df_club)
            
    
    df_all = df_all[['Spieltag', 'Saison', 'Vereins_ID', 'Verein', 'L1_Forecast', 'L2_Forecast', 'L3_Forecast', 
                     'L4_Forecast', 'L5_Forecast']]
    
    df_all = df_all[df_all['Saison']==saison]  
    df_all = df_all[df_all['Spieltag']==spieltag] 
    df_all = df_all.drop_duplicates()
    
    return df_all

#df_form = get_form_pl('2021/22', 8)

#df_form_forecast = get_form_forcast_pl('2021/22', 21)
#df_form_forecast = df_form_forecast.drop_duplicates()

#df_form_forecast['Spieltag']
#db.upload_replace_local_data_to_database(df_form, 'pl_features_club_form')
#db.upload_local_data_to_database(df_form_forecast, 'pl_features_forecast_club_form')


def first_gameday_pl(saison, spieltag):
    
    df = db.get_table('pl_data_vereine_spielplan') 
    df = df[df['Saison']==saison]

    vereine = df['Vereins_ID'].drop_duplicates()
    
    df_all = pd.DataFrame()
    
    for v in vereine:
        df_club = df[df['Vereins_ID']==v]
        df_club = df_club.assign(L1_Forecast = 0, L2_Forecast = 0, L3_Forecast = 0, L4_Forecast = 0, L5_Forecast = 0)
        df_all = df_all.append(df_club)
        
    df_all = df_all[['Spieltag', 'Saison', 'Vereins_ID', 'Verein', 'L1_Forecast', 'L2_Forecast', 'L3_Forecast', 
                     'L4_Forecast', 'L5_Forecast']]
    return df_all

#df = first_gameday('2021/22', 1)
#db.upload_replace_local_data_to_database(df, 'bl1_features_forecast_club_form')
























