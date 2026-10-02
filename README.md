# 🚕 NYC Uber Rides Dashboard

Dashboard interactivo desarrollado en **Python** y **Streamlit** para la exploración y visualización de solicitudes de viajes de Uber en la ciudad de Nueva York (Septiembre de 2014).

🚀 **Demo en vivo:** [Probar Dashboard Interactivo](https://nyc-uber-dashboard.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat&logo=pandas&logoColor=white)

---

## 📌 Descripción General
*
Esta aplicación web interactiva permite analizar la distribución espacio-temporal de los viajes de Uber en NYC. El objetivo es identificar **patrones de demanda por hora del día y día de la semana**, visualizar la **concentración geográfica** de viajes en un mapa interactivo y consultar métricas agregadas en tiempo real a través de un panel organizado en pestañas.
---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python
- **Análisis y Manipulación de Datos:** Pandas
- **Framework Web / Dashboard:** Streamlit
- **Optimización:** Decoradores de caché (`@st.cache_data`) para la carga eficiente en memoria y submuestreo de puntos geoespaciales.

---

## ⚙️ Funcionalidades del Dashboard

- **Métricas Generales (KPIs):**
  - Registros cargados en la muestra.
  - Viajes del período filtrado.
  - Promedio de viajes por día.
  - Hora pico de actividad.
- **Filtro Lateral Dinámico:**
  - Selección de la **muestra de filas** a procesar (10.000 a 100.000).
  - Selector de **rango de fechas** disponible.
  - Selector de **rango horario** (0 a 23 hs).
  - Control de **zonas con más recogidas** a visualizar.
- **Pestañas de Análisis (`st.tabs`):**
  - **Resumen:** Matriz de calor (heatmap) interactiva por día y hora, gráficos de barras por día de la semana, top de horas más activas y top de zonas aproximadas con más recogidas.
  - **Mapa:** Mapa geoespacial interactivo optimizado con renderizado dinámico de puntos de recogida.
  - **Datos:** Opción para inspeccionar y explorar la tabla de datos filtrados.

---

## 📊 Fuente de Datos

El dataset proviene del repositorio de datos públicos de prueba de Streamlit (`uber-raw-data-sep14.csv.gz`), el cual contiene registros con marcas de tiempo (`date/time`), latitud (`lat`), longitud (`lon`) y base operativa (`base`).

---

## 🚀 Cómo Ejecutar Localmente

### 1. Clona el repositorio
```bash
git clone https://github.com/mmartinnnnnn/Uber-NYC-Dashboard.git
cd Uber-NYC-Dashboard
```

### 2. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecuta la aplicación
```bash
streamlit run uber_pickups.py
```
