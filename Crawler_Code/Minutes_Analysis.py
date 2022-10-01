#packages and modules
import pandas as pd



import Read_Load_Database as db



f = db.get_data_db(23)
df = f.get_data()

#df.to_csv('D:/Crawling/minutes.csv')

df['Goals_home'] = pd.to_numeric(df['Home_Minutes'].str.split('+', expand = True)[0],errors='coerce')
df['Goals_away'] = pd.to_numeric(df['Away_Minutes'].str.split('+', expand = True)[0],errors='coerce')

df = df[['home_id', 'away_id', 'Goals_home', 'Goals_away', 'Spieltag']]
df = df.sort_values(by = ['Spieltag', 'home_id'])


list_with = []
list_without = []
df_over = pd.DataFrame()

spieltage = df['Spieltag'].drop_duplicates()


for s in spieltage:
    
    df_spieltag = df[df['Spieltag']==s]
    einzelne_spiele = df_spieltag['home_id'].drop_duplicates()
    
    for v in einzelne_spiele:
        df_v = df_spieltag[df_spieltag['home_id']==v]
        
        with_df = df_v[(df_v['Goals_home']>79) | (df_v['Goals_away']>79)]
        #with_df = df_v[(df_v['Goals_home']>78)]
        #with_df_away = df_v[]

        if len(with_df)>0:
            df_over = df_over.append(with_df)
            
            
df_test = df_over.drop_duplicates(['Spieltag', 'home_id'])
df_counter = df.drop_duplicates(['Spieltag', 'home_id'])

print(1/(1-len(df_test)/len(df_counter)))