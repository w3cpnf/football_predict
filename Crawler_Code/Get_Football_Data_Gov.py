import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd


#import other files 
import Read_Load_Database as db


def get_staging_football(spieltag, saison):
    
    df = pd.read_csv('D:/Projects/Football/Database/2021_22.csv')
    df = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG','HTHG', 'HTAG', 'HS', 
                           'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A',
                           'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA']]
    df['Date'] = pd.to_datetime(df['Date'])
    
    df = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG','HTHG', 'HTAG', 'HS', 
                           'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A',
                           'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA']]
    df = df.replace({'Bayern Munich':'FC Bayern München', 'Dortmund': 'Borussia Dortmund'
                     ,'Ein Frankfurt':'Eintracht Frankfurt', 'FC Koln':'1. FC Köln', 'Hannover':'Hannover 96'
                     ,'Hertha': 'Hertha BSC', 'Hoffenheim':'TSG 1899 Hoffenheim', 'M\'gladbach':'Borussia Mönchengladbach'
                     ,'Paderborn':'SC Paderborn 07', 'Augsburg':'FC Augsburg', 'Hamburg':'Hamburger SV'
                     ,'Leverkusen':'Bayer 04 Leverkusen', 'Schalke 04':'FC Schalke 04','Stuttgart':'VfB Stuttgart'
                     ,'Werder Bremen':'SV Werder Bremen','Wolfsburg':'VfL Wolfsburg','Freiburg':'Sport-Club Freiburg'
                     ,'Mainz':'1. FSV Mainz 05','Darmstadt':'SV Darmstadt 98','Ingolstadt':'FC Ingolstadt 04'
                     ,'Fortuna Dusseldorf':'Fortuna Düsseldorf','Nurnberg':'1. FC Nürnberg'
                     ,'Union Berlin':'1. FC Union Berlin', 'Bielefeld':'DSC Arminia Bielefeld'
                     ,'Greuther Furth':'SpVgg Greuther Fürth', 'Bochum':'VfL Bochum'})
    
    df = df.rename(columns={'Date': 'Datum', 'HomeTeam': 'Heimmannschaft', 'AwayTeam':'Auswärtsmannschaft', 'FTHG':'Heimtore'
                            ,'FTAG':'Auswärtstore', 'HTHG':'Heimtore_Halbzeit', 'HTAG':'Auswärtstore_Halbzeit'
                            ,'HS':'Schüsse_Heim', 'AS':'Schüsse_Auswärts', 'HST':'Torschüsse_Heim'
                            , 'AST':'Torschüsse_Auswärts'
                            ,'HF':'Fouls_Heim','AF':'Fouls_Auswärts','HC':'Ecken_Heim','AC':'Ecken_Auswärts'
                            ,'HY':'Gelbe_Karten_Heim','AY':'Gelbe_Karten_Auswärts', 'HR':'Rote_Karten_Heim'
                            ,'AR':'Rote_Karten_Auswärts'})
    
    df = df.assign(Saison = saison)
    
    df['Datum'] = pd.to_datetime(df['Datum'])
    
    f1 = db.get_data_db(27)
    df_join = f1.get_data()
    df_join = df_join[df_join['Saison']==saison]
    
    df_all = df.merge(df_join, on = ['Heimmannschaft', 'Auswärtsmannschaft', 'Saison'])
    
    df_all = df_all[df_all['Spieltag']==spieltag]
    print(df_all)
    return df_all



def get_data(saison, spieltag):
    
    df_gov = db.get_table('bl1_staging_football_uk') 
    df = df_gov[['Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 
                           'Saison', 'Spieltag', 'Auswärtstore_Halbzeit', 'Schüsse_Heim', 'Schüsse_Auswärts', 
                           'Torschüsse_Heim', 'Torschüsse_Auswärts', 'Fouls_Heim', 'Fouls_Auswärts', 'Ecken_Heim',
                           'Ecken_Auswärts', 'Gelbe_Karten_Heim', 'Gelbe_Karten_Auswärts',
                           'Rote_Karten_Heim', 'Rote_Karten_Auswärts']]

    df = df[df['Saison']==saison]
    df = df[df['Spieltag']==spieltag]

    return df
    
def get_odds(saison, spieltag):
    df_gov = db.get_table('bl1_staging_football_uk') 
    
    df = df_gov[['Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 
                'Saison', 'Spieltag', 'B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA']]
    df = df[df['Saison']==saison]
    df = df[df['Spieltag']==spieltag]

    return df



def get_feature_odds(df):
    
    df = df[['Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 
            'Saison', 'Spieltag', 'B365H', 'B365D', 'B365A']] 
    
    return df


#df = get_staging_football(12, '2021/22')
#db.upload_local_data_to_database(df, 'bl1_staging_football_uk')
#df_game_data = get_data('2021/22', 12)
#df_bookmaker = get_odds('2021/22', 14)
#df_feature_odds = get_feature_odds('2021/22', 14)
#db.upload_local_data_to_database(df_bookmaker, 'bl1_data_vereine_bookmaker_odds')
#db.upload_local_data_to_database(df_game_data, 'bl1_data_vereine_data_gov')

#db.upload_local_data_to_database(df_feature_odds, 'bl1_features_odds')


def get_staging_football_pl(spieltag, saison):
    
    df = pd.read_csv('D:/Projects/Football/Database/pl_2021_22.csv')
    df = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG','HTHG', 'HTAG', 'HS', 
                           'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A',
                           'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA']]
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    df = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG','HTHG', 'HTAG', 'HS', 
                           'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A',
                           'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA']]
    df = df.replace({'Arsenal':'FC Arsenal', 'Leicester':'Leicester City', 'Everton':'FC Everton', 'Man United':'Manchester United'
                     ,'Swansea': 'Swansea City', 'QPR':'Queens Park Rangers', 'Hull':'Hull City', 'Sheffield United':'Sheffield United'
                     ,'Stoke':'Stoke City', 'West Brom':'West Bromwich Albion', 'Sunderland':'AFC Sunderland'
                     ,'West Ham':'West Ham United','Tottenham':'Tottenham Hotspur', 'Wolves':'Wolverhampton Wanderers'
                     ,'Liverpool':'FC Liverpool','Southampton':'FC Southampton','Newcastle':'Newcastle United'
                     ,'Man City':'Manchester City','Burnley':'FC Burnley', 'Huddersfield':'Huddersfield Town'
                     ,'Chelsea':'FC Chelsea', 'Bournemouth':'AFC Bournemouth', 'Brighton':'Brighton & Hove Albion'
                     ,'Norwich':'Norwich City', 'Watford':'FC Watford', 'Middlesbrough':'FC Middlesbrough'
                     ,'Cardiff':'Cardiff City', 'Fulham':'FC Fulham', 'Leeds':'Leeds United', 'Brentford':'FC Brentford'})
    
    df = df.rename(columns={'Date': 'Datum', 'HomeTeam': 'Heimmannschaft', 'AwayTeam':'Auswärtsmannschaft', 'FTHG':'Heimtore'
                            ,'FTAG':'Auswärtstore', 'HTHG':'Heimtore_Halbzeit', 'HTAG':'Auswärtstore_Halbzeit'
                            ,'HS':'Schüsse_Heim', 'AS':'Schüsse_Auswärts', 'HST':'Torschüsse_Heim'
                            , 'AST':'Torschüsse_Auswärts'
                            ,'HF':'Fouls_Heim','AF':'Fouls_Auswärts','HC':'Ecken_Heim','AC':'Ecken_Auswärts'
                            ,'HY':'Gelbe_Karten_Heim','AY':'Gelbe_Karten_Auswärts', 'HR':'Rote_Karten_Heim'
                            ,'AR':'Rote_Karten_Auswärts'})
    df = df.assign(Saison = saison)
    
    df['Datum'] = pd.to_datetime(df['Datum'])
    
    f1 = db.get_data_db(68)
    df_join = f1.get_data()
    df_join = df_join[df_join['Saison']==saison]
    print(df_join['Heimmannschaft'])
    print(df['Heimmannschaft'])
    df_all = df.merge(df_join, on = ['Heimmannschaft', 'Auswärtsmannschaft', 'Saison'])
    print(df_all)
    df_all = df_all[df_all['Spieltag']==spieltag]
    print(df_all)
    return df_all


def get_data_pl(saison, spieltag):
    
    df_gov = db.get_table('pl_staging_football_uk') 
    df = df_gov[['Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 
                           'Saison', 'Spieltag', 'Auswärtstore_Halbzeit', 'Schüsse_Heim', 'Schüsse_Auswärts', 
                           'Torschüsse_Heim', 'Torschüsse_Auswärts', 'Fouls_Heim', 'Fouls_Auswärts', 'Ecken_Heim',
                           'Ecken_Auswärts', 'Gelbe_Karten_Heim', 'Gelbe_Karten_Auswärts',
                           'Rote_Karten_Heim', 'Rote_Karten_Auswärts']]

    df = df[df['Saison']==saison]
    df = df[df['Spieltag']==spieltag]

    return df

    df_gov = f.get_data()
    df = df_gov[['Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 
                           'Saison', 'Spieltag', 'Auswärtstore_Halbzeit', 'Schüsse_Heim', 'Schüsse_Auswärts', 
                           'Torschüsse_Heim', 'Torschüsse_Auswärts', 'Fouls_Heim', 'Fouls_Auswärts', 'Ecken_Heim',
                           'Ecken_Auswärts', 'Gelbe_Karten_Heim', 'Gelbe_Karten_Auswärts',
                           'Rote_Karten_Heim', 'Rote_Karten_Auswärts']]

    df = df[df['Saison']==saison]
    df = df[df['Spieltag']==spieltag]

    return df
    
def get_odds_pl(saison, spieltag):
    df_gov = db.get_table('pl_staging_football_uk') 
    
    df = df_gov[['Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 
                'Saison', 'Spieltag', 'B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA']]
    df = df[df['Saison']==saison]
    df = df[df['Spieltag']==spieltag]

    return df



def get_feature_odds_pl(df):
    
    df = df[['Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 
            'Saison', 'Spieltag', 'B365H', 'B365D', 'B365A']] 
    
    return df

#df = get_staging_football_pl(16, '2021/22')
#db.upload_local_data_to_database(df, 'pl_staging_football_uk')
#df_game_data = get_data_pl('2021/22', 16)
#df_bookmaker = get_odds_pl('2021/22', 16)
#df_feature_odds = get_feature_odds_pl(df_bookmaker)
#db.upload_local_data_to_database(df_bookmaker, 'pl_data_vereine_bookmaker_odds')
#db.upload_local_data_to_database(df_game_data, 'pl_data_vereine_data_gov')

#db.upload_local_data_to_database(df_feature_odds, 'pl_features_odds')

