#Projet fin sass
#Imortation de biblio Pandas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData , Table,func ,select ,case 




load_dotenv()
    
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


#!!!!!!!! la connexion avec la base de donne

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

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
df_sous_ensemble = df[nv_colonnes].copy() 

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
print('**** drop')
print(df_sous_ensemble.drop("seqn", axis=1))
df_sous_ensemble=df_sous_ensemble.drop("seqn", axis=1)
print('**** colums')
print(df_sous_ensemble.columns)

##** 10 -Identifier les valeurs manquantes (NaN) dans les colonnes.
#print(df_sous_ensemble.isnull().sum())

##** 11-Remplacer les valeurs manquantes :
#    *education : remplacer par la médiane

#    *weight, height, bmi : remplacer par la moyenne
df_sous_ensemble['education'].fillna(df_sous_ensemble['education'].median())

df_sous_ensemble['height'].fillna(df_sous_ensemble['height'].mean())
df_sous_ensemble['bmi'].fillna(df_sous_ensemble['bmi'].mean())

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
   


#** 15-Remplacer les codes numériques par des labels explicites dans trois colonnes :

#smoking : {1: 'yes', 2: 'no', 7: nan, 8: nan}
df_sous_ensemble['smoking'] = df_sous_ensemble['smoking'].replace({1:'yes',2:'no',7:"nan",8:"nan"})
#gender : {1: 'male', 2: 'female'}

df_sous_ensemble["gender"] = df_sous_ensemble["gender"].replace({1: "femme", 2: "homme"})
#education :{    1: '<9th grade', 2: '9-11th grade', 3: 'HS or GED', 4: 'Some college / AA', 5: 'College or above', 7: 'Other', 8: 'Other'}
df_sous_ensemble['education'] = df_sous_ensemble['education'].replace({    1: '<9th grade', 2: '9-11th grade', 3: 'HS or GED', 4: 'Some college / AA', 5: 'College or above', 7: 'Other', 8: 'Other'})

# print(df_sous_ensemble)

#** 16-Analyser les relations entre variables :


#Utiliser Seaborn Pairplot

plt.title('les relation entre les variable')
sns.pairplot(df_sous_ensemble, hue='gender')
#plt.show()
#Créer des graphiques individuels pour observer la distribution ou la corrélation de chaque attribut.
plt.title("Distribution de l'age")
for i in collone:
    sns.histplot(df_sous_ensemble[i])

df_sous_ensemble.to_csv('data_nettoye.csv')
#**17 Sql

metadata = MetaData()
df_sous_ensemble.to_sql('health_data_cleaned', engine, if_exists='append', index=False)

#** Quelle est la répartition des individus par genre (gender)
health_data = Table('health_data_cleaned', metadata , autoload_with=engine)

with engine.begin() as conn:
    r1 = conn.execute(
        select(health_data.c.gender, func.count().label("nombre"))
        .group_by(health_data.c.gender)
    )
    for row in r1:
        print(f"Genre: {row.gender}, Nombre: {row.nombre}")


#*Quelle est la répartition des individus en fonction de leurs habitudes de tabagisme (smoking) 
with engine.begin() as conn:
    result = conn.execute(
        select(health_data.c.smoking, func.count().label("nombre"))
        .group_by(health_data.c.smoking)
    )
    for row in result:
        print(f"Fumeur: {row.smoking}, Nombre: {row.nombre}")
    #**Quelle est la moyenne de l'IMC (bmi) pour chaque genre (gender) 
    result2 = conn.execute(
        select(health_data.c.gender, func.avg(health_data.c.bmi).label("bmi_moyen"))
        .group_by(health_data.c.gender)
    )
    for row in result2:
        print(f"Genre: {row.gender}, BMI moyen: {row.bmi_moyen}")
    #**Comment les individus se répartissent-ils en fonction de leur niveau d'éducation (education) ?
    result3 = conn.execute(
        select(health_data.c.education, func.count().label("bmi_moyen"))
        .group_by(health_data.c.education)
    )
    for row in result3:
        print(f"education: {row}")



#** Quelle est l'évolution de l'IMC moyen (bmi) en fonction des tranches d'âge (par exemple, 18-30, 31-50, 51+) 
age_groupe = case(
    (health_data.c.age.between(18,30),'18-30'),
    (health_data.c.age.between(31,35),'31-35'),
    (health_data.c.age.between(18,30),'18-30')
    (health_data.c.age >=51 , "51+")
)



