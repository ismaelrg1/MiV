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
# print(df['Hora_dia'])

data = pd.DataFrame()

#
# eventos_por_dia = df.groupby(['Descripcio_dia_setmana', 'Mes_any', 'Dia_mes'])['Numero_expedient'].count().reset_index()
# # print(eventos_por_dia)
#
#
# plt.figure(figsize = (20,10))
#
# data['Fecha'] = '2022-' + eventos_por_dia["Mes_any"].astype(str) + '-' + eventos_por_dia['Dia_mes'].astype(str)
# data['Fecha'] = pd.to_datetime(list(data['Fecha']))
# data['Evento'] = eventos_por_dia["Numero_expedient"]
#
# events = pd.Series(list(data['Evento']), index=list(data["Fecha"]))
# print(events)
# # print(data["Evento"])
#
# fig, ax = calmap.calendarplot(events)
#
# # Añadir un título
# plt.title('Mapa de Calor de Eventos', fontsize=16)
#
# fig.colorbar(ax[0].get_children()[1], ax=ax.ravel().tolist(), orientation='horizontal')
#
# # Mostrar el mapa de calor
# plt.show()

###########################################################################
# import plotly.express as px
#
# test = df.groupby(['Longitud', 'Latitud'])
# eventos_por_calle = df.groupby(["Nom_carrer"])['Numero_expedient'].count().reset_index()
# eventos_por_calle["Longitud"] = df.groupby(["Nom_carrer"],as_index=False)['Longitud']
# prueba = df.groupby(["Nom_carrer"],as_index=False).first()
# eventos_por_calle["Latitud"] = df.groupby(["Nom_carrer"],as_index=False)['Latitud']
#
#
# fig = px.density_mapbox(df, lat = 'Latitud', lon = 'Longitud',
#                         radius = 8,
#                         center = dict(lat = 41.39, lon = 2.16),
#                         zoom = 12,
#                         mapbox_style = 'open-street-map')
#
# fig.show()
#


##############################################
import seaborn as sns

data = pd.DataFrame()


semana_por_hora = df.groupby(['Descripcio_dia_setmana', "Hora_dia"])['Numero_expedient'].count().reset_index()


days = {"Dilluns": 0, "Dimarts": 1,"Dimecres": 2,"Dijous": 3,"Divendres": 4,"Dissabte": 5,"Diumenge": 6}

plt.figure(figsize = (20,10))



semana_por_hora['Descripcio_dia_setmana'] = semana_por_hora["Descripcio_dia_setmana"].apply(lambda x: days[x])
# print(semana_por_hora)

out = semana_por_hora.groupby(['Descripcio_dia_setmana', "Hora_dia"])['Numero_expedient'].mean().unstack()
print(out)



sns.heatmap(out, cmap ='coolwarm',linewidths=1)


# xticks defines the Y-axes' labels
xticks_labels=['12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM']

plt.xticks(np.arange(24) + .5, labels=xticks_labels)

yticks_labels=['Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres', 'Disabte', 'Diumenge']
plt.yticks(np.arange(7) + .5, labels=yticks_labels)


plt.title("Traffic over the day")
plt.show()