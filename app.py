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

# --- 2. DISEÑO CSS MODERNO Y ESTÉTICA CLÍNICA ---
st.markdown("""
    <style>
    /* Fondo general gris azulado suave */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #F4F7F9 !important;
        color: #1E293B !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Ocultar barra superior por defecto */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    /* Pestañas modernas (Tabs) */
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 10px 10px 0px 0px !important;
        padding: 10px 16px !important;
    }
    
    /* Contenedores estilo Tarjeta (Cards) */
    .css-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
    }

    /* Estilos de botones de alto relieve táctil */
    .stButton > button {
        width: 100% !important;
        height: 56px !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.2s ease;
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Botón verde de Inicio */
    div.stButton > button[key="btn_now_in"] {
        background: linear-gradient(135deg, #2E7D32, #1B5E20) !important;
        color: white !important;
    }
    
    /* Botón celeste de Término */
    div.stButton > button[key="btn_now_fi"] {
        background: linear-gradient(135deg, #0288D1, #01579B) !important;
        color: white !important;
    }

    /* Botón azul guardar */
    div.stButton > button[key="btn_save_final"] {
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        color: white !important;
    }

    /* Ajuste de tipografía e inputs */
    label, p, span, h1, h2, h3 {
        color: #0F172A !important;
    }
    
    div[data-baseweb="select"] > div, input {
        background-color: #F8FAFC !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Manejo de base de datos
USER_DB = "perfil_usuario.csv"
EPISODES_DB = "bitacora_episodios.csv"

def guardar_datos(df, filename):
    df.to_csv(filename, index=False)

def cargar_datos(filename, columnas):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame(columns=columnas)

# Inicializar estados de hora en sesión
ahora_cl = obtener_ahora_chile()
if "hora_inicio_auto" not in st.session_state:
    st.session_state["hora_inicio_auto"] = ahora_cl.time()
if "fecha_inicio_auto" not in st.session_state:
    st.session_state["fecha_inicio_auto"] = ahora_cl.date()

if "hora_termino_auto" not in st.session_state:
    st.session_state["hora_termino_auto"] = ahora_cl.time()
if "fecha_termino_auto" not in st.session_state:
    st.session_state["fecha_termino_auto"] = ahora_cl.date()

# --- 3. DICCIONARIO MULTIIDIOMA ---
DICCIONARIO = {
    "ES": {
        "titulo": "🫁 Control de Asma",
        "subtitulo": "Asistente digital de registro clínico",
        "tab_registro": "🚨 Registrar Crisis",
        "tab_bitacora": "📊 Bitácora Médica",
        "tab_perfil": "👤 Perfil",
        "btn_inicio_ahora": "🟢 INICIAR CRISIS AHORA",
        "btn_termino_ahora": "🩵 TERMINAR CRISIS AHORA",
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
        "ubicacion": "Entorno o detonante probable",
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
        "btn_termino_ahora": "🩵 END FLARE-UP NOW",
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
        "ubicacion": "Environment or potential trigger",
        "obs": "Additional notes",
        "btn_guardar": "💾 SAVE TO LOG",
        "descargar": "📥 Download Report (CSV)"
    }
}

lang_choice = st.sidebar.selectbox("🌐 Idioma / Language", ["Español", "English"])
lang = "ES" if lang_choice == "Español" else "EN"
txt = DICCIONARIO[lang]

# Encabezado principal
st.title(txt["titulo"])
st.caption(txt["subtitulo"])

# Carga de datos generales
cols_user = ["Nombre", "Edad", "Peso", "Genero", "Diagnosticado", "Enfermedad"]
df_user = cargar_datos(USER_DB, cols_user)

cols_ep = ["Fecha_Inicio", "Hora_Inicio", "Fecha_Termino", "Hora_Termino", "Sintomas", "Malestar_Inicio", "Malestar_Termino", "Medicamento", "Puffs", "Ubicacion", "Observaciones"]
df_ep = cargar_datos(EPISODES_DB, cols_ep)

# --- 4. NAVEGACIÓN PRINCIPAL POR PESTAÑAS (TABS) ---
tab_reg, tab_bit, tab_per = st.tabs([txt["tab_registro"], txt["tab_bitacora"], txt["tab_perfil"]])

# ==================== PESTAÑA 1: REGISTRO DE CRISIS ====================
with tab_reg:
    # Botón rápido superior de Inicio
    if st.button(txt["btn_inicio_ahora"], key="btn_now_in"):
        ahora = obtener_ahora_chile()
        st.session_state["hora_inicio_auto"] = ahora.time()
        st.session_state["fecha_inicio_auto"] = ahora.date()
        st.toast("🟢 Hora de inicio capturada con éxito", icon="⏱️")

    with st.form("form_episodio", clear_on_submit=False):
        st.markdown("### ⏱️ Inicio del Evento")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            f_in = st.date_input("Fecha Inicio", st.session_state["fecha_inicio_auto"])
            h_in = st.time_input("Hora Inicio", st.session_state["hora_inicio_auto"])
        with col_t2:
            m_in = st.slider(txt["malestar_in"], 1, 10, value=5)

        st.markdown("---")
        sintomas_sel = st.multiselect(
            txt["sintoma"], 
            options=txt["sintomas_lista"],
            default=[txt["sintomas_lista"][0]]
        )

        st.markdown("---")
        st.markdown(f"### {txt['med_tit']}")
        med = st.selectbox("Medicamento", ["Salbutamol / Rescate", "Inhalador Corticoide", "Corticoide Oral", "Ninguno", "Otro"])
        puffs = st.radio(txt["puffs"], ["0", "1 Puff", "2 Puffs", "3+ Puffs"], horizontal=True, index=2)
        ubicacion = st.text_input(txt["ubicacion"], value="Casa / Habitación")

        st.markdown("---")
        st.markdown("### 🩵 Término del Evento")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f_fi = st.date_input("Fecha Término", st.session_state["fecha_termino_auto"])
            h_fi = st.time_input("Hora Término", st.session_state["hora_termino_auto"])
        with col_f2:
            m_fi = st.slider(txt["malestar_fi"], 1, 10, value=2)

        obs = st.text_area(txt["obs"], placeholder="Escribe notas relevantes aquí...")

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
            st.success("¡Episodio registrado en la bitácora!")
            st.rerun()

    # Botón rápido inferior de Término
    if st.button(txt["btn_termino_ahora"], key="btn_now_fi"):
        ahora = obtener_ahora_chile()
        st.session_state["hora_termino_auto"] = ahora.time()
        st.session_state["fecha_termino_auto"] = ahora.date()
        st.toast("🩵 Hora de término capturada con éxito", icon="✨")

# ==================== PESTAÑA 2: BITÁCORA Y MÉTRICAS ====================
with tab_bit:
    if not df_ep.empty:
        # Métricas rápidas (KPIs)
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        with col_kpi1:
            st.metric("Total Episodios", len(df_ep))
        with col_kpi2:
            st.metric("Último Medicamento", df_ep["Medicamento"].iloc[-1].split('/')[0])
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
        st.success(f"**Paciente registrado:** {df_user['Nombre'].iloc[0]} | **Diagnóstico:** {df_user['Enfermedad'].iloc[0]}")
