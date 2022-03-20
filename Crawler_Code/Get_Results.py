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
    
        spieltag = self.spieltag
        saison = self.saison
        season_entered = saison[0:4]+'-'+saison[5:7]
        
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get('https://www.kicker.de/1-bundesliga/spieltag/'+str(season_entered)+'/'+str(spieltag))
        
        time.sleep(2)
        
        clubs = driver.find_elements_by_xpath("//div[@class='kick__v100-gameCell__team__name']")
        results = driver.find_elements_by_xpath("//div[@class='kick__v100-scoreBoard__scoreHolder ']")
        halftime_results = driver.find_elements_by_xpath("//div[@class='kick__v100-scoreBoard__scoreHolder kick__v100-scoreBoard__scoreHolder--subscore']")
        
        f_1 = t.get_df(results)
        f_2 = t.get_df(clubs)    
        f_3 = t.get_df(halftime_results) 
        
        df_clubs = f_2.df()
        df_clubs.columns = ['Verein']
 
        df_clubs = df_clubs.replace({'Bayern München': 'FC Bayern München', 'Bor. Mönchengladbach': 'Borussia Mönchengladbach', 'TSG Hoffenheim': 'TSG 1899 Hoffenheim',
                                     'SC Freiburg': 'Sport-Club Freiburg', 'Werder Bremen': 'SV Werder Bremen',
                                     'Arminia Bielefeld':'DSC Arminia Bielefeld'})
        df_id = db.get_table('master_vereins_id')
        
        #df_clubs = df_clubs[df_clubs['Verein']!='FC Augsburg']
        #df_clubs = df_clubs[df_clubs['Verein']!='1. FSV Mainz 05']       
        df_clubs = df_clubs.merge(df_id, on = 'Verein', how = 'inner')

        df_clubs = df_clubs.assign(Auswärtsmannschaft = 0, Auswärtsmannschaft_ID = 0)
        
        for i in range(1, len(df_clubs)):
            df_clubs.iloc[i-1, 2] = df_clubs.iloc[i, 0]
            df_clubs.iloc[i-1, 3] = df_clubs.iloc[i, 1]  
            
        df_clubs = df_clubs.iloc[::2]  
        df_clubs.index = range(len(df_clubs))
        df_clubs = df_clubs.assign(Spieltag = spieltag, Saison = saison, Jahr = 2021)
        df_clubs = df_clubs.rename(columns={"Verein": "Heimmannschaft", "Vereins_ID": "Heimmannschaft_ID"})      
        df_halftime = f_3.df()
        df_ergebnisse = f_1.df()
        
        df_ergebnisse['Ergebnis'] = df_ergebnisse[0] + df_ergebnisse[1] + df_ergebnisse[2]
        df_halftime['HalbzeitErgebnis'] = df_halftime[0] + df_halftime[1] + df_halftime[2]
        
        df_halftime = df_halftime.drop([0,1,2], axis = 1)
        df_ergebnisse = df_ergebnisse.drop([0,1,2], axis = 1)
 

        df = pd.concat([df_clubs, df_ergebnisse, df_halftime], axis = 1)
       
        driver.quit()

        df = df[['Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft', 'Ergebnis', 'HalbzeitErgebnis', 
                         'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Saison']]

        df = df.drop_duplicates()
        return df
    
#e = get_results_class(25, '2021/22')
#df = e.get_results()
# df.iloc[5,5] = 31
# df.iloc[5,6] = 'DSC Arminia Bielefeld'

# df.iloc[6,6] = 'VfL Bochum'
# df.iloc[6,5] = 26
# df.iloc[6,2] = 'Eintracht Frankfurt'
# df.iloc[6,1] = 12

# df.iloc[7,6] = 'RB Leipzig'
# df.iloc[7,5] = 2
# df.iloc[7,2] = 'SpVgg Greuther Fürth'
# df.iloc[7,1] = 26
# df = df[df['Auswärtsmannschaft']!= 0]
#db.upload_local_data_to_database(df, 'bl1_staging_ergebnisse')

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
        df_heim = df_heim[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Saison']]
        
        df_auswärts = df_auswärts.assign(Differenz = lambda x: x['Tore']-x['Gegentore'])
        df_auswärts['Spiel_Ausgang'] = df_auswärts['Differenz'].apply(lambda x: '1' if x > 0 else ('-1' if x < 0 else '0'))
        df_auswärts = df_auswärts.rename(columns = {'Auswärtsmannschaft_ID':'Vereins_ID', 'Auswärtsmannschaft':'Verein', 'Heimmannschaft_ID':'Gegner_ID', 'Heimmannschaft':'Gegner'})
        df_auswärts = df_auswärts.assign(Heim = 0)
        df_auswärts = df_auswärts[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Saison']]
            
        df_all = df_heim.append(df_auswärts)
        df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Saison']]
        
        return df_all
 


class coming_matchday:
    
    def __init__(self, spieltag, season):

        self.spieltag = spieltag
        self.season = season   
        
    def get_coming_matchday(self):
        spieltag = self.spieltag
        season = self.season
        season_entered = season[0:4]+'-'+season[5:7]
        
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get('https://www.kicker.de/1-bundesliga/spieltag/'+str(season_entered)+'/'+str(spieltag))
        
        time.sleep(5)
        vereine = driver.find_elements_by_xpath("//div[@class='kick__v100-gameCell__team__name']")
       
        f_2 = t.get_df(vereine)
        df_clubs = f_2.df()
        df_clubs.columns = ['Verein']
        
        df_clubs = df_clubs.replace({'Bayern München': 'FC Bayern München', 'Bor. Mönchengladbach': 'Borussia Mönchengladbach', 'TSG Hoffenheim': 'TSG 1899 Hoffenheim',
                                     'SC Freiburg': 'Sport-Club Freiburg', 'Werder Bremen': 'SV Werder Bremen',
                                     'Arminia Bielefeld':'DSC Arminia Bielefeld'})
        v_id = db.get_data_db(3)
        df_id = v_id.get_data()       
        df_clubs = df_clubs.merge(df_id, on = 'Verein', how = 'inner')
        df_clubs = df_clubs.assign(Auswärtsmannschaft = 0, Auswärtsmannschaft_ID = 0)
        
        for i in range(1, len(df_clubs)):
            df_clubs.iloc[i-1, 2] = df_clubs.iloc[i, 0]
            df_clubs.iloc[i-1, 3] = df_clubs.iloc[i, 1]
            
        df_clubs = df_clubs.assign(Spieltag = spieltag, Saison = season)   
        df_clubs = df_clubs.rename(columns={"Verein": "Heimmannschaft", "Vereins_ID": "Heimmannschaft_ID"})
        
        driver.quit()
        df_clubs = df_clubs.iloc[::2]        
     
        df_clubs = df_clubs[[ 'Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Spieltag', 'Saison']]
        
        return df_clubs


#d = coming_matchday(1, '2021/22')
#df = d.get_coming_matchday()
#db.upload_local_db_data(df, 18)
  

              
def categorisation_1(saison, spieltag):  
          
    f = db.get_data_db(20)
    df = f.get_data()
    #df = df[df['Saison']==saison]
    #df = df[df['Spieltag']==spieltag]
    
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
    df_heim['Spiel_Ausgang'] = df_heim['Differenz'].apply(lambda x: '1' if x > 0 else ('0' if x < 0 else '0.5'))
    df_heim = df_heim.rename(columns = {'Heimmannschaft_ID':'Vereins_ID', 'Heimmannschaft':'Verein', 'Auswärtsmannschaft_ID':'Gegner_ID', 'Auswärtsmannschaft':'Gegner'})
    df_heim = df_heim.assign(Heim = 1)
    df_heim = df_heim[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Saison']]
    
    df_auswärts = df_auswärts.assign(Differenz = lambda x: x['Tore']-x['Gegentore'])
    df_auswärts['Spiel_Ausgang'] = df_auswärts['Differenz'].apply(lambda x: '1' if x > 0 else ('0' if x < 0 else '0.5'))
    df_auswärts = df_auswärts.rename(columns = {'Auswärtsmannschaft_ID':'Vereins_ID', 'Auswärtsmannschaft':'Verein', 'Heimmannschaft_ID':'Gegner_ID', 'Heimmannschaft':'Gegner'})
    df_auswärts = df_auswärts.assign(Heim = 0)
    df_auswärts = df_auswärts[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Saison']]
        
    df_all = df_heim.append(df_auswärts)
    df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Saison']]
    
    return df_all

#df = categorisation_1('2014/15', 1)
#.upload_replace_local_data_to_database(df, 'bl1_data_ergebnisse_normalisiert')


class coming_matchday_premier_league:
    
    def __init__(self, spieltag, season):

        self.spieltag = spieltag
        self.season = season   
        
    def get_coming_matchday(self):
        spieltag = self.spieltag
        season = self.season
        season_entered = season[0:4]+'-'+season[5:7]

        url = 'https://www.kicker.de/premier-league/spieltag/'+str(season_entered)+'/'+str(spieltag)
        print(url)
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get(url)

        time.sleep(5)
        vereine = driver.find_elements_by_xpath("//div[@class='kick__v100-gameCell__team__name']")
       
        f_2 = t.get_df(vereine)
        df_clubs = f_2.df()
        df_clubs = df_clubs.iloc[0:20]
        df_clubs.columns = ['Verein']

        v_id = db.get_data_db(3)
        df_id = v_id.get_data()       
        df_clubs = df_clubs.merge(df_id, on = 'Verein', how = 'inner')
        df_clubs = df_clubs.assign(Auswärtsmannschaft = 0, Auswärtsmannschaft_ID = 0)
        
        for i in range(1, len(df_clubs)):
            df_clubs.iloc[i-1, 2] = df_clubs.iloc[i, 0]
            df_clubs.iloc[i-1, 3] = df_clubs.iloc[i, 1]
            
        df_clubs = df_clubs.assign(Spieltag = spieltag, Saison = season)   
        df_clubs = df_clubs.rename(columns={"Verein": "Heimmannschaft", "Vereins_ID": "Heimmannschaft_ID"})
        
        driver.quit()
        df_clubs = df_clubs.iloc[::2]        
     
        df_clubs = df_clubs[[ 'Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Spieltag', 'Saison']]
        
        return df_clubs


#d = coming_matchday_premier_league(1, '2014/15')
#df = d.get_coming_matchday()
#db.upload_local_db_data(df, 18)



class get_premierleague_results_class:
    
    def __init__(self, spieltag, saison):

        self.spieltag = spieltag
        self.saison = saison
        
    def get_results(self):
    
        spieltag = self.spieltag
        saison = self.saison
        season_entered = saison[0:4]+'-'+saison[5:7]
        
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get('https://www.kicker.de/premier-league/spieltag/'+str(season_entered)+'/'+str(spieltag))
        #driver.get('https://www.kicker.de/1-bundesliga/spieltag/'+str(season_entered)+'/'+str(spieltag))
        
        time.sleep(2)
        
        clubs = driver.find_elements_by_xpath("//div[@class='kick__v100-gameCell__team__name']")
        results = driver.find_elements_by_xpath("//div[@class='kick__v100-scoreBoard__scoreHolder ']")
        halftime_results = driver.find_elements_by_xpath("//div[@class='kick__v100-scoreBoard__scoreHolder kick__v100-scoreBoard__scoreHolder--subscore']")
        
        f_1 = t.get_df(results)
        
        f_2 = t.get_df(clubs)    
        f_3 = t.get_df(halftime_results) 
        
        df_clubs = f_2.df()
        df_clubs.columns = ['Verein']
        df_clubs = df_clubs.iloc[0:20]
        #print(df_clubs)
        #df_clubs = df_clubs[df_clubs['Verein']!='FC Arsenal']
        #df_clubs = df_clubs[df_clubs['Verein']!='FC Liverpool']
        #df_clubs = df_clubs[df_clubs['Verein']!='FC Chelsea']
        #df_clubs = df_clubs[df_clubs['Verein']!='Leicester City']


        v_id = db.get_data_db(3)
        df_id = v_id.get_data()       
        df_clubs = df_clubs.merge(df_id, on = 'Verein', how = 'inner')

        df_clubs = df_clubs.assign(Auswärtsmannschaft = 0, Auswärtsmannschaft_ID = 0)

        for i in range(1, len(df_clubs)):
            df_clubs.iloc[i-1, 2] = df_clubs.iloc[i, 0]
            df_clubs.iloc[i-1, 3] = df_clubs.iloc[i, 1]  
            
        df_clubs = df_clubs.iloc[::2]  

        df_clubs.index = range(len(df_clubs))
        df_clubs = df_clubs.assign(Spieltag = spieltag, Saison = saison)
        df_clubs = df_clubs.rename(columns={"Verein": "Heimmannschaft", "Vereins_ID": "Heimmannschaft_ID"})    

        df_halftime = f_3.df()
        df_ergebnisse = f_1.df()
        print(df_ergebnisse)
        df_ergebnisse = df_ergebnisse.iloc[0:10]
        df_ergebnisse['Ergebnis'] = df_ergebnisse[0] + df_ergebnisse[1] + df_ergebnisse[2]
        df_halftime['HalbzeitErgebnis'] = df_halftime[0] + df_halftime[1] + df_halftime[2]
        df_halftime = df_halftime.iloc[0:10]
        df_halftime = df_halftime.drop([0,1,2], axis = 1)
        df_ergebnisse = df_ergebnisse.drop([0,1,2], axis = 1)

        df = pd.concat([df_clubs, df_ergebnisse, df_halftime], axis = 1)

        driver.quit()

        df = df[['Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft', 'Ergebnis', 'HalbzeitErgebnis', 
                         'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Saison']]

        df = df.drop_duplicates()

        
        return df
    
#e = get_premierleague_results_class(27, '2021/22')
#df = e.get_results()
#df = df.dropna()
#db.upload_local_data_to_database(df, 'pl_staging_ergebnisse')


class categorisation_premier_league:
        
    def __init__(self, saison, spieltag):       
        self.saison = saison
        self.spieltag = spieltag
              
    def categorisation_premier_league(self):  
        saison = self.saison
        spieltag = self.spieltag
                
        f = db.get_data_db(56)
        df = f.get_data()
        df = df[df['Saison']==saison]
        df = df[df['Spieltag']==spieltag]
        
        df = df.drop('HalbzeitErgebnis', axis = 1)
        df_tore_heim = df['Ergebnis'].str.split(':', expand = True)
        df_tore_auswärts = df['Ergebnis'].str.split(':', expand = True)
        df_tore_heim.columns = ['Tore', 'Gegentore']
        df_tore_auswärts.columns = ['Gegentore', 'Tore']
        f1 = t.as_int(df_tore_heim, 1)
        f2 = t.as_int(df_tore_auswärts, 1)
        df_tore_heim = f1.columns_to_int()
        df_tore_auswärts = f2.columns_to_int()
        df_heim = pd.concat([df_tore_heim, df], axis = 1)
        df_auswärts = pd.concat([df_tore_auswärts, df], axis = 1)
    
        df_heim = df_heim.assign(Differenz = lambda x: x['Tore']-x['Gegentore'])
        df_heim['Spiel_Ausgang'] = df_heim['Differenz'].apply(lambda x: '1' if x > 0 else ('-1' if x < 0 else '0'))
        df_heim = df_heim.rename(columns = {'Heimmannschaft_ID':'Vereins_ID', 'Heimmannschaft':'Verein', 'Auswärtsmannschaft_ID':'Gegner_ID', 'Auswärtsmannschaft':'Gegner'})
        df_heim = df_heim.assign(Heim = 1)
        df_heim = df_heim[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Saison']]
        
        df_auswärts = df_auswärts.assign(Differenz = lambda x: x['Tore']-x['Gegentore'])
        df_auswärts['Spiel_Ausgang'] = df_auswärts['Differenz'].apply(lambda x: '1' if x > 0 else ('-1' if x < 0 else '0'))
        df_auswärts = df_auswärts.rename(columns = {'Auswärtsmannschaft_ID':'Vereins_ID', 'Auswärtsmannschaft':'Verein', 'Heimmannschaft_ID':'Gegner_ID', 'Heimmannschaft':'Gegner'})
        df_auswärts = df_auswärts.assign(Heim = 0)
        df_auswärts = df_auswärts[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner','Saison']]
            
        df_all = df_heim.append(df_auswärts)
        df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Spiel_Ausgang', 'Heim', 'Tore', 'Gegentore', 'Gegner_ID', 'Gegner', 'Saison']]
        
        return df_all
    
    
#f = categorisation_premier_league('2014/15', 1)
#df = f.categorisation_premier_league() 
#db.upload_local_data_to_database(df, 'pl_data_ergebnisse_kategorisiert')

