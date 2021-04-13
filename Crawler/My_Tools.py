import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

import pandas as pd
import numpy as np


class get_df:
    
    def __init__(self, list_crawled):
        self.list_crawled = list_crawled

    def df(self):   
        list_crawled = self.list_crawled
        l = len(list_crawled)
        data = []
        for n in range(l):
            data.append(list_crawled[n].text)
        df = pd.DataFrame(data)     
        df = df[0].str.split('\n', expand = True)
        return df
    
    
class as_int:
    
    def __init__(self, df, case):
        self.df = df
        self.case = case
    def columns_to_int(self):   
        df = self.df
        case = self.case
        l_c = len(df.columns)
        
        if case == 1:
            for c in range(l_c):
                df.iloc[:,c] = df.iloc[:,c].astype(int)
                
        if case == 2:
            for c in range(1,l_c):
                df.iloc[:,c] = df.iloc[:,c].astype(int)            
        return df
 
    
class add_goals:
        
    def __init__(self, df, df_erg, spieltag):
                 
        self.df = df
        self.spieltag = spieltag
        self.df_erg = df_erg
        
    def get_bl1_club_data_result(self):
        
        df = self.df
        s = self.spieltag
        df_erg = self.df_erg
        
        df_erg = df_erg[df_erg['Spieltag'] == s]
        df = df[df['Spieltag'] == s]
        
        df_h = df_erg[['Heimmannschaft', 'Heimmannschaft_ID', 'Ergebnis']]
        df_h = df_h.assign(Heim = 1)
        df_a = df_erg[['Auswärtsmannschaft', 'Auswärtsmannschaft_ID', 'Ergebnis']]
        df_a = df_a.assign(Heim = 0)
        df_h[['Tore', 'Gegentore']] = df_h['Ergebnis'].str.split(':', expand = True)
        df_a[['Gegentore', 'Tore']] = df_a['Ergebnis'].str.split(':', expand = True)
        df_h = df_h.drop(['Ergebnis' ,'Tore'], axis = 1)
        df_a = df_a.drop(['Ergebnis','Tore'], axis = 1)
        
        df_h = df_h.rename(columns={'Heimmannschaft': 'Verein', 'Heimmannschaft_ID':'Vereins_ID'})
        df_a = df_a.rename(columns={'Auswärtsmannschaft': 'Verein', 'Auswärtsmannschaft_ID':'Vereins_ID'})
        
        df_ergebnisse = df_h.append(df_a)
        
        df_complete = df.merge(df_ergebnisse, on = ['Vereins_ID', 'Verein'], how = 'inner')
        
        return df_complete


def merge_on_club(df_1, df_2):
    df = df_1.merge(df_2, on = ['Vereins_ID', 'Verein'], how = 'inner')
    return df



class unify_letters:
    
    def __init__(self, df, param):
        
        self.df = df
        self.param = param
          
    def replace_letters(self):
        
        df = self.df
        param = self.param
        
        if param == 1:
            l_spieler = []
            for spieler in df['Spieler']:    
                spieler =  spieler.replace('ó','o')
                spieler =  spieler.replace('í','i')
                spieler =  spieler.replace('á','a')
                spieler =  spieler.replace('š','s')
                spieler =  spieler.replace('Ş','S')
                spieler =  spieler.replace('ć','c')
                spieler =  spieler.replace('é','e')
                spieler =  spieler.replace('ô','o')
                spieler =  spieler.replace('č','c')
                spieler =  spieler.replace('ř','r')
                spieler =  spieler.replace('ý','y')
                spieler =  spieler.replace('ł','l')
                spieler =  spieler.replace('å','a')
                spieler =  spieler.replace('á','a')
                spieler =  spieler.replace('Á','A')
                spieler =  spieler.replace('ð','d')
                spieler =  spieler.replace('è','e')
                spieler =  spieler.replace('ë','e')
                spieler =  spieler.replace('ą','a')
                spieler =  spieler.replace('ú','u')
                spieler =  spieler.replace('ã','a')
                spieler =  spieler.replace('ê','e')
                spieler =  spieler.replace('ç','c')
                spieler =  spieler.replace('ø','ö')
                spieler =  spieler.replace('ñ','n')
                
                l_spieler.append(spieler)
            
            df['Spieler'] = l_spieler
            
        if param == 2:
            l_trainer = []
            for trainer in df['Trainer']:    
                trainer =  trainer.replace('ó','o')
                trainer =  trainer.replace('í','i')
                trainer =  trainer.replace('á','a')
                trainer =  trainer.replace('š','s')
                trainer =  trainer.replace('Ş','S')
                trainer =  trainer.replace('ć','c')
                trainer =  trainer.replace('é','e')
                trainer =  trainer.replace('ô','o')
                trainer =  trainer.replace('č','c')
                trainer =  trainer.replace('ř','r')
                trainer =  trainer.replace('ý','y')
                trainer =  trainer.replace('ł','l')
                trainer =  trainer.replace('å','a')
                trainer =  trainer.replace('á','a')
                trainer =  trainer.replace('Á','A')
                trainer =  trainer.replace('ð','d')
                trainer =  trainer.replace('è','e')
                trainer =  trainer.replace('ë','e')
                trainer =  trainer.replace('ą','a')
                trainer =  trainer.replace('ú','u')
                trainer =  trainer.replace('ã','a')
                trainer =  trainer.replace('ê','e')
                trainer =  trainer.replace('ç','c')
                trainer =  trainer.replace('ø','ö')
                trainer =  trainer.replace('ñ','n')
                trainer =  trainer.replace('Č','C')
                trainer =  trainer.replace('ş','s')
                trainer =  trainer.replace('ı','i')  
                
                l_trainer.append(trainer)
                
            df['Trainer'] = l_trainer
        
        return df

   
def find_player_1(driver):
    clubs = driver.find_elements_by_class_name('odd')
    
    if clubs:
        return clubs
    else:
        return False
    
def find_player_2(driver):
    clubs = driver.find_elements_by_class_name('even')
    
    if clubs:
        return clubs
    else:
        return False

def get_list(l_1):
    l_2 = []
    i = len(l_1)
    for x in range(0,i):
        l_2.append(l_1[x].text)
        
    return l_2

def get_dataframe(l_1):
    l_2 = []
    
    for x in range(len(l_1)):
        l_2.append(l_1[x].text)
    df = pd.DataFrame(l_2)   
        
    return df

def find_date(driver):
    clubs = driver.find_elements_by_class_name('col-12')
    
    if clubs:
        return clubs
    else:
        return False
    
    
def get_new_player(df_1, df_2):
    df_rest = df_1.merge(df_2, on = ['Spieler'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
    df_rest = df_rest[['Spieler']]
    return df_rest



def columns(df, y):   
    #column = c[0]
    df.index = range(len(df))
    
    if y == 1:
        df.columns = ['Spieler']
        df = df.assign(Verein = 0, Position = 0)
           
    if y == 2:
        df.columns = ['Pkt_Spieltag']
        df = df.assign(Min_Spieltag = 0, Durchschnitt_Note = 0, Durchschnitt_Pos_Pkt = 0)
        
    if y == 3:
        df.columns = ['Abgwehrte_Schüsse']
        df = df.assign(Paraden = 0, Weiße_Weste = 0, Strafraum_Beherrschung = 0, Elfmeter_Pariert = 0, Großchancen_Pariert = 0, Fehler = 0)
        
    if y == 4:
        df.columns = ['Erfolgreiche_Pässe']
        df = df.assign(Gewonnene_Zweikämpfe = 0, Gewonnene_Luftkämpfe = 0, Erfolgreiche_Tacklings = 0, Fouls = 0, Geklärte_Bälle = 0, Abgefangene_Bälle = 0,
                       Ball_Eroberungen = 0, Ballverluste = 0, Erfolgreiche_Dribblings = 0, Torschuss_Vorlagen = 0, Kreierte_Großchancen = 0,
                       Schüsse_aufs_Tor = 0, Schussgenauigkeit = 0, Fehler_vor_Schuss_Gegentor = 0, Geblockte_Bälle = 0)
    if y == 5:
        df.columns = ['Saison']
        df = df.assign(Von = 0, Bis = 0)
        
    if y == 6:
        df.columns = ['Gesamt']
        df = df.assign(Angriff = 0, Abwehr = 0, Mittelfeld = 0, Hits = 0,  Verein = 0, Wettbewerb = 0)
        
    if y == 7:
        df = df.assign(x = 0, y = 0, c = 0) 
        df.columns = ['X', 'Place', 'Verein',  'Verein']
                
    if y == 8:
        df = df.assign(x = 0)      
        df.columns = ['Verein',  'Verein']
        
    if y == 9:
        df = df.assign(x = 0)      
        df.columns = ['Kaderwert', 'WertPerSpieler']
        
    col = len(df.columns)
    l_3 = int(len(df)/col)
    for c2 in range(0, l_3):   
        for c3 in range(0, col):
            df.iloc[c2,c3] = df.iloc[c2*col+c3,0]
    drop = []    
    for c4 in range(l_3,len(df)):
        drop.append(c4)
            
    df = df.drop(drop, axis = 0)  
    
    return df 

def get_outer_on_player(df_1, df_2):
    
    df_rest = df_1.merge(df_2, on = ['Spieler'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']

    return df_rest 

def change_name_ligainsider(df):
    df = df.replace({'Aaron':'Aaron Martin', 'Michael Cuisance':'Mickael Cuisance', 'Evan N\'Dicka':'Evan Ndicka', 'Pierre Kunde':'Kunde Malong'})
    df = df.replace({'Gladbach':'Borussia Mönchengladbach', 'SC Freiburg': 'Sport-Club Freiburg'})
    return df    

def get_numbers(df):
    
    df['Note_Spieltag'] = df['Note_Spieltag'].apply(lambda x: x.strip()).replace('', np.nan).fillna(0)
    df['Note_Spieltag'] = df['Note_Spieltag'].str.replace(',','.').astype(float)
    df['Durchschnitt_Note'] = df['Durchschnitt_Note'].apply(lambda x: x.strip()).replace('', np.nan).fillna(0)
    df['Durchschnitt_Note'] = df['Durchschnitt_Note'].fillna(0).str.replace(',','.').astype(float)
    df['Durchschnitt_Pos_Pkt'] = df['Durchschnitt_Pos_Pkt'].apply(lambda x: x.strip()).replace('', np.nan).fillna(0)
    df['Durchschnitt_Pos_Pkt'] = df['Durchschnitt_Pos_Pkt'].fillna(0).str.replace(',','.').astype(float)
    df['Pkt_Spieltag'] = df['Pkt_Spieltag'].apply(lambda x: x.strip()).replace('', np.nan).fillna(0)
    df['Pkt_Spieltag']  = df['Pkt_Spieltag'].astype(float)
    df = df.fillna(0)
    
    return df    

class get_df_without:
    
    def __init__(self, list_crawled):
        self.list_crawled = list_crawled

    def df_without(self):   
        list_crawled = self.list_crawled
        l = len(list_crawled)
        data = []
        for n in range(l):
            data.append(list_crawled[n].text)
        df = pd.DataFrame(data)     
        return df


