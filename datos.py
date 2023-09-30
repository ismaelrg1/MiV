import numpy as np
import pandas as pd
import calmap
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


import datetime as dt
from datetime import datetime


df = pd.read_csv('data.csv')
gb = df.keys()


print(gb)
# print(df['NK_Any'])

data = pd.DataFrame()
#
# #Importing the seaborn library along with other dependencies

# # Creating new features from the data


eventos_por_dia = df.groupby(['Descripcio_dia_setmana', 'Mes_any', 'Dia_mes'])['Numero_expedient'].count().reset_index()
# print(eventos_por_dia)


plt.figure(figsize = (20,10))
#
# calmap.yearplot(eventos_por_dia['Numero_expedient'], cmap='YlGn', fillcolor='lightgrey',daylabels='MTWTFSS',dayticks=[0, 2, 4, 6], linewidth=2)

# print(eventos_por_dia["Mes_any"])

# data['Fecha'] = eventos_por_dia["Mes_any"].str.cat(eventos_por_dia['Dia_mes'], sep= "-")
data['Fecha'] = '2022-' + eventos_por_dia["Mes_any"].astype(str) + '-' + eventos_por_dia['Dia_mes'].astype(str)
#print(data['Fecha'])
data['Fecha'] = pd.to_datetime(list(data['Fecha']))
data['Evento'] = eventos_por_dia["Numero_expedient"]

events = pd.Series(list(data['Evento']), index=list(data["Fecha"]))
#print(events)
# print(data["Evento"])

fig, ax = calmap.calendarplot(events)

# Añadir un título
plt.title('Mapa de Calor de Eventos', fontsize=16)

fig.colorbar(ax[0].get_children()[1], ax=ax.ravel().tolist(), orientation='horizontal')

# Mostrar el mapa de calor
plt.show()


import plotly.express as px

test = df.groupby(['Longitud', 'Latitud'])
eventos_por_calle = df.groupby(["Nom_carrer"])['Numero_expedient'].count().reset_index()
eventos_por_calle["Longitud"] = df.groupby(["Nom_carrer"],as_index=False)['Longitud']
prueba = df.groupby(["Nom_carrer"],as_index=False).first()
print(prueba)
eventos_por_calle["Latitud"] = df.groupby(["Nom_carrer"],as_index=False)['Latitud']
print(eventos_por_calle["Latitud"])

fig = px.density_mapbox(df, lat = 'Latitud', lon = 'Longitud',
                        radius = 8,
                        center = dict(lat = 41.39, lon = 2.16),
                        zoom = 12,
                        mapbox_style = 'open-street-map')

fig.show()



