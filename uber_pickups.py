import streamlit as st
import pandas as pd

st.set_page_config(page_title='Uber NYC', layout='wide')  # config principal de la app

st.title('Pedidos de Uber en NYC')  # título principal visible en la interfaz

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
    data['day_name'] = data[DATE_COLUMN].dt.day_name()  # agrega el nombre del día de la semana
    data['hour'] = data[DATE_COLUMN].dt.hour  # extrae la hora del día
    return data


data_load_state = st.text('Cargando datos...')  # mensaje mientras carga el dataset
nrows = st.sidebar.number_input('Cantidad de filas a cargar', min_value=30000, max_value=50000, step=2000, value=30000)
data = load_data(int(nrows))  # carga la cantidad de filas seleccionada por el usuario
data_load_state.text('¡Listo! (usando st.cache_data)')  # actualiza el mensaje cuando termina la carga

st.sidebar.header('Filtros')  # menú lateral con controles de la app
hour_to_filter = st.sidebar.slider('Hora del día', 0, 23, 17)  # selector de hora para filtrar viajes
selected_day = st.sidebar.selectbox('Día de la semana', ['Todos', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
show_raw_data = st.sidebar.checkbox('Mostrar datos brutos')  # permite visualizar el DataFrame completo

if selected_day == 'Todos':
    filtered_data = data[data['hour'] == hour_to_filter]  # filtra por la hora seleccionada
else:
    filtered_data = data[(data['hour'] == hour_to_filter) & (data['day_name'] == selected_day)]

col1, col2, col3, col4 = st.columns(4)  # crea cuatro columnas para métricas
col1.metric('Total de viajes', len(data))  # cantidad total de filas del dataset
col2.metric('Promedio por hora', round(len(data) / 24, 1))  # promedio de viajes por hora
col3.metric('Hora pico', data['hour'].value_counts().idxmax())  # hora con más viajes
col4.metric('Día más activo', data['day_name'].value_counts().idxmax())  # día con más viajes

st.subheader(f'Mapa de viajes a las {hour_to_filter}:00')  # título del mapa con la hora actual
st.map(filtered_data)  # muestra los viajes en el mapa

st.subheader('Cantidad de viajes por hora')  # gráfico con la distribución por hora
hour_counts = data['hour'].value_counts().sort_index()  # cuenta el número de viajes por cada hora
st.bar_chart(hour_counts)  # dibuja el gráfico de barras

if show_raw_data:
    st.subheader('Datos brutos')  # sección para ver los datos completos si el usuario lo solicita
    st.write(data.head(1000))  # muestra solo las primeras 1000 filas para no saturar la vista

