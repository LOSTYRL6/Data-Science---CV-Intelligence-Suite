# 🚀 Multi-Tool Intelligence Dashboard (Streamlit)

Este repositorio es la culminación de mi especialización en **Data Science & Machine Learning**, integrando tres proyectos avanzados en una única interfaz interactiva desarrollada con **Streamlit**. 

Aquí demuestro mi capacidad para manejar el ciclo completo del dato: desde la extracción y limpieza hasta el modelado predictivo, calibración de negocio y visualización profesional.

---

## 🛠️ Stack Tecnológico
* **Lenguajes:** Python (Pandas, NumPy)
* **Machine Learning:** Scikit-Learn (K-Means, KNN, Random Forest Classifier, PCA)
* **Visualización:** Plotly, Seaborn, Matplotlib, Power BI
* **Despliegue e Interfaz:** Streamlit, Joblib, HTML5/CSS3 (Flexbox Dinámico)

---

## 🎮 Proyecto 1: Recomendador de Videojuegos (Unsupervised ML)
**Objetivo:** Motor de recomendación de precisión que sugiere 5 títulos similares basados en el "ADN" de mecánicas y etiquetas de un juego base.
* **Algoritmos y Modelado:** Enfoque híbrido. Uso de **K-Means** en fase de laboratorio para la estructuración y segmentación macro del catálogo, y búsqueda de proximidad quirúrgica uno a uno mediante **K-Nearest Neighbors (KNN)** en producción.
* **Pipeline de Datos:** Procesamiento de variables categóricas complejas (One-Hot Encoding) y reducción de dimensionalidad con **PCA** (de 400+ a 300 componentes principales) para eliminar ruido estructural y acelerar el cálculo de distancias.
* **Interfaz Avanzada y UI/UX:** * Consumo directo de la CDN oficial de Valve para renderizar de forma dinámica las carátulas oficiales usando los `AppIDs` de Steam.
    * Sistema de **Explainable AI (IA Explicable)** mediante el cálculo de la intersección matemática de conjuntos para aislar y justificar los tags comunes.
    * Inyección de estilos web personalizados (*chips* de etiquetas) utilizando contenedores **Flexbox** adaptativos y paletas cromáticas dinámicas indexadas por funciones hash.

## 💻 Proyecto 2: Dashboard de Mercado de Hardware (BI & Analytics FinTech)
**Objetivo:** Motor de Business Intelligence para analizar la volatilidad de precios en consolas y hardware portátil frente a indicadores macroeconómicos y tasas de cambio internacionales.
* **ETL Avanzada y Conexión de APIs:** Consumo en tiempo real de tipos de cambio oficiales (*OpenExchangeRates API*) con sistemas *fallback* de seguridad, y extracción automatizada de la serie histórica del **CPI (Consumer Price Index)** desde los servidores de la **FRED (Federal Reserve Bank of St. Louis)**.
* **Ingeniería de Datos Financieros:** Procesamiento de series temporales mediante remuestreo mensual (`resample('MS')`) e interpolación lineal de datos distribuidos (`interpolate()`) para estandarizar índices de base 100 desde las fechas de lanzamiento originales.
* **Arquitectura de Reportes en Plotly:**
    1. **Evolución Monetaria:** Análisis de series de tiempo de precios históricos convertidos dinámicamente a Euros (EUR).
    2. **Snapshot de Mercado Actual:** Matriz comparativa del estado de precios actual por consola mediante paletas cromáticas corporativas indexadas.
    3. **Análisis de Poder Adquisitivo:** Gráficos de doble eje (Precio Relativo vs. Inflación Acumulada USA) para rastrear la pérdida o ganancia de valor real frente al coste de la vida.
    4. **Company Intelligence:** Análisis agregado por fabricante (Sony, Microsoft, Nintendo, Valve, ASUS) mediante segmentación semántica de marcas.

## 🎓 Proyecto 3: Predictor de Riesgo y Éxito Académico (Supervised ML)
**Objetivo:** Clasificador preventivo para identificar alumnos en riesgo de exclusión o suspenso a principio de curso.
* **Modelado:** Pipeline de Machine Learning utilizando `StandardScaler` y un **Random Forest Classifier** con balanceo de pesos (`class_weight='balanced'`) para mitigar el fuerte desequilibrio de clases del dataset original (67% aprobados frente a 33% suspensos).
* **Evaluación Científica:** Validación mediante Matriz de Confusión y reporte de clasificación, logrando un **71% de Accuracy global** y un ojo clínico del **94% de Recall** para la detección de perfiles aptos.
* **Lógica de Negocio y Calibración (Mano Dura):** Implementación de un motor de reglas heurísticas personalizado en Streamlit para corregir el sesgo optimista del modelo matemático en "casos esquina" (*edge cases*). Incluye penalizaciones dinámicas calibradas por absentismo crítico, suspensos previos y factores de estilo de vida para garantizar un sistema de alerta temprana de alta fiabilidad en el entorno escolar.
* **Análisis de Impacto:** Gráfico interactivo que desglosa en tiempo real el impacto positivo o negativo de cada variable en la probabilidad de éxito de cada alumno.

---

## 📂 Estructura del Repositorio
* **`app.py`**: El "cerebro" y punto de entrada de la aplicación Streamlit.
* **`Proyecto1/`**: Contiene el laboratorio (`.ipynb`), el dataset de juegos, mapas vectoriales de PCA y el archivo serializado del modelo KNN.
* **`Proyecto2/`**: Scripts de análisis de hardware y archivos de Power BI.
* **`Proyecto3/`**: Dataset académico, notebooks de entrenamiento supervisado y archivo serializado del modelo de bosque (`.pkl`).
* **`views/`**: Carpeta núcleo del despliegue que aloja los scripts ejecutables de Python encargados de renderizar la lógica visual e interactiva de cada aplicación en la interfaz web.

## ⚙️ Instalación y Uso
1. Clonar el repositorio.
2. Instalar las dependencias requeridas.
3. Ejecutar la aplicación localmente:
   ```bash
   streamlit run app.py