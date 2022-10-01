import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')


import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

import My_Tools as t

def delete_matchday_club(table, saison, spieltag, vereins_id):
    query = "delete from " +table + " where saison = " +  saison + " and spieltag = " + spieltag + " and vereins_id = " + vereins_id
    t.delete(query)

def get_table(table):
    query = 'select* from '+table   
    df = t.connection(query)
    return df

def delete_table_saison(table, saison):
    query = 'delete from '+table + ' where saison = ' +  saison 
    t.connection(query)

def get_startelf_grades():
    query = '''
select 
	s.saison, s.spieltag, s.Vereins_ID,
    s.Spieler_1, k1.Spieler, k1.Position, k1.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k1 on s.Vereins_ID = k1.Vereins_ID and s.Spieler_1 = k1.Spieler_ID and k1.Spieltag = s.Spieltag and s.Saison = k1.Saison    
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_2, k2.Spieler, k2.Position,  k2.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k2 on s.Vereins_ID = k2.Vereins_ID and s.Spieler_2 = k2.Spieler_ID and k2.Spieltag = s.Spieltag and s.Saison = k2.Saison       
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_3, k3.Spieler, k3.Position,  k3.Kicker_Grade_Average 
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k3 on s.Vereins_ID = k3.Vereins_ID and s.Spieler_3 = k3.Spieler_ID and k3.Spieltag = s.Spieltag and s.Saison = k3.Saison  
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_4, k4.Spieler, k4.Position,  k4.Kicker_Grade_Average 
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k4 on s.Vereins_ID = k4.Vereins_ID and s.Spieler_4 = k4.Spieler_ID and k4.Spieltag = s.Spieltag and s.Saison = k4.Saison
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_5, k5.Spieler, k5.Position,  k5.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k5 on s.Vereins_ID = k5.Vereins_ID and s.Spieler_5 = k5.Spieler_ID and k5.Spieltag = s.Spieltag and s.Saison = k5.Saison
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_6, k6.Spieler, k6.Position,  k6.Kicker_Grade_Average  
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k6 on s.Vereins_ID = k6.Vereins_ID and s.Spieler_6 = k6.Spieler_ID and k6.Spieltag = s.Spieltag and s.Saison = k6.Saison    
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_7, k7.Spieler, k7.Position,  k7.Kicker_Grade_Average  
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k7 on s.Vereins_ID = k7.Vereins_ID and s.Spieler_7 = k7.Spieler_ID and k7.Spieltag = s.Spieltag and s.Saison = k7.Saison  
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_8, k8.Spieler, k8.Position,  k8.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k8 on s.Vereins_ID = k8.Vereins_ID and s.Spieler_8 = k8.Spieler_ID and k8.Spieltag = s.Spieltag and s.Saison = k8.Saison  
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_9, k9.Spieler, k9.Position,  k9.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k9 on s.Vereins_ID = k9.Vereins_ID and s.Spieler_9 = k9.Spieler_ID and k9.Spieltag = s.Spieltag and s.Saison = k9.Saison     
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_10, k10.Spieler, k10.Position,  k10.Kicker_Grade_Average 
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k10 on s.Vereins_ID = k10.Vereins_ID and s.Spieler_10 = k10.Spieler_ID and k10.Spieltag = s.Spieltag and s.Saison = k10.Saison         
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_11, k11.Spieler, k11.Position,  k11.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade k11 on s.Vereins_ID = k11.Vereins_ID and s.Spieler_11 = k11.Spieler_ID and k11.Spieltag = s.Spieltag and s.Saison = k11.Saison  
        
    order by saison, spieltag, Vereins_ID'''
    
    df = t.connection(query)
    
    return df


def get_startelf_grades_forecast():
    query = '''

select 
	s.saison, s.spieltag, s.Vereins_ID,
    s.Spieler_1, k1.Spieler, k1.Position, k1.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k1 on s.Vereins_ID = k1.Vereins_ID and s.Spieler_1 = k1.Spieler_ID and k1.Spieltag + 1 = s.Spieltag and s.Saison = k1.Saison    
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_2, k2.Spieler, k2.Position,  k2.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k2 on s.Vereins_ID = k2.Vereins_ID and s.Spieler_2 = k2.Spieler_ID and k2.Spieltag + 1 = s.Spieltag and s.Saison = k2.Saison       
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_3, k3.Spieler, k3.Position,  k3.Kicker_Grade_Average 
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k3 on s.Vereins_ID = k3.Vereins_ID and s.Spieler_3 = k3.Spieler_ID and k3.Spieltag + 1 = s.Spieltag and s.Saison = k3.Saison  
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_4, k4.Spieler, k4.Position,  k4.Kicker_Grade_Average 
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k4 on s.Vereins_ID = k4.Vereins_ID and s.Spieler_4 = k4.Spieler_ID and k4.Spieltag + 1 = s.Spieltag and s.Saison = k4.Saison
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_5, k5.Spieler, k5.Position,  k5.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k5 on s.Vereins_ID = k5.Vereins_ID and s.Spieler_5 = k5.Spieler_ID and k5.Spieltag + 1 = s.Spieltag and s.Saison = k5.Saison
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_6, k6.Spieler, k6.Position,  k6.Kicker_Grade_Average  
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k6 on s.Vereins_ID = k6.Vereins_ID and s.Spieler_6 = k6.Spieler_ID and k6.Spieltag + 1 = s.Spieltag and s.Saison = k6.Saison    
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_7, k7.Spieler, k7.Position,  k7.Kicker_Grade_Average  
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k7 on s.Vereins_ID = k7.Vereins_ID and s.Spieler_7 = k7.Spieler_ID and k7.Spieltag + 1 = s.Spieltag and s.Saison = k7.Saison  
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_8, k8.Spieler, k8.Position,  k8.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k8 on s.Vereins_ID = k8.Vereins_ID and s.Spieler_8 = k8.Spieler_ID and k8.Spieltag + 1 = s.Spieltag and s.Saison = k8.Saison  
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_9, k9.Spieler, k9.Position,  k9.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k9 on s.Vereins_ID = k9.Vereins_ID and s.Spieler_9 = k9.Spieler_ID and k9.Spieltag + 1 = s.Spieltag and s.Saison = k9.Saison     
        
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_10, k10.Spieler, k10.Position,  k10.Kicker_Grade_Average 
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k10 on s.Vereins_ID = k10.Vereins_ID and s.Spieler_10 = k10.Spieler_ID and k10.Spieltag + 1 = s.Spieltag and s.Saison = k10.Saison         
        UNION
    
    select 
    	s.saison, s.spieltag, s.Vereins_ID,
        s.Spieler_11, k11.Spieler, k11.Position,  k11.Kicker_Grade_Average
    from 
    	bl1_features_startelf s
    inner join 
    	bl1_data_kicker_average_grade_forecast k11 on s.Vereins_ID = k11.Vereins_ID and s.Spieler_11 = k11.Spieler_ID and k11.Spieltag + 1 = s.Spieltag and s.Saison = k11.Saison  
        
    order by saison, spieltag, Vereins_ID'''
    
    df = t.connection(query)
    
    return df

def get_system_trainer():
   
    query = '''
    select
    vss1.vereins_id, vss1.Verein, vss1.Saison, vss1.Spieltag, ms.System_ID, o.Trainer_ID
    from
    bl1_data_vereine_spielsystem vss1
    left outer join
    master_system ms on ms.System = vss1.Spiel_System
    inner JOIN
    bl1_data_trainer_spiele o ON vss1.vereins_id = o.Vereins_ID
    AND
    vss1.Saison = o.Saison
    AND
    vss1.Spieltag = o.Spieltag;'''
       
    df = t.connection(query)              
    return df

def get_system_trainer_startelf():
   
    query = '''
    select
    vss1.vereins_id, vss1.Verein, vss1.Saison, vss1.Spieltag, ms.System_ID, o.Trainer_ID, s.Spieler_1,
        s.Spieler_2, s.Spieler_3, s.Spieler_4, s.Spieler_5, s.Spieler_6, s.Spieler_7, s.Spieler_8
        ,s.Spieler_9, s.Spieler_10, s.Spieler_11
    from
    bl1_data_vereine_spielsystem vss1
    left outer join
    master_system ms on ms.System = vss1.Spiel_System
    inner JOIN
    bl1_data_trainer_spiele o ON vss1.vereins_id = o.Vereins_ID
    AND
    vss1.Saison = o.Saison
    AND
    vss1.Spieltag = o.Spieltag
    inner join
    bl1_features_startelf s on vss1.vereins_id = s.Vereins_ID
    AND
    vss1.Saison = s.Saison
    AND
    vss1.Spieltag = s.Spieltag;'''
       
    df = t.connection(query)              
    return df


   
def upload_local_data_to_database(df, table):
    engine = create_engine('mysql+mysqlconnector://root:pw@localhost:3306/bl1_daten', echo=False)
    df.to_sql(name=table, con=engine, if_exists = 'append', index=False)
    #print("Data succesfully uploaded")
    
def upload_replace_local_data_to_database(df, table):
    engine = create_engine('mysql+mysqlconnector://root:pw@localhost:3306/bl1_daten', echo=False)
    df.to_sql(name=table, con=engine, if_exists = 'replace', index=False)
    #print("Data succesfully uploaded")