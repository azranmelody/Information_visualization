import numpy as np
import pandas as pd

import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

sheet_name="נתוני סקר תיירות נכנסת 2019"
filepath = r"C:\Users\Anon\Downloads\Dataset-30-11-21.csv"
#Read file and select columns
df = pd.read_csv(filepath,encoding= 'unicode_escape',
                 usecols=["Q date", "Country name","WHAT WAS THE  PRINCIPAL TYPE OF ACCOMMODATION YOU USED  IN ISRAEL:","AGE GROUP: yourself (age):" , "Overall satisfaction" , "value for money"])
df.columns =["date","country","trip_type","age_group","satisfaction","value_for_money"]

#Drop NONE values
df=df.dropna()

#convert columns to int
df['trip_type']  = df['trip_type'].astype('int')
df['age_group']  = df['age_group'].astype('int')
df['satisfaction']  = df['satisfaction'].astype('int')
df['value_for_money']  = df['value_for_money'].astype('int')

#Preprocessing
df.loc[(df['country'] == 'United States of America (USA)'),'country'] = 'USA'
df.loc[(df['country'] == 'Russian Federation'),'country'] = 'Russia'
df.loc[(df['trip_type'] == 1),'trip_type'] = 'Holiday, leisure, recreation'
df.loc[(df['trip_type'] == 2),'trip_type'] = 'Touring and sightseeing'
df.loc[(df['trip_type'] == 3),'trip_type'] = 'Religious tour, pilgrimage'
df.loc[(df['trip_type'] == 4),'trip_type'] = 'Visit friends and relatives'
df.loc[(df['trip_type'] == 5),'trip_type'] = 'Congresses/fairs/conferences/exhibition'
df.loc[(df['trip_type'] == 6),'trip_type'] = 'Business'
df.loc[(df['trip_type'] == 7),'trip_type'] = 'Medical treatment'
df.loc[(df['trip_type'] == 8),'trip_type'] = 'Study and research'
df.loc[(df['trip_type'] == 9),'trip_type'] = 'other'



df.loc[(df['age_group'] == 1),'age_group'] = '0-15'
df.loc[(df['age_group'] == 2),'age_group'] = '16-24'
df.loc[(df['age_group'] == 3),'age_group'] = '25-34'
df.loc[(df['age_group'] == 4),'age_group'] = '35-44'
df.loc[(df['age_group'] == 5),'age_group'] = '45-54'
df.loc[(df['age_group'] == 6),'age_group'] = '55-64'
df.loc[(df['age_group'] == 7),'age_group'] = '65+'




df['date']=pd.to_datetime(df["date"])


df = df.sort_values(by=['date'], ascending=True)
df['date']=df['date'].dt.strftime('%d/%m/%Y')
df['month'] = df['date'].apply(lambda s:s.split('/')[1])
df = df.reset_index(drop=True)

heatmap = pd.pivot_table(data=df,index=['country'],columns=["month"],values=["satisfaction"],aggfunc=[np.mean])
heatmap = heatmap.round(1)

months = list(dict.fromkeys(df['month'].tolist()))
heatmap.columns=months
# _r reverses the normal order of the color map 'RdYlGn'
sns.heatmap(heatmap, cmap='RdYlGn', xticklabels=True, yticklabels=True, annot=False)
plt.show()



fig = px.choropleth(df, locations="country",
                    color=(df["satisfaction"]),
                    hover_name="country",
                    hover_data=['satisfaction','value_for_money'],
                    locationmode="country names",
                    animation_frame='month',
                    color_continuous_midpoint = 3,
color_continuous_scale=px.colors.diverging.RdYlGn)
fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor="white",height= 700,title_text = 'Visiting Israel by trip type at 2019',font_size=18)
fig.show()
print(df)




