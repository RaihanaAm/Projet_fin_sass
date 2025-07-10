#Projet fin sass
#Imortation de biblio Pandas
import pandas as pd
import numpy as np

#** 1-Charger le jeu de données à l’aide de Pandas.
df = pd.read_csv('DataSet.csv')
 

###** 2-Afficher la taille (dimensions) du dataset (lignes, colonnes).
#print(df.shape)
#result :(5735, 28)

###** 3-Lister les colonnes disponibles dans le dataset.
#print(df.columns)
#result :Index(['SEQN', 'ALQ101', 'ALQ110', 'ALQ130', 'SMQ020', 'RIAGENDR', 'RIDAGEYR','RIDRETH1', 'DMDCITZN', 'DMDEDUC2', 'DMDMARTL', 'DMDHHSIZ', 'WTINT2YR',....# 

###** 4-Créer un sous-ensemble du jeu de données contenant uniquement les colonnes suivantes :
    ##['SEQN','SMQ020', 'RIAGENDR', 'RIDAGEYR','DMDEDUC2','BMXWT', 'BMXHT', 'BMXBMI'].


nv_colonnes = ['SEQN', 'SMQ020', 'RIAGENDR', 'RIDAGEYR', 'DMDEDUC2', 'BMXWT', 'BMXHT', 'BMXBMI']
df_sous_ensemble = df[nv_colonnes]

#print(df_sous_ensemble.head())

#** 5-Afficher les informations générales (.info()) sur ce sous-ensemble.
#df_sous_ensemble.info()

#**6-Renommer les colonnes avec des noms plus explicites : ['seqn','smoking','gender', 'age','education','weight','height','bmi'].

df_sous_ensemble.columns=['seqn','smoking','gender', 'age','education','weight','height','bmi']


#print(df_sous_ensemble.columns.to_list())

#** -7-Vérifier la présence de doublons dans le dataset.
#print(df_sous_ensemble.duplicated())

#** 8-Supprimer les doublons si nécessaire.
#drop_duplicated()

##** 9- Supprimer la colonne 'seqn', considérée comme un identifiant inutile pour l’analyse.
#print(df_sous_ensemble.drop("seqn", axis=1))

##** 10 -Identifier les valeurs manquantes (NaN) dans les colonnes.
#print(df_sous_ensemble.isnull().sum())

##** 11-Remplacer les valeurs manquantes :
#    *education : remplacer par la médiane
df_sous_ensemble.education  =df_sous_ensemble.education.fillna(df_sous_ensemble.education.median)

#    *weight, height, bmi : remplacer par la moyenne
df_sous_ensemble.weight  =df_sous_ensemble.weight.fillna(df_sous_ensemble.weight.mean)
df_sous_ensemble.height  =df_sous_ensemble.height.fillna(df_sous_ensemble.height.mean)
df_sous_ensemble.bmi  =df_sous_ensemble.bmi.fillna(df_sous_ensemble.bmi.mean)
#print(df_sous_ensemble.isnull().sum())


#** 12-Afficher les statistiques descriptives (moyenne, écart-type, min, max, etc.) du dataset.
#print(df_sous_ensemble.describe())

#** 13- Détecter les valeurs aberrantes (outliers) à l’aide de méthodes statistiques

collone = ["gender","age","weight","height","bmi"]
#convert to float
for col in collone:
   df_sous_ensemble[col] = pd.to_numeric(df_sous_ensemble[col], errors='coerce')



for i in collone:

    Q1= df_sous_ensemble[i].quantile(0.25)
    Q3= df_sous_ensemble[i].quantile(0.75)
    IRQ = Q3-Q1
    v_min= Q1-1.5*IRQ
    v_max= Q3 +1.5*IRQ
   #outliers
    outliers = (df_sous_ensemble[i] < v_min) | (df_sous_ensemble[i] > v_max)
    #** 14-Supprimer les outliers pour améliorer la qualité des données.
    df_sous_ensemble = df_sous_ensemble[(df_sous_ensemble[i] >= v_min) &  (df_sous_ensemble[i] <= v_max)]
    df_sous_ensemble = df_sous_ensemble.reset_index(drop=True)
   

print(df_sous_ensemble)


