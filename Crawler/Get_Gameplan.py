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
        
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get('https://www.kicker.de/1-bundesliga/spieltag/2020-21/'+str(gameday))
        time.sleep(5)
        spiele = driver.find_elements_by_xpath("//div[@class='kick__v100-gameList__header']")
        time.sleep(5)
        vereine = driver.find_elements_by_xpath("//div[@class='kick__v100-gameCell__team__name']")
       
        f_1 = t.get_df(spiele)
        f_2 = t.get_df(vereine)
        df_date = f_1.df()
        df_clubs = f_2.df()
        
        # df_date = df_date.iloc[0:len(df_date)-1]
        # df_clubs = df_clubs.iloc[0:len(df_clubs)-2]
        # print(df_date)
        # print(df_clubs)
        driver.quit()
        
        if english_week == 1:

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
            
        if english_week == 2:

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

        if english_week == 3:
            

            date_1 = pd.to_datetime(df_date.iloc[0,0][9:19], dayfirst=True, infer_datetime_format=True)
            date_2 = pd.to_datetime(df_date.iloc[1,0][9:19], dayfirst=True, infer_datetime_format=True)
            date_3 = pd.to_datetime(df_date.iloc[2,0][9:19], dayfirst=True, infer_datetime_format=True)
            date_4 = pd.to_datetime(df_date.iloc[3,0][8:18], dayfirst=True, infer_datetime_format=True)
            
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
                
        v_id = db.get_data_db(3)

        df_id = v_id.get_data()
        df_clubs = df_clubs.replace({'Bayern München': 'FC Bayern München', 'Bor. Mönchengladbach': 'Borussia Mönchengladbach', 'TSG Hoffenheim': 'TSG 1899 Hoffenheim',
                                     'SC Freiburg': 'Sport-Club Freiburg', 'Werder Bremen': 'SV Werder Bremen',
                                     'Arminia Bielefeld':'DSC Arminia Bielefeld'})     
        
        df_k = df_clubs.merge(df_id, on = 'Verein', how = 'inner')
        df_k = df_k.assign(Spieltag = gameday, Saison = season)
        df_k['Datum'] = pd.to_datetime(df_k['Datum'])
        df_k = df_k[['Vereins_ID', 'Verein','Saison', 'Spieltag','Datum','Jahr', 'Monat', 'Woche', 'Tag']]
        
        return df_k
    
# f = spielplan(20, 3, '2020/21')
# df = f.get_spielplan()

# #db.upload_local_db_data(df, 8)
# import mysql.connector
# from sqlalchemy import create_engine

# engine = create_engine('mysql+mysqlconnector://root:Teleshop,1871@localhost:3306/bl1_daten', echo=False)
# df.to_sql(name='bl1_data_vereine_spielplan', con=engine, if_exists = 'append', index=False)



