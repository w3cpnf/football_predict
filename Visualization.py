import pandas as pd
import mysql
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
from matplotlib import lines
pd.options.mode.chained_assignment = None

     
def get_vereine(df):
    
    vid = df['Vereins_ID'].drop_duplicates()
    df_all = pd.DataFrame()
    df_all_1 = pd.DataFrame()
    for v in vid:
        df_v = df[df['Vereins_ID']==v]
        if len(df_v)>132:
            df_all = df_all.append(df_v)
        
    gid = df_all['Gegner_ID'].drop_duplicates()

    for g in gid:
        df_v = df_all[df_all['Gegner_ID']==g]
        if len(df_v)>132:
            df_all_1 = df_all_1.append(df_v)
    df = df.sort_values(by = ['Saison', 'Spieltag', 'Vereins_ID'])
    return df_all_1


class descreptive_results:
    
    def __init__(self, df):
        self.df = df
        
    def opponent_statistic(self):
        df = self.df
        df = df.sort_values(by = ['Saison', 'Spieltag', 'Vereins_ID']) 
        v_id = df['Vereins_ID'].drop_duplicates()
        df_complete = pd.DataFrame()
        
        for v in v_id:
            df_v = df[df['Vereins_ID']==v]
            g_id = df_v['Gegner_ID'].drop_duplicates()
            
            df_v = df_v.assign(Victory_all = len(df_v[df_v['Spiel_Ausgang']==1])/len(df_v), Draw_all = len(df_v[df_v['Spiel_Ausgang']==0])/len(df_v), 
                               Lost_all = len(df_v[df_v['Spiel_Ausgang']==-1])/len(df_v))
            for g in g_id:
                df_g = df_v[df_v['Gegner_ID']==g]
                
                if len(df_g) == 0:
                    pass
                else:
                    df_g = df_g.assign(Victory_P = len(df_g[df_g['Spiel_Ausgang']==1])/len(df_g), Draw_P = len(df_g[df_g['Spiel_Ausgang']==0])/len(df_g), 
                                       Lost_P = len(df_g[df_g['Spiel_Ausgang']==-1])/len(df_g))
                    df_g = df_g[['Verein', 'Vereins_ID', 'Gegner', 'Gegner_ID', 'Victory_all', 'Draw_all', 'Lost_all', 'Victory_P', 'Draw_P', 'Lost_P']]
                    df_complete = df_complete.append(df_g) 
       
        return df_complete
    
       
class plot_bar_charts:
    
    def __init__(self, df):
        self.df = df
        
    def plot_victories(self):
        df = self.df
        v_id = df['Vereins_ID'].drop_duplicates()
        
        for v in v_id:
    
            df_verein = df[df['Vereins_ID']==v]
            verein = df_verein['Verein'].iloc[0]
            win = df_verein.sort_values('Victory_P')
    
            plt.rcdefaults()
            fig, ax = plt.subplots()
            fig.set_size_inches(10, 7)
            # Example data
            clubs = []
            wins = []
            for g in win['Gegner']:
                clubs.append(g) 
            for w in win['Victory_P']:
                wins.append(w)
            y_pos = np.arange(len(clubs))
                   
            ax.barh(y_pos, wins, align='center')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(clubs)
            ax.invert_yaxis()  # labels read top-to-bottom
            ax.set_xlabel('Win percentage in the seasons from 2010/11 to 2019/20' + "\n" +'against clubs with a minimum history of 4 seasons in the 1 Bundesliga')
            ax.set_title('Statistic of '+ str(verein))
    
            plt.legend(handles = [lines.Line2D([1,1],[1,1], color = 'r', ls='--', label = 'total win percentage of '+ "\n" + str(verein))], loc='upper right')
            plt.axvline(x= df_verein['Victory_all'].iloc[0], ls='--', color='r')
            
            plt.show()      
            
    def plot_draw(self):
        df = self.df
        v_id = df['Vereins_ID'].drop_duplicates()
        
        for v in v_id:
    
            df_verein = df[df['Vereins_ID']==v]
            verein = df_verein['Verein'].iloc[0]
            head = df_verein.sort_values('Draw_P')
    
            plt.rcdefaults()
            fig, ax = plt.subplots()
            fig.set_size_inches(10, 7)
            # Example data
            clubs = []
            for g in head['Gegner']:
                clubs.append(g)
            performance = []
            for p in head['Draw_P']:
                performance.append(p)
            y_pos = np.arange(len(clubs))
                   
            ax.barh(y_pos, performance, align='center')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(clubs)
            ax.invert_yaxis()  # labels read top-to-bottom
            ax.set_xlabel('Draw percentage in the seasons from 2010/11 to 2019/20' + "\n" +'against clubs with a minimum history of 4 seasons in the 1 Bundesliga')
            ax.set_title('Statistic of '+ str(verein))
    
            plt.legend(handles = [lines.Line2D([1,1],[1,1], color = 'r', ls='--', label = 'total draw average of '+ "\n" + str(verein))], loc='upper right')
            plt.axvline(x= df_verein['Draw_all'].iloc[0], ls='--', color='r')
            
            plt.show()
            
    def plot_lost(self):
        df = self.df
        v_id = df['Vereins_ID'].drop_duplicates()
        
        for v in v_id:
    
            df_verein = df[df['Vereins_ID']==v]
            verein = df_verein['Verein'].iloc[0]
            head = df_verein.sort_values('Lost_P')
    
            plt.rcdefaults()
            fig, ax = plt.subplots()
            fig.set_size_inches(10, 7)
            # Example data
            clubs = []
            for g in head['Gegner']:
                clubs.append(g)
            performance = []
            for p in head['Lost_P']:
                performance.append(p)
            y_pos = np.arange(len(clubs))
                   
            ax.barh(y_pos, performance, align='center')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(clubs)
            ax.invert_yaxis()  # labels read top-to-bottom
            ax.set_xlabel('Loss percentage in the seasons from 2010/11 to 2019/20' + "\n" +'against clubs with a minimum history of 4 seasons in the 1 Bundesliga')
            ax.set_title('Statistic of '+ str(verein))
    
            plt.legend(handles = [lines.Line2D([1,1],[1,1], color = 'r', ls='--', label = 'total loss average of '+ str(verein))], loc='upper right')
            plt.axvline(x= df_verein['Lost_all'].iloc[0], ls='--', color='r')
            
            plt.show()  
 




