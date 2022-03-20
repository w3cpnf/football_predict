import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import re

import Read_Load_Database as db
import My_Tools as t


def get_referees(gameday, saison):

    #f1 = db.get_data_db(33)
    f1 = db.get_data_db(20)
    df_vereine = f1.get_data()
    df_vereine = df_vereine[df_vereine['Saison']==saison]
    
    
    f2 = db.get_data_db(21)
    df_schiedsrichter = f2.get_data()
    df_schiedsrichter = df_schiedsrichter[df_schiedsrichter['Saison']==saison]
    #df_schiedsrichter = df_schiedsrichter[df_schiedsrichter['Schiedsrichter_ID']==14]
    df_schiedsrichter.index = range(len(df_schiedsrichter))
    
    l1 = df_schiedsrichter['Webpage']
    l2 = df_schiedsrichter['Schiedsrichter']
    l3 = df_schiedsrichter['Schiedsrichter_ID']
    

    df_complete = pd.DataFrame()
    
    for b in range(len(l1)):
    
        w = l1[b]
        sch = l2[b]
        s_id = l3[b]
        
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get(w)
        table = driver.find_elements_by_xpath("//div[@class='responsive-table']")   
        
        data = []
        for n in range(len(table)):
            data.append(table[n].text)
        
        data_1 = data[1].split('-')
        new = []
        for i in range(len(data_1)):
            if data_1[i]!=' ':
                new.append(data_1[i])
        
        df = pd.DataFrame()
        spieltage = []
        vereine = []
        for s in range(len(new)):
            if s == 0:
                new_1 = new[s].split('\n')
                game_1 = re.sub("\s\s+", " ", new_1[2]).strip().split(' ')
                spieltag_1 = int(game_1[0])
                verein_1 = game_1[2] +' '+ game_1[3]
                spieltage.append(spieltag_1)
                vereine.append(verein_1)
            if s == 1:
                new_2 = re.sub("\s\s+", " ",new[s]).strip().split('\n')
                
                if len(new_2)>1:
                    
                    game_2 = new_2[1].split(' ')
                    spieltag_2 = int(game_2[0])
                    verein_2 = game_2[2] +' '+ game_2[3]
                    spieltage.append(spieltag_2)
                    vereine.append(verein_2)
                else:
                
                    game_2 = new_2[0].split(' ')
                    spieltag_2 = int(game_2[0])
                    verein_2 = game_2[2] +' '+ game_2[3]
                    spieltage.append(spieltag_2)
                    vereine.append(verein_2)
                
            if s > 1:
                new_3 = re.sub("\s\s+", " ",new[s]).strip()
                if len(new_3)>3:
                    new_3 = new_3.split(' ')
                    
                    if '\n' in new_3[0]:
                        integer = new_3[0].split('\n')
                        spieltag = int(integer[1])
                        verein = new_3[2] +' '+ new_3[3]
                        spieltage.append(spieltag)
                        vereine.append(verein)    
                    else:
                        spieltag = int(new_3[0])
                        verein = new_3[2] +' '+ new_3[3]
                        spieltage.append(spieltag)
                        vereine.append(verein)
        
                   
                      
        df['Spieltag']=spieltage
        df['Heimmannschaft'] = vereine
        df = df.assign(Schiedsrichter = sch, Schiedsrichter_ID = s_id)
        df = df.replace({'Bor. Dortmund': 'Borussia Dortmund', 'Bay. Leverkusen': 'Bayer 04 Leverkusen', 'SC Freiburg':'Sport-Club Freiburg',
                            'F. Düsseldorf':'Fortuna Düsseldorf', 'Union Berlin':'1. FC Union Berlin', 'Bayern München':'FC Bayern München', 
                            'SC Paderborn':'SC Paderborn 07', '1.FSV Mainz':'1. FSV Mainz 05', 'FC Schalke':'FC Schalke 04',
                            'TSG Hoffenheim':'TSG 1899 Hoffenheim', 'E. Frankfurt':'Eintracht Frankfurt', 'Werder Bremen':'SV Werder Bremen', 
                            '1.FC Köln':'1. FC Köln', 'Bor. M\'gladbach':'Borussia Mönchengladbach', 'Arm. Bielefeld':'DSC Arminia Bielefeld', 
                            '1.FC Nürnberg':'1. FC Nürnberg'})  
        
        df = df.merge(df_vereine, on = ['Heimmannschaft', 'Spieltag'], how = 'inner')
        df = df[['Schiedsrichter_ID', 'Schiedsrichter', 'Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 
                 'Auswärtsmannschaft','Saison',  'Jahr']]
        
        driver.quit()
        df_complete = df_complete.append(df)
        #df_complete = df_complete[df_complete['Spieltag']==gameday]
        
    return df_complete

#df = get_referees(1, '2016/17')
#df = get_refrees()
import time



def get_ref(i):

    f1 = db.get_data_db(20)
    df_vereine = f1.get_data()
    df_vereine = df_vereine[df_vereine['Saison']=='2020/21']
        
        
    f2 = db.get_data_db(21)
    df_schiedsrichter = f2.get_data()
    df_schiedsrichter = df_schiedsrichter[df_schiedsrichter['Saison']=='2020/21']
    df_schiedsrichter.index = range(len(df_schiedsrichter))
        
    l1 = df_schiedsrichter['Webpage']
    l2 = df_schiedsrichter['Schiedsrichter']
    l3 = df_schiedsrichter['Schiedsrichter_ID']
    
    w = l1[i]
    sch = l2[i]
    s_id = l3[i]
    print(s_id)
    url = w + 'plus/0?funktion=1&saison_id=2020&wettbewerb_id=L1'
    driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
    driver.get(url)
            
    time.sleep(3)
    table = driver.find_elements_by_xpath("//div[@class='responsive-table']")   
    
    data = []
    for n in range(len(table)):
        data.append(table[n].text)
    
    data_1 = data[1].split('-')
    new = []
    for i in range(len(data_1)):
        if data_1[i]!=' ':
            new.append(data_1[i])
                    
    df = pd.DataFrame()
    spieltage = []
    vereine = []

    for s in range(len(new)):
        if s == 0:
            new_1 = new[s].split('\n')
            game_1 = re.sub("\s\s+", " ", new_1[2]).strip().split(' ')
            spieltag_1 = int(game_1[0])
            verein_1 = game_1[2] +' '+ game_1[3]
            spieltage.append(spieltag_1)
            vereine.append(verein_1)
        if s == 1:
            new_2 = re.sub("\s\s+", " ",new[s]).strip().split('\n')
            
            if len(new_2)>1:
                
                game_2 = new_2[1].split(' ')
                spieltag_2 = int(game_2[0])
                verein_2 = game_2[2] +' '+ game_2[3]
                spieltage.append(spieltag_2)
                vereine.append(verein_2)
            else:
            
                game_2 = new_2[0].split(' ')
                spieltag_2 = int(game_2[0])
                verein_2 = game_2[2] +' '+ game_2[3]
                spieltage.append(spieltag_2)
                vereine.append(verein_2)
            
        if s > 1:
            new_3 = re.sub("\s\s+", " ",new[s]).strip()
            
            if len(new_3)>3:
                new_3 = new_3.split(' ')
            
              
                if '\n' in new_3[0]:
                    integer = new_3[0].split('\n')
                    spieltag = int(integer[1])
                    verein = new_3[2] +' '+ new_3[3]
                    spieltage.append(spieltag)
                    vereine.append(verein)
                  
                elif '\n' in new_3[1]:
                  
                    integer_12 = new_3[1].split('\n')
                    integer = integer_12[1] #integer_12[0]
                    spieltag = int(integer)
                    verein = new_3[3] +' '+ new_3[4]
                    spieltage.append(spieltag)
                    vereine.append(verein)
                else:
                    spieltag = int(new_3[0])
                    verein = new_3[2] +' '+ new_3[3]
                    spieltage.append(spieltag)
                    vereine.append(verein)
    
               
            
    df['Spieltag']=spieltage
    df['Heimmannschaft'] = vereine
    print(vereine)
    print(len(vereine))
    
    df['Heimmannschaft'] = df['Heimmannschaft'].str.strip()
    df = df.assign(Schiedsrichter = sch, Schiedsrichter_ID = s_id)
    df = df.replace({'Bor. Dortmund': 'Borussia Dortmund', 'Bay. Leverkusen': 'Bayer 04 Leverkusen', 'SC Freiburg':'Sport-Club Freiburg',
                        'F. Düsseldorf':'Fortuna Düsseldorf', 'Union Berlin':'1. FC Union Berlin', 'Bayern München':'FC Bayern München', 
                        'SC Paderborn':'SC Paderborn 07', '1.FSV Mainz':'1. FSV Mainz 05', 'FC Schalke':'FC Schalke 04',
                        'TSG Hoffenheim':'TSG 1899 Hoffenheim', 'E. Frankfurt':'Eintracht Frankfurt', 'Werder Bremen':'SV Werder Bremen', 
                        '1.FC Köln':'1. FC Köln', 'Bor. M\'gladbach':'Borussia Mönchengladbach', 'Arm. Bielefeld':'DSC Arminia Bielefeld',
                        'FC Ingolstadt':'FC Ingolstadt 04', 'SV Darmstadt':'SV Darmstadt 98', '1.FC Nürnberg':'1. FC Nürnberg'})  
    
    print(len(df[['Heimmannschaft', 'Spieltag']]))
    print(df[['Heimmannschaft', 'Spieltag']])
    
    df = df.merge(df_vereine, on = ['Heimmannschaft', 'Spieltag'], how = 'inner')
    df = df[['Schiedsrichter_ID', 'Schiedsrichter', 'Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 
             'Auswärtsmannschaft','Saison',  'Jahr']]
    df = df.drop_duplicates()
    driver.quit()
                
    # else:
        
    #     df = pd.DataFrame()
    #     spieltage = []
    #     vereine = []
    
    #     for s in range(len(new)):
    #         if s == 0:
    #             new_1 = new[s].split('\n')
    #             game_1 = re.sub("\s\s+", " ", new_1[2]).strip().split(' ')
    #             spieltag_1 = int(game_1[0])
    #             verein_1 = game_1[2] +' '+ game_1[3]
    #             spieltage.append(spieltag_1)
    #             vereine.append(verein_1)
                
    #         if s > 0:
    #             new_3 = re.sub("\s\s+", " ",new[s]).strip()
    #             if len(new_3)>3:
    #                 new_3 = new_3.split(' ')
                    
    #                 if '\n' in new_3[0]:
    #                     integer = new_3[0].split('\n')
    #                     spieltag = int(integer[1])
    #                     verein = new_3[2] +' '+ new_3[3]
    #                     spieltage.append(spieltag)
    #                     vereine.append(verein)    
    #                 if '\n' in new_3[1]:
    #                     spieltag = int(new_3[0])
    #                     verein = new_3[3] +' '+ new_3[4]
    #                     spieltage.append(spieltag)
    #                     vereine.append(verein)
    #                 else:
    #                     spieltag = int(new_3[0])
    #                     verein = new_3[2] +' '+ new_3[3]
    #                     spieltage.append(spieltag)
    #                     vereine.append(verein)
        
                   
                      
    #     df['Spieltag']=spieltage
    #     df['Heimmannschaft'] = vereine
    #     df['Heimmannschaft'] = df['Heimmannschaft'].str.strip()
    #     df = df.assign(Schiedsrichter = sch, Schiedsrichter_ID = s_id)
    #     df['Heimmannschaft'] = df['Heimmannschaft'].strip()
    #     df = df.replace({'Bor. Dortmund': 'Borussia Dortmund', 'Bay. Leverkusen': 'Bayer 04 Leverkusen', 'SC Freiburg':'Sport-Club Freiburg',
    #                         'F. Düsseldorf':'Fortuna Düsseldorf', 'Union Berlin':'1. FC Union Berlin', 'Bayern München':'FC Bayern München', 
    #                         'SC Paderborn':'SC Paderborn 07', '1.FSV Mainz':'1. FSV Mainz 05', 'FC Schalke':'FC Schalke 04',
    #                         'TSG Hoffenheim':'TSG 1899 Hoffenheim', 'E. Frankfurt':'Eintracht Frankfurt', 'Werder Bremen':'SV Werder Bremen', 
    #                         '1.FC Köln':'1. FC Köln', 'Bor. M\'gladbach':'Borussia Mönchengladbach', 'Arm. Bielefeld':'DSC Arminia Bielefeld',
    #                         'FC Ingolstadt':'FC Ingolstadt 04', 'SV Darmstadt':'SV Darmstadt 98', 'VfB Stuttgart':'VfB Stuttgart',
    #                         '1.FC Nürnberg':'1. FC Nürnberg'})  
        
    #     df = df.merge(df_vereine, on = ['Heimmannschaft', 'Spieltag'], how = 'inner')
    #     df = df[['Schiedsrichter_ID', 'Schiedsrichter', 'Spieltag', 'Heimmannschaft_ID', 'Heimmannschaft', 'Auswärtsmannschaft_ID', 
    #              'Auswärtsmannschaft','Saison',  'Jahr']]
        
    
 
        
    return df
        
                 
#df = get_ref(25)         
#db.upload_local_db_data(df, 25)            
#len(df['Heimmannschaft'])




# driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
# driver.get('https://www.bundesliga.com/de/bundesliga/news/schiedsrichter-ansetzungen-bundesliga-spieltag.jsp')
# test = driver.find_elements_by_xpath("//p[@class='paragraph ng-star-inserted']")   
# df = t.get_dataframe(test)

# hometeams = []
# awayteams = []
# referees = []

# for i in range(0,27,3):
#     print(i)
#     if i == 0:
#         auswärtsmannschaft = df[0].iloc[i].split('-')[1].strip()
#         awayteams.append(auswärtsmannschaft)
#         heimmannschaft = df[0].iloc[i].split('-')[0].strip()
#         hometeams.append(heimmannschaft)
#         schiedsrichter = df[0].iloc[i+1].split(',')[0].split('(')[0].strip()
#         referees.append(schiedsrichter)
#     if i > 0:
#         auswärtsmannschaft = df[0].iloc[i].split('-')[1].strip()
#         awayteams.append(auswärtsmannschaft)
#         heimmannschaft = df[0].iloc[i].split('-')[0].strip()
#         hometeams.append(heimmannschaft)
#         schiedsrichter = df[0].iloc[i+1].split(',')[0].split('(')[0].strip()
#         referees.append(schiedsrichter)

# df = pd.DataFrame(
# {'Heimmannschaft': hometeams,
#  'Auswärtsmannschaft': awayteams,
#  'Schiedsrichter': referees
# })
    
# df['Heimmannschaft']


















