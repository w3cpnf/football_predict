import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')


#packages and modules
import pandas as pd
from selenium import webdriver
import time


import Tools as t
import Read_Load_Database as db

l_v = ['https://www.transfermarkt.de/fc-bayern-munchen/startseite/verein/27/saison_id/2020',, 
       'https://www.transfermarkt.de/borussia-dortmund/startseite/verein/16/saison_id/2020',
       'https://www.transfermarkt.de/fc-schalke-04/startseite/verein/33/saison_id/2020',
       'https://www.transfermarkt.de/vfl-wolfsburg/startseite/verein/82/saison_id/2020',
       'https://www.transfermarkt.de/bayer-04-leverkusen/startseite/verein/15/saison_id/2020',
       'https://www.transfermarkt.de/tsg-1899-hoffenheim/startseite/verein/533/saison_id/2020',
       'https://www.transfermarkt.de/tsg-1899-hoffenheim/startseite/verein/533/saison_id/2020',
       'https://www.transfermarkt.de/sc-freiburg/startseite/verein/60/saison_id/2020']

id_vereine = [27, 16, 33, 82, 15,  18, 533, 39, 44, 24, 86,  60, 23826, 3, 89, 10, 79]

# 167,
vereine = ['fc-bayern-munchen', 'borussia-dortmund', 'fc-schalke-04', 'vfl-wolfsburg', 'bayer-04-leverkusen', 'borussia-monchengladbach', 'tsg-1899-hoffenheim', 
            '1-fsv-mainz-05', 'hertha-bsc', 'eintracht-frankfurt', 'sv-werder-bremen',  'sc-freiburg', 'rasenballsport-leipzig', '1-fc-koln',
            '1-fc-union-berlin', 'arminia-bielefeld', 'vfb-stuttgart']
            
#'fc-augsburg', 
vereine_name = ['FC Bayern München', 'Borussia Dortmund', 'FC Schalke 04', 'VfL Wolfsburg', 'Bayer 04 Leverkusen', 
                'Borussia Mönchengladbach', 'TSG 1899 Hoffenheim', '1. FSV Mainz 05', 'Hertha BSC', 'Eintracht Frankfurt',
                'SV Werder Bremen',  'Sport-Club Freiburg', 'RB Leipzig', '1. FC Köln', '1. FC Union Berlin', 
                'DSC Arminia Bielefeld', 'VfB Stuttgart']
#'FC Augsburg',



class player_age_worth:
    
    
    def __init__(self, l1, l2, l3):
        
        self.l1 = l1
        self.l2 = l2 
        self.l3 = l3 


    def get_player_age_worth(self):
        
        l1 = self.l1
        l2 = self.l2
        l3 = self.l3
        
        df_complete = pd.DataFrame()
        
        nbr_clubs = len(l1)
        
        for i in range(nbr_clubs):
            
            v1 = l1[i]
            v2 = l2[i]
            v3 = l3[i]
                  
            url = 'https://www.transfermarkt.de/'+str(v1)+'/startseite/verein/'+str(v2)+'/saison_id/2020'                
            driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
            driver.get(url)
        
            player_o = driver.find_elements_by_xpath("//tr[@class='odd']")
            player_e = driver.find_elements_by_xpath("//tr[@class='even']")  
                    
            f1 = t.get_df(player_o)
            f2 = t.get_df(player_e)
            player_1 = f1.df()
            player_2 = f2.df()
                    
            def prepare(df):
                df[1] = df[1].astype(str)
                indexNames = df[df[1]=='None'].index
                df.drop(indexNames, inplace=True)
                df[3] = df[3].map(str) + player_1[4].map(str) 
                df[3] = df[3].str.split('€', expand = True)
                df = df.drop(columns = [0,4], axis = 1)
                df_1 = df[[1,2]]
                df_2 = df[3].str.split('(', expand = True)
                df_3 = df_2[[0]]
                df_4 = df_2[1].str.split(')', expand = True)
                df_2 = df_4[[0]]
                df_5 = df_4[[1]]
                df_all = pd.concat([df_1, df_2, df_3, df_5], axis = 1)
                df_all.columns = ['Spieler', 'Position', 'Alter', 'Geburtstag', 'Wert']
                
                return df_all
            
            df_all_1 = prepare(player_1)
            df_all_2 = prepare(player_2)
            
            df_all = pd.concat([df_all_1, df_all_2], axis = 0, ignore_index = True)
            df_all = df_all.assign(Verein = v3)
            
            df_complete = df_complete.append(df_all)
            driver.quit()
            
        return df_complete
 
    
f = player_age_worth(vereine, id_vereine, vereine_name)
df = f.get_player_age_worth()