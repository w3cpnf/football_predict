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
    
    def __init__(self, spieltag, saison):

        self.spieltag = spieltag
        self.saison = saison
        
    def get_game_data(self):
        
        s = self.spieltag
        saison = self.saison
        
        d = db.get_data_db(20)
        df = d.get_data()
        
        df = df[df['Saison']==saison] 
        df_1 = df[df['Spieltag']==s] 
        df_all = pd.DataFrame()
        
        df_1.index = range(len(df_1.index))
        vereine = df_1['Heimmannschaft'].drop_duplicates()
        
        for v in vereine:
            
            df_v = df_1[df_1['Heimmannschaft']==v]
            
            df_h = df_v[['Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft', 'Saison']]
            df_a = df_v[['Spieltag', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Saison']]
            
            a = df_a['Auswärtsmannschaft'].iloc[0]
            
            df_h = df_h.rename(columns = {'Heimmannschaft_ID': 'Vereins_ID', 'Heimmannschaft':'Verein'})
            df_a = df_a.rename(columns = {'Auswärtsmannschaft_ID': 'Vereins_ID', 'Auswärtsmannschaft':'Verein'})
                      
            driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
            driver.get('http://www.google.com')
            
            if v == 'RB Leipzig':
                v = a
                
            if v == '1. FC Union Berlin':
                v = 'Union Berlin'
            
            if v == 'FC Schalke 04':
                v = 'Schalke 04'
                
            if v == 'FC Bayern München':
                v = 'Bayern München'  
                      
            if v == '1. FC Köln':
                v = 'FC Köln'  
                
            query = 'bundesliga ergebnisse '+ str(v) + ' ' + str(s) + ' Spieltag'
            search = driver.find_element_by_name('q')
            search.send_keys(query)
            time.sleep(3)
            search.send_keys(Keys.RETURN)
            time.sleep(2)
            #driver.find_element_by_xpath('//*[@text ="Ich stimme zu"]').click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//button[@id="L2AGLb"]'))).click()
            time.sleep(2)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'imso-hov')))
            #imso-ani imso_mh__tas
            #
            element.click()
            time.sleep(5)
            spiel = driver.find_elements_by_xpath("//tr[@class='MzWkAb']")
            
            f = t.get_df(spiel)
            df_spiel = f.df() 
            df_spiel = df_spiel[0].str.split(' ', expand = True)
            driver.quit()
            
            df_h = df_h.assign(Ballbesitz = df_spiel[0].iloc[2], Torschüsse = df_spiel[0].iloc[1], Schüsse = df_spiel[0].iloc[0], RoteKarten = df_spiel[0].iloc[7], Pässe = df_spiel[0].iloc[3], 
                               Passquote = df_spiel[0].iloc[4], Fouls = df_spiel[0].iloc[5], GelbeKarten = df_spiel[0].iloc[6], Ecken = df_spiel[0].iloc[9], Abseits = df_spiel[0].iloc[8],
                               Heim = 1)   
            
            df_a= df_a.assign(Ballbesitz = df_spiel[3].iloc[2], Torschüsse = df_spiel[2].iloc[1], Schüsse = df_spiel[2].iloc[0], RoteKarten = df_spiel[3].iloc[7], Pässe = df_spiel[2].iloc[3],
                              Passquote = df_spiel[2].iloc[4], Fouls = df_spiel[2].iloc[5], GelbeKarten = df_spiel[3].iloc[6], Ecken = df_spiel[2].iloc[9], Abseits = df_spiel[2].iloc[8],
                              Heim = 0) 
            df_both = pd.concat([df_h, df_a], axis = 0)
            
            df_both = df_both.assign(Flanken = 0)
            df_both = df_both[['Vereins_ID', 'Verein', 'Spieltag', 'Torschüsse', 'Schüsse', 'Fouls', 'GelbeKarten', 'RoteKarten', 'Flanken', 'Ecken', 'Ballbesitz', 'Heim', 'Saison']]
            df_all = df_all.append(df_both)
            
        return df_all
    

#f = game_data(28, '2020/21')
#df = f.get_game_data()
#db.upload_local_db_data(df, 5)
    
def get_game_data(s):
    

        d = db.get_data_db(20)
        df = d.get_data()
        df = df[df['Saison']=='2016/17']
        df_1 = df[df['Spieltag']==s]
        df_1.index = range(len(df_1.index))
        df_all = pd.DataFrame()

        
        vereine = df_1['Heimmannschaft'].drop_duplicates()
        
        for v in vereine:
            
            df_v = df_1[df_1['Heimmannschaft']==v]
            
            df_h = df_v[['Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft', 'Saison']]
            df_a = df_v[['Spieltag', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Saison']]
            
            a = df_a['Auswärtsmannschaft'].iloc[0]
            
            df_h = df_h.rename(columns = {'Heimmannschaft_ID': 'Vereins_ID', 'Heimmannschaft':'Verein'})
            df_a = df_a.rename(columns = {'Auswärtsmannschaft_ID': 'Vereins_ID', 'Auswärtsmannschaft':'Verein'})
                      
            driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
            driver.get('http://www.google.com')
            
            if v == 'RB Leipzig':
                v = a
            
            query = 'bundesliga ergebnisse saison 2016/17 '+ str(v) + ' ' + str(s) + ' Spieltag'
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
            #Passquote = df_spiel[0].iloc[4] Passquote = df_spiel[2].iloc[4]
            df_h = df_h.assign(Ballbesitz = df_spiel[0].iloc[2], Torschüsse = df_spiel[0].iloc[1], Schüsse = df_spiel[0].iloc[0], RoteKarten = df_spiel[0].iloc[6], Pässe = df_spiel[0].iloc[3], 
                               Fouls = df_spiel[0].iloc[4], GelbeKarten = df_spiel[0].iloc[5], Ecken = df_spiel[0].iloc[8], Abseits = df_spiel[0].iloc[7], Heim = 1)   
            
            df_a= df_a.assign(Ballbesitz = df_spiel[3].iloc[2], Torschüsse = df_spiel[2].iloc[1], Schüsse = df_spiel[2].iloc[0], RoteKarten = df_spiel[3].iloc[6], Pässe = df_spiel[2].iloc[3],
                             Fouls = df_spiel[2].iloc[4], GelbeKarten = df_spiel[3].iloc[5], Ecken = df_spiel[2].iloc[8], Abseits = df_spiel[2].iloc[7], Heim = 0)
    
            df_both = pd.concat([df_h, df_a], axis = 0)
            
            df_both = df_both.assign(Flanken = 0)

            df_both = df_both[['Vereins_ID', 'Verein', 'Spieltag', 'Torschüsse', 'Schüsse', 'Fouls', 'GelbeKarten', 'RoteKarten', 'Flanken', 'Ecken', 'Ballbesitz', 'Heim', 'Saison']]
            df_all = df_all.append(df_both)
        
        return df_all

#df = get_game_data(32)
#db.upload_local_db_data(df, 5)

        
def get_game_data_single_games(spieltag, saison, h_id, var, url):
        
    d = db.get_data_db(20)
    df = d.get_data()
    
    df = df[df['Saison']==saison] 
    df_1 = df[df['Spieltag']==spieltag] 
             
    df_v = df_1[df_1['Heimmannschaft_ID']==h_id]
    
    df_h = df_v[['Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft', 'Saison']]
    df_a = df_v[['Spieltag', 'Auswärtsmannschaft_ID', 'Auswärtsmannschaft', 'Saison']]
    
    df_h = df_h.rename(columns = {'Heimmannschaft_ID': 'Vereins_ID', 'Heimmannschaft':'Verein'})
    df_a = df_a.rename(columns = {'Auswärtsmannschaft_ID': 'Vereins_ID', 'Auswärtsmannschaft':'Verein'})
              
    driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
    driver.get(url)
    
    time.sleep(5)
    spiel = driver.find_elements_by_xpath("//tr[@class='MzWkAb']")

    f = t.get_df(spiel)
    df_spiel = f.df() 
    print(df_spiel)
    df_spiel = df_spiel[0].str.split(' ', expand = True)
    driver.quit()
    print(df_spiel)
    
    if var == 1:
        df_h = df_h.assign(Schüsse = df_spiel[0].iloc[0], Torschüsse = df_spiel[0].iloc[1], Ballbesitz = df_spiel[0].iloc[2], 
                           Pässe = df_spiel[0].iloc[3], RoteKarten = df_spiel[0].iloc[7], 
                           Passquote = df_spiel[0].iloc[4], Fouls = df_spiel[0].iloc[5], GelbeKarten = df_spiel[0].iloc[6], Ecken = df_spiel[0].iloc[9], Abseits = df_spiel[0].iloc[8],
                           Heim = 1)   
        
        df_a= df_a.assign(Ballbesitz = df_spiel[3].iloc[2], Torschüsse = df_spiel[2].iloc[1], Schüsse = df_spiel[2].iloc[0], RoteKarten = df_spiel[3].iloc[7], Pässe = df_spiel[2].iloc[3],
                          Passquote = df_spiel[2].iloc[4], Fouls = df_spiel[2].iloc[5], GelbeKarten = df_spiel[3].iloc[6], Ecken = df_spiel[2].iloc[9], Abseits = df_spiel[2].iloc[8],
                          Heim = 0) 
    if var == 2:     
        df_h = df_h.assign(Schüsse = df_spiel[0].iloc[0], Torschüsse = df_spiel[0].iloc[1], Ballbesitz = df_spiel[0].iloc[2], 
                           Pässe = df_spiel[0].iloc[3], Fouls = df_spiel[0].iloc[4], GelbeKarten = df_spiel[0].iloc[5], 
                           RoteKarten = df_spiel[0].iloc[6], Abseits = df_spiel[0].iloc[7],Ecken = df_spiel[0].iloc[8],
                           Heim = 1)   
        
        df_a= df_a.assign(Ballbesitz = df_spiel[3].iloc[2], Torschüsse = df_spiel[2].iloc[1], 
                          Schüsse = df_spiel[2].iloc[0], RoteKarten = df_spiel[3].iloc[6], Pässe = df_spiel[2].iloc[3],
                          Fouls = df_spiel[2].iloc[4], GelbeKarten = df_spiel[3].iloc[5], Ecken = df_spiel[2].iloc[8],
                          Abseits = df_spiel[2].iloc[7], Heim = 0)    
        
    df_both = pd.concat([df_h, df_a], axis = 0)
    
    df_both = df_both.assign(Flanken = 0)
    df_both = df_both.assign(Passquote = 0)
    df_both = df_both[['Vereins_ID', 'Verein', 'Spieltag', 'Torschüsse', 'Schüsse', 'Fouls', 'GelbeKarten', 'RoteKarten', 'Flanken', 'Ecken', 'Ballbesitz', 'Heim', 'Saison']]
        
    return df_both

#df = get_game_data_single_games(32, '2016/17', 23, 2, 'https://www.google.de/search?q=bundesliga+saison+2016%2F17+spieltag+32&sxsrf=ALeKk019VSRQn_ifjbFN47cOM1tWv2cJpA%3A1622972216430&ei=OJe8YKnbGfX97_UPh9mPqA8&oq=bundesliga+saison+2016%2F17+spieltag+32&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEM0CMgUIABDNAjIFCAAQzQI6BwgAEEcQsAM6BggAEBYQHlDu0ZAJWN_SkAlgt92QCWgCcAJ4AIABiQGIAfsBkgEDMi4xmAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwip18LT2oLxAhX1_rsIHYfsA_UQ4dUDCA4&uact=5#sie=m;/g/11ggrl17zl;2;/m/037169;dt;fp;1;;')
#db.upload_local_db_data(df, 5)

