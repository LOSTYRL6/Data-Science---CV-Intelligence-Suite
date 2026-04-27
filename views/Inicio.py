import streamlit as st
import base64

# Configuración de página (asegúrate de que sea la primera línea de Streamlit)
st.set_page_config(page_title="Data Science Suite", layout="wide")

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Intentar cargar la imagen de fondo
try:
    img = get_base64("Image/fondo3.gif")
except:
    img = "" # Fallback si no encuentra la imagen

# --- BLOQUE DE ESTILO CSS PREMIUM ---
st.markdown(f"""
    <style>
    /* 1. Fondo con degradado y GIF */
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                          url("data:image/gif;base64,{img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* 2. Reducir espacio superior del Header */
    .block-container {{
        padding-top: 2rem !important;
    }}
    .card{{
        padding: 20px; 
        border-radius: 15px 15px 0 0;
        height: 250px;
        border: solid 1px black;
        transition: all 0.5s;
    }}
    .card:hover {{
        transform: scale(1.03s);
    }}
 /* Efectos de Hover: Borde completo de color + Borde izquierdo más grueso */
    .card-videojuegos:hover {{
        border: 1px solid #FF4B4B !important; 
        border-left: 8px solid #FF4B4B !important; /* Engrosamos un poco el borde izquierdo al pasar el mouse */
        transform: scale(1.05); 
    }}
    
    .card-hardware:hover {{
        border: 1px solid #00CC96 !important; 
        border-left: 8px solid #00CC96 !important; 
        transform: scale(1.05); 
    }}
    
    .card-estudiantil:hover {{
        border: 1px solid #636EFA !important; 
        border-left: 8px solid #636EFA !important; 
        transform: scale(1.05); 
    }}

    /* El efecto Active es el "clic" físico (el hundimiento) */
    .custom-card:active {{
        transform: scale(0.95) rotateZ(1.7deg);
    }}

    /* 3. Efecto Cristal (Glassmorphism) en contenedores */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: rgba(38, 39, 48, 0.4) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
    }}
    
    /* 4. Animación Hover en las tarjetas */
    [data-testid="column"] {{
        transition: transform 0.3s ease-in-out !important;
    }}
    
    [data-testid="column"]:hover {{
        transform: scale(1.03);
    }}

    /* 5. Ajuste de botones para fusión perfecta */
    div.stButton > button {{
        margin-top: 7.5px !important;
        border-top-left-radius: 0px !important;
        border-top-right-radius: 0px !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: 0.3s;
    }}
    
    div.stButton > button:hover {{
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- CONTENIDO DE LA PÁGINA ---

izq, centro, der = st.columns([1, 8, 1])

with centro:
    # Título con degradado moderno
    st.markdown("""
        <h1 style='text-align: center; 
                   background: linear-gradient(90deg, #FF4B4B, #636EFA);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-size: 3.5rem;
                   font-weight: 800;
                   margin-bottom: 0px;'>
            Suite de Data Science
        </h1>
        <p style='text-align: center; color: #808495; font-size: 1.2rem; margin-bottom: 40px;'>
            Explora modelos inteligentes de recomendación y predicción técnica
        </p>
    """, unsafe_allow_html=True)

    # Contenedor de proyectos
    with st.container(border=True):
        st.markdown("<h2 style='text-align: center; color: white;'>🎮 Mis Proyectos Principales</h2>", unsafe_allow_html=True)
        st.write("\n")

        col1, col2, col3 = st.columns(3)

        # --- PROYECTO 1: VIDEOJUEGOS ---
        with col1:
            st.markdown("""
                <div class="card card-videojuegos" style="background-color: rgba(255, 75, 75, 0.15); 
                            border-left: 5px solid #FF4B4B;">
                    <h4 style="margin-top: 0; color: white;">Videojuegos</h4>
                    <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">Sistema inteligente de recomendación usando KNN y PCA.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Acceder al Recomendador 🎮", key="btn_videojuegos", use_container_width=True):
                st.switch_page("views/recomendador.py")

        # --- PROYECTO 2: HARDWARE ---
        with col2:
            st.markdown("""
                <div class="card card-hardware" style="background-color: rgba(0, 204, 150, 0.15); 
                            border-left: 5px solid #00CC96; ">
                    <h4 style="margin-top: 0; color: white;">Hardware</h4>
                    <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">Análisis predictivo de precios y stock de componentes.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Analizar Mercado 💻", key="btn_hardware", use_container_width=True):
                st.switch_page("views/hardware.py")

        # --- PROYECTO 3: ESTUDIANTIL ---
        with col3:
            st.markdown("""
                <div class="card card-estudiantil" style="background-color: rgba(99, 110, 250, 0.15); 
                            border-left: 5px solid #636EFA">
                    <h4 style="margin-top: 0; color: white;">Estudiantil</h4>
                    <p style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">Clasificación y predicción de éxito académico.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Predecir Éxito 🎓", key="btn_estudiante", use_container_width=True):
                st.switch_page("views/estudiante.py")

    st.write("\n")
    st.info("💡 Usa el menú de la izquierda para explorar cada modelo de forma detallada.")