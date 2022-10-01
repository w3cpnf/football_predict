import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import re
import numpy as np
import Read_Load_Database as db
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# driver = webdriver.Chrome(service=Service('D:\Projects\Football\Database\Crawler_Code\Webdrivers\chromedriver.exe'))
# driver.get('https://www.transfermarkt.de/dr-felix-brych/profil/schiedsrichter/2')


# #html = driver.find_elements("xpath", "//div[@class='responsive-table']")
# teams_html = driver.find_elements("xpath", "//td[@class='no-border-links']")
# spieltag_html = driver.find_elements("xpath", "//td[@class='zentriert']")

# spieltage = []
# for n in range(len(spieltag_html)):
#     spieltage.append(spieltag_html[n].text)

# bundesliga_spieltag = list()
# for s in range(len(spieltage)):
#     if len(spieltage[s]) == 10:
#         if len(spieltage[s-1]) == 1:
#             bundesliga_spieltag.append(int(spieltage[s-1]))

# teams = []
# for n in range(len(teams_html)):
#     teams.append(teams_html[n].text)

# df_teams = pd.DataFrame(teams)
# df_teams = df_teams[0].str.split('(', expand = True)
# teams = df_teams[0].iloc[0:2*len(bundesliga_spieltag)]
# df_teams = pd.DataFrame(teams)
# df_teams.columns = ['Heimmannschaft']
# df_teams = df_teams.assign(Auswärtsmannschaft = np.nan)

# for team in range(0, len(df_teams), 2):
#     df_teams.iloc[team, 1] = df_teams.iloc[team + 1, 0]
# df_teams = df_teams.dropna()
# df_teams = df_teams.assign(Spieltag = bundesliga_spieltag)



def get_referees(gameday, saison):



    df_vereine = db.get_table('bl1_staging_ergebnisse')
    df_vereine = df_vereine[df_vereine['Saison']==saison]
    
    

    df_schiedsrichter = db.get_table('bl1_mapping_schiedsrichter')
    df_schiedsrichter = df_schiedsrichter[df_schiedsrichter['Saison']==saison]
    df_schiedsrichter.index = range(len(df_schiedsrichter))
    
    l1 = df_schiedsrichter['Webpage']
    l2 = df_schiedsrichter['Schiedsrichter']
    l3 = df_schiedsrichter['Schiedsrichter_ID']
    

    df_complete = pd.DataFrame()
    
    for b in range(len(l1)):
    #for b in range(1,2):
    
        url = l1[b]
        url = url + '/plus/0?funktion=1&saison_id=2021&wettbewerb_id=L1'
        sch = l2[b]
        s_id = l3[b]
        
        driver = webdriver.Chrome(service=Service('D:\Projects\Football\Database\Crawler_Code\Webdrivers\chromedriver.exe'))
        driver.get(url)
        time.sleep(3)
        teams_html = driver.find_elements("xpath", "//td[@class='no-border-links']")
        spieltag_html = driver.find_elements("xpath", "//td[@class='zentriert']")
        
        spieltage = []
        for n in range(len(spieltag_html)):
            spieltage.append(spieltag_html[n].text)
        
        bundesliga_spieltag = list()

        for s in range(len(spieltage)):
            if len(spieltage[s]) == 10:

                if len(spieltage[s-1]) == 1 or len(spieltage[s-1]) == 2:

                    bundesliga_spieltag.append(int(spieltage[s-1]))

        teams = []
        for n in range(len(teams_html)):
            teams.append(teams_html[n].text)
        
        df_teams = pd.DataFrame(teams)
        df_teams = df_teams[0].str.split('(', expand = True)

        teams = df_teams[0].iloc[0:2*len(bundesliga_spieltag)]
        df_teams = pd.DataFrame(teams)
        df_teams.columns = ['Heimmannschaft']
        df_teams = df_teams.assign(Auswärtsmannschaft = np.nan)
        
        for team in range(0, len(df_teams), 2):
            df_teams.iloc[team, 1] = df_teams.iloc[team + 1, 0]
        df_teams = df_teams.dropna()
        df_teams = df_teams.assign(Spieltag = bundesliga_spieltag)
        

        df_teams = df_teams.assign(Schiedsrichter = sch, Schiedsrichter_ID = s_id)
        df_teams['Heimmannschaft'] = df_teams['Heimmannschaft'].str.strip()
        df_teams['Auswärtsmannschaft'] = df_teams['Auswärtsmannschaft'].str.strip()
        df_teams = df_teams.replace({'Bor. Dortmund': 'Borussia Dortmund', 'Bay. Leverkusen': 'Bayer 04 Leverkusen', 'SC Freiburg':'Sport-Club Freiburg',
                            'F. Düsseldorf':'Fortuna Düsseldorf', 'Union Berlin':'1. FC Union Berlin', 'Bayern München':'FC Bayern München', 
                            'SC Paderborn':'SC Paderborn 07', '1.FSV Mainz 05':'1. FSV Mainz 05', 'FC Schalke':'FC Schalke 04',
                            'TSG Hoffenheim':'TSG 1899 Hoffenheim', 'E. Frankfurt':'Eintracht Frankfurt', 'Werder Bremen':'SV Werder Bremen', 
                            '1.FC Köln':'1. FC Köln', 'Bor. M\'gladbach':'Borussia Mönchengladbach', 'Arm. Bielefeld':'DSC Arminia Bielefeld', 
                            '1.FC Nürnberg':'1. FC Nürnberg', 'Greuther Fürth':'SpVgg Greuther Fürth'})  

        #print(df_vereine)
        df = df_teams.merge(df_vereine, on = ['Heimmannschaft', 'Spieltag', 'Auswärtsmannschaft'], how = 'inner')

        df = df[['Schiedsrichter_ID', 'Schiedsrichter', 'Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 
                 'Auswärtsmannschaft','Saison']]

        driver.quit()
        df_complete = df_complete.append(df)
        #df_complete = df_complete[df_complete['Spieltag']==gameday]
        
    return df_complete

df = get_referees(1, '2021/22')
db.upload_local_data_to_database(df, 'bl1_data_schiedsrichter_spiele')











