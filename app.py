import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Control de Asma", 
    page_icon="🫁", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Función de zona horaria oficial Chile
def obtener_ahora_chile():
    tz = pytz.timezone('America/Santiago')
    return datetime.now(tz)

# --- 2. DISEÑO CSS ESTILO APP MÓVIL ---
st.markdown("""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #F4F7F9 !important;
        color: #1E293B !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 10px 10px 0px 0px !important;
        padding: 10px 16px !important;
    }

    .stButton > button {
        width: 100% !important;
        height: 54px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.2s ease;
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    div.stButton > button[key="btn_now_in"] {
        background: linear-gradient(135deg, #2E7D32, #1B5E20) !important;
        color: white !important;
    }
    
    div.stButton > button[key="btn_now_fi"] {
        background: linear-gradient(135deg, #0288D1, #01579B) !important;
        color: white !important;
    }

    div.stButton > button[key="btn_save_final"] {
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        color: white !important;
    }

    label, p, span, h1, h2, h3 {
        color: #0F172A !important;
    }
    
    div[data-baseweb="select"] > div, input {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Archivos de persistencia
USER_DB = "perfil_usuario.csv"
EPISODES_DB = "bitacora_episodios.csv"

def guardar_datos(df, filename):
    df.to_csv(filename, index=False)

def cargar_datos(filename, columnas):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame(columns=columnas)

# --- 3. INICIALIZACIÓN Y RESET DE ESTADO DEL FORMULARIO ---
ahora_cl = obtener_ahora_chile()

def resetear_formulario():
    ahora = obtener_ahora_chile()
    st.session_state["f_in"] = ahora.date()
    st.session_state["h_in"] = ahora.time()
    st.session_state["m_in"] = 5
    st.session_state["sintomas"] = []
    st.session_state["med"] = "Salbutamol / Rescate"
    st.session_state["puffs"] = "2 Puffs"
    st.session_state["ubicacion"] = "Casa / Habitación"
    st.session_state["f_fi"] = ahora.date()
    st.session_state["h_fi"] = ahora.time()
    st.session_state["m_fi"] = 2
    st.session_state["obs"] = ""

if "f_in" not in st.session_state:
    resetear_formulario()

# Diccionario Multiidioma
DICCIONARIO = {
    "ES": {
        "titulo": "🫁 Control de Asma",
        "subtitulo": "Asistente digital de registro clínico",
        "tab_registro": "🚨 Registrar Crisis",
        "tab_bitacora": "📊 Bitácora Médica",
        "tab_perfil": "👤 Perfil",
        "btn_inicio_ahora": "🟢 INICIAR CRISIS AHORA",
        "btn_termino_ahora": "🩵 TERMINAR CRISIS AHORA (ALIVIO)",
        "sintoma": "Síntomas observados:",
        "sintomas_lista": [
            "Dificultad para respirar (Disnea)",
            "Exceso de secreciones / Flemas",
            "Tos persistente",
            "Silbido en el pecho (Sibilancias)",
            "Opresión en el pecho",
            "Fatiga o cansancio extremo",
            "Otro"
        ],
        "malestar_in": "Nivel de malestar al INICIO (1-10)",
        "malestar_fi": "Nivel de malestar al TÉRMINO (1-10)",
        "med_tit": "💊 Medicación Aplicada",
        "puffs": "Dosis / Puffs",
        "ubicacion": "Entorno / Ubicación",
        "obs": "Observaciones adicionales",
        "btn_guardar": "💾 GUARDAR EN BITÁCORA",
        "descargar": "📥 Descargar Reporte (CSV)"
    },
    "EN": {
        "titulo": "🫁 Asthma Control",
        "subtitulo": "Digital clinical tracking assistant",
        "tab_registro": "🚨 Log Flare-Up",
        "tab_bitacora": "📊 Medical Log",
        "tab_perfil": "👤 Profile",
        "btn_inicio_ahora": "🟢 START FLARE-UP NOW",
        "btn_termino_ahora": "🩵 END FLARE-UP NOW (RELIEF)",
        "sintoma": "Observed symptoms:",
        "sintomas_lista": [
            "Shortness of breath",
            "Excess mucus / Phlegm",
            "Persistent cough",
            "Wheezing",
            "Chest tightness",
            "Extreme fatigue",
            "Other"
        ],
        "malestar_in": "Discomfort level at START (1-10)",
        "malestar_fi": "Discomfort level at END (1-10)",
        "med_tit": "💊 Applied Medication",
        "puffs": "Dose / Puffs",
        "ubicacion": "Environment / Location",
        "obs": "Additional notes",
        "btn_guardar": "💾 SAVE TO LOG",
        "descargar": "📥 Download Report (CSV)"
    }
}

lang_choice = st.sidebar.selectbox("🌐 Idioma / Language", ["Español", "English"])
lang = "ES" if lang_choice == "Español" else "EN"
txt = DICCIONARIO[lang]

st.title(txt["titulo"])
st.caption(txt["subtitulo"])

cols_user = ["Nombre", "Edad", "Peso", "Genero", "Diagnosticado", "Enfermedad"]
df_user = cargar_datos(USER_DB, cols_user)

cols_ep = ["Fecha_Inicio", "Hora_Inicio", "Fecha_Termino", "Hora_Termino", "Sintomas", "Malestar_Inicio", "Malestar_Termino", "Medicamento", "Puffs", "Ubicacion", "Observaciones"]
df_ep = cargar_datos(EPISODES_DB, cols_ep)

# Navegación Pestañas
tab_reg, tab_bit, tab_per = st.tabs([txt["tab_registro"], txt["tab_bitacora"], txt["tab_perfil"]])

# ==================== PESTAÑA 1: REGISTRO DE CRISIS ====================
with tab_reg:
    # 1. BOTÓN SUPERIOR DE INICIO
    if st.button(txt["btn_inicio_ahora"], key="btn_now_in"):
        ahora = obtener_ahora_chile()
        st.session_state["f_in"] = ahora.date()
        st.session_state["h_in"] = ahora.time()
        st.toast("🟢 Fecha y hora de inicio capturadas automáticamente", icon="⏱️")
        st.rerun()

    st.markdown("### ⏱️ Datos del Inicio")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        f_in_val = st.date_input("Fecha Inicio", key="f_in")
        h_in_val = st.time_input("Hora Inicio", key="h_in")
    with col_t2:
        m_in_val = st.slider(txt["malestar_in"], 1, 10, key="m_in")

    sintomas_val = st.multiselect(
        txt["sintoma"], 
        options=txt["sintomas_lista"],
        key="sintomas"
    )

    st.markdown("---")
    st.markdown(f"### {txt['med_tit']}")
    med_val = st.selectbox("Medicamento", ["Salbutamol / Rescate", "Inhalador Corticoide", "Corticoide Oral", "Ninguno", "Otro"], key="med")
    puffs_val = st.radio(txt["puffs"], ["0", "1 Puff", "2 Puffs", "3+ Puffs"], horizontal=True, key="puffs")
    ubicacion_val = st.text_input(txt["ubicacion"], key="ubicacion")

    st.markdown("---")
    
    # 2. BOTÓN DE TÉRMINO
    if st.button(txt["btn_termino_ahora"], key="btn_now_fi"):
        ahora = obtener_ahora_chile()
        st.session_state["f_fi"] = ahora.date()
        st.session_state["h_fi"] = ahora.time()
        st.toast("🩵 Fecha y hora de término capturadas", icon="✨")
        st.rerun()

    st.markdown("### 🩵 Datos del Término")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_fi_val = st.date_input("Fecha Término", key="f_fi")
        h_fi_val = st.time_input("Hora Término", key="h_fi")
    with col_f2:
        m_fi_val = st.slider(txt["malestar_fi"], 1, 10, key="m_fi")

    st.markdown("---")
    obs_val = st.text_area(txt["obs"], placeholder="Escribe notas relevantes aquí...", key="obs")

    # 3. GUARDADO Y LIMPIEZA DE FORMULARIO
    if st.button(txt["btn_guardar"], key="btn_save_final"):
        str_sintomas = ", ".join(sintomas_val) if sintomas_val else "Ninguno reportado"
        
        nueva_fila = pd.DataFrame([[
            f_in_val.strftime("%Y-%m-%d"),
            h_in_val.strftime("%H:%M"),
            f_fi_val.strftime("%Y-%m-%d"),
            h_fi_val.strftime("%H:%M"),
            str_sintomas,
            m_in_val,
            m_fi_val,
            med_val,
            puffs_val,
            ubicacion_val,
            obs_val
        ]], columns=cols_ep)
        
        df_final = pd.concat([df_ep, nueva_fila], ignore_index=True)
        guardar_datos(df_final, EPISODES_DB)
        
        # Limpieza de formulario
        resetear_formulario()
        st.success("✅ ¡Registro guardado exitosamente en la bitácora!")
        st.rerun()

# ==================== PESTAÑA 2: BITÁCORA Y MÉTRICAS ====================
with tab_bit:
    if not df_ep.empty:
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        with col_kpi1:
            st.metric("Total Episodios", len(df_ep))
        with col_kpi2:
            st.metric("Último Medicamento", str(df_ep["Medicamento"].iloc[-1]).split('/')[0])
        with col_kpi3:
            st.metric("Malestar Promedio", f"{round(df_ep['Malestar_Inicio'].mean(), 1)}/10")

        st.markdown("---")
        st.markdown("### 📋 Historial Detallado")
        st.dataframe(df_ep.iloc[::-1], use_container_width=True)
        
        csv = df_ep.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=txt["descargar"],
            data=csv,
            file_name=f"reporte_asma_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv'
        )
    else:
        st.info("Aún no hay episodios registrados en el sistema.")

# ==================== PESTAÑA 3: PERFIL DEL PACIENTE ====================
with tab_per:
    with st.form("form_user"):
        nom = st.text_input("Nombre completo", value=df_user["Nombre"].iloc[0] if not df_user.empty else "")
        ed = st.number_input("Edad", min_value=0, max_value=120, value=int(df_user["Edad"].iloc[0]) if not df_user.empty else 30)
        pe = st.number_input("Peso (kg)", min_value=0.0, max_value=250.0, value=float(df_user["Peso"].iloc[0]) if not df_user.empty else 70.0)
        gen = st.selectbox("Género", ["Masculino", "Femenino", "Otro"], index=0)
        diag = st.radio("¿Diagnosticado por médico?", ["Sí", "No"], index=0)
        enf = st.text_input("Enfermedad específica / Diagnóstico", value=df_user["Enfermedad"].iloc[0] if not df_user.empty else "Asma Bronquial")
        
        if st.form_submit_button("Guardar Perfil"):
            guardar_datos(pd.DataFrame([[nom, ed, pe, gen, diag, enf]], columns=cols_user), USER_DB)
            st.success("Perfil guardado correctamente.")
            st.rerun()

    if not df_user.empty:
        st.markdown("---")
        st.info(f"**Paciente registrado:** {df_user['Nombre'].iloc[0]} | **Diagnóstico:** {df_user['Enfermedad'].iloc[0]}")
