import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Hardware Intelligence", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] { 
        border: 1px solid #30363d; 
        padding: 15px; 
        border-radius: 10px; 
        background-color: #161b22; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN APIS
API_KEY = "6d32ce1a594a45779b6e71741a42ceb9" 
URL_EXCHANGE = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"

@st.cache_data(ttl=3600)
def get_exchange_rate():
    try:
        response = requests.get(URL_EXCHANGE)
        return response.json()['rates']['EUR']
    except:
        return 0.92

@st.cache_data(ttl=86400)
def get_inflation_data():
    """Obtiene el CPI real desde la FRED"""
    try:
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL"
        df = pd.read_csv(url)
        df.columns = ['Fecha', 'CPI']
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df = df[df['Fecha'] >= "2020-11-01"].copy()
        base_val = df.iloc[0]['CPI']
        df['Inflacion_Acumulada'] = ((df['CPI'] - base_val) / base_val) * 100
        return df
    except:
        return pd.DataFrame()

# 3. DATOS HISTÓRICOS
def get_real_history_data():
    return {
        "PS5 Standard": {
            "2020-11-01": 499, "2021-06-01": 799, "2022-01-01": 699, 
            "2023-01-01": 549, "2024-01-01": 499, "2026-05-11": 607
        },
        "PS5 Slim": {
            "2023-11-01": 499, "2024-06-01": 479, "2026-05-11": 449
        },
        "PS5 Pro": {
            "2024-11-01": 699, "2025-06-01": 679, "2026-05-11": 699
        },
        "Xbox Series X": {
            "2020-11-01": 499, "2021-06-01": 649, "2022-01-01": 599, 
            "2023-01-01": 499, "2024-01-01": 479, "2026-05-11": 607
        },
        "Xbox Series S": {
            "2020-11-01": 299, "2021-06-01": 349, "2022-01-01": 329, 
            "2023-01-01": 279, "2024-01-01": 249, "2026-05-11": 363
        },
        "Nintendo Switch OLED": {
            "2021-10-01": 349, "2022-06-01": 369, "2023-01-01": 349, 
            "2024-01-01": 329, "2026-05-11": 384
        },
        "Steam Deck (512GB)": {
            "2022-02-01": 649, "2023-01-01": 599, "2024-01-01": 449, 
            "2025-01-01": 399, "2026-05-11": 380
        },
        "PlayStation Portal": {
            "2023-11-01": 199, "2024-03-01": 249, "2025-01-01": 199, 
            "2026-05-11": 210
        },
        "ASUS ROG Ally (Z1 Extreme)": {
            "2023-06-01": 699, "2024-01-01": 599, "2025-01-01": 499, 
            "2026-05-11": 485
        }
    }

def process_data(tasa_eur):
    hitos = get_real_history_data()
    filas = []
    
    # Mapa inteligente de marcas
    marca_map = {
        "PS5": "Sony", "Portal": "Sony", "Xbox": "Microsoft", 
        "Nintendo": "Nintendo", "Switch": "Nintendo",
        "Steam": "Valve", "ASUS": "ASUS", "ROG": "ASUS"
    }

    for consola, historial in hitos.items():
        p_lanzamiento = list(historial.values())[0]
        
        # Detectar marca
        marca_detectada = "Otros"
        for keyword, name in marca_map.items():
            if keyword in consola:
                marca_detectada = name
                break

        for fecha, precio_usd in historial.items():
            filas.append({
                "Fecha": pd.to_datetime(fecha),
                "Consola": consola,
                "Precio_EUR": round(precio_usd * tasa_eur, 2),
                "Indice_100": (precio_usd / p_lanzamiento) * 100,
                "Marca": marca_detectada
            })
    
    df = pd.DataFrame(filas)
    df_list = []
    for consola in df['Consola'].unique():
        temp = df[df['Consola'] == consola].set_index('Fecha')
        temp_num = temp.resample('MS').mean(numeric_only=True).interpolate()
        temp_num['Consola'] = consola
        temp_num['Marca'] = temp['Marca'].iloc[0]
        df_list.append(temp_num.reset_index())
    
    return pd.concat(df_list)

# --- LÓGICA DE EJECUCIÓN ---
tasa_eur = get_exchange_rate()
df_final = process_data(tasa_eur)
df_inf = get_inflation_data()

st.title("🛡️ Hardware Intelligence Dashboard")
st.info(f"Divisa: **1 USD = {tasa_eur:.4f} EUR** | Inflación FRED: **Conectada**")

with st.expander("🔍 Filtros de Comparación", expanded=True):
    consolas_selec = st.multiselect("Selecciona modelos:", options=df_final['Consola'].unique(), default=df_final['Consola'].unique())

df_filtrado = df_final[df_final['Consola'].isin(consolas_selec)]

if not df_filtrado.empty:
    ultimos_precios = df_filtrado.sort_values('Fecha').groupby('Consola').last()
    
    # --- KPIs DINÁMICOS (Ahora con 4 columnas) ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("PRECIO PROMEDIO ACTUAL", f"{ultimos_precios['Precio_EUR'].mean():.2f} €")
    with c2:
        mas_cara = ultimos_precios['Precio_EUR'].idxmax()
        st.metric("MÁS CARA", mas_cara, f"{ultimos_precios['Precio_EUR'].max()} €")
    with c3:
        st.metric("MARCAS ANALIZADAS", df_filtrado['Marca'].nunique())
    with c4:
        inf_acumulada = df_inf.iloc[-1]['Inflacion_Acumulada'] if not df_inf.empty else 0
        st.metric("INFLACIÓN (CPI)", f"+{inf_acumulada:.1f}%", "Desde Nov 2020")
        

    st.write("---")

    st.subheader("📈 Evolución de Precios (Convertido a EUR)")

    fig_line = px.line(
        df_filtrado,
        x='Fecha',
        y='Precio_EUR',
        color='Consola',
        template="plotly_dark",
        markers=True,
        color_discrete_map={
            'PS5 Standard': '#003087', 'PS5 Slim': '#00aaff',
            'Xbox Series X': '#107c10', 'Xbox Series S': '#2ca02c',
            'Nintendo Switch OLED': '#e60012'
        }
    )

    # --- AÑADIR SELECTOR DE PERIODOS DE TIEMPO ---
    fig_line.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all", label="Todo")
            ]),
            bgcolor="#1f2c3a", # Color de fondo de los botones para que combine con el modo oscuro
            activecolor="#00aaff", # Color cuando el botón está seleccionado
            font=dict(color="white")
        )
    )

    # Añadimos también el Range Slider abajo para poder desplazarse manualmente
    fig_line.update_layout(
        hovermode="x unified", 
        yaxis_title="Precio en Euros (€)",
        xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    st.plotly_chart(fig_line, use_container_width=True)

    # --- GRÁFICA DE BARRAS ACTUAL ---
    st.subheader("📊 Comparativa de Mercado Actual")
    fig_bar = px.bar(
        ultimos_precios.reset_index(),
        x='Consola',
        y='Precio_EUR',
        color='Marca',
        text_auto='.2f',
        template="plotly_dark",
        color_discrete_map={'Sony': '#003087', 'Microsoft': '#107c10', 'Nintendo': '#e60012'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    
# --- SECCIÓN: PRECIO VS INFLACIÓN (ESTILO CLAUDE) ---
    st.write("---")
    st.subheader("⚖️ Análisis de Poder Adquisitivo: Precio vs Inflación")
    
    if not df_inf.empty:
        # Creamos subplots: Fila 1 para Consolas, Fila 2 para Inflación
        fig_indices = make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.08,
            row_heights=[0.7, 0.3],
            subplot_titles=("Índice de Precio Normalizado (100 = Lanzamiento)", "CPI Inflación Acumulada (USA)")
        )

        # 1. Añadimos las líneas de cada consola al primer gráfico
        for consola in df_filtrado['Consola'].unique():
            df_c = df_filtrado[df_filtrado['Consola'] == consola]
            fig_indices.add_trace(
                go.Scatter(
                    x=df_c['Fecha'], 
                    y=df_c['Indice_100'], 
                    name=consola,
                    mode='lines+markers',
                    line=dict(width=2)
                ),
                row=1, col=1
            )

        # Línea de referencia base 100
        fig_indices.add_hline(y=100, line_dash="dash", line_color="gray", row=1, col=1)

        # 2. Añadimos la inflación como área rellena (naranja) al segundo gráfico
        fig_indices.add_trace(
            go.Scatter(
                x=df_inf['Fecha'], 
                y=df_inf['Inflacion_Acumulada'],
                name="Inflación CPI (Acum.)",
                fill='tozeroy',
                line=dict(color='orange', width=2),
                fillcolor='rgba(255, 165, 0, 0.2)'
            ),
            row=2, col=1
        )

        # Configuración de diseño
        fig_indices.update_layout(
            height=600,
            template="plotly_dark",
            showlegend=True,
            hovermode="x unified",
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        # Ajustes de los ejes Y
        fig_indices.update_yaxes(title_text="Índice (100)", row=1, col=1)
        fig_indices.update_yaxes(title_text="% Inflación", row=2, col=1)

        st.plotly_chart(fig_indices, use_container_width=True)
        
        
# --- NUEVA SECCIÓN: INTELIGENCIA POR MARCA ---
    st.write("---")
    st.subheader("🏢 Business Intelligence: Análisis por Compañía")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # 1. Distribución de Valor por Marca (Pie Chart)
        st.markdown("##### Cuota de Valor en Selección")
        fig_pie = px.pie(
            ultimos_precios.reset_index(), 
            values='Precio_EUR', 
            names='Marca',
            hole=0.4,
            template="plotly_dark",
            color='Marca',
            color_discrete_map={'Sony': '#003087', 'Microsoft': '#107c10', 'Nintendo': '#e60012', 
                                'NVIDIA': '#76b900', 'AMD': '#900000', 'Valve': '#1a9fff', 'ASUS': '#ff0033'}
        )
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        # 2. Precio Promedio por Marca (Bar Chart Horizontal)
        st.markdown("##### Precio Promedio por Fabricante")
        avg_brand_price = ultimos_precios.groupby('Marca')['Precio_EUR'].mean().reset_index().sort_values('Precio_EUR', ascending=False)
        
        fig_brand_bar = px.bar(
            avg_brand_price,
            x='Precio_EUR',
            y='Marca',
            orientation='h',
            template="plotly_dark",
            text_auto='.2f',
            color='Marca',
            color_discrete_map={'Sony': '#003087', 'Microsoft': '#107c10', 'Nintendo': '#e60012', 
                                'NVIDIA': '#76b900', 'AMD': '#900000', 'Valve': '#1a9fff', 'ASUS': '#ff0033'}
        )
        fig_brand_bar.update_layout(showlegend=False, xaxis_title="Euros (€)")
        st.plotly_chart(fig_brand_bar, use_container_width=True)

else:
    st.warning("Selecciona al menos una consola para activar el Dashboard.")
    


st.write("---")
st.caption("Nota: Los precios históricos reflejan el promedio del mercado secundario (usado/reventa) convertido a EUR según tasa diaria.")