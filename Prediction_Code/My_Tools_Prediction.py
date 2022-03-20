import os
os.chdir('D:/Projects/Football/Prediction_Code')


import pandas as pd
import Read_Load_Prediction as db


def get_relevant_gameday(gameday, season):
    
    f = db.get_data_db(4)
    df = f.get_data()
    df = df[df['Saison']==season]
    df = df[df['Spieltag']==gameday]
    
    return df
    
    
def conceeded_goals(df):
    df_all = pd.DataFrame()
    vereine = df['OpponentID'].drop_duplicates()
    
    for v in vereine:
        d = df[df['OpponentID']==v]
        l = len(d)
        d = d.assign(ZugelassenTore_Mittelwert = 0)
        for i in range(l):    
            d.iloc[i,4] = d.iloc[0:i+1,1].sum()/len(d.iloc[0:i+1,1])
        
        df_all = df_all.append(d)
        
    return df_all
    
    
def running_mean_heim(df):
    df_all = pd.DataFrame()
    vereine = df['Home_ID'].drop_duplicates()
    
    for v in vereine:
        d = df[df['Home_ID']==v]
        l = len(d)
        d = d.assign(Tore_Mittelwert = 0)
        for i in range(l):    
            d.iloc[i,4] = d.iloc[0:i+1,1].sum()/len(d.iloc[0:i+1,1])
        
        df_all = df_all.append(d)
        
    return df_all

def running_mean_auswärts(df):
    df_all = pd.DataFrame()
    vereine = df['Vereins_ID'].drop_duplicates()
    
    for v in vereine:
        d = df[df['Vereins_ID']==v]
        l = len(d)
        d = d.assign(Tore_Mittelwert = 0)
        for i in range(l):    
            d.iloc[i,4] = d.iloc[0:i+1,1].sum()/len(d.iloc[0:i+1,1])
        
        df_all = df_all.append(d)
        
    return df_all

def drop_less_home(df):
    vereine = df['Home_ID'].drop_duplicates()
    df_all = pd.DataFrame()
    for v in vereine:
        df_v = df[df['Home_ID']==v]
        l = len(df_v)
        
        if l > 90:
            df_all = df_all.append(df_v)
            
    return df_all

def drop_less_away(df):
    vereine = df['Vereins_ID'].drop_duplicates()
    df_all = pd.DataFrame()
    for v in vereine:
        df_v = df[df['Vereins_ID']==v]
        l = len(df_v)
        
        if l > 90:
            df_all = df_all.append(df_v)
            
    return df_all    