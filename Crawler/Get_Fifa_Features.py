import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time

#import other files 
import My_Tools as t
import Read_Load_Database as db

class fifa_features:
    
    def __init__(self, saison, spieltag, url):

        self.spieltag = spieltag
        self.url = url
        self.saison = saison
    
    def get_fifa_features(self):
        
        s = self.spieltag
        url = self.url
        saison = self.saison
        
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get(url)
        time.sleep(2)
        clubs = driver.find_elements_by_xpath("//td[@class='col-name-wide']") 
        overall = driver.find_elements_by_xpath("//td[@class='col col-oa']")
        attack = driver.find_elements_by_xpath("//td[@class='col col-at']")
        mittelfeld = driver.find_elements_by_xpath("//td[@class='col col-md']")
        abwehr = driver.find_elements_by_xpath("//td[@class='col col-df']")
    
                
        f_ver = t.get_df(clubs)
        df_verein = f_ver.df() 
        
        f_over =  t.get_df(overall)
        df_over = f_over.df() 
        
        f_attackt =  t.get_df(attack)
        df_attack = f_attackt.df() 
        
        f_mittelfeld =  t.get_df(mittelfeld)
        df_mittelfeld = f_mittelfeld.df()  
        
        f_abwehr =  t.get_df(abwehr)
        df_abwehr = f_abwehr.df()         
        
        driver.quit()
        df_verein = df_verein.drop(1, axis = 1)
        df_verein.columns = ['Verein']
        df_over.columns = ['Gesamt']
        df_attack.columns = ['Angriff']
        df_mittelfeld.columns = ['Mittelfeld']
        df_abwehr.columns = ['Abwehr']
        
        df = pd.concat([df_verein, df_over, df_attack, df_mittelfeld, df_abwehr], axis = 1)
        
        d = db.get_data_db(2)
        df_v = d.get_data()
        df_v = df_v[df_v['Saison']==saison]
        df_v = df_v[df_v['Spieltag']==s]
        df = df.replace({'SC Freiburg':'Sport-Club Freiburg', 'DSC Arminia Bielefeld':'DSC Arminia Bielefeld'})
        df = df.merge(df_v, on = 'Verein', how = 'inner')
        df = df[['Vereins_ID', 'Verein', 'Spieltag', 'Gesamt', 'Angriff', 'Abwehr', 'Mittelfeld', 'Jahr', 'Saison']]
        print(df)
        
        return df