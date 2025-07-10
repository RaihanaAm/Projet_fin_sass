#Projet fin sass
#Imortation de biblio Pandas
import pandas as pd

#** 1-Charger le jeu de données à l’aide de Pandas.
df = pd.read_csv('DataSet.csv')
 

###** 2-Afficher la taille (dimensions) du dataset (lignes, colonnes).
print(df.shape)
#result :(5735, 28)

###** 3-Lister les colonnes disponibles dans le dataset.
print(df.columns)
#result :Index(['SEQN', 'ALQ101', 'ALQ110', 'ALQ130', 'SMQ020', 'RIAGENDR', 'RIDAGEYR','RIDRETH1', 'DMDCITZN', 'DMDEDUC2', 'DMDMARTL', 'DMDHHSIZ', 'WTINT2YR',....# 

###** 4-Créer un sous-ensemble du jeu de données contenant uniquement les colonnes suivantes :
    ##['SEQN','SMQ020', 'RIAGENDR', 'RIDAGEYR','DMDEDUC2','BMXWT', 'BMXHT', 'BMXBMI'].


nv_colonnes = ['SEQN', 'SMQ020', 'RIAGENDR', 'RIDAGEYR', 'DMDEDUC2', 'BMXWT', 'BMXHT', 'BMXBMI']
df_sous_ensemble = df[nv_colonnes]

#print(df_sous_ensemble.head())

#** 5-Afficher les informations générales (.info()) sur ce sous-ensemble.
df_sous_ensemble.info()

#**6-Renommer les colonnes avec des noms plus explicites : ['seqn','smoking','gender', 'age','education','weight','height','bmi'].

col_renamme = ['seqn','smoking','gender', 'age','education','weight','height','bmi']

df_sous_ensemble= df_sous_ensemble.rename(columns={"SEQN":"seqn",'SMQ020':'smoking','RIAGENDR':'gender','RIDAGEYR':'age','DMDEDUC2':'education','BMXWT':'weight','BMXHT':'height','BMXBMI':'bmi'})
print(df_sous_ensemble.columns.to_list())

#** -7-Vérifier la présence de doublons dans le dataset.
print(df_sous_ensemble.duplicated())

#** 8-Supprimer les doublons si nécessaire.
#drop_duplicated()

##** 9- Supprimer la colonne 'seqn', considérée comme un identifiant inutile pour l’analyse.
#print(df_sous_ensemble.drop("seqn", axis=1))

##** 10 -Identifier les valeurs manquantes (NaN) dans les colonnes.
print(df_sous_ensemble.isnull().sum())