import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time

#import other files 
import My_Tools as t
import Read_Load_Database as db

#columns_list_clubs = ['intensive-laeufe']

class club_data_bl:

    def __init__(self, spieltag, column_list):

        self.spieltag = spieltag
        self.column_list = column_list
        
        
    def get_club_stat_data(self):              
        first_value = self.column_list[0]
        s = self.spieltag 
        l_c = len(self.column_list)
        df_all = pd.DataFrame()
                      
        d = db.get_data_db(3)
        df = d.get_data()
        
        for i in range(l_c):
            c = self.column_list[i]
            print(c)
        
            while c not in df_all.columns:
                driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
                driver.get('https://www.bundesliga.com/de/statistiken/bundesliga/aktuelle-saison/spieltag-'+str(self.spieltag)+'/club-statistiken/'+c)
                #driver.get('https://www.bundesliga.com/de/bundesliga/statistiken/clubs/'+c)
                time.sleep(5)
                clubs_first = driver.find_elements_by_xpath("//span[@class='name']")
                clubs_sec = driver.find_elements_by_xpath("//span[@class='name ng-star-inserted']")
                tore_first = driver.find_elements_by_xpath("//span[@class='value fixed']")
                tore_sec = driver.find_elements_by_xpath("//span[@class='value']") 
                
                try:

                    f1 = t.get_df(clubs_first)
                    df_vereine_2 = f1.df()

                    f2 = t.get_df(clubs_sec)
                    df_vereine_1 = f2.df()
 
                    if c == 'gewonnene-zweikaempfe' or c == 'gewonnene-kopfballduelle' or c == 'flanken' or c == 'gelbe-karten':
                       
                        df_vereine_2 = df_vereine_2.iloc[i+3:17+i+1,:]
                       
                        
                    elif c == 'fouls' or c == 'laufdistanz' or c == 'sprints' :
                        df_vereine_2 = df_vereine_2.iloc[i+4:i+19,:]
                        
                    elif c == 'intensive-laeufe': 
                        df_vereine_2 = df_vereine_2.iloc[18:34,:]   
         

                    else:
                        df_vereine_2 = df_vereine_2.iloc[i+2:17+i,:]
                        
                    
                    f3 = t.get_df(tore_first)
                    df_stat_2 = f3.df()
                    
                    df_stat_2 = df_stat_2.iloc[2:17,:]

                
                    f4 = t.get_df(tore_sec)
                    df_stat_1 = f4.df()
                    
                    if c == 'gewonnene-zweikaempfe' or c == 'gewonnene-kopfballduelle' or c == 'flanken'or c == 'gelbe-karten':                  
                        df_stat_1 = df_stat_1.iloc[i+1:3+i+1,:]
                        
                    
                    elif c == 'fouls' or c == 'laufdistanz' or c == 'sprints' :
                        df_stat_1 = df_stat_1.iloc[i+2:i+5,:]
                        
                    elif c == 'intensive-laeufe': 
                    
                        df_stat_1 = df_stat_1.iloc[16:19,:]   
        
                    else:
                        
                        df_stat_1 = df_stat_1.iloc[i:3+i,:]
                        
                    df_vereine = pd.concat([df_vereine_1, df_vereine_2],axis = 0)
                    df_stat = pd.concat([df_stat_1, df_stat_2],axis = 0)


                    df_vereine.index = range(len(df_vereine))
                    df_stat.index = range(len(df_stat))
                    
                    #print(df_vereine)
                    #print(df_stat)
                    df_c = pd.concat([df_vereine, df_stat], axis = 1)
                    #print(df_c)
                    driver.quit()
                    df_c.columns = ['Verein', c]      
                    df_c = df_c.replace({'TSG Hoffenheim':'TSG 1899 Hoffenheim'})
                    print(df_c)
                    if c == first_value:
                        df_all = df.merge(df_c, on = 'Verein', how = 'inner')                               
                    else:
                        df_all = df_all.merge(df_c, on = 'Verein', how = 'inner')
                                                
                except ValueError as v:          
                    print(v)

        df_all = df_all.assign(Spieltag = s)
        
        df_all = df_all.rename({'tore':'Tore', 'torschusse':'Torschüsse', 'torschusse-latte-pfosten': 'Pfosten', 'eigentore':'Eigentore', 'elfmeter':'Elfmeter', 'verwandelte-elfmeter':'Elfmetertore',
                   'gelbe-karten':'GelbeKarten', 'fouls':'Fouls', 'gewonnene-zweikaempfe':'ZweikämpfeGewonnen', 'gewonnene-kopfballduelle':'KopfbälleGewonnen', 'laufdistanz':'Laufleistung',
                   'sprints':'Sprints', 'intensive-laeufe':'IntensivesLaufen', 'passquote':'Passquote', 'flanken':'Flanken'}, axis=1)     
        f_erg = db.get_data_db(12)
        df_erg = f_erg.get_data()

        f_s = db.get_data_db(22)
        df_plan  = f_s.get_data()
        
        df_complete = df_all.merge(df_plan, on = ['Vereins_ID', 'Spieltag'])
        f = t.add_goals(df_complete,df_erg, s)
        df_complete = f.get_bl1_club_data_result()
        df_complete = df_complete[['Vereins_ID', 'Verein', 'Spieltag', 'Tore', 'Torschüsse', 'Pfosten', 'Eigentore', 'Elfmeter', 'Elfmetertore',
                                   'ZweikämpfeGewonnen', 'GelbeKarten', 'Fouls', 'KopfbälleGewonnen', 'Laufleistung', 'Sprints', 'IntensivesLaufen', 
                                   'Passquote', 'Flanken', 'Heim', 'Gegentore', 'Jahr', 'Woche', 'Saison']]
        return df_complete

#f = club_data_bl(18, columns_list_clubs)
#df = f.get_club_stat_data()