#web crawler to get football resutls, statistical sports data such as goals or shoots on the goal, the estimated value of the club, possession of the ball
#and clubs strength from the game fifa for the Bundesliga.


#Parameter 
spieltag = 1
columns_list = ['tore', 'torschusse' ,'torschusse-latte-pfosten', 'eigentore', 'elfmeter', 'elfmeter-verwandelt','gelbe-karten','fouls-am-gegner', 'zweikampfe-gewonnen',
                'kopfball-duelle-gewonnen', 'laufdistanz', 'sprints', 'intensive-laufe', 'pass-quote', 'flanken']

vereine = ['FC Bayern München']
saison = '2019/20'


import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


#extract data and get data frame
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
 
#transform object or string into integer
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

 #get date, year and week of the game day  
class get_date_of_gameday:

    def __init__(self, spieltag, saison):
        self.spieltag = spieltag
        self.saison = saison
        
    def get_time(self):
        
        s = self.spieltag
        saison = self.saison
        zeit = []
        driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
        #driver = webdriver.Chrome('D:\Crawling\chromedriver')
        driver.get('https://www.bundesliga.com/de/bundesliga/spieltag/2019-2020/'+str(s))
    
        wann = driver.find_elements_by_xpath("//span[@class='ng-star-inserted']")
        text = wann[0].text
        date = pd.to_datetime(text[9:19], dayfirst=True, infer_datetime_format=True)
        week = date.week
        year = date.year
       
        zeit.extend((week, year, saison))
        driver.quit()

        return zeit    
    


class club_match_day_data:
    
    def __init__(self, column_list, spieltag, vereine, saison):
        self.column_list = column_list
        self.spieltag = spieltag
        self.vereine = vereine
        self.saison = saison
        
    def get_results(self):
        
        s = self.spieltag
        driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
        driver.get('https://www.bundesliga.com/de/bundesliga/spieltag/2019-2020/'+str(s))
        erg = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'matchDataRow')))
        f = get_df(erg)
        df_erg = f.df()
        driver.quit()
        df_erg = df_erg.drop([3], axis = 1)
        df_erg.columns = ['Heimmannschaft', 'Ergebnis', 'HalbzeitErgebnis', 'Auswärtsmannschaft']
        
        return df_erg
    
        
    def get_club_stat_data(self):              

        s = self.spieltag 
        df_all = pd.DataFrame()
        first_value = self.column_list[0]             
        for c in self.column_list:
            while c not in df_all.columns:
                driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
                driver.get('https://www.bundesliga.com/de/statistiken/bundesliga/aktuelle-saison/spieltag-'+str(self.spieltag)+'/club-statistiken/'+c)
                time.sleep(5)
                clubs = driver.find_elements_by_xpath("//a[@class='list-group-item']")
                
                try:
                    f = get_df(clubs)
                    df_c = f.df()
                    driver.quit()
                    df_c.columns = ['Place', 'Verein', c]   
                    df_c = df_c.drop(['Place'], axis = 1)
                    
                    if c == first_value:
                        df_all = df_c                               
                    else:
                        df_all = df_all.merge(df_c, on = 'Verein', how = 'inner')
                                                
                except ValueError as v:          
                    print(v)
        
        df_all = df_all.assign(Spieltag = s)
   
        d = get_date_of_gameday(spieltag, saison)
        l_d = d.get_time()
        df_all = df_all.assign(Woche = l_d[0], Jahr = l_d[1], Saison = l_d[2])
        
        return df_all
    
    
    def get_fifa_features(self):
        
        s = self.spieltag
        
        driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
        driver.get('https://sofifa.com/teams?type=all&lg%5B%5D=19')
        time.sleep(2)
        clubs = driver.find_elements_by_xpath("//td[@class='col-name-wide']") 
        overall = driver.find_elements_by_xpath("//td[@class='col col-oa']")
        attack = driver.find_elements_by_xpath("//td[@class='col col-at']")
        mittelfeld = driver.find_elements_by_xpath("//td[@class='col col-md']")
        abwehr = driver.find_elements_by_xpath("//td[@class='col col-df']")
        d = get_date_of_gameday(spieltag, saison)
        l_d = d.get_time()
                
        f_ver = get_df(clubs)
        df_verein = f_ver.df() 
        
        f_over = get_df(overall)
        df_over = f_over.df() 
        
        f_attackt = get_df(attack)
        df_attack = f_attackt.df() 
        
        f_mittelfeld = get_df(mittelfeld)
        df_mittelfeld = f_mittelfeld.df()  
        
        f_abwehr = get_df(abwehr)
        df_abwehr = f_abwehr.df()         
        
        driver.quit()
        df_verein = df_verein.drop(1, axis = 1)
        df_verein.columns = ['Verein']
        df_over.columns = ['Gesamt']
        df_attack.columns = ['Angriff']
        df_mittelfeld.columns = ['Mittelfeld']
        df_abwehr.columns = ['Abwehr']
        
        df = pd.concat([df_verein, df_over, df_attack, df_mittelfeld, df_abwehr], axis = 1)
        df = df.assign(Woche = l_d[0], Jahr = l_d[1], Saison = l_d[2], Spieltag = s)
        
        return df
       
    def get_club_value(self):
        
        s = self.spieltag
        driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
        driver.get('https://www.transfermarkt.de/1-bundesliga/startseite/wettbewerb/L1')
        time.sleep(2)
        odd = driver.find_elements_by_xpath("//tr[@class='odd']")   
        even = driver.find_elements_by_xpath("//tr[@class='even']")     
        f1 = get_df(odd)
        f2 = get_df(even)
        df_odd = f1.df()
        df_even = f2.df()
        driver.quit()
        df_wert = df_even.append(df_odd)
            
        d = get_date_of_gameday(spieltag, saison)
        l_d = d.get_time()
        df_wert = df_wert.assign(Woche = l_d[0], Jahr = l_d[1], Saison = l_d[2], Spieltag = s)    

        return df_wert
    
    def get_possession(self):
        
        s = self.spieltag
        vereine = self.vereine
        saison = self.saison
        
        df_all = pd.DataFrame()
        
        for v in vereine:
            
            driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
            driver.get('http://www.google.com')
                      
            query = 'bundesliga ergebnisse saison ' + str(saison) + ' ' + str(v)
            search = driver.find_element_by_name('q')
            search.send_keys(query)
            time.sleep(3)
            search.send_keys(Keys.RETURN)
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'imso-hov')))
            element.click()
            time.sleep(3)
            spiel = driver.find_elements_by_xpath("//tr[@class='MzWkAb']")
            
            f = get_df(spiel)
            df_spiel = f.df() 
            driver.quit()
            
            df_spiel = df_spiel[0].str.split(' ', expand = True)
                        
        return df_spiel

#win = 1, draw = 0, defeat = -1
class categorisation:
        
    def __init__(self, df_erg):       
        self.df_erg = df_erg
              
    def categorisation(self):  
        df = self.df_erg
                
        df = df.drop('HalbzeitErgebnis', axis = 1)
        df_tore_heim = df['Ergebnis'].str.split(':', expand = True)
        df_tore_auswärts = df['Ergebnis'].str.split(':', expand = True)
        df_tore_heim.columns = ['Tore', 'Gegentore']
        df_tore_auswärts.columns = ['Gegentore', 'Tore']
        
        f1 = as_int(df_tore_heim,1)
        f2 = as_int(df_tore_auswärts,1)
        df_tore_heim = f1.columns_to_int()
        df_tore_auswärts = f2.columns_to_int()
        
        df_heim = pd.concat([df_tore_heim, df], axis = 1)
        df_auswärts = pd.concat([df_tore_auswärts, df], axis = 1)
    
        df_heim = df_heim.assign(Differenz = lambda x: x['Tore']-x['Gegentore'])
        df_heim['Spiel_Ausgang'] = df_heim['Differenz'].apply(lambda x: '1' if x > 0 else ('-1' if x < 0 else '0'))
        df_heim = df_heim.rename(columns = {'Heimmannschaft_ID':'Vereins_ID', 'Heimmannschaft':'Verein', 'Auswärtsmannschaft_ID':'Gegner_ID', 'Auswärtsmannschaft':'Gegner'})

        
        df_auswärts = df_auswärts.assign(Differenz = lambda x: x['Tore']-x['Gegentore'])
        df_auswärts['Spiel_Ausgang'] = df_auswärts['Differenz'].apply(lambda x: '1' if x > 0 else ('-1' if x < 0 else '0'))
        df_auswärts = df_auswärts.rename(columns = {'Auswärtsmannschaft_ID':'Vereins_ID', 'Auswärtsmannschaft':'Verein', 'Heimmannschaft_ID':'Gegner_ID', 'Heimmannschaft':'Gegner'})

        df_all = df_heim.append(df_auswärts)

        
        return df_all
    

