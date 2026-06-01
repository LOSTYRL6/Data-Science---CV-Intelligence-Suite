import streamlit as st
import pandas as pd
import pickle
import joblib

st.set_page_config(
    page_title="Data Science Suite - Portfolio",
    page_icon="🚀",
    layout="wide"
)

@st.cache_resource
def cargar_recursos():
    df_steam = pd.read_pickle('./Proyecto1/modelo/datos_steam_con_clusters.pkl')
    knn = joblib.load('./Proyecto1/modelo/modelo_recomendador.joblib')
    pipeline = joblib.load('./Proyecto1/modelo/pipeline_steam.joblib')

    with open('./Proyecto1/modelo/dict_imagenes.pkl', 'rb') as f:
        dict_imgs = pickle.load(f)

    recursos_academia = joblib.load('./Proyecto3/modelo/modelo_predictor_estudiantes.pkl')
    
    return df_steam, knn, pipeline, dict_imgs, recursos_academia

try:
    df_steam, knn, pipeline, dict_imgs, recursos_academia = cargar_recursos()

    st.session_state['df_steam'] = df_steam
    st.session_state['knn'] = knn
    st.session_state['pipeline'] = pipeline
    st.session_state['dict_imagenes'] = dict_imgs

    st.session_state['recursos_academia'] = recursos_academia
    
except Exception as e:
    st.error(f"⚠️ Error al cargar los modelos de Steam o Academia: {e}")
pg = st.navigation({
    "Principal": [
        st.Page("views/Inicio.py", title="Inicio", icon="🏠", default=True),
    ],
    "Proyectos": [
        st.Page("views/recomendadores.py", title="Recomendador de Juegos", icon="🎮"),
        st.Page("views/hardwars.py", title="Mercado Hardware", icon="💻"),
        st.Page("views/estudiantess.py", title="Predictor Estudiantil", icon="🎓"),
    ]
})
pg.run()