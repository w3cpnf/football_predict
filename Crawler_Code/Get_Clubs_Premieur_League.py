import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
from selenium import webdriver
import time

import My_Tools as t
import Read_Load_Database as db

     
def clubs_premier_league():
    

    driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
    driver.get('https://www.transfermarkt.de/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2021')
    time.sleep(5)
  
    verein = driver.find_elements_by_xpath("//a[@class='vereinprofil_tooltip tooltipstered']") 
   
    f2 = t.get_df(verein) 

    df_verein = f2.df()

    df_verein[0] = df_verein[df_verein[0].astype(bool)]
    df_verein = df_verein.dropna()
    df_verein.index = range(len(df_verein))
    df_verein = df_verein.iloc[0:20,:]
    df_verein.columns = ['Verein']
    #print(df_kader)

    driver.quit()
    df_verein = df_verein.dropna()#
    
    f1 = db.get_data_db(3)
    df_vereins_id = f1.get_data()
    df_new = df_verein.merge(df_vereins_id, on = ['Verein'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
    df_new['Vereins_ID'] = range(df_vereins_id.tail(1).iloc[0,0]+1,df_vereins_id.tail(1).iloc[0,0]+len(df_new)+1)
    df_new = df_new[['Verein', 'Vereins_ID']]
    #df_verein['Vereins_ID'] = range(1,len(df_verein)+1)
    return df_new


#df = clubs_premier_league()
#db.upload_local_data_to_database(df, 'master_vereins_id')

