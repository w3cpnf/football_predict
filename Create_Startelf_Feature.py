import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#import other files 
import Read_Load_Database as db
import numpy as np 
import pandas as pd




def get_kicker_average_forecast():
    df = db.get_table('bl1_data_spieler_kicker_position')
    df_all = pd.DataFrame()
    for spieler in df['Spieler_ID'].drop_duplicates():
        df_spieler = df[df['Vereins_ID']==spieler]
        
        df_spieler = df_spieler.assign(Kicker_Grade_Average = 1)
        
        for s in range(len(df_spieler)):
            df_1 = df_spieler.iloc[0:s+1, :] 
            df_spieler.iloc[s, 8] = round(np.mean(df_1['Note']), 2)
        
        #df_all = df_all.append(df_spieler)
        df_all = pd.concat([df_all, df_spieler])
    return df_all


def get_kicker_average():
    df = db.get_table('bl1_data_spieler_kicker_position')
    df_all = pd.DataFrame()
    for spieler in df['Spieler_ID'].drop_duplicates():
        df_spieler = df[df['Vereins_ID']==spieler]
        
        df_spieler = df_spieler.assign(Kicker_Grade_Average = 1)
        
        for s in range(len(df_spieler)):
            df_1 = df_spieler.iloc[0:s, :] 
            df_spieler.iloc[s, 8] = round(np.mean(df_1['Note']), 2)
        
        #df_all = df_all.append(df_spieler)
        df_all = pd.concat([df_all, df_spieler])
    return df_all



def get_kicker_position_features():
    
    df = db.get_startelf_grades()
    df = df[['saison', 'spieltag', 'Vereins_ID', 'Position', 'Kicker_Grade_Average']]
    df = df.rename(columns={"saison": "Saison", "spieltag": "Spieltag"})
    df = df.fillna(3.0)
    df_all = pd.DataFrame()
    
    for saison in df['Saison'].drop_duplicates():
        df_saison = df[df['Saison'] == saison]
        
        for spieltag in df['Spieltag'].drop_duplicates():
            df_spieltag = df_saison[df_saison['Spieltag'] == spieltag]
            
            for verein in df['Vereins_ID'].drop_duplicates():
                df_verein = df_spieltag[df_spieltag['Vereins_ID'] == verein]
                
                abwehr = round(np.mean(df_verein[df_verein['Position'] == 'Abwehr']['Kicker_Grade_Average']), 2)
                mittelfeld = round(np.mean(df_verein[df_verein['Position'] == 'Mittelfeld']['Kicker_Grade_Average']), 2)
                sturm = round(np.mean(df_verein[df_verein['Position'] == 'Sturm']['Kicker_Grade_Average']), 2)
                tor = round(np.mean(df_verein[df_verein['Position'] == 'Tor']['Kicker_Grade_Average']), 2)
                
                df_verein = df_verein.assign(Abwehr_Kicker_Feature = abwehr, Mittelfeld_Kicker_Feature = mittelfeld
                                             ,Sturm_Kicker_Feature = sturm, Tor_Kicker_Feature =  tor )
                
                df_all = pd.concat([df_all, df_verein])
    df_all = df_all[['Saison', 'Spieltag', 'Vereins_ID', 'Abwehr_Kicker_Feature', 'Mittelfeld_Kicker_Feature'
                     ,'Sturm_Kicker_Feature', 'Tor_Kicker_Feature']]
    df_all = df_all.drop_duplicates()
    
    return df_all


def get_kicker_position_features_forecast():
    
    df = db.get_startelf_grades_forecast()
    df = df[['saison', 'spieltag', 'Vereins_ID', 'Position', 'Kicker_Grade_Average']]
    df = df.rename(columns={"saison": "Saison", "spieltag": "Spieltag"})
    
    df_all = pd.DataFrame()
    
    for saison in df['Saison'].drop_duplicates():
        df_saison = df[df['Saison'] == saison]
        
        for spieltag in df['Spieltag'].drop_duplicates():
            df_spieltag = df_saison[df_saison['Spieltag'] == spieltag]
            
            for verein in df['Vereins_ID'].drop_duplicates():
                df_verein = df_spieltag[df_spieltag['Vereins_ID'] == verein]
                
                abwehr = round(np.mean(df_verein[df_verein['Position'] == 'Abwehr']['Kicker_Grade_Average']), 2)
                mittelfeld = round(np.mean(df_verein[df_verein['Position'] == 'Mittelfeld']['Kicker_Grade_Average']), 2)
                sturm = round(np.mean(df_verein[df_verein['Position'] == 'Sturm']['Kicker_Grade_Average']), 2)
                tor = round(np.mean(df_verein[df_verein['Position'] == 'Tor']['Kicker_Grade_Average']), 2)
                
                df_verein = df_verein.assign(Abwehr_Kicker_Feature = abwehr, Mittelfeld_Kicker_Feature = mittelfeld
                                             ,Sturm_Kicker_Feature = sturm, Tor_Kicker_Feature =  tor )
                
                df_all = pd.concat([df_all, df_verein])
    df_all = df_all[['Saison', 'Spieltag', 'Vereins_ID', 'Abwehr_Kicker_Feature', 'Mittelfeld_Kicker_Feature'
                     ,'Sturm_Kicker_Feature', 'Tor_Kicker_Feature']]
    df_all = df_all.drop_duplicates()
    df_all = df_all.fillna(3.0)
    return df_all
#df_stat = get_opponent_stat()
#df_stat_forecast = get_opponent_statistic_forecast()

#df_stat_pl = get_opponent_stat_premierleague()
#df_stat_forecast_pl = get_opponent_statistic_forecast_premierleague()

#df_kicker_forecast = get_kicker_average_forecast()
#df_kicker = get_kicker_average()


#df_kicker_1 = df_kicker_forecast[df_kicker_forecast['Saison'] == '2014/15']
#df_kicker_2 = df_kicker_forecast[df_kicker_forecast['Saison'] == '2015/16']
#df_kicker_3 = df_kicker_forecast[df_kicker_forecast['Saison'] == '2017/18']
#df_kicker_4 = df_kicker_forecast[df_kicker_forecast['Saison'] == '2018/19']
#df_kicker_5 = df_kicker_forecast[df_kicker_forecast['Saison'] > '2018/19']

df_kicker_feature = get_kicker_position_features()
#df_kicker_feature_forecast = get_kicker_position_features_forecast()


#db.upload_replace_local_data_to_database(df_stat_forecast, 'bl1_feature_opponent_statistic_forecast')
#db.upload_replace_local_data_to_database(df_stat, 'bl1_feature_opponent_statistic')

#db.upload_replace_local_data_to_database(df_stat_forecast_pl, 'pl_feature_opponent_statistic_forecast')
#db.upload_replace_local_data_to_database(df_stat_pl, 'pl_feature_opponent_statistic')

#db.upload_local_data_to_database(df_kicker_5, 'bl1_data_kicker_average_grade_forecast')
#db.upload_local_data_to_database(df_kicker_5, 'bl1_data_kicker_average_grade')

#db.upload_replace_local_data_to_database(df_kicker_feature_forecast, 'bl1_feature_kicker_average_grade_forecast')
#db.upload_replace_local_data_to_database(df_kicker_feature, 'bl1_feature_kicker_average_grade')

