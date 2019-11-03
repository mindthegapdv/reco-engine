import pandas as pd
import random
import numpy as np
from py2neo import Graph, Node, Relationship
import os

#loads historical orders and participants
df = pd.read_csv("static/orders.csv")
df2 = pd.read_csv('static/participants.csv')

# gets max group size
df_agg = df[['client', 'people']]
df_agg = df_agg.groupby('client').max().reset_index()

# gets members per group
list2=[]
for i in range(len(df_agg)):
    num = df_agg['people'][i]
    for k in range(num): 
        list1 = list(df_agg.iloc[i])
        list1.append(random.randrange(120)+1)
        list2.append(list1)
df3 = pd.DataFrame(list2, columns=['client', 'people', 'id'])
df3.to_csv("static/membership.csv", index=False)

# gets random members per group participating in orders each day
list4 = []
for i in range(len(df)):
    num = df['people'][i]
    list1 = list(df3.loc[df3['client']==df['client'][i]]['id'])
    list2 = random.sample(list1, (num-1))
    for item in list2:
        list3 = list(df.iloc[i])
        list3.append(item)
        list4.append(list3)
df4 = pd.DataFrame(list4, columns=['order_id', 'date', 'time', 'people', 'catering', 'client', 'id'])

df_final = pd.merge(df4, df2, on='id', how='left')
df_final.to_csv("static/final_dataset.csv", index=False)


