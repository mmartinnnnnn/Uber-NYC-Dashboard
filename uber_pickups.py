import streamlit as st
import pandas as pd

st.set_page_config(page_title='Uber NYC', layout='wide')  # config principal de la app

st.title('Viajes de Uber en Nueva York')  # título principal visible en la interfaz
st.caption('Explorá la actividad de recogidas por hora y día de la semana.')

DATE_COLUMN = 'date/time'  # nombre de la columna de fecha y hora en el DataFrame
DATA_URL = (
    'https://s3-us-west-2.amazonaws.com/'
    'streamlit-demo-data/uber-raw-data-sep14.csv.gz'
)

@st.cache_data  # guarda la salida de la función para no volver a cargar datos si se ejecuta otra vez
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)  # lee solo las primeras nrows filas del CSV
    data.columns = [str(column).lower() for column in data.columns]  # normaliza nombres de columnas a minúsculas
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])  # convierte la fecha a formato datetime
    day_names = {
        0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves',
        4: 'Viernes', 5: 'Sábado', 6: 'Domingo',
    }
    data['day_name'] = data[DATE_COLUMN].dt.dayofweek.map(day_names)  # agrega el nombre del día de la semana
    data['hour'] = data[DATE_COLUMN].dt.hour  # extrae la hora del día
    return data


st.sidebar.header('Datos y filtros')  # menú lateral con controles de la app
nrows = st.sidebar.number_input(
    'Filas de la muestra', min_value=10000, max_value=100000,
    step=10000, value=30000, help='Se cargan las primeras filas disponibles del archivo.',
)

with st.spinner('Cargando datos...'):
    try:
        data = load_data(int(nrows))  # carga la cantidad de filas seleccionada por el usuario
    except Exception as error:
        st.error(f'No se pudieron cargar los datos. Revisá tu conexión e intentá nuevamente. ({error})')
        st.stop()

if data.empty:
    st.error('El archivo no devolvió registros para analizar.')
    st.stop()

min_date = data[DATE_COLUMN].min().date()
max_date = data[DATE_COLUMN].max().date()
selected_dates = st.sidebar.date_input(
    'Rango de fechas', value=(min_date, max_date), min_value=min_date, max_value=max_date,
)
if isinstance(selected_dates, tuple):
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
    elif selected_dates:
        start_date = end_date = selected_dates[0]
    else:
        start_date = end_date = min_date
else:
    start_date = end_date = selected_dates

hour_start, hour_end = st.sidebar.slider(
    'Rango horario', min_value=0, max_value=23, value=(0, 23),
)
zone_limit = st.sidebar.slider('Cantidad de zonas a mostrar', 5, 30, 10, step=5)
show_data = st.sidebar.checkbox('Mostrar datos filtrados')  # permite visualizar los datos filtrados

date_mask = data[DATE_COLUMN].dt.date.between(start_date, end_date)
hour_mask = data['hour'].between(hour_start, hour_end)
filtered_data = data[date_mask & hour_mask]  # filtra por las fechas y horas seleccionadas
st.sidebar.caption(
    f'Muestra: primeras {len(data):,} filas cargadas. '
    f'Fechas disponibles: {min_date:%d/%m/%Y} a {max_date:%d/%m/%Y}.'
)

col1, col2, col3, col4 = st.columns(4)  # crea cuatro columnas para métricas
col1.metric('Registros cargados', f'{len(data):,}')  # cantidad total de filas del dataset
col2.metric('Viajes del período', f'{len(filtered_data):,}')
unique_days = filtered_data[DATE_COLUMN].dt.date.nunique()
avg_daily_trips = len(filtered_data) / unique_days if unique_days > 0 else 0
col3.metric('Promedio de viajes por día', f'{avg_daily_trips:,.0f}')
hour_counts = filtered_data['hour'].value_counts().reindex(
    range(hour_start, hour_end + 1), fill_value=0,
).sort_index()
peak_hour = int(hour_counts.idxmax()) if not filtered_data.empty else None
col4.metric('Hora más activa', f'{peak_hour:02d}:00' if peak_hour is not None else 'Sin datos')

st.caption(
    f'Analizando {len(filtered_data):,} de {len(data):,} registros cargados '
    f'({start_date:%d/%m/%Y}–{end_date:%d/%m/%Y}, '
    f'{hour_start:02d}:00–{hour_end:02d}:59). '
    'El promedio diario considera los días con viajes dentro de esta muestra.'
)

overview_tab, map_tab, data_tab = st.tabs(['Resumen', 'Mapa', 'Datos'])

with overview_tab:
    st.subheader('Patrones de actividad')
    st.caption('Cada celda muestra la cantidad de viajes para un día de la semana y una hora.')
    day_order = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    heatmap = filtered_data.pivot_table(
        index='day_name', columns='hour', values=DATE_COLUMN, aggfunc='count', fill_value=0,
    ).reindex(index=day_order, columns=range(hour_start, hour_end + 1), fill_value=0)
    heatmap.columns = [f'{hour:02d}:00' for hour in heatmap.columns]
    st.dataframe(
        heatmap.style.background_gradient(cmap='YlOrRd', axis=None).format('{:,.0f}'),
            width='stretch',
    )

    chart_col1, chart_col2 = st.columns(2)
    day_counts = filtered_data['day_name'].value_counts().reindex(day_order, fill_value=0)
    with chart_col1:
        st.subheader('Viajes por día de la semana')
        st.bar_chart(day_counts)

    with chart_col2:
        st.subheader('Horas más activas')
        top_hours = hour_counts.nlargest(10).sort_values(ascending=True)
        if top_hours.sum() == 0:
            st.info('No hay viajes para el período seleccionado.')
        else:
            top_hours.index = [f'{hour:02d}:00' for hour in top_hours.index]
            st.bar_chart(top_hours, horizontal=True)

    st.subheader(f'{zone_limit} zonas aproximadas con más recogidas')
    st.caption('Las zonas se agrupan por coordenadas redondeadas; no representan límites oficiales de barrios.')
    if filtered_data.empty:
        st.info('No hay zonas para mostrar con los filtros seleccionados.')
    else:
        zone_data = filtered_data.copy()
        zone_data['zona'] = (
            zone_data['lat'].round(2).map(lambda value: f'{value:.2f}') + ', '
            + zone_data['lon'].round(2).map(lambda value: f'{value:.2f}')
        )
        top_zones = zone_data['zona'].value_counts().head(zone_limit).rename_axis('Zona aproximada')
        st.bar_chart(top_zones, horizontal=True)

with map_tab:
    st.subheader('Recogidas en el período seleccionado')
    if filtered_data.empty:
        st.info('No hay viajes para la combinación de filtros seleccionada.')
    else:
        map_data = filtered_data[['lat', 'lon']]
        if len(map_data) > 10000:
            map_data = map_data.sample(10000, random_state=42)
        st.map(map_data)  # muestra los viajes en el mapa
        st.caption(f'{len(map_data):,} puntos en el mapa; {len(filtered_data):,} viajes en el período.')

with data_tab:
    if show_data:
        st.subheader('Datos filtrados')  # sección para ver los datos filtrados si el usuario lo solicita
        st.dataframe(filtered_data.head(1000), use_container_width=True)  # muestra hasta 1000 filas para no saturar la vista
    else:
        st.info('Activá “Mostrar datos filtrados” en el panel lateral para ver la tabla.')

