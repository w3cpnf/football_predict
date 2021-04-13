import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


import My_Tools as t
import Read_Load_Database as db

class game_data:
    
    def __init__(self, spieltag):

        self.spieltag = spieltag
        
    def get_game_data(self):
        
        s = self.spieltag
        d = db.get_data_db(2)
        df = d.get_data()
        
        df_all = pd.DataFrame()
        df_1 = df[df['Spieltag']==s] 
        df_1.index = range(len(df_1.index))
        vereine = df_1['Heimmannschaft'].drop_duplicates()
        
        for v in vereine:
            
            df_v = df_1[df_1['Heimmannschaft']==v]
            
            df_h = df_v[['Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft','Jahr', 'Woche', 'Saison']]
            df_a = df_v[['Spieltag', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Jahr', 'Woche', 'Saison']]
            
            a = df_a['Auswärtsmannschaft'].iloc[0]
            
            df_h = df_h.rename(columns = {'Heimmannschaft_ID': 'Vereins_ID', 'Heimmannschaft':'Verein'})
            df_a = df_a.rename(columns = {'Auswärtsmannschaft_ID': 'Vereins_ID', 'Auswärtsmannschaft':'Verein'})
                      
            driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
            driver.get('http://www.google.com')
            
            if v == 'RB Leipzig':
                v = a
            
            query = 'bundesliga ergebnisse '+ str(v) + ' ' + str(s) + ' Spieltag'
            search = driver.find_element_by_name('q')
            search.send_keys(query)
            time.sleep(3)
            search.send_keys(Keys.RETURN)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'imso-hov')))
            element.click()
            time.sleep(3)
            spiel = driver.find_elements_by_xpath("//tr[@class='MzWkAb']")
            
            f = t.get_df(spiel)
            df_spiel = f.df() 
            df_spiel = df_spiel[0].str.split(' ', expand = True)
            driver.quit()
            
            df_h = df_h.assign(Ballbesitz = df_spiel[0].iloc[2], Torschüsse = df_spiel[0].iloc[1], Schüsse = df_spiel[0].iloc[0], RoteKarten = df_spiel[0].iloc[7], Pässe = df_spiel[0].iloc[3], 
                               Passquote = df_spiel[0].iloc[4], Fouls = df_spiel[0].iloc[5], GelbeKarten = df_spiel[0].iloc[6], Ecken = df_spiel[0].iloc[9], Abseits = df_spiel[0].iloc[8])   
            
            df_a= df_a.assign(Ballbesitz = df_spiel[3].iloc[2], Torschüsse = df_spiel[2].iloc[1], Schüsse = df_spiel[2].iloc[0], RoteKarten = df_spiel[3].iloc[7], Pässe = df_spiel[2].iloc[3],
                              Passquote = df_spiel[2].iloc[4], Fouls = df_spiel[2].iloc[5], GelbeKarten = df_spiel[3].iloc[6], Ecken = df_spiel[2].iloc[9], Abseits = df_spiel[2].iloc[8])
    
            df_both = pd.concat([df_h, df_a], axis = 0)
            
            df_both = df_both.assign(Flanken = 0)
            df_both = df_both[['Vereins_ID', 'Verein', 'Spieltag', 'Torschüsse', 'Schüsse', 'Fouls', 'GelbeKarten', 'RoteKarten', 'Flanken', 'Ecken', 'Ballbesitz', 'Heim', 'Jahr', 'Woche', 'Saison']]
            df_all = df_all.append(df_both)
            
        return df_all
    
    
def get_game_data(s):
    

        d = db.get_data_db(20)
        df = d.get_data()
        
        df_all = pd.DataFrame()
        df_1 = df[df['Spieltag']==s] 
        df_1.index = range(len(df_1.index))
        vereine = df_1['Heimmannschaft'].drop_duplicates()
        
        for v in vereine:
            
            df_v = df_1[df_1['Heimmannschaft']==v]
            
            df_h = df_v[['Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft','Jahr', 'Saison']]
            df_a = df_v[['Spieltag', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Jahr', 'Saison']]
            
            a = df_a['Auswärtsmannschaft'].iloc[0]
            
            df_h = df_h.rename(columns = {'Heimmannschaft_ID': 'Vereins_ID', 'Heimmannschaft':'Verein'})
            df_a = df_a.rename(columns = {'Auswärtsmannschaft_ID': 'Vereins_ID', 'Auswärtsmannschaft':'Verein'})
                      
            driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
            driver.get('http://www.google.com')
            
            if v == 'RB Leipzig':
                v = a
            
            query = 'bundesliga ergebnisse saison 2017/18 '+ str(v) + ' ' + str(s) + ' Spieltag'
            search = driver.find_element_by_name('q')
            search.send_keys(query)
            time.sleep(3)
            search.send_keys(Keys.RETURN)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'imso-hov')))
            element.click()
            time.sleep(3)
            spiel = driver.find_elements_by_xpath("//tr[@class='MzWkAb']")
            
            f = t.get_df(spiel)
            df_spiel = f.df() 
            df_spiel = df_spiel[0].str.split(' ', expand = True)
            driver.quit()
            
            df_h = df_h.assign(Ballbesitz = df_spiel[0].iloc[2], Torschüsse = df_spiel[0].iloc[1], Schüsse = df_spiel[0].iloc[0], RoteKarten = df_spiel[0].iloc[7], Pässe = df_spiel[0].iloc[3], 
                               Passquote = df_spiel[0].iloc[4], Fouls = df_spiel[0].iloc[5], GelbeKarten = df_spiel[0].iloc[6], Ecken = df_spiel[0].iloc[9], Abseits = df_spiel[0].iloc[8])   
            
            df_a= df_a.assign(Ballbesitz = df_spiel[3].iloc[2], Torschüsse = df_spiel[2].iloc[1], Schüsse = df_spiel[2].iloc[0], RoteKarten = df_spiel[3].iloc[7], Pässe = df_spiel[2].iloc[3],
                              Passquote = df_spiel[2].iloc[4], Fouls = df_spiel[2].iloc[5], GelbeKarten = df_spiel[3].iloc[6], Ecken = df_spiel[2].iloc[9], Abseits = df_spiel[2].iloc[8])
    
            df_both = pd.concat([df_h, df_a], axis = 0)
            
            df_both = df_both.assign(Flanken = 0)

            df_both = df_both[['Vereins_ID', 'Verein', 'Spieltag', 'Torschüsse', 'Schüsse', 'Fouls', 'GelbeKarten', 'RoteKarten', 'Flanken', 'Ecken', 'Ballbesitz', 'Heim', 'Jahr', 'Saison']]
            df_all = df_all.append(df_both)
        
        return df_all

#df = get_game_data(1)


