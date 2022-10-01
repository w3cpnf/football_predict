import Read_Load_Database as db
import pandas as pd



def get_system_trainer():
    df_system_trainer = db.get_system_trainer()
    df_system_trainer = df_system_trainer.dropna()
    df_system_trainer['System_Trainer'] = df_system_trainer['System_ID'].astype(str) + ',' + df_system_trainer['Trainer_ID'].astype(str)
   
    df_all = pd.DataFrame()
   
    for v_id in df_system_trainer['vereins_id'].drop_duplicates():
        df_team = df_system_trainer[df_system_trainer['vereins_id'] == v_id]
       
        for trainer in df_team['Trainer_ID'].drop_duplicates():
            df = df_team[df_team['Trainer_ID']==trainer]
           
            df = df[['vereins_id', 'Verein', 'Saison', 'Spieltag', 'Trainer_ID', 'System_Trainer']]
            df = df.drop_duplicates('System_Trainer')
            df.index = range(len(df_all), len(df_all)+len(df))
            df['Trainer_System_ID'] = df.index
            df_all = df_all.append(df)
           
    return df_all

df = get_system_trainer()


