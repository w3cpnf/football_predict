import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time

#import other files 
import My_Tools as t 
import Read_Load_Database as db

# always recent gameday
perf_url = 'https://www.ligainsider.de/bundesliga/noten/spieltag/saison-2020-2021/60107/'


class perf_index:
    
    def __init__(self, spieltag, url):
        self.spieltag = spieltag
        self.url = url

    def get_perf_index(self):
        url = self.url
        s = self.spieltag
        
        driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
        driver.get(url)
        
        time.sleep(10)
        player = driver.find_elements_by_xpath("//td[@class='text-left']")
        time.sleep(10)
        info = driver.find_elements_by_xpath("//td[@class='text-right']")
        time.sleep(10)
        note = driver.find_elements_by_xpath("//td[@class='text-right sorting_1']")
        
        
        f1 = t.get_df(player)
        f2 = t.get_df(info)
        f3 = t.get_df(note)
        
        df_player = f1.df()
        df_info = f2.df() 
        df_note = f3.df() 

        df_note.columns = ['Note_Spieltag']
        driver.quit()
        df_p = t.columns(df_player, 1)
        df_i = t.columns(df_info, 2)


        df_all = pd.concat([df_p, df_note, df_i], axis = 1) 
        df_all = df_all.assign(Spieltag = s)
        
        f4 = t.unify_letters(df_all, 1)
        df_all = f4.replace_letters()
        df_all = t.change_name_ligainsider(df_all)
        df_all = t.get_numbers(df_all)
    
        f5 = db.get_data_db(1)
        df_spieler_id = f5.get_data()  

        df_all = df_all.merge(df_spieler_id, on = 'Spieler', how = 'inner')
        
        f6 = db.get_data_db(13)
        df_spiele_plan = f6.get_data()
        df_all= df_all.merge(df_spiele_plan, on = ['Spieltag', 'Verein'], how = 'inner')
        
        return df_all 
    

#f = perf_index(1, perf_url)
#df = f.get_perf_index()













