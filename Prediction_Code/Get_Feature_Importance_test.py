import os
os.chdir('D:/Projects/Football/Prediction_Code')
#https://mljar.com/blog/feature-importance-in-random-forest/


import Read_Load_Prediction as db
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
#import shap
from matplotlib import pyplot as plt
from sklearn.datasets import make_regression
from sklearn.tree import DecisionTreeRegressor
from matplotlib import pyplot
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot
import time


f1 = db.get_data_db(12)
df1 = f1.get_data()

f2 = db.get_data_db(13)
df2 = f2.get_data()

df = df1.merge(df2, on = ['Saison', 'Spieltag', 'Heimmannschaft', 'Heimmannschaft_ID', 'Gegner_ID'])
df = df.sort_values(['Saison', 'Spieltag'])

df = df[df['Heimmannschaft_ID']==16]

df_correlation = df[['Spiel_Ausgang', 'Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
       'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz', 'Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
       'Trainer_ID', 'Gegner_Trainer_ID', 'L1', 'L2', 'L3', 'L4', 'L5', 'GegnerL1', 'GegnerL2', 'GegnerL3', 'GegnerL4', 'GegnerL5',
       'B365H', 'B365D', 'B365A', 'HeimSystem', 'AuswärtsSystem', 'Home_Shot_Feature', 'Home_Shot_On_Goal_Feature', 'Home_Fouls_Feature',
       'Home_Corner_Feature', 'Home_Yellowcard_Feature', 'Home_Redcard_Feature', 'Away_Shot_Feature', 'Away_Shot_On_Goal_Feature', 
       'Away_Fouls_Feature', 'Away_Corner_Feature', 'Away_Yellowcard_Feature', 'Away_Redcard_Feature']]  

y = df[['Spiel_Ausgang']]
X = df[['Gegner_ID', 'Kaderwert_Differenz', 'Kaderwert_Per_Spieler_Differenz', 'Abwehrdifferenz',
       'Gesamtdiffferenz', 'Angriffdifferenz', 'Mittelfelddifferenz', 'Heimangriff_Abwehr_Differenz', 'Auswärtsangriff_Abwehr_Differenz',
       'Trainer_ID', 'Gegner_Trainer_ID', 'L1', 'L2', 'L3', 'L4', 'L5', 'GegnerL1', 'GegnerL2', 'GegnerL3', 'GegnerL4', 'GegnerL5',
       'B365H', 'B365D', 'B365A', 'HeimSystem', 'AuswärtsSystem', 'Home_Shot_Feature', 'Home_Shot_On_Goal_Feature', 'Home_Fouls_Feature',
       'Home_Corner_Feature', 'Home_Yellowcard_Feature', 'Home_Redcard_Feature', 'Away_Shot_Feature', 'Away_Shot_On_Goal_Feature', 
       'Away_Fouls_Feature', 'Away_Corner_Feature', 'Away_Yellowcard_Feature', 'Away_Redcard_Feature']]    




X_train, X_test, y_train, y_test = train_test_split(X, y)


feature_names = [f"feature {i}" for i in range(X.shape[1])]
forest = RandomForestClassifier(random_state=0)
forest.fit(X_train, y_train)

start_time = time.time()
result = permutation_importance(
    forest, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2
)
elapsed_time = time.time() - start_time
print(f"Elapsed time to compute the importances: {elapsed_time:.3f} seconds")

forest_importances = pd.Series(result.importances_mean, index=feature_names)

fig, ax = plt.subplots()
forest_importances.plot.bar(yerr=result.importances_std, ax=ax)
ax.set_title("Feature importances using permutation on full model")
ax.set_ylabel("Mean accuracy decrease")
fig.tight_layout()
plt.show()











# random forest for feature importance on a classification problem
# define dataset
X, y = make_classification(n_samples=1000, n_features=40, n_informative=5, n_redundant=5, random_state=1)
# define the model
model = RandomForestClassifier()
# fit the model
model.fit(X, y)
# get importance
importance = model.feature_importances_
# summarize feature importance
for i,v in enumerate(importance):
	print('Feature: %0d, Score: %.5f' % (i,v))
# plot feature importance
pyplot.bar([x for x in range(len(importance))], importance)
pyplot.show()









corrmat = df_correlation.corr()
top_corr_features = corrmat.index
plt.matshow(df_correlation.corr())
plt.show()
#plot heat map
g=sns.heatmap(df[top_corr_features].corr(),annot=True,cmap="RdYlGn")
plt.savefig('D:/Projects/Football/Prediction_Code/Correlation/correlation.png')




f = db.get_data_db(1)
df = f.get_data()
df = df[df['Heimmannschaft_ID']==1]
df_X = df[['Gegner_ID', 'Kaderwert_Differenz']]

df_Y = df[['Spiel_Ausgang']]

X_train = df_X.iloc[:,:].values[:-10]
X_test = df_X.iloc[:,:].values[-10:]
y_train = df_Y.iloc[:, :].values[:-10]
y_test = df_Y.iloc[:, :].values[-10:]
rf = RandomForestRegressor(n_estimators=2000)
rf.fit(X_train, y_train)
rf.feature_importances_
#outcome = random_forest(4, '2020/21', 31,[1,2,3,4,5,6,7,8,9,10,11,12, 13, 14,15,16], 1000)

    # X = df.iloc[:,1:10]  #independent columns
    # y = df.iloc[:,0] 
    # print(y)
    
    # model = ExtraTreesClassifier()
    # model.fit(X,y) 
    # print(model.feature_importances_)
    # feat_importances = pd.Series(model.feature_importances_, index=X.columns)
    # feat_importances.nlargest(10).plot(kind='barh')
    # plt.show()
perm_importance = permutation_importance(rf, X_test, y_test)

explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test)

# define dataset
X, y = make_regression(n_samples=1000, n_features=40, n_informative=5, random_state=0)
# define the model
model = DecisionTreeRegressor()
# fit the model
model.fit(X, y)
# get importance
importance = model.feature_importances_
# summarize feature importance
for i,v in enumerate(importance):
	print('Feature: %0d, Score: %.5f' % (i,v))
# plot feature importance
pyplot.bar([x for x in range(len(importance))], importance)
pyplot.show()



# decision tree for feature importance on a classification problem


# define dataset
X, y = make_classification(n_samples=1000, n_features=40, n_informative=5, n_redundant=5, random_state=1)
# define the model
model = DecisionTreeClassifier()
# fit the model
model.fit(X, y)
# get importance
importance = model.feature_importances_
# summarize feature importance
for i,v in enumerate(importance):
	print('Feature: %0d, Score: %.5f' % (i,v))
# plot feature importance
pyplot.bar([x for x in range(len(importance))], importance)
pyplot.show()



# random forest for feature importance on a regression problem
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot
# define dataset
X, y = make_regression(n_samples=1000, n_features=40, n_informative=5, random_state=1)
# define the model
model = RandomForestRegressor()
# fit the model
model.fit(X, y)
# get importance
importance = model.feature_importances_
# summarize feature importance
for i,v in enumerate(importance):
	print('Feature: %0d, Score: %.5f' % (i,v))
# plot feature importance
pyplot.bar([x for x in range(len(importance))], importance)
pyplot.show()