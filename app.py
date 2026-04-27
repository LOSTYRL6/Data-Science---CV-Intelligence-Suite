import streamlit as st
import pandas as pd
import pickle # <--- Asegúrate de que este import esté arriba
import joblib

# 1. CONFIGURACIÓN
st.set_page_config(
    page_title="Data Science Suite - Portfolio",
    page_icon="🚀",
    layout="wide"
)

# 2. CARGA DE RECURSOS
@st.cache_resource
def cargar_recursos():
    # Cargamos los archivos que ya tenías
    df = pd.read_pickle('./Proyecto1/modelo/datos_steam_con_clusters.pkl')
    knn = joblib.load('./Proyecto1/modelo/modelo_recomendador.joblib')
    pipeline = joblib.load('./Proyecto1/modelo/pipeline_steam.joblib')

    with open('./Proyecto1/modelo/dict_imagenes.pkl', 'rb') as f:
        dict_imgs = pickle.load(f)
    
    return df, knn, pipeline, dict_imgs # <--- Lo devolvemos también

try:
    df_steam, knn, pipeline, dict_imgs = cargar_recursos()
    
    st.session_state['df_steam'] = df_steam
    st.session_state['knn'] = knn
    st.session_state['pipeline'] = pipeline
    st.session_state['dict_imagenes'] = dict_imgs # <--- CLAVE PARA LAS IMÁGENES
    
except Exception as e:
    st.error(f"⚠️ Error al cargar modelos: {e}")
pg = st.navigation({
    "Principal": [
        st.Page("views/inicio.py", title="Inicio", icon="🏠", default=True),
    ],
    "Proyectos": [
        st.Page("views/recomendador.py", title="Recomendador de Juegos", icon="🎮"),
        st.Page("views/hardware.py", title="Mercado Hardware", icon="💻"),
        st.Page("views/estudiante.py", title="Predictor Estudiantil", icon="🎓"),
    ]
})

# 4. SIDEBAR COMÚN
st.sidebar.info("Grandmaster Dev: Tu Nombre/GitHub")

# Ejecución
pg.run()