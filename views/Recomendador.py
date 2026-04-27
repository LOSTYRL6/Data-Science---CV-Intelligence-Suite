import streamlit as st

# 1. Recuperamos los datos y modelos de la sesión (cargados en el archivo principal)
df_steam = st.session_state.get('df_steam')
knn = st.session_state.get('knn')
pipeline = st.session_state.get('pipeline')
dict_imagenes = st.session_state.get('dict_imagenes', {}) # Diccionario de AppIDs

# Paleta de 30 colores para las etiquetas
COLORES_TAGS = [
    ("rgba(0, 204, 150, 0.15)", "#00CC96"), ("rgba(99, 110, 250, 0.15)", "#636EFA"),
    ("rgba(255, 75, 75, 0.15)", "#FF4B4B"), ("rgba(255, 161, 90, 0.15)", "#FFA15A"),
    ("rgba(171, 71, 188, 0.15)", "#AB47BC"), ("rgba(0, 191, 255, 0.15)", "#00BFFF"),
    ("rgba(238, 255, 65, 0.15)", "#EEFF41"), ("rgba(255, 105, 180, 0.15)", "#FF69B4"),
    ("rgba(255, 215, 0, 0.15)", "#FFD700"), ("rgba(64, 224, 208, 0.15)", "#40E0D0"),
    ("rgba(127, 255, 0, 0.15)", "#7FFF00"), ("rgba(255, 0, 255, 0.15)", "#FF00FF"),
    ("rgba(0, 255, 255, 0.15)", "#00FFFF"), ("rgba(138, 43, 226, 0.15)", "#8A2BE2"),
    ("rgba(240, 230, 140, 0.15)", "#F0E68C"), ("rgba(255, 127, 80, 0.15)", "#FF7F50"),
    ("rgba(0, 250, 154, 0.15)", "#00FA9A"), ("rgba(186, 85, 211, 0.15)", "#BA55D3"),
    ("rgba(255, 20, 147, 0.15)", "#FF1493"), ("rgba(30, 144, 255, 0.15)", "#1E90FF"),
    ("rgba(0, 255, 127, 0.15)", "#00FF7F"), ("rgba(218, 112, 214, 0.15)", "#DA70D6"),
    ("rgba(255, 160, 122, 0.15)", "#FFA07A"), ("rgba(173, 255, 47, 0.15)", "#ADFF2F"),
    ("rgba(75, 0, 130, 0.15)", "#4B0082"), ("rgba(250, 128, 114, 0.15)", "#FA8072"),
    ("rgba(124, 252, 0, 0.15)", "#7CFC00"), ("rgba(221, 160, 221, 0.15)", "#DDA0DD"),
    ("rgba(0, 206, 209, 0.15)", "#00CED1"), ("rgba(255, 69, 0, 0.15)", "#FF4500")
]

# Función para encontrar etiquetas comunes
def obtener_coincidencias(df, juego_usuario, juego_recomendado):
    tags_u = set(df.columns[(df.loc[juego_usuario] == 1)])
    tags_r = set(df.columns[(df.loc[juego_recomendado] == 1)])
    
    def normalizar(t):
        return t.lower().replace("-", "").replace(" ", "")

    mapa_bonito = {normalizar(t): t for t in tags_r}
    tags_u_clean = {normalizar(t) for t in tags_u}
    tags_r_clean = set(mapa_bonito.keys())
    
    comunes_clean = tags_u_clean.intersection(tags_r_clean)
    return [mapa_bonito[t] for t in comunes_clean]

# --- INTERFAZ ---
st.title("🎮 Recomendador de Videojuegos")
st.markdown("Escribe tu juego favorito y descubre nuevas joyas basadas en sus etiquetas y mecánicas.")

if df_steam is not None:
    busqueda = st.selectbox(
        "Busca un juego...", 
        options=df_steam.index,
        index=None, 
        placeholder="Ej: Counter-Strike, Portal 2..."
    )

    if busqueda:
        if st.button("✨ ¡Recomiéndame!"):
            # Transformación de datos
            datos_crudos = df_steam.loc[[busqueda]].drop(columns=['cluster'], errors='ignore')
            datos_scaled = pipeline.named_steps['standardscaler'].transform(datos_crudos)
            datos_transformados = pipeline.named_steps['pca'].transform(datos_scaled)
            
            # KNN
            distancias, indices = knn.kneighbors(datos_transformados, n_neighbors=6)
            recomendados = df_steam.index[indices[0][1:]].tolist()
            
            st.divider()
            st.subheader(f"Si te gusta '{busqueda}', te encantarán:")
            
            for juego in recomendados:
                with st.container(border=True):
                    col_info, col_tags = st.columns([1, 2])
                    
                    with col_info:
                        # 📸 Lógica de Imagen usando el AppID del diccionario
                        appid = dict_imagenes.get(juego)
                        
                        st.markdown(f"### {juego}")
                        
                        if appid:
                            url_img = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"
                            st.image(url_img, use_container_width=True)

                    with col_tags:
                        comunes = obtener_coincidencias(df_steam, busqueda, juego)
                        
                        if comunes:
                            st.markdown("<p style='font-weight: bold; font-size: 1.3rem; margin-bottom: 8px;'>¿Por qué este juego?</p>", unsafe_allow_html=True)
                            # Contenedor Flexbox para etiquetas de colores
                            etiquetas_html = '<div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; align-item: center">'
                            
                            for tag in comunes[:15]:
                                bg, txt = COLORES_TAGS[hash(tag) % len(COLORES_TAGS)]
                                etiquetas_html += f'''
                                    <span style="
                                        background-color: {bg};
                                        border: 1px solid {txt};
                                        border-radius: 15px;
                                        padding: 3px 12px;
                                        font-size: 1rem;
                                        margin: 10px;
                                        color: {txt};
                                        min-width: 150px;
                                        font-weight: bold;
                                        white-space: nowrap;
                                        display: flex;
                                        justify-content: center;
                                        align-items: center;
                                        height: 30px;">
                                        {tag}
                                    </span>'''

                            etiquetas_html += '</div>'
                            st.markdown(etiquetas_html, unsafe_allow_html=True)
                        else:
                            st.info("Similitud técnica detectada (coincidencia en estructura profunda).")
else:
    st.error("Error: No se pudieron cargar los datos de Steam.")