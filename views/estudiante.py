import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px

st.title("🎓 Panel de Gestión Académica")
st.markdown("Registra a tus alumnos y utiliza la IA para predecir el rendimiento grupal con un enfoque preventivo.")

# 1. Recuperar recursos del session_state (cargados en app.py)
recursos = st.session_state.get('recursos_academia')
if not recursos:
    st.error("⚠️ Error: No se pudo cargar el modelo. Asegúrate de que el archivo .pkl esté en la carpeta correcta.")
    st.stop()

modelo = recursos['modelo']
columnas_modelo = recursos['columnas']

# 2. Inicializar la lista de clase si no existe
if 'lista_clase' not in st.session_state:
    st.session_state.lista_clase = []

# --- INTERFAZ ---
col_form, col_lista = st.columns([1, 1.8])

with col_form:
    st.subheader("📝 Registro de Alumno")
    with st.form("form_registro", clear_on_submit=True):
        nombre = st.text_input("Nombre del Estudiante", placeholder="Ej. Juan Pérez")
        
        absences = st.slider("Faltas de asistencia", 0, 93, 0, 
                             help="Número total de días que el alumno ha faltado a clase durante el curso.")
        
        failures = st.number_input("Suspensos previos", 0, 3, 0,
                                   help="Número de materias suspendidas en cursos anteriores (máximo 3).")
        
        studytime = st.select_slider("Horas de estudio semanal", 
                                     options=[1, 2, 3, 4],
                                     help="1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h semanales.")
        
        salidas = st.slider("Vida social / Salidas", 1, 5, 3,
                            help="Frecuencia con la que el alumno sale con amigos (1: Muy poco, 5: Mucho).")
        
        alcohol = st.slider("Consumo alcohol (Finde)", 1, 5, 1,
                            help="Consumo de alcohol durante el fin de semana (1: Muy bajo, 5: Muy alto).")
        
        salud = st.slider("Estado de salud", 1, 5, 5,
                          help="Percepción del estado de salud actual (1: Muy mala, 5: Excelente).")
        
        btn_add = st.form_submit_button("Añadir a la lista ➕")
        
        if btn_add:
            if len(st.session_state.lista_clase) < 50:
                nuevo_alumno = {
                    "Nombre": nombre if nombre else f"Alumno {len(st.session_state.lista_clase)+1}",
                    "absences": absences,
                    "failures": failures,
                    "studytime": studytime,
                    "goout": salidas,
                    "Walc": alcohol,
                    "health": salud
                }
                st.session_state.lista_clase.append(nuevo_alumno)
                st.rerun() # Refrescamos para mostrar en la lista derecha inmediatamente
            else:
                st.warning("Límite de 50 alumnos alcanzado.")

with col_lista:
    st.subheader(f"📋 Alumnos Registrados ({len(st.session_state.lista_clase)}/50)")
    
    if st.session_state.lista_clase:
        for i, alumno in enumerate(st.session_state.lista_clase):
            col_n, col_x = st.columns([4, 1])
            with col_n:
                st.write(f"👤 **{alumno['Nombre']}** | Faltas: {alumno['absences']} | Suspensos: {alumno['failures']} | Estudios: {alumno['studytime']}  | Sali: {alumno['goout']} | Salud: {alumno['health']} ")
            with col_x:
                if st.button("❌", key=f"del_{i}", help=f"Eliminar a {alumno['Nombre']}"):
                    st.session_state.lista_clase.pop(i)
                    st.rerun()
        
        st.divider()
        
        col_btns = st.columns(2)
        with col_btns[0]:
            if st.button("🧹 Limpiar Todo"):
                st.session_state.lista_clase = []
                st.rerun()
        
        with col_btns[1]:
            lanzar_ia = st.button("🔮 Lanzar Predicción Grupal", type="primary")

        if lanzar_ia:
            st.divider()
            st.subheader("🚀 Resultados de la IA")
            
            resultados_finales = []
            
            # RECALCULAMOS LAS PREDICCIONES
            for alumno in st.session_state.lista_clase:
                registro_completo = {col: 0 for col in columnas_modelo}
                defaults = {'age': 18, 'Medu': 2, 'Fedu': 2, 'traveltime': 2, 'famsup': 0, 'internet': 0, 'higher': 0}
                registro_completo.update(defaults)
                registro_completo.update(alumno) 
                
                df_input = pd.DataFrame([registro_completo])[columnas_modelo]
                
                # Definimos 'prob' aquí
                prob = modelo.predict_proba(df_input)[0][1]

                # Regla de seguridad (Mano dura)
                if alumno["absences"] > 30 or alumno["failures"] >= 2:
                    prob = prob * 0.5  

                # Definimos 'pred_final' aquí
                pred_final = 1 if prob >= 0.5 else 0
                
                resultados_finales.append({
                    "Nombre": alumno["Nombre"],
                    "Estado": "Aprobado ✅" if pred_final == 1 else "En Riesgo 🚨",
                    "Confianza %": int(round(prob * 100, 0))
                })
            
            df_res = pd.DataFrame(resultados_finales)

            # --- MÉTRICAS RESUMEN ---
            riesgo_total = len(df_res[df_res["Estado"] == "En Riesgo 🚨"])
            m1, m2 = st.columns(2)
            m1.metric("Total Alumnos", len(df_res))
            m2.metric("En Riesgo Académico", riesgo_total, delta=-riesgo_total, delta_color="inverse")
            
            # --- GRÁFICO CON SEABORN ---
            import seaborn as sns
            import matplotlib.pyplot as plt

            # Forzamos el estilo oscuro de Matplotlib para que coincida con Streamlit
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(10, 5))
            
            sns.barplot(
                data=df_res, 
                x="Estado", 
                y="Confianza %", 
                hue="Estado",
                palette={"Aprobado ✅": "#2ecc71", "En Riesgo 🚨": "#e74c3c"},
                errorbar="sd", # Muestra la desviación estándar (qué tanto varían los alumnos)
                capsize=.1,    # Añade "bigotes" al errorbar
                ax=ax
            )

            # Línea de umbral crítico
            ax.axhline(50, color="white", linestyle="--", alpha=0.5)
            
            # Configurar etiquetas
            ax.set_ylim(0, 105)
            ax.set_title("Promedio de Confianza Grupal (con Desviación)", fontsize=14, pad=20)
            ax.set_ylabel("Confianza Media %")
            
            # Añadir etiquetas de valor encima de las barras
            for p in ax.patches:
                if p.get_height() > 0: # Evitar etiquetas en barras vacías
                    ax.annotate(f'{p.get_height():.1f}%', 
                                (p.get_x() + p.get_width() / 2., p.get_height()), 
                                ha = 'center', va = 'center', 
                                xytext = (0, 9), 
                                textcoords = 'offset points',
                                color="white", fontweight='bold')

            sns.despine(left=True, bottom=True)
            st.pyplot(fig)
            st.write("### 🔍 Análisis de Factores de Riesgo")
            st.info("Este mapa muestra cómo se relacionan las variables introducidas con la probabilidad de éxito calculada.")
            
            fig_heat, ax_heat = plt.subplots(figsize=(8, 4))
            
            # Calculamos la correlación entre las variables de entrada y el resultado
            # Usamos df_res["Confianza %"] para ver qué influye más en la nota
            df_corr = pd.DataFrame(st.session_state.lista_clase)
            df_corr["Prob_Exito"] = df_res["Confianza %"]
            
            # Seleccionamos solo las numéricas para el heatmap
            corr_matrix = df_corr.select_dtypes(include=['number']).corr()
            
            sns.heatmap(
                corr_matrix[['Prob_Exito']].sort_values(by='Prob_Exito', ascending=False),
                annot=True, 
                cmap='RdYlGn', # Rojo (Riesgo) a Verde (Éxito)
                fmt=".2f",
                ax=ax_heat
            )
            
            ax_heat.set_title("Impacto de las Variables en el Rendimiento", color="white")
            st.pyplot(fig_heat)
            
            st.dataframe(df_res, hide_index=True, use_container_width=True)
            # --- BOTÓN DE DESCARGA ---
            # Convertimos el DataFrame de resultados a CSV
            csv = df_res.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Descargar Informe de Predicciones (CSV)",
                data=csv,
                file_name='predicciones_rendimiento_academico.csv',
                mime='text/csv',
                help="Haz clic para descargar un archivo compatible con Excel con los resultados del análisis."
            )
    else:
        st.info("La lista está vacía. Registra alumnos a la izquierda para analizar el aula.")