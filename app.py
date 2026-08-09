import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURACIÓN DE PÁGINA E INTERFAZ ---
st.set_page_config(page_title="Control de Asma", page_icon="🫁", layout="centered")

# Inyección de CSS forzado para evitar el fondo negro por modo oscuro en móviles
st.markdown("""
    <style>
    /* Forzar fondo blanco y texto oscuro en toda la app */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    
    /* Forzar contenedores y tarjetas en fondo claro */
    [data-testid="stExpander"], div[role="radiogroup"], .stSelectbox {
        background-color: #F8F9FA !important;
        border-radius: 10px !important;
        padding: 5px !important;
    }

    /* Botones generales grandes con excelente visibilidad */
    .stButton > button {
        width: 100% !important;
        height: 60px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    
    /* Estilo del botón principal de guardado */
    div.stButton > button:first-child {
        background-color: #2E7D32 !important;
        color: white !important;
    }
    
    /* Textos y etiquetas adaptadas para lectura fácil */
    label, .stRadio p, .stSelectbox p, p, h1, h2, h3, span {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #1A1A1A !important;
    }
    </style>
""", unsafe_allow_html=True)

# Archivos de datos locales para la marcha blanca
USER_DB = "perfil_usuario.csv"
EPISODES_DB = "bitacora_episodios.csv"

def guardar_datos(df, filename):
    df.to_csv(filename, index=False)

def cargar_datos(filename, columnas):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame(columns=columnas)

# --- 2. DICCIONARIO MULTIIDIOMA ---
DICCIONARIO = {
    "ES": {
        "titulo": "🫁 Control de Asma",
        "subtitulo": "Registro rápido de crisis y medicación",
        "perfil_tit": "👤 Perfil del Paciente",
        "reg_tit": "🚨 Registrar Episodio",
        "sintoma": "Síntoma principal",
        "malestar_in": "Malestar al INICIO (1-10)",
        "malestar_fi": "Malestar al TÉRMINO (1-10)",
        "med_tit": "💊 Medicación aplicada",
        "puffs": "Cantidad de Puffs",
        "ubicacion": "Entorno / Ubicación",
        "obs": "Observaciones breves",
        "btn_guardar": "✅ GUARDAR EPISODIO",
        "historial_tit": "📊 Bitácora para el Médico",
        "descargar": "📥 Descargar Reporte (CSV)"
    },
    "EN": {
        "titulo": "🫁 Asthma Control",
        "subtitulo": "Quick flare-up & medication tracker",
        "perfil_tit": "👤 Patient Profile",
        "reg_tit": "🚨 Log Flare-Up",
        "sintoma": "Main symptom",
        "malestar_in": "Discomfort at START (1-10)",
        "malestar_fi": "Discomfort at END (1-10)",
        "med_tit": "💊 Medication taken",
        "puffs": "Puff count",
        "ubicacion": "Environment / Location",
        "obs": "Brief notes",
        "btn_guardar": "✅ SAVE EPISODE",
        "historial_tit": "📊 Doctor's Log",
        "descargar": "📥 Download Report (CSV)"
    }
}

# Selector de idioma en barra lateral
lang_choice = st.sidebar.selectbox("🌐 Idioma / Language", ["Español", "English"])
lang = "ES" if lang_choice == "Español" else "EN"
txt = DICCIONARIO[lang]

st.title(txt["titulo"])
st.caption(txt["subtitulo"])

# --- 3. MÓDULO PERFIL DE USUARIO ---
cols_user = ["Nombre", "Edad", "Peso", "Genero", "Diagnosticado", "Enfermedad"]
df_user = cargar_datos(USER_DB, cols_user)

with st.expander(txt["perfil_tit"], expanded=df_user.empty):
    with st.form("form_user"):
        nom = st.text_input("Nombre completo", value=df_user["Nombre"].iloc[0] if not df_user.empty else "")
        ed = st.number_input("Edad", min_value=0, max_value=120, value=int(df_user["Edad"].iloc[0]) if not df_user.empty else 30)
        pe = st.number_input("Peso (kg)", min_value=0.0, max_value=250.0, value=float(df_user["Peso"].iloc[0]) if not df_user.empty else 70.0)
        gen = st.selectbox("Género", ["Masculino", "Femenino", "Otro"], index=0)
        diag = st.radio("¿Diagnosticado?", ["Sí", "No"], index=0)
        enf = st.text_input("Enfermedad específica", value=df_user["Enfermedad"].iloc[0] if not df_user.empty else "")
        
        if st.form_submit_button("Guardar Perfil"):
            guardar_datos(pd.DataFrame([[nom, ed, pe, gen, diag, enf]], columns=cols_user), USER_DB)
            st.rerun()

if not df_user.empty:
    st.info(f"**Paciente:** {df_user['Nombre'].iloc[0]} | **Diagnóstico:** {df_user['Enfermedad'].iloc[0]}")

# --- 4. MÓDULO REGISTRO DE EPISODIOS ---
st.header(txt["reg_tit"])
cols_ep = ["Fecha", "Hora_Inicio", "Hora_Termino", "Sintoma", "Malestar_Inicio", "Malestar_Termino", "Medicamento", "Puffs", "Ubicacion", "Observaciones"]
df_ep = cargar_datos(EPISODES_DB, cols_ep)

with st.form("form_episodio", clear_on_submit=True):
    sintoma = st.selectbox(txt["sintoma"], ["Dificultad para respirar / Shortness of breath", "Exceso de secreciones / Cough & mucus", "Sibilancias / Wheezing", "Otro / Other"])
    
    col1, col2 = st.columns(2)
    with col1:
        h_in = st.time_input("Hora Inicio", datetime.now().time())
        m_in = st.selectbox(txt["malestar_in"], list(range(1, 11)), index=4)
    with col2:
        h_fi = st.time_input("Hora Término", datetime.now().time())
        m_fi = st.selectbox(txt["malestar_fi"], list(range(1, 11)), index=1)
    
    st.markdown(f"### {txt['med_tit']}")
    med = st.selectbox("Medicamento / Medication", ["Salbutamol / Rescate", "Inhalador Corticoide", "Corticoide Oral", "Ninguno", "Otro"])
    puffs = st.radio(txt["puffs"], ["0", "1 Puff", "2 Puffs", "3+ Puffs"], horizontal=True, index=2)
    
    ubicacion = st.text_input(txt["ubicacion"], value="Casa / Home")
    obs = st.text_area(txt["obs"])
    
    if st.form_submit_button(txt["btn_guardar"]):
        nueva_fila = pd.DataFrame([[
            datetime.now().strftime("%Y-%m-%d"),
            h_in.strftime("%H:%M"),
            h_fi.strftime("%H:%M"),
            sintoma,
            m_in,
            m_fi,
            med,
            puffs,
            ubicacion,
            obs
        ]], columns=cols_ep)
        
        df_final = pd.concat([df_ep, nueva_fila], ignore_index=True)
        guardar_datos(df_final, EPISODES_DB)
        st.success("¡Registrado!")
        st.rerun()

# --- 5. MÓDULO HISTORIAL Y DESCARGA ---
st.header(txt["historial_tit"])
if not df_ep.empty:
    st.dataframe(df_ep.iloc[::-1], use_container_width=True)
    csv = df_ep.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=txt["descargar"],
        data=csv,
        file_name=f"reporte_asma_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )
