import streamlit as st
import pandas as pd
import pickle
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
    # --- RECURSOS PROYECTO 1 (STEAM) ---
    df_steam = pd.read_pickle('./Proyecto1/modelo/datos_steam_con_clusters.pkl')
    knn = joblib.load('./Proyecto1/modelo/modelo_recomendador.joblib')
    pipeline = joblib.load('./Proyecto1/modelo/pipeline_steam.joblib')

    with open('./Proyecto1/modelo/dict_imagenes.pkl', 'rb') as f:
        dict_imgs = pickle.load(f)
    
    # --- RECURSOS PROYECTO 3 (ACADEMIA) ---
    # Cargamos el diccionario que contiene el pipeline y las columnas
    recursos_academia = joblib.load('./Proyecto3/modelo/modelo_predictor_estudiantes.pkl')
    
    # Devolvemos todo en una sola tupla
    return df_steam, knn, pipeline, dict_imgs, recursos_academia

try:
    # Desempaquetamos todos los recursos
    df_steam, knn, pipeline, dict_imgs, recursos_academia = cargar_recursos()
    
    # --- Guardar en Session State para Proyecto 1 ---
    st.session_state['df_steam'] = df_steam
    st.session_state['knn'] = knn
    st.session_state['pipeline'] = pipeline
    st.session_state['dict_imagenes'] = dict_imgs
    
    # --- Guardar en Session State para Proyecto 3 ---
    # Guardamos el diccionario completo (contiene 'modelo' y 'columnas')
    st.session_state['recursos_academia'] = recursos_academia
    
except Exception as e:
    st.error(f"⚠️ Error al cargar los modelos de Steam o Academia: {e}")
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