import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# --- 1. CONFIGURACIÓN DE PÁGINA Y ZONA HORARIA CHILE ---
st.set_page_config(page_title="Control de Asma", page_icon="🫁", layout="centered")

# Función para obtener fecha y hora exactas de Chile (America/Santiago)
def obtener_ahora_chile():
    tz = pytz.timezone('America/Santiago')
    return datetime.now(tz)

# CSS para forzar tema claro, contraste y estilos de botones
st.markdown("""
    <style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    
    [data-testid="stExpander"], div[role="radiogroup"], .stSelectbox, .stMultiSelect {
        background-color: #F8F9FA !important;
        border-radius: 10px !important;
        padding: 5px !important;
    }

    .stButton > button {
        width: 100% !important;
        height: 60px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        margin-top: 5px;
        margin-bottom: 10px;
        border: none !important;
    }
    
    /* Botón Inicio Verde */
    div.stButton > button[key="btn_now_in"] {
        background-color: #2E7D32 !important;
        color: white !important;
    }
    
    /* Botón Término Celeste */
    div.stButton > button[key="btn_now_fi"] {
        background-color: #0288D1 !important;
        color: white !important;
    }

    /* Botón Guardar Final Azul */
    div.stButton > button[key="btn_save_final"] {
        background-color: #1565C0 !important;
        color: white !important;
    }
    
    label, .stRadio p, .stSelectbox p, .stMultiSelect p, p, h1, h2, h3, span {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #1A1A1A !important;
    }
    </style>
""", unsafe_allow_html=True)

# Archivos de datos
USER_DB = "perfil_usuario.csv"
EPISODES_DB = "bitacora_episodios.csv"

def guardar_datos(df, filename):
    df.to_csv(filename, index=False)

def cargar_datos(filename, columnas):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame(columns=columnas)

# Inicializar marcas de tiempo con hora local de Chile
ahora_cl = obtener_ahora_chile()

if "hora_inicio_auto" not in st.session_state:
    st.session_state["hora_inicio_auto"] = ahora_cl.time()
if "fecha_inicio_auto" not in st.session_state:
    st.session_state["fecha_inicio_auto"] = ahora_cl.date()

if "hora_termino_auto" not in st.session_state:
    st.session_state["hora_termino_auto"] = ahora_cl.time()
if "fecha_termino_auto" not in st.session_state:
    st.session_state["fecha_termino_auto"] = ahora_cl.date()

# --- 2. DICCIONARIO MULTIIDIOMA ---
DICCIONARIO = {
    "ES": {
        "titulo": "🫁 Control de Asma",
        "subtitulo": "Registro rápido de crisis y medicación",
        "perfil_tit": "👤 Perfil del Paciente",
        "reg_tit": "🚨 Registrar Episodio",
        "btn_inicio_ahora": "🟢 INICIAR CRISIS AHORA",
        "btn_termino_ahora": "🩵 TERMINAR CRISIS AHORA (ALIVIO)",
        "sintoma": "Síntomas presentes (selección múltiple):",
        "sintomas_lista": [
            "Dificultad para respirar (Disnea)",
            "Exceso de secreciones / Flemas",
            "Tos persistente",
            "Silbido en el pecho (Sibilancias)",
            "Opresión en el pecho",
            "Fatiga o cansancio extremo",
            "Otro"
        ],
        "malestar_in": "Malestar al INICIO (1-10)",
        "malestar_fi": "Malestar al TÉRMINO (1-10)",
        "med_tit": "💊 Medicación aplicada",
        "puffs": "Cantidad de Puffs",
        "ubicacion": "Entorno / Ubicación",
        "obs": "Observaciones breves",
        "btn_guardar": "💾 GUARDAR EN BITÁCORA",
        "historial_tit": "📊 Bitácora para el Médico",
        "descargar": "📥 Descargar Reporte (CSV)"
    },
    "EN": {
        "titulo": "🫁 Asthma Control",
        "subtitulo": "Quick flare-up & medication tracker",
        "perfil_tit": "👤 Patient Profile",
        "reg_tit": "🚨 Log Flare-Up",
        "btn_inicio_ahora": "🟢 START FLARE-UP NOW",
        "btn_termino_ahora": "🩵 END FLARE-UP NOW (RELIEF)",
        "sintoma": "Symptoms present (select multiple):",
        "sintomas_lista": [
            "Shortness of breath",
            "Excess mucus / Phlegm",
            "Persistent cough",
            "Wheezing",
            "Chest tightness",
            "Extreme fatigue",
            "Other"
        ],
        "malestar_in": "Discomfort at START (1-10)",
        "malestar_fi": "Discomfort at END (1-10)",
        "med_tit": "💊 Medication taken",
        "puffs": "Puff count",
        "ubicacion": "Environment / Location",
        "obs": "Brief notes",
        "btn_guardar": "💾 SAVE TO LOG",
        "historial_tit": "📊 Doctor's Log",
        "descargar": "📥 Download Report (CSV)"
    }
}

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

# 1. BOTÓN DE INICIO (Ubicado al principio del módulo de registro)
if st.button(txt["btn_inicio_ahora"], key="btn_now_in"):
    ahora = obtener_ahora_chile()
    st.session_state["hora_inicio_auto"] = ahora.time()
    st.session_state["fecha_inicio_auto"] = ahora.date()
    st.toast("🟢 Hora de inicio capturada automáticamente", icon="⏱️")

cols_ep = ["Fecha_Inicio", "Hora_Inicio", "Fecha_Termino", "Hora_Termino", "Sintomas", "Malestar_Inicio", "Malestar_Termino", "Medicamento", "Puffs", "Ubicacion", "Observaciones"]
df_ep = cargar_datos(EPISODES_DB, cols_ep)

with st.form("form_episodio", clear_on_submit=False):
    st.markdown("### 🕒 Tiempos y Síntomas de Inicio")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        f_in = st.date_input("Fecha Inicio", st.session_state["fecha_inicio_auto"])
        h_in = st.time_input("Hora Inicio", st.session_state["hora_inicio_auto"])
        m_in = st.selectbox(txt["malestar_in"], list(range(1, 11)), index=4)
        
    with col_t2:
        sintomas_sel = st.multiselect(
            txt["sintoma"], 
            options=txt["sintomas_lista"],
            default=[txt["sintomas_lista"][0]]
        )

    st.markdown(f"### {txt['med_tit']}")
    med = st.selectbox("Medicamento / Medication", ["Salbutamol / Rescate", "Inhalador Corticoide", "Corticoide Oral", "Ninguno", "Otro"])
    puffs = st.radio(txt["puffs"], ["0", "1 Puff", "2 Puffs", "3+ Puffs"], horizontal=True, index=2)
    
    ubicacion = st.text_input(txt["ubicacion"], value="Casa / Home")
    
    # 2. BOTÓN DE TÉRMINO / ALIVIO (Ubicado después de Entorno/Ubicación y antes de Observaciones)
    st.markdown("---")
    st.markdown("### 🩵 Término del Episodio (Cierre)")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_fi = st.date_input("Fecha Término", st.session_state["fecha_termino_auto"])
        h_fi = st.time_input("Hora Término", st.session_state["hora_termino_auto"])
    with col_f2:
        m_fi = st.selectbox(txt["malestar_fi"], list(range(1, 11)), index=1)
        
    obs = st.text_area(txt["obs"])
    
    if st.form_submit_button(txt["btn_guardar"], key="btn_save_final"):
        str_sintomas = ", ".join(sintomas_sel) if sintomas_sel else "No especificado"
        
        nueva_fila = pd.DataFrame([[
            f_in.strftime("%Y-%m-%d"),
            h_in.strftime("%H:%M"),
            f_fi.strftime("%Y-%m-%d"),
            h_fi.strftime("%H:%M"),
            str_sintomas,
            m_in,
            m_fi,
            med,
            puffs,
            ubicacion,
            obs
        ]], columns=cols_ep)
        
        df_final = pd.concat([df_ep, nueva_fila], ignore_index=True)
        guardar_datos(df_final, EPISODES_DB)
        st.success("¡Episodio guardado exitosamente en la bitácora!")
        st.rerun()

# 3. BOTÓN DE TÉRMINO DIRECTO EN LA INTERFAZ
if st.button(txt["btn_termino_ahora"], key="btn_now_fi"):
    ahora = obtener_ahora_chile()
    st.session_state["hora_termino_auto"] = ahora.time()
    st.session_state["fecha_termino_auto"] = ahora.date()
    st.toast("🩵 Hora de término capturada automáticamente", icon="✨")

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
