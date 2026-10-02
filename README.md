# 🚕 NYC Uber Rides Dashboard

Dashboard interactivo desarrollado en **Python** y **Streamlit** para la exploración y visualización de solicitudes de viajes de Uber en la ciudad de Nueva York (Septiembre de 2014).

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat&logo=pandas&logoColor=white)

---

## 📌 Descripción General

Esta aplicación web interactiva permite analizar la distribución espacio-temporal de los viajes de Uber en NYC. El objetivo es identificar **patrones de demanda por hora del día y día de la semana**, visualizar la **concentración geográfica** de viajes en un mapa interactivo y consultar métricas agregadas en tiempo real.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python
- **Análisis y Manipulación de Datos:** Pandas
- **Framework Web / Dashboard:** Streamlit
- **Optimización:** Decoradores de caché de Streamlit (`@st.cache_data`) para la carga eficiente de datos en memoria.

---

## ⚙️ Funcionalidades del Dashboard

- **Métricas Generales (KPIs):** Visualización instantánea del total de viajes cargados, promedio de viajes por hora, hora pico y día de mayor actividad.
- **Filtro Lateral Dinámico:**
  - Selección interactiva de la **cantidad de filas** a procesar (30.000 a 50.000).
  - Filtrado de viajes por **hora del día** (0 a 23 hs).
  - Filtrado por **día de la semana** (lunes a domingo o vista consolidada).
- **Mapa Geoespacial:** Representación gráfica de la densidad de recogidas según la hora y el día seleccionados.
- **Gráfico de Barras Temporal:** Distribución del volumen de viajes por hora.
- **Inspección de Datos:** Opción para explorar el dataset crudo (*raw data*).

---

## 📊 Fuente de Datos

El dataset proviene del repositorio de datos públicos de prueba de Streamlit (`uber-raw-data-sep14.csv.gz`), el cual contiene registros con marcas de tiempo (`date/time`), latitud (`lat`), longitud (`lon`) y base operativa (`base`).

---

## 🚀 Cómo Ejecutar Localmente

### 1. Clona el repositorio
```bash
git clone [https://github.com/mmartinnnnnn/Uber-NYC-Dashboard.git](https://github.com/mmartinnnnnn/Uber-NYC-Dashboard.git)
cd Uber-NYC-Dashboard
