import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')
#packages and modules
import pandas as pd

#import other files 
import Read_Load_Database as db

d = db.get_data_db(22)
df = d.get_data()

def get_form(df):
    
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
    df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Heim', 'Jahr', 'Saison', 'L1', 'L2', 'L3', 'L4', 'L5']]    
    return df_all


def get_form_home_away(df):
    
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
            df_club_home = df_club_home[['Spieltag', 'HL1', 'HL2',
                             'HL3', 'HL4', 'HL5']]               
            #'Vereins_ID', 'Verein', 'Heim', 'Jahr', 'Saison',
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
            df_club_away = df_club_away[['Spieltag', 
                     'AL1', 'AL2', 'AL3', 'AL4', 'AL5']]    
            #'Vereins_ID', 'Verein', 'Heim', 'Jahr', 'Saison', 
            #df_both = df_club_home.merge(df_club_away, how = 'outer', on = 'Spieltag')
            #merge on spielatg, saison, vereins_id and verein
            df_both = pd.concat([df_club_home, df_club_away], axis = 0)
            
            df_all = df_all.append(df_both)
            
            
    # df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Heim', 'Jahr', 'Saison', 'HL1', 'HL2', 'HL3', 'HL4', 'HL5',
    #                  'AL1', 'AL2', 'AL3', 'AL4', 'AL5']]    
    # df_all = df_all.dropna()
    # df_all.index = range(len(df_all))
    
    return df_all

df_form_home_away = get_form_home_away(df)

def get_form_forcast(df):
    
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
            df_all = df_all.append(df_club)
    
    df_forecast = pd.DataFrame()
    df_all = df_all[['Spieltag', 'Saison', 'Vereins_ID', 'Verein', 'L1_Forecast', 'L2_Forecast', 'L3_Forecast', 
                     'L4_Forecast', 'L5_Forecast']]
    df_current_season = df_all[df_all['Saison']=='2020/21']  
    vereine_current = df_current_season['Vereins_ID'].drop_duplicates()
    
    for v1 in vereine_current:
        df_club_current = df_current_season[df_current_season['Vereins_ID']==v1]
        df_club_current = df_club_current.tail(1)
        df_club_current = df_club_current.assign(Spieltag = lambda x: x['Spieltag']+1)
        df_forecast = df_forecast.append(df_club_current)
        
    return df_forecast

#df_form = get_form(df)

#df_form_forecast = get_form_forcast(df)


#db.upload_replace_local_data_to_database(df_form_home_away, 'bl1_features_club_home_away_form')
#db.upload_replace_local_data_to_database(df_form, 'bl1_features_club_form')
#db.upload_replace_local_data_to_database(df_form_forecast, 'bl1_features_forecast_club_form')

#f = db.get_data_db(23)
#df_kommender_spieltag = f.get_data()
#df_kommender_spieltag = df_kommender_spieltag[df_kommender_spieltag['Spieltag']==27]