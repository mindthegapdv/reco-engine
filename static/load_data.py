import pandas as pd
import random
import numpy as np
from py2neo import Graph, Node, Relationship
from os import environ

df = pd.read_csv("orders.csv")
df2 = pd.read_csv('food_coded.csv')

df_agg = df[['client', 'people']]
df_agg = df_agg.groupby('client').max().reset_index()

list2=[]
for i in range(len(df_agg)):
    num = df_agg['people'][i]
    for k in range(num): 
        list1 = list(df_agg.iloc[i])
        list1.append(random.randrange(120)+1)
        list2.append(list1)
df3 = pd.DataFrame(list2, columns=['client', 'people', 'id'])

list4 = []
for i in range(len(df)):
    num = df['people'][i]
    list1 = list(df3.loc[df3['client']==df['client'][i]]['id'])
    list2 = random.sample(list1, (num-1))
    for item in list2:
        list3 = list(df.iloc[i])
        list3.append(item)
        list4.append(list3)
df4 = pd.DataFrame(list4, columns=['date', 'time', 'people', 'catering', 'client', 'id'])

df_final = pd.merge(df4, df2, on='id', how='left')
df_final.to_csv("final_dataset.csv")


# graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
# graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
# graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
# graph = Graph(graphenedb_url, user=graphenedb_user, password=graphenedb_pass, bolt = True, secure = True, http_port = 24789, https_port = 24780)


# query = '''LOAD CSV WITH HEADERS FROM "file:///companies_final.csv" AS row
# 		CREATE (c:Company {name: row.companyName, founded: toInteger(row.founded), headquartersCity: row.headquartersCity})'''
# df = pd.DataFrame(graph.run(query))
# df.columns=['id', 'gender']
# print(df.head())
