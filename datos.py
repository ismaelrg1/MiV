import numpy as np
import pandas as pd
import calmap
import matplotlib.pyplot as plt


##############Accidentes según causa conductor gestionados por la Guàrdia Urbana a la ciutat de Barcelona

# Lectura de datos
df = pd.read_csv('data.csv')
gb = df.keys()

data = pd.DataFrame()
plt.figure(figsize = (20,10))


# Primera grafica
############################################

# Contar los accidentes que han sucedido cada dia
eventos_por_dia = df.groupby(['Descripcio_dia_setmana', 'Mes_any', 'Dia_mes'])['Numero_expedient'].count().reset_index()

data['Fecha'] = '2022-' + eventos_por_dia["Mes_any"].astype(str) + '-' + eventos_por_dia['Dia_mes'].astype(str)
data['Fecha'] = pd.to_datetime(list(data['Fecha']))
data['Evento'] = eventos_por_dia["Numero_expedient"]

# Crear un dataframe con indice la fecha y valor la cantidad de accidentes de ese dia
events = pd.Series(list(data['Evento']), index=list(data["Fecha"]))

# Creacion del mapa
ax = calmap.yearplot(events,cmap='BuGn',year=2022, vmin= 25,daylabels='MTWTFSS', dayticks=[0, 2, 4, 6])

# Añadir un título
plt.title('Accidentes gestionados por la Guàrdia Urbana a la ciutat de Barcelona', fontsize=27)

# Ajustes de posicion y tamaño del texto
ax.set_yticklabels(ax.get_yticklabels(), fontsize=20)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=20, y=0.3)
ax.set_ylim(-5,10)

# Crear la legenda del mapa de calor
colorbar = plt.cm.ScalarMappable(cmap='BuGn', norm=plt.Normalize(vmin=25, vmax=events.max()))
colorbar.set_array([])

plt.colorbar(colorbar, ax=ax, orientation='horizontal', pad=0.02)

# Añadir el año en el lateral
plt.text(-1, 3.5, '2022', fontsize=50, rotation='vertical', va='center', ha='center')

# Mostrar el mapa de calor
plt.show()


# Segunda grafica
##########################################################################
import plotly.express as px

data = df.copy()

# Juntamos las columna para hacer una columan con la fecha y hora
data['Time'] = pd.to_datetime(df[['NK_Any','Mes_any', 'Dia_mes', 'Hora_dia']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')
data = data.drop(columns=['NK_Any','Mes_any', 'Dia_mes', 'Hora_dia'])

# Crear el mapa
fig = px.scatter_mapbox(data, lat = 'Latitud', lon = 'Longitud',
                        center = dict(lat = 41.39, lon = 2.16),
                        zoom = 12,
                        size_max = 0.1,
                        color_discrete_sequence=['blue'],
                        mapbox_style = 'open-street-map',
                        hover_name='Descripcio_causa_mediata',
                        custom_data=['Time', 'Nom_barri', 'Nom_carrer', 'Num_postal ']
                        )
# Personaliza la etiqueta de información (tooltip)
fig.update_traces(
    hovertemplate='<br>'.join([
        '<b>Causa: %{hovertext}</b>',
        '',
        'Fecha: %{customdata[0]:%Y-%m-%d}',
        'Barrio: %{customdata[1]}',
        'Calle: %{customdata[2]}',
        'CP: %{customdata[3]}'
    ]),
    hoverlabel=dict(
        bgcolor='lightblue',  # Color de fondo del tooltip
        font=dict(color='black')  # Color del texto en el tooltip
    )
)


fig.show()


# Tercera grafica
##############################################
import seaborn as sns

# Agrupar datos por hora y semana
semana_por_hora = df.groupby(['Descripcio_dia_setmana', "Hora_dia"])['Numero_expedient'].count().reset_index()


days = {"Dilluns": 0, "Dimarts": 1,"Dimecres": 2,"Dijous": 3,"Divendres": 4,"Dissabte": 5,"Diumenge": 6}

plt.figure(figsize = (20,10))

# Cambiamos los dias de la semana de nombre a numeros
semana_por_hora['Descripcio_dia_setmana'] = semana_por_hora["Descripcio_dia_setmana"].apply(lambda x: days[x])

# Contamos la media de accidentes que hay por semana a cada hora
out = semana_por_hora.groupby(["Hora_dia", 'Descripcio_dia_setmana'])['Numero_expedient'].mean().unstack()

# Creamos el mapa
ax = sns.heatmap(out, cmap ='coolwarm', annot=True, fmt="")


# Definimos los ylabels y xlabels
yticks_labels=['12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM']

plt.yticks(np.arange(24) + .5, labels=yticks_labels, rotation=45)

xticks_labels=['Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres', 'Disabte', 'Diumenge']
plt.xticks(np.arange(7) + .5, labels=xticks_labels)

# Titulo
titulo = "Media de accidentes gestionados por la Guàrdia Urbana a la ciutat de Barcelona en 2022"
plt.title(titulo, fontsize=16)

plt.show()