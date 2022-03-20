import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time

import My_Tools as t 
import Read_Load_Database as db

class spielplan:
    
    def __init__(self, gameday, english_week, season):
        self.gameday = gameday
        self.english_week = english_week
        self.season = season
        
    def get_spielplan(self):
        gameday = self.gameday
        english_week = self.english_week
        season = self.season
        
        season_entered = season[0:4]+'-'+season[5:7]

        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        url = 'https://www.kicker.de/1-bundesliga/spieltag/'+str(season_entered)+'/'+str(gameday)

        driver.get(url)
        time.sleep(5)
        spiele = driver.find_elements_by_xpath("//div[@class='kick__v100-gameList__header']")
        time.sleep(5)
        vereine = driver.find_elements_by_xpath("//div[@class='kick__v100-gameCell__team__name']")
       
        f_1 = t.get_df(spiele)
        f_2 = t.get_df(vereine)
        df_date = f_1.df()
        df_clubs = f_2.df()
    
        #df_date = df_date.iloc[0:17]
        #df_clubs = df_clubs.iloc[0:18]
        # print(df_date)
        #print(df_clubs)
        driver.quit()
        
        if english_week == 1:

            date_1 = pd.to_datetime(df_date.iloc[0,0][10:20], dayfirst=True, infer_datetime_format=True)
            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(18):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
                
        if english_week == 2:

            date_1 = pd.to_datetime(df_date.iloc[0,0][10:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][10:20], dayfirst=True, infer_datetime_format=True)
            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(14):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(14,18):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2
            
        if english_week == 3:

            date_1 = pd.to_datetime(df_date.iloc[0,0][9:19], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][9:19], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][9:19], dayfirst=True, infer_datetime_format=True)
            
            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(2):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(2,14):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2
                
            for i in range(14,18):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = year_3
                df_clubs.iloc[i,3] = month_3
                df_clubs.iloc[i,4] = week_3
                df_clubs.iloc[i,5] = day_3

        if english_week == 4:
            

            date_1 = pd.to_datetime(df_date.iloc[0,0][9:19], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][9:19], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][9:19], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][8:18], dayfirst=True, infer_datetime_format=True)
            #date_4 = pd.to_datetime(df_date.iloc[3,0][9:19], dayfirst=True, infer_datetime_format=True)
            #date_4 = pd.to_datetime('10.03.2021', dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            month_4 = date_4.month
            day_4 = date_4.day
            week_4 = date_4.week
            year_4 = date_4.year

            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(2):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = int(year_1)
                df_clubs.iloc[i,3] = int(month_1)
                df_clubs.iloc[i,4] = int(week_1)
                df_clubs.iloc[i,5] = int(day_1)
                
            for i in range(2,12):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = int(year_2)
                df_clubs.iloc[i,3] = int(month_2)
                df_clubs.iloc[i,4] = int(week_2)
                df_clubs.iloc[i,5] = int(day_2)
                
            for i in range(12,16):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = int(year_3)
                df_clubs.iloc[i,3] = int(month_3)
                df_clubs.iloc[i,4] = int(week_3)
                df_clubs.iloc[i,5] = int(day_3)
                
            for i in range(16,18):
                df_clubs.iloc[i,1] = date_4
                df_clubs.iloc[i,2] = int(year_4)
                df_clubs.iloc[i,3] = int(month_4)
                df_clubs.iloc[i,4] = int(week_4)
                df_clubs.iloc[i,5] = int(day_4)
       
        df_id = db.get_table('master_vereins_id')
        df_clubs = df_clubs.replace({'Bayern München': 'FC Bayern München', 'Bor. Mönchengladbach': 'Borussia Mönchengladbach', 'TSG Hoffenheim': 'TSG 1899 Hoffenheim',
                                     'SC Freiburg': 'Sport-Club Freiburg', 'Werder Bremen': 'SV Werder Bremen',
                                     'Arminia Bielefeld':'DSC Arminia Bielefeld'})     

        df_k = df_clubs.merge(df_id, on = 'Verein', how = 'inner')
        df_k = df_k.assign(Spieltag = gameday, Saison = season)
        print(df_k)
        df_k['Datum'] = pd.to_datetime(df_k['Datum'])
        df_k = df_k[['Vereins_ID', 'Verein','Saison', 'Spieltag','Datum','Jahr', 'Monat', 'Woche', 'Tag']]
        
        return df_k
    
#f = spielplan(32, 2, '2020/21')
#df = f.get_spielplan()


class spielplan_premier_leauge:
    
    def __init__(self, gameday, english_week, season):
        self.gameday = gameday
        self.english_week = english_week
        self.season = season
        
    def get_spielplan(self):
        gameday = self.gameday
        english_week = self.english_week
        season = self.season
        
        season_entered = season[0:4]+'-'+season[5:7]

        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        #url = 'https://www.kicker.de/1-bundesliga/spieltag/'+str(season_entered)+'/'+str(gameday)
        driver.get('https://www.kicker.de/premier-league/spieltag/'+str(season_entered)+'/'+str(gameday))
        #driver.get(url)
        time.sleep(5)
        spiele = driver.find_elements_by_xpath("//div[@class='kick__v100-gameList__header']")
        time.sleep(5)
        vereine = driver.find_elements_by_xpath("//div[@class='kick__v100-gameCell__team__name']")
       
        f_1 = t.get_df(spiele)
        f_2 = t.get_df(vereine)
        df_date = f_1.df()
        df_clubs = f_2.df()
    
        #df_date = df_date.iloc[0:17]
        #df_clubs = df_clubs.iloc[0:18]
        # print(df_date)
        #print(df_clubs)
        driver.quit()
        
        if english_week == 1:

            date_1 = pd.to_datetime(df_date.iloc[0,0][10:20], dayfirst=True, infer_datetime_format=True)
            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(20):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
                
        if english_week == 2:

            date_1 = pd.to_datetime(df_date.iloc[0,0][9:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][9:20], dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(16):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(16,20):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2
                
        if english_week == 21:

            date_1 = pd.to_datetime(df_date.iloc[0,0][9:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][9:20], dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(14):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(14,20):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2   
                
        if english_week == 22:

            date_1 = pd.to_datetime(df_date.iloc[0,0][9:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][9:20], dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(12):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(12,20):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2   

        if english_week == 23:

            date_1 = pd.to_datetime(df_date.iloc[0,0][9:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][9:20], dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(8):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(8,20):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2 

        if english_week == 24:

            date_1 = pd.to_datetime(df_date.iloc[0,0][9:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][9:20], dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(10):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(10,20):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2 

        if english_week == 25:

            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][10:22], dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(18):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(18,20):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2                 
                
        if english_week == 3:

            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)

            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(14):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(14,18):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2
                
            for i in range(18,20):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = year_3
                df_clubs.iloc[i,3] = month_3
                df_clubs.iloc[i,4] = week_3
                df_clubs.iloc[i,5] = day_3

        if english_week == 31:

            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)

            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(12):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(12,18):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2
                
            for i in range(18,20):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = year_3
                df_clubs.iloc[i,3] = month_3
                df_clubs.iloc[i,4] = week_3
                df_clubs.iloc[i,5] = day_3
                
        if english_week == 32:

            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)

            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(16):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(16,18):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2
                
            for i in range(18,20):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = year_3
                df_clubs.iloc[i,3] = month_3
                df_clubs.iloc[i,4] = week_3
                df_clubs.iloc[i,5] = day_3   
                
        if english_week == 33:

            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)

            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(2):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(2,16):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2
                
            for i in range(16,20):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = year_3
                df_clubs.iloc[i,3] = month_3
                df_clubs.iloc[i,4] = week_3
                df_clubs.iloc[i,5] = day_3   
                
        if english_week == 34:

            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][10:22], dayfirst=True, infer_datetime_format=True)

            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(2):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(2,12):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2
                
            for i in range(12,20):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = year_3
                df_clubs.iloc[i,3] = month_3
                df_clubs.iloc[i,4] = week_3
                df_clubs.iloc[i,5] = day_3 
                
        if english_week == 35:

            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)

            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(8):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(8,16):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2
                
            for i in range(16,20):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = year_3
                df_clubs.iloc[i,3] = month_3
                df_clubs.iloc[i,4] = week_3
                df_clubs.iloc[i,5] = day_3           

        if english_week == 36:

            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][10:22], dayfirst=True, infer_datetime_format=True)
            print(date_3)
            
            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(6):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = year_1
                df_clubs.iloc[i,3] = month_1
                df_clubs.iloc[i,4] = week_1
                df_clubs.iloc[i,5] = day_1
                
            for i in range(6,16):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = year_2
                df_clubs.iloc[i,3] = month_2
                df_clubs.iloc[i,4] = week_2
                df_clubs.iloc[i,5] = day_2
                
            for i in range(16,20):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = year_3
                df_clubs.iloc[i,3] = month_3
                df_clubs.iloc[i,4] = week_3
                df_clubs.iloc[i,5] = day_3   
                
        if english_week == 4:
            
            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][8:20], dayfirst=True, infer_datetime_format=True)
            #date_4 = pd.to_datetime(df_date.iloc[3,0][9:19], dayfirst=True, infer_datetime_format=True)
            #date_4 = pd.to_datetime('10.03.2021', dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            month_4 = date_4.month
            day_4 = date_4.day
            week_4 = date_4.week
            year_4 = date_4.year

            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(12):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = int(year_1)
                df_clubs.iloc[i,3] = int(month_1)
                df_clubs.iloc[i,4] = int(week_1)
                df_clubs.iloc[i,5] = int(day_1)
                
            for i in range(12,16):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = int(year_2)
                df_clubs.iloc[i,3] = int(month_2)
                df_clubs.iloc[i,4] = int(week_2)
                df_clubs.iloc[i,5] = int(day_2)
                
            for i in range(16,18):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = int(year_3)
                df_clubs.iloc[i,3] = int(month_3)
                df_clubs.iloc[i,4] = int(week_3)
                df_clubs.iloc[i,5] = int(day_3)
                
            for i in range(18,20):
                df_clubs.iloc[i,1] = date_4
                df_clubs.iloc[i,2] = int(year_4)
                df_clubs.iloc[i,3] = int(month_4)
                df_clubs.iloc[i,4] = int(week_4)
                df_clubs.iloc[i,5] = int(day_4)

        if english_week == 41:
            
            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][10:22], dayfirst=True, infer_datetime_format=True)
            #date_4 = pd.to_datetime(df_date.iloc[3,0][9:19], dayfirst=True, infer_datetime_format=True)
            #date_4 = pd.to_datetime('10.03.2021', dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            month_4 = date_4.month
            day_4 = date_4.day
            week_4 = date_4.week
            year_4 = date_4.year

            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(10):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = int(year_1)
                df_clubs.iloc[i,3] = int(month_1)
                df_clubs.iloc[i,4] = int(week_1)
                df_clubs.iloc[i,5] = int(day_1)
                
            for i in range(10,16):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = int(year_2)
                df_clubs.iloc[i,3] = int(month_2)
                df_clubs.iloc[i,4] = int(week_2)
                df_clubs.iloc[i,5] = int(day_2)
                
            for i in range(16,18):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = int(year_3)
                df_clubs.iloc[i,3] = int(month_3)
                df_clubs.iloc[i,4] = int(week_3)
                df_clubs.iloc[i,5] = int(day_3)
                
            for i in range(18,20):
                df_clubs.iloc[i,1] = date_4
                df_clubs.iloc[i,2] = int(year_4)
                df_clubs.iloc[i,3] = int(month_4)
                df_clubs.iloc[i,4] = int(week_4)
                df_clubs.iloc[i,5] = int(day_4)
                
        if english_week == 42:
            
            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][8:20], dayfirst=True, infer_datetime_format=True)
            #date_4 = pd.to_datetime(df_date.iloc[3,0][9:19], dayfirst=True, infer_datetime_format=True)
            #date_4 = pd.to_datetime('10.03.2021', dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            month_4 = date_4.month
            day_4 = date_4.day
            week_4 = date_4.week
            year_4 = date_4.year

            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(2):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = int(year_1)
                df_clubs.iloc[i,3] = int(month_1)
                df_clubs.iloc[i,4] = int(week_1)
                df_clubs.iloc[i,5] = int(day_1)
                
            for i in range(2,8):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = int(year_2)
                df_clubs.iloc[i,3] = int(month_2)
                df_clubs.iloc[i,4] = int(week_2)
                df_clubs.iloc[i,5] = int(day_2)
                
            for i in range(8,16):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = int(year_3)
                df_clubs.iloc[i,3] = int(month_3)
                df_clubs.iloc[i,4] = int(week_3)
                df_clubs.iloc[i,5] = int(day_3)
                
            for i in range(16,20):
                df_clubs.iloc[i,1] = date_4
                df_clubs.iloc[i,2] = int(year_4)
                df_clubs.iloc[i,3] = int(month_4)
                df_clubs.iloc[i,4] = int(week_4)
                df_clubs.iloc[i,5] = int(day_4)         
                
        if english_week == 5:
            

            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_5 = pd.to_datetime(df_date.iloc[4,0][10:22], dayfirst=True, infer_datetime_format=True)
            #date_4 = pd.to_datetime('10.03.2021', dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            month_4 = date_4.month
            day_4 = date_4.day
            week_4 = date_4.week
            year_4 = date_4.year
            
            month_5 = date_5.month
            day_5 = date_5.day
            week_5 = date_5.week
            year_5 = date_5.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(2):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = int(year_1)
                df_clubs.iloc[i,3] = int(month_1)
                df_clubs.iloc[i,4] = int(week_1)
                df_clubs.iloc[i,5] = int(day_1)
                
            for i in range(2,10):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = int(year_2)
                df_clubs.iloc[i,3] = int(month_2)
                df_clubs.iloc[i,4] = int(week_2)
                df_clubs.iloc[i,5] = int(day_2)
                
            for i in range(10,14):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = int(year_3)
                df_clubs.iloc[i,3] = int(month_3)
                df_clubs.iloc[i,4] = int(week_3)
                df_clubs.iloc[i,5] = int(day_3)
                
            for i in range(14,18):
                df_clubs.iloc[i,1] = date_4
                df_clubs.iloc[i,2] = int(year_4)
                df_clubs.iloc[i,3] = int(month_4)
                df_clubs.iloc[i,4] = int(week_4)
                df_clubs.iloc[i,5] = int(day_4) 
                
            for i in range(18,20):
                df_clubs.iloc[i,1] = date_5
                df_clubs.iloc[i,2] = int(year_5)
                df_clubs.iloc[i,3] = int(month_5)
                df_clubs.iloc[i,4] = int(week_5)
                df_clubs.iloc[i,5] = int(day_5) 
                
        if english_week == 51:
            

            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_5 = pd.to_datetime(df_date.iloc[4,0][8:20], dayfirst=True, infer_datetime_format=True)
            #date_4 = pd.to_datetime('10.03.2021', dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            month_4 = date_4.month
            day_4 = date_4.day
            week_4 = date_4.week
            year_4 = date_4.year
            
            month_5 = date_5.month
            day_5 = date_5.day
            week_5 = date_5.week
            year_5 = date_5.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(2):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = int(year_1)
                df_clubs.iloc[i,3] = int(month_1)
                df_clubs.iloc[i,4] = int(week_1)
                df_clubs.iloc[i,5] = int(day_1)
                
            for i in range(2,12):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = int(year_2)
                df_clubs.iloc[i,3] = int(month_2)
                df_clubs.iloc[i,4] = int(week_2)
                df_clubs.iloc[i,5] = int(day_2)
                
            for i in range(12,16):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = int(year_3)
                df_clubs.iloc[i,3] = int(month_3)
                df_clubs.iloc[i,4] = int(week_3)
                df_clubs.iloc[i,5] = int(day_3)
                
            for i in range(16,18):
                df_clubs.iloc[i,1] = date_4
                df_clubs.iloc[i,2] = int(year_4)
                df_clubs.iloc[i,3] = int(month_4)
                df_clubs.iloc[i,4] = int(week_4)
                df_clubs.iloc[i,5] = int(day_4) 
                
            for i in range(18,20):
                df_clubs.iloc[i,1] = date_5
                df_clubs.iloc[i,2] = int(year_5)
                df_clubs.iloc[i,3] = int(month_5)
                df_clubs.iloc[i,4] = int(week_5)
                df_clubs.iloc[i,5] = int(day_5) 
                
                               
        if english_week == 6:
            
            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_5 = pd.to_datetime(df_date.iloc[4,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_6 = pd.to_datetime(df_date.iloc[5,0][8:20], dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            month_4 = date_4.month
            day_4 = date_4.day
            week_4 = date_4.week
            year_4 = date_4.year
            
            month_5 = date_5.month
            day_5 = date_5.day
            week_5 = date_5.week
            year_5 = date_5.year

            month_6 = date_6.month
            day_6 = date_6.day
            week_6 = date_6.week
            year_6 = date_6.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(6):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = int(year_1)
                df_clubs.iloc[i,3] = int(month_1)
                df_clubs.iloc[i,4] = int(week_1)
                df_clubs.iloc[i,5] = int(day_1)
                
            for i in range(6,10):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = int(year_2)
                df_clubs.iloc[i,3] = int(month_2)
                df_clubs.iloc[i,4] = int(week_2)
                df_clubs.iloc[i,5] = int(day_2)
                
            for i in range(10,12):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = int(year_3)
                df_clubs.iloc[i,3] = int(month_3)
                df_clubs.iloc[i,4] = int(week_3)
                df_clubs.iloc[i,5] = int(day_3)
                
            for i in range(12,14):
                df_clubs.iloc[i,1] = date_4
                df_clubs.iloc[i,2] = int(year_4)
                df_clubs.iloc[i,3] = int(month_4)
                df_clubs.iloc[i,4] = int(week_4)
                df_clubs.iloc[i,5] = int(day_4) 
                
            for i in range(14,16):
                df_clubs.iloc[i,1] = date_5
                df_clubs.iloc[i,2] = int(year_5)
                df_clubs.iloc[i,3] = int(month_5)
                df_clubs.iloc[i,4] = int(week_5)
                df_clubs.iloc[i,5] = int(day_5)   
                
            for i in range(16,20):
                df_clubs.iloc[i,1] = date_6
                df_clubs.iloc[i,2] = int(year_6)
                df_clubs.iloc[i,3] = int(month_6)
                df_clubs.iloc[i,4] = int(week_6)
                df_clubs.iloc[i,5] = int(day_6)  
                
        if english_week == 61:
            
            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_5 = pd.to_datetime(df_date.iloc[4,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_6 = pd.to_datetime(df_date.iloc[5,0][10:22], dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            month_4 = date_4.month
            day_4 = date_4.day
            week_4 = date_4.week
            year_4 = date_4.year
            
            month_5 = date_5.month
            day_5 = date_5.day
            week_5 = date_5.week
            year_5 = date_5.year

            month_6 = date_6.month
            day_6 = date_6.day
            week_6 = date_6.week
            year_6 = date_6.year
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(2):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = int(year_1)
                df_clubs.iloc[i,3] = int(month_1)
                df_clubs.iloc[i,4] = int(week_1)
                df_clubs.iloc[i,5] = int(day_1)
                
            for i in range(2,4):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = int(year_2)
                df_clubs.iloc[i,3] = int(month_2)
                df_clubs.iloc[i,4] = int(week_2)
                df_clubs.iloc[i,5] = int(day_2)
                
            for i in range(4,6):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = int(year_3)
                df_clubs.iloc[i,3] = int(month_3)
                df_clubs.iloc[i,4] = int(week_3)
                df_clubs.iloc[i,5] = int(day_3)
                
            for i in range(6,8):
                df_clubs.iloc[i,1] = date_4
                df_clubs.iloc[i,2] = int(year_4)
                df_clubs.iloc[i,3] = int(month_4)
                df_clubs.iloc[i,4] = int(week_4)
                df_clubs.iloc[i,5] = int(day_4) 
                
            for i in range(8,16):
                df_clubs.iloc[i,1] = date_5
                df_clubs.iloc[i,2] = int(year_5)
                df_clubs.iloc[i,3] = int(month_5)
                df_clubs.iloc[i,4] = int(week_5)
                df_clubs.iloc[i,5] = int(day_5)   
                
            for i in range(16,20):
                df_clubs.iloc[i,1] = date_6
                df_clubs.iloc[i,2] = int(year_6)
                df_clubs.iloc[i,3] = int(month_6)
                df_clubs.iloc[i,4] = int(week_6)
                df_clubs.iloc[i,5] = int(day_6)  
                
        if english_week == 7:
            
            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][10:22], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_5 = pd.to_datetime(df_date.iloc[4,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_6 = pd.to_datetime(df_date.iloc[5,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_7 = pd.to_datetime(df_date.iloc[6,0][8:20], dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            month_4 = date_4.month
            day_4 = date_4.day
            week_4 = date_4.week
            year_4 = date_4.year
            
            month_5 = date_5.month
            day_5 = date_5.day
            week_5 = date_5.week
            year_5 = date_5.year

            month_6 = date_6.month
            day_6 = date_6.day
            week_6 = date_6.week
            year_6 = date_6.year
            
            month_7 = date_7.month
            day_7 = date_7.day
            week_7 = date_7.week
            year_7 = date_7.year    
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(2):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = int(year_1)
                df_clubs.iloc[i,3] = int(month_1)
                df_clubs.iloc[i,4] = int(week_1)
                df_clubs.iloc[i,5] = int(day_1)
                
            for i in range(2,8):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = int(year_2)
                df_clubs.iloc[i,3] = int(month_2)
                df_clubs.iloc[i,4] = int(week_2)
                df_clubs.iloc[i,5] = int(day_2)
                
            for i in range(8,12):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = int(year_3)
                df_clubs.iloc[i,3] = int(month_3)
                df_clubs.iloc[i,4] = int(week_3)
                df_clubs.iloc[i,5] = int(day_3)
                
            for i in range(12,14):
                df_clubs.iloc[i,1] = date_4
                df_clubs.iloc[i,2] = int(year_4)
                df_clubs.iloc[i,3] = int(month_4)
                df_clubs.iloc[i,4] = int(week_4)
                df_clubs.iloc[i,5] = int(day_4) 
                
            for i in range(14,16):
                df_clubs.iloc[i,1] = date_5
                df_clubs.iloc[i,2] = int(year_5)
                df_clubs.iloc[i,3] = int(month_5)
                df_clubs.iloc[i,4] = int(week_5)
                df_clubs.iloc[i,5] = int(day_5)   
                
            for i in range(16,18):
                df_clubs.iloc[i,1] = date_6
                df_clubs.iloc[i,2] = int(year_6)
                df_clubs.iloc[i,3] = int(month_6)
                df_clubs.iloc[i,4] = int(week_6)
                df_clubs.iloc[i,5] = int(day_6)            
                
            for i in range(18,20):
                df_clubs.iloc[i,1] = date_6
                df_clubs.iloc[i,2] = int(year_7)
                df_clubs.iloc[i,3] = int(month_7)
                df_clubs.iloc[i,4] = int(week_7)
                df_clubs.iloc[i,5] = int(day_7)   
                
        if english_week == 8:
            
            date_1 = pd.to_datetime(df_date.iloc[0,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_5 = pd.to_datetime(df_date.iloc[4,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_6 = pd.to_datetime(df_date.iloc[5,0][8:20], dayfirst=True, infer_datetime_format=True)
            date_7 = pd.to_datetime(df_date.iloc[6,0][10:22], dayfirst=True, infer_datetime_format=True)
            date_8 = pd.to_datetime(df_date.iloc[7,0][8:20], dayfirst=True, infer_datetime_format=True)

            month_1 = date_1.month
            day_1 = date_1.day
            week_1 = date_1.week
            year_1 = date_1.year
            
            month_2 = date_2.month
            day_2 = date_2.day
            week_2 = date_2.week
            year_2 = date_2.year
            
            month_3 = date_3.month
            day_3 = date_3.day
            week_3 = date_3.week
            year_3 = date_3.year
            
            month_4 = date_4.month
            day_4 = date_4.day
            week_4 = date_4.week
            year_4 = date_4.year
            
            month_5 = date_5.month
            day_5 = date_5.day
            week_5 = date_5.week
            year_5 = date_5.year

            month_6 = date_6.month
            day_6 = date_6.day
            week_6 = date_6.week
            year_6 = date_6.year
            
            month_7 = date_7.month
            day_7 = date_7.day
            week_7 = date_7.week
            year_7 = date_7.year
            
            month_8 = date_8.month
            day_8 = date_8.day
            week_8 = date_8.week
            year_8 = date_8.year           
            
            df_clubs.columns = ['Verein']
            df_clubs = df_clubs.assign(Datum = 0)
            df_clubs = df_clubs.assign(Jahr = 0)
            df_clubs = df_clubs.assign(Monat = 0)
            df_clubs = df_clubs.assign(Woche = 0)
            df_clubs = df_clubs.assign(Tag = 0)

            for i in range(2):
                df_clubs.iloc[i,1] = date_1
                df_clubs.iloc[i,2] = int(year_1)
                df_clubs.iloc[i,3] = int(month_1)
                df_clubs.iloc[i,4] = int(week_1)
                df_clubs.iloc[i,5] = int(day_1)
                
            for i in range(2,6):
                df_clubs.iloc[i,1] = date_2
                df_clubs.iloc[i,2] = int(year_2)
                df_clubs.iloc[i,3] = int(month_2)
                df_clubs.iloc[i,4] = int(week_2)
                df_clubs.iloc[i,5] = int(day_2)
                
            for i in range(6,10):
                df_clubs.iloc[i,1] = date_3
                df_clubs.iloc[i,2] = int(year_3)
                df_clubs.iloc[i,3] = int(month_3)
                df_clubs.iloc[i,4] = int(week_3)
                df_clubs.iloc[i,5] = int(day_3)
                
            for i in range(10,12):
                df_clubs.iloc[i,1] = date_4
                df_clubs.iloc[i,2] = int(year_4)
                df_clubs.iloc[i,3] = int(month_4)
                df_clubs.iloc[i,4] = int(week_4)
                df_clubs.iloc[i,5] = int(day_4) 
                
            for i in range(12,14):
                df_clubs.iloc[i,1] = date_5
                df_clubs.iloc[i,2] = int(year_5)
                df_clubs.iloc[i,3] = int(month_5)
                df_clubs.iloc[i,4] = int(week_5)
                df_clubs.iloc[i,5] = int(day_5)   
                
            for i in range(14,16):
                df_clubs.iloc[i,1] = date_6
                df_clubs.iloc[i,2] = int(year_6)
                df_clubs.iloc[i,3] = int(month_6)
                df_clubs.iloc[i,4] = int(week_6)
                df_clubs.iloc[i,5] = int(day_6)            
                
            for i in range(16,18):
                df_clubs.iloc[i,1] = date_6
                df_clubs.iloc[i,2] = int(year_7)
                df_clubs.iloc[i,3] = int(month_7)
                df_clubs.iloc[i,4] = int(week_7)
                df_clubs.iloc[i,5] = int(day_7)  

            for i in range(18,20):
                df_clubs.iloc[i,1] = date_6
                df_clubs.iloc[i,2] = int(year_8)
                df_clubs.iloc[i,3] = int(month_8)
                df_clubs.iloc[i,4] = int(week_8)
                df_clubs.iloc[i,5] = int(day_8) 
                 
        df_id = db.get_table('master_vereins_id')
        df_clubs = df_clubs[df_clubs['Datum']!=0]
        df_clubs = df_clubs.replace({'Bayern München': 'FC Bayern München', 'Bor. Mönchengladbach': 'Borussia Mönchengladbach', 'TSG Hoffenheim': 'TSG 1899 Hoffenheim',
                                     'SC Freiburg': 'Sport-Club Freiburg', 'Werder Bremen': 'SV Werder Bremen',
                                     'Arminia Bielefeld':'DSC Arminia Bielefeld'})     

        df_k = df_clubs.merge(df_id, on = 'Verein', how = 'inner')
        df_k = df_k.assign(Spieltag = gameday, Saison = season)
        print(df_k)
        df_k['Datum'] = pd.to_datetime(df_k['Datum'])
        df_k = df_k[['Vereins_ID', 'Verein','Saison', 'Spieltag','Datum','Jahr', 'Monat', 'Woche', 'Tag']]
        
        return df_k
    
#f = spielplan_premier_leauge(12, 21, '2015/16')
#df = f.get_spielplan()
#db.upload_local_data_to_database(df, 'pl_data_vereine_spielplan')