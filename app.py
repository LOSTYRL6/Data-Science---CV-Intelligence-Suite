import streamlit as st

st.set_page_config(
    page_title="Data Science Suite - Portfolio",
    page_icon="🚀",
    layout="wide"
)
st.sidebar.title("🎮 Menú Principal")
st.sidebar.markdown("---")

opcion = st.sidebar.radio(
    "Selecciona un Proyecto:",
    ["Inicio", "Recomendador de Juegos", "Mercado Hardware", "Predictor Estudiantil"]
)

st.sidebar.markdown("---")
st.sidebar.info("Grandmaster Dev: Tu Nombre/GitHub")

if opcion == "Inicio":
    st.title("🚀 Bienvenidos a mi Suite de Data Science")
    st.markdown("""
    Este dashboard integra mis tres proyectos estrella desarrollados tras mi especialización en **Machine Learning**. 
    Usa el menú de la izquierda para navegar por las diferentes aplicaciones.
    """)
    

elif opcion == "Recomendador de Juegos":
    st.title("🎮 Recomendador de Videojuegos")
    st.write("Aquí irá tu lógica de ML No Supervisado (K-Means).")
    
elif opcion == "Mercado Hardware":
    st.title("💻 Análisis de Mercado Hardware")
    st.write("Visualización de precios y comparación de stock (Power BI / Pandas).")

elif opcion == "Predictor Estudiantil":
    st.title("🎓 Predictor de Éxito Académico")
    st.write("Modelo predictivo basado en Machine Learning Supervisado.")