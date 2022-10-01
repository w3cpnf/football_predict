#packages and modules
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


import Tools as t
import Read_Load_Database as db

# columns_list_player = ['tore', 'torvorlagen','torschusse','elfmeter', 'elfmeter-verwandelt' ,'torschusse-latte-pfosten','pass-quote', 'ballbesitz-phasen', 'zweikampfe-gewonnen', 'kopfball-duelle-gewonnen',
#                 'flanken','gelbe-karten','fouls-am-gegner', 'laufdistanz' ,'sprints','intensive-laufe', 'torwart-paraden']

columns_list_player = ['intensive-laufe']

class player_data:
    
    def __init__(self, spieltag, l_player):
        
        self.spieltag = spieltag
        self.l_player = l_player
        
    def get_playe_data(self):
        
        df_all = pd.DataFrame()   
        new_clubs = pd.DataFrame()
        s = self.spieltag
        cl = self.l_player
        first = cl[0]
        
        def find(driver):
            clubs = driver.find_elements_by_class_name('list-group-item')
            
            if clubs:
                return clubs
            else:
                return False
        spieler_id = db.get_data_db(1)
        df_spieler_id = spieler_id.get_data()    
        
        for c in cl:   
        
            while c not in new_clubs.columns:
                driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
    
                driver.get('https://www.bundesliga.com/de/statistiken/bundesliga/aktuelle-saison/spieltag-'+str(s)+'/spieler-statistiken/'+str(c))
                time.sleep(10)
                click_more = True
                while click_more:
                    time.sleep(1)
                    #weiter = driver.find_elements_by_class_name('load-more')
                    #weiter = driver.find_elements_by_class_name('playerRow view-more linkActive ng-star-inserted')
                    #weiter = driver.find_element(By.xpath("//button[text()=' Mehr laden ']"))

                    weiter = driver.find_element_by_xpath('//button[text()=" Mehr laden "]')
                    
                    #driver.execute_script(script, args)
                    #print(len(weiter))
                    if weiter:
                        #weiter.click()
                        driver.execute_script("arguments[0].style.visibility='hidden'", weiter)
                    else:
                        click_more = False
                    
                clubs = WebDriverWait(driver,10).until(find)
        
        
                try:
                    i = len(clubs)
                    l_clubs = []
                    
                    if i == 1:
                        new_clubs = pd.DataFrame({'Spieler': [], 'Verein': [], c : []})
                    else:
                        for i in range(1,i):
                            l_clubs.append(clubs[i].text)
                          
                        df_clubs_1 = pd.DataFrame(l_clubs)
                        new_clubs = df_clubs_1[0].str.split('\n', expand = True)
                        new_clubs.columns = [ 'Platz','Spieler','Verein', c] 
                        new_clubs = new_clubs.drop(['Platz'], axis = 1)
                    
                except ValueError as v:          
                    print(v)
                
                
                driver.quit()
            
         
    
            if c == first:
                df_all = new_clubs.merge(df_spieler_id, on = 'Spieler', how = 'inner')
                new_clubs = pd.DataFrame() 
     
                 
            else:
                df_2 = new_clubs.merge(df_spieler_id, on = 'Spieler', how = 'inner')
                new_clubs = pd.DataFrame() 
                 
                df_uebereinstimmend = df_all.merge(df_2, on = ['Spieler_ID', 'Spieler', 'Verein'], how = 'inner')
                df_rest_1 = df_all.merge(df_2, on = ['Spieler_ID', 'Spieler', 'Verein'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='right_only'] 
                df_rest_2 = df_all.merge(df_2, on = ['Spieler_ID', 'Spieler', 'Verein'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
                 
                df_rest_1 = df_rest_1.drop(columns = ['_merge'], axis = 1)
                df_rest_2 = df_rest_2.drop(columns = ['_merge'], axis = 1)
                df_rest_1 = df_rest_1.fillna(0)
                df_rest_2 = df_rest_2.fillna(0)
                print(df_rest_1)
                print(df_rest_2)
                df_all = df_uebereinstimmend.append([df_rest_1, df_rest_2])
                 
        df_all['Spieltag'] = s
        
        #need info for season, woche, spiettag, jahr
        
        d_id = db.get_data_db(3)
        df = d_id.get_data()
        df_all = df_all.merge(df, on = 'Verein', how = 'inner')
        df_all = df_all.drop_duplicates()

    
        
        df_all = df_all.drop_duplicates()
        df_all = df_all.rename({'tore':'Tore', 'torvorlagen':'Torvorlagen','torschusse':'Torschüsse', 'torschusse-latte-pfosten': 'Pfosten', 'eigentore':'Eigentore', 'elfmeter':'Elfmeter', 
                                 'elfmeter-verwandelt':'ElfmeterTore', 'gelbe-karten':'GelbeKarten', 'fouls-am-gegner':'Fouls', 'zweikampfe-gewonnen':'ZweikämpfeGewonnen', 
                                 'kopfball-duelle-gewonnen':'KopfbälleGewonnen', 'laufdistanz':'Laufleistung',
                                 'sprints':'Sprints', 'intensive-laufe':'IntensivesLaufen', 'pass-quote':'Passquote', 'flanken':'Flanken', 'ballbesitz-phasen': 'Ballbesitzphasen',
                                 'torwart-paraden':'Paraden'}, axis=1)  
    
        df_all = df_all[['Spieler_ID', 'Spieler', 'Vereins_ID', 'Verein', 'Spieltag', 'Tore', 'Torvorlagen', 'Torschüsse', 'Pfosten', 'Elfmeter', 'ElfmeterTore',
                         'Passquote', 'Ballbesitzphasen', 'KopfbälleGewonnen', 'Flanken', 'GelbeKarten', 'Fouls', 'Laufleistung', 'Sprints',
                         'IntensivesLaufen', 'Paraden', 'Jahr', 'Woche', 'Saison']]
        
        
        return df_all
   
    
#f = player_data(2, columns_list_player)
#df = f.get_playe_data()




