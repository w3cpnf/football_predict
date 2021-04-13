import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

#import other files 
import My_Tools as t
import Read_Load_Database as db


class get_results_class:
    
    def __init__(self, spieltag, saison):

        self.spieltag = spieltag
        self.saison = saison
        
    def get_results(self):
    
        s = self.spieltag
        saison = self.saison
        season = saison[0:4]+'-20'+saison[5:7]
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get('https://www.bundesliga.com/de/bundesliga/spieltag/'+str(season)+'/'+str(s))
        erg = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'matchDataRow')))
        f = t.get_df(erg)
        df_erg = f.df()
        time.sleep(2)
       
        f = db.get_data_db(2)
        df_spielplan = f.get_data()
        df_spielplan = df_spielplan[df_spielplan['Saison']==saison]
        df_spielplan = df_spielplan[df_spielplan['Spieltag']==s]
        driver.quit()
  
        df_erg = df_erg.replace({'Bayer 04': 'Bayer 04 Leverkusen', 'SV Werder': 'SV Werder Bremen', 'SC Freiburg':'Sport-Club Freiburg',
                             'Borussia M\'gladbach':'Borussia Mönchengladbach', 'Union Berlin':'1. FC Union Berlin', 'FC Bayern':'FC Bayern München', 
                             'SCP07':'SC Paderborn 07', 'Mainz 05':'1. FSV Mainz 05', 'Schalke 04':'FC Schalke 04', 'TSG Hoffenheim':'TSG 1899 Hoffenheim'})
        df_erg = df_erg.drop([3], axis = 1)

        df_erg.columns = ['Heimmannschaft', 'Ergebnis', 'HalbzeitErgebnis', 'Auswärtsmannschaft']
        

        d = db.get_data_db(3)
        df = d.get_data()
        
        df_erg = df_erg.merge(df, left_on=['Heimmannschaft'] , right_on='Verein', how = 'inner')
        df_erg = df_erg.rename({'Vereins_ID':'Heimmannschaft_ID'}, axis = 1) 
        df_erg = df_erg.drop(['Verein'], axis = 1)
        df_erg = df_erg.merge(df, left_on=['Auswärtsmannschaft'] , right_on='Verein', how = 'inner')
        df_erg = df_erg.rename({'Vereins_ID':'Auswärtsmannschaft_ID'}, axis = 1) 
        df_erg = df_erg.drop(['Verein'], axis = 1)
        df_erg = df_erg.assign(Spieltag = s)
        df_erg = df_erg.merge(df_spielplan, left_on=['Heimmannschaft_ID', 'Spieltag'] , right_on=['Vereins_ID', 'Spieltag'], how = 'inner')
        df_erg = df_erg[['Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft', 'Ergebnis', 'HalbzeitErgebnis', 'Auswärtsmannschaft_ID', 
                        'Auswärtsmannschaft', 'Jahr', 'Saison']]

        df_erg = df_erg.drop_duplicates()
        return df_erg
    

class categorisation:
        
    def __init__(self, saison, spieltag):       
        self.saison = saison
        self.spieltag = spieltag
              
    def categorisation(self):  
        saison = self.saison
        spieltag = self.spieltag
                
        f = db.get_data_db(20)
        df = f.get_data()
        df = df[df['Saison']==saison]
        df = df[df['Spieltag']==spieltag]
        
        df = df.drop('HalbzeitErgebnis', axis = 1)
        df_tore_heim = df['Ergebnis'].str.split(':', expand = True)
        df_tore_auswärts = df['Ergebnis'].str.split(':', expand = True)
        df_tore_heim.columns = ['Tore', 'Gegentore']
        df_tore_auswärts.columns = ['Gegentore', 'Tore']
        f1 = t.as_int(df_tore_heim,1)
        f2 = t.as_int(df_tore_auswärts,1)
        df_tore_heim = f1.columns_to_int()
        df_tore_auswärts = f2.columns_to_int()
        df_heim = pd.concat([df_tore_heim, df], axis = 1)
        df_auswärts = pd.concat([df_tore_auswärts, df], axis = 1)
    
        df_heim = df_heim.assign(Differenz = lambda x: x['Tore']-x['Gegentore'])
        df_heim['Spiel_Ausgang'] = df_heim['Differenz'].apply(lambda x: '1' if x > 0 else ('-1' if x < 0 else '0'))
        df_heim = df_heim.rename(columns = {'Heimmannschaft_ID':'Vereins_ID', 'Heimmannschaft':'Verein', 'Auswärtsmannschaft_ID':'Gegner_ID', 'Auswärtsmannschaft':'Gegner'})
        df_heim = df_heim.assign(Heim = 1)
        df_heim = df_heim[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Jahr', 'Saison']]
        
        df_auswärts = df_auswärts.assign(Differenz = lambda x: x['Tore']-x['Gegentore'])
        df_auswärts['Spiel_Ausgang'] = df_auswärts['Differenz'].apply(lambda x: '1' if x > 0 else ('-1' if x < 0 else '0'))
        df_auswärts = df_auswärts.rename(columns = {'Auswärtsmannschaft_ID':'Vereins_ID', 'Auswärtsmannschaft':'Verein', 'Heimmannschaft_ID':'Gegner_ID', 'Heimmannschaft':'Gegner'})
        df_auswärts = df_auswärts.assign(Heim = 0)
        df_auswärts = df_auswärts[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Jahr','Saison']]
            
        df_all = df_heim.append(df_auswärts)
        df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Jahr',  'Saison']]
        
        return df_all
 


class coming_matchday:
    
    def __init__(self, spieltag, saison):

        self.spieltag = spieltag
        self.saison = saison   
        
    def get_coming_matchday(self):
        
        s = self.spieltag
        saison = self.saison
        season = saison[0:4]+'-20'+saison[5:7]
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get('https://www.bundesliga.com/de/bundesliga/spieltag/'+str(season)+'/'+str(s))
        erg = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'matchDataRow')))
        f = t.get_df(erg)
        df_erg = f.df()
        driver.quit()
        
        df_erg = df_erg.replace({'Bayer 04': 'Bayer 04 Leverkusen', 'SV Werder': 'SV Werder Bremen', 'SC Freiburg':'Sport-Club Freiburg',
                             'Borussia M\'gladbach':'Borussia Mönchengladbach', 'Union Berlin':'1. FC Union Berlin', 'FC Bayern':'FC Bayern München', 
                             'SCP07':'SC Paderborn 07', 'Mainz 05':'1. FSV Mainz 05', 'Schalke 04':'FC Schalke 04', 'TSG Hoffenheim':'TSG 1899 Hoffenheim'})

        if len(df_erg.columns)==4:
            df_erg = df_erg.drop([1,2], axis = 1)
        if len(df_erg.columns)==3:
            df_erg = df_erg.drop([1], axis = 1)
           
        
        df_erg.columns = ['Heimmannschaft', 'Auswärtsmannschaft']

        df_erg = df_erg.assign(Spieltag = s, Saison = saison)    
        d = db.get_data_db(3)
        df = d.get_data()
        
        df_erg = df_erg.merge(df, left_on=['Heimmannschaft'] , right_on='Verein', how = 'inner')
        df_erg = df_erg.rename({'Vereins_ID':'Heimmannschaft_ID'}, axis = 1) 
        df_erg = df_erg.drop(['Verein'], axis = 1)
        df_erg = df_erg.merge(df, left_on=['Auswärtsmannschaft'] , right_on='Verein', how = 'inner')
        df_erg = df_erg.rename({'Vereins_ID':'Auswärtsmannschaft_ID'}, axis = 1) 
        df_erg = df_erg.drop(['Verein'], axis = 1)
    
        df_erg = df_erg[[ 'Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Spieltag', 'Saison']]
        
        return df_erg


#d = coming_matchday(27, '2020/21')
#df = d.get_coming_matchday()


