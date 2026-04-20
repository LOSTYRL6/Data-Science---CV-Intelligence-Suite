# 🚀 Multi-Tool Intelligence Dashboard (Streamlit)

Este repositorio es la culminación de mi especialización en **Data Science & Machine Learning**, integrando tres proyectos avanzados en una única interfaz interactiva desarrollada con **Streamlit**. 

Aquí demuestro mi capacidad para manejar el ciclo completo del dato: desde la extracción y limpieza hasta el modelado predictivo y la visualización profesional.

---
## 🛠️ Stack Tecnológico
**Lenguajes:** Python (Pandas, Numpy)  
**Machine Learning:** Scikit-Learn (K-Means, KNN, Random Forest, PCA)  
**Visualización:** Plotly, Seaborn, Matplotlib, Power BI  
**Despliegue:** Streamlit

---

## 🎮 Proyecto 1: Recomendador de Videojuegos (Unsupervised ML)
**Objetivo:** Motor de recomendación que sugiere 5 títulos similares basados en ADN de juego (géneros, categorías y tags).
* **Algoritmos:** Clustering con **K-Means** y búsqueda de proximidad con **K-Nearest Neighbors (KNN)**.
* **Feature Engineering:** Procesamiento de variables categóricas mediante One-Hot Encoding y reducción de 400+ dimensiones a 300 componentes principales con **PCA**.
* **Visualización:** Gráfico 3D interactivo en **Plotly** representando la segmentación de los clusters.

## 💻 Proyecto 2: Dashboard de Mercado de Hardware (BI & Analytics)
**Objetivo:** Análisis de volatilidad de precios en GPUs y consolas vs. indicadores macroeconómicos.
* **Proceso ETL:** Consumo de APIs y limpieza de datos para análisis histórico.
* **Business Intelligence:** Integración de **Power BI** para dashboards dinámicos con DAX y filtros avanzados.
* **Ética de Datos:** Implementación de buenas prácticas en Web Scraping y privacidad.

## 🎓 Proyecto 3: Predictor de Éxito Académico (Supervised ML)
**Objetivo:** Clasificador científico para predecir el rendimiento estudiantil.
* **Modelado:** Comparativa entre **Regresión Logística y Random Forest** para optimizar el F1-Score.
* **EDA:** Análisis de correlación multivariable mediante Heatmaps para identificar predictores clave (sueño, estudio, conectividad).

---

## 📂 Estructura del Repositorio
* **`app.py`**: El "cerebro" y punto de entrada de la aplicación Streamlit.
* **`Proyecto1/`**: Contiene el laboratorio (`.ipynb`), el dataset de juegos y el modelo entrenado.
* **`Proyecto2/`**: Scripts de análisis de hardware y archivos de Power BI.
* **`Proyecto3/`**: Dataset académico y notebooks de entrenamiento supervisado.

## ⚙️ Instalación y Uso
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt` (Próximamente).
3. Ejecutar: `streamlit run app.py`