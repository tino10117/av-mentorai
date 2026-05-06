# =========================================
# AV MentorAI - VERSION DEMO PRIVADA COMPLETA
# =========================================

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import hashlib
import random
from datetime import date
import pandas as pd
import html
import uuid

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

APP_NAME = "AV MentorAI"
APP_TAGLINE = "Tu mentor personal premium para negocios, ventas y crecimiento."

DATA_DIR = "usuarios_av_mentorai"
os.makedirs(DATA_DIR, exist_ok=True)

MODO_DEV = True
APP_VERSION = "Demo privada v1.0"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚡",
    layout="wide"
)

# =========================================
# CSS RESPONSIVE PREMIUM
# =========================================

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1f2937 0%, #0b1120 45%, #020617 100%);
    color: white;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 6rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #111827 100%);
}

h1, h2, h3, h4, p, label, span {
    color: #f8fafc !important;
}

.av-logo {
    font-size: 52px;
    font-weight: 900;
    background: linear-gradient(90deg, #facc15, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.av-subtitle {
    font-size: 18px;
    color: #cbd5e1 !important;
    margin-bottom: 14px;
}

.hero-card, .card, .metric-card, .plan-card, .challenge-card {
    background: rgba(15, 23, 42, 0.88);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0px 12px 32px rgba(0,0,0,0.30);
    margin-bottom: 16px;
}

.hero-card {
    background: linear-gradient(135deg, rgba(250,204,21,0.16), rgba(56,189,248,0.10));
    border: 1px solid rgba(250,204,21,0.35);
}

.metric-card {
    text-align: center;
}

.challenge-card {
    background: linear-gradient(135deg, rgba(249,115,22,0.18), rgba(250,204,21,0.10));
    border: 1px solid rgba(250,204,21,0.45);
}

.chat-user {
    background: rgba(30, 41, 59, 0.95);
    border-left: 5px solid #facc15;
    padding: 18px;
    border-radius: 20px;
    margin-bottom: 16px;
}

.chat-ai {
    background: rgba(15, 23, 42, 0.96);
    border-left: 5px solid #38bdf8;
    padding: 18px;
    border-radius: 20px;
    margin-bottom: 16px;
}

.chat-name {
    font-weight: 900;
    color: #facc15 !important;
    margin-bottom: 8px;
}

.chat-text {
    color: #f8fafc !important;
    line-height: 1.6;
    font-size: 16px;
}

.badge {
    display: inline-block;
    background: linear-gradient(90deg, #facc15, #f97316);
    color: #111827 !important;
    padding: 8px 13px;
    border-radius: 15px;
    font-weight: 800;
    margin: 4px;
    font-size: 14px;
}

.small-text {
    color: #cbd5e1 !important;
    font-size: 15px;
}

.stButton>button {
    border-radius: 14px;
    border: 1px solid rgba(250,204,21,0.45);
    background: linear-gradient(90deg, #facc15, #f97316);
    color: #111827;
    font-weight: 800;
}

.stTextInput input, .stTextArea textarea {
    background-color: #0f172a !important;
    color: #f8fafc !important;
    border-radius: 14px !important;
    border: 1px solid rgba(250,204,21,0.35) !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #0f172a !important;
    color: #f8fafc !important;
    border: 1px solid rgba(250,204,21,0.35) !important;
    border-radius: 16px !important;
}

/* CELULAR */
@media (max-width: 768px) {
    .av-logo {
        font-size: 36px;
    }

    .av-subtitle {
        font-size: 15px;
    }

    .hero-card, .card, .metric-card, .plan-card, .challenge-card {
        padding: 16px;
        border-radius: 18px;
    }

    .chat-text {
        font-size: 15px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================
# USUARIOS
# =========================================

def limpiar_email(email):
    return email.lower().strip().replace("@", "_at_").replace(".", "_")

def archivo_usuario(email):
    return os.path.join(DATA_DIR, f"{limpiar_email(email)}.json")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def usuario_default(nombre, email, password):
    return {
        "nombre": nombre,
        "email": email,
        "password": hash_password(password),
        "password_hash": hash_password(password),
        "plan": "Gratis",

        "xp": 0,
        "racha": 0,
        "messages": [],
        "memoria_larga": [],

        "onboarding_completo": False,
        "objetivo": "",
        "negocio": "",
        "tipo_negocio": "",
        "nivel_usuario": "Principiante",
        "tiempo_diario": "",
        "principal_dificultad": "",

        "meta_mensual": "",
        "ingresos_objetivo": 0,
        "habito_clave": "",

        "desafios_completados": 0,
        "objetivos_completados": 0,
        "logros": [],
        "xp_history": [],

        "ultima_fecha": "",
        "fecha_desafio": "",
        "desafio_actual": "",
        "preguntas_hoy": 0,
        "fecha_preguntas": "",

        "feedback": []
    }

def guardar_usuario(data):
    with open(archivo_usuario(data["email"]), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def cargar_usuario(email):
    path = archivo_usuario(email)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        default = usuario_default(
            data.get("nombre", ""),
            data.get("email", email),
            "123456"
        )

        for key, value in default.items():
            if key not in data:
                data[key] = value

        return data

    return None

def crear_usuario(nombre, email, password):
    if cargar_usuario(email):
        return False

    data = usuario_default(nombre, email, password)
    guardar_usuario(data)
    return True

def login(email, password):
    user = cargar_usuario(email)

    if not user:
        return None

    password_guardada = user.get("password") or user.get("password_hash")

    if password_guardada == hash_password(password):
        return user

    return None

# =========================================
# FUNCIONES APP
# =========================================

def calcular_nivel(xp):
    if xp < 100:
        return "Nivel 1 - Inicial"
    if xp < 300:
        return "Nivel 2 - En crecimiento"
    if xp < 700:
        return "Nivel 3 - Estratega"
    if xp < 1200:
        return "Nivel 4 - Empresario Pro"
    return "Nivel 5 - Élite"

def progreso_nivel(xp):
    if xp < 100:
        return xp / 100
    if xp < 300:
        return (xp - 100) / 200
    if xp < 700:
        return (xp - 300) / 400
    if xp < 1200:
        return (xp - 700) / 500
    return 1

def desbloquear_logros(user):
    reglas = [
        (user["xp"] >= 100, "Primeros 100 XP"),
        (user["xp"] >= 300, "Mente en crecimiento"),
        (user["xp"] >= 700, "Estratega en formación"),
        (user["racha"] >= 3, "Racha de 3 días"),
        (user["racha"] >= 7, "Semana imparable"),
        (user["desafios_completados"] >= 5, "5 desafíos completados"),
        (user["objetivos_completados"] >= 3, "Constructor de objetivos")
    ]

    for condicion, logro in reglas:
        if condicion and logro not in user["logros"]:
            user["logros"].append(logro)

def sumar_xp(cantidad):
    user = st.session_state.user_data
    user["xp"] += cantidad

    hoy = str(date.today())

    if user.get("ultima_fecha", "") != hoy:
        user["racha"] += 1
        user["ultima_fecha"] = hoy

    user["xp_history"].append({
        "fecha": hoy,
        "xp": user["xp"]
    })

    desbloquear_logros(user)
    guardar_usuario(user)

def generar_desafio(user):
    desafios = [
        "Mandá mensajes a 3 clientes potenciales.",
        "Publicá un producto o servicio hoy.",
        "Analizá un negocio local y anotá qué harías mejor.",
        "Pensá una oferta irresistible: producto + beneficio + urgencia.",
        "Grabá un video corto vendiendo algo.",
        "Diseñá una promoción simple por WhatsApp.",
        "Buscá 3 competidores en Instagram y analizá qué hacen bien.",
        "Mejorá la descripción de un producto o servicio.",
        "Creá una lista de 10 productos o servicios que podrías vender.",
        "Armá una estrategia para vender más sin bajar demasiado el margen."
    ]

    hoy = str(date.today())

    if user.get("fecha_desafio", "") != hoy:
        user["desafio_actual"] = random.choice(desafios)
        user["fecha_desafio"] = hoy
        guardar_usuario(user)

    return user["desafio_actual"]

def transcribir_audio(audio_file):
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text

def generar_voz(texto):
    audio_path = f"respuesta_av_mentorai_{uuid.uuid4().hex}.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=texto[:1200]
    ) as response:
        response.stream_to_file(audio_path)

    return audio_path

def render_chat_message(role, content):
    safe_content = content

    if role == "user":
        name = "Vos"
        css_class = "chat-user"
    else:
        name = "AV MentorAI"
        css_class = "chat-ai"

    st.markdown(f"""
    <div class="{css_class}">
        <div class="chat-name">{name}</div>
        <div class="chat-text">{safe_content}</div>
    </div>
    """, unsafe_allow_html=True)

def obtener_ultima_respuesta(user):
    for msg in reversed(user["messages"]):
        if msg["role"] == "assistant":
            return msg["content"]
    return None

def crear_system_prompt(user, modo, desafio):
    memoria_larga = "\n".join(user.get("memoria_larga", [])[-10:])

    return f"""
    Eres AV MentorAI, un mentor personal premium de negocios, ventas, marketing y disciplina.

    Datos del usuario:
    Nombre: {user["nombre"]}
    Email: {user["email"]}
    Plan: {user["plan"]}
    Objetivo principal: {user["objetivo"]}
    Negocio o idea: {user["negocio"]}
    Tipo de negocio: {user["tipo_negocio"]}
    Nivel del usuario: {user["nivel_usuario"]}
    Tiempo diario disponible: {user["tiempo_diario"]}
    Principal dificultad: {user["principal_dificultad"]}
    XP: {user["xp"]}
    Racha: {user["racha"]}
    Desafíos completados: {user["desafios_completados"]}
    Objetivos completados: {user["objetivos_completados"]}
    Meta mensual: {user["meta_mensual"]}
    Objetivo de ingresos: {user["ingresos_objetivo"]}
    Hábito clave: {user["habito_clave"]}
    Modo actual: {modo}
    Desafío diario actual: {desafio}

    Memoria importante:
    {memoria_larga}

    Identidad:
    - Tu nombre es AV MentorAI.
    - Sos moderno, directo, motivador y estratégico.
    - Sonás como mentor real, no como IA genérica.
    - Tenés personalidad fuerte, pero positiva.
    - Usás frases propias como:
      "No lo pienses tanto, ejecutalo."
      "La claridad aparece cuando te movés."
      "El negocio no premia al que sabe más, premia al que acciona mejor."

    Estilo:
    - Español latino.
    - Claro, humano y práctico.
    - No des respuestas eternas.
    - Usá ejemplos de WhatsApp, Instagram, TikTok, Mercado Libre, kioscos, supermercados, comida, ropa, servicios y reventa.
    - Si hace falta, sé exigente y directo.
    - Siempre terminá con una acción concreta para hacer HOY.

    Especialidades:
    - Si el modo es Especialista Supermercados, enfocáte en stock, rotación, ventas, compras, márgenes y clientes.
    - Si el modo es Especialista E-commerce, enfocáte en tienda online, fotos, catálogo, conversión y redes.
    - Si el modo es Especialista Reventa, enfocáte en comprar barato, vender con margen y conseguir clientes.
    - Si el modo es Especialista Restaurante, enfocáte en menú, costos, delivery, rotación y experiencia.
    - Si el modo es Especialista Inmobiliaria, enfocáte en captación, negociación, objeciones y cierres.
    - Si el modo es Simulación con Cliente Difícil, actuá como cliente complicado, con objeciones reales.
    - Si el modo es Modo Empresario Exigente, sé más duro, directo y desafiante.
    - Si el modo es Modo Mentor Millonario, hablá con visión grande, mentalidad de crecimiento y estrategia.
    """

def generar_resumen_inteligente(user):
    if not user["messages"]:
        return "Todavía no hay suficiente conversación para crear una memoria inteligente."

    ultimos = user["messages"][-8:]

    texto = "\n".join([
        f'{m["role"]}: {m["content"]}'
        for m in ultimos
    ])

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Resume datos importantes del usuario para memoria futura. Sé breve y práctico."
                },
                {
                    "role": "user",
                    "content": texto
                }
            ]
        )

        resumen = response.choices[0].message.content
        user["memoria_larga"].append(resumen)
        guardar_usuario(user)
        return resumen

    except Exception as e:
        return f"No se pudo generar memoria inteligente: {e}"

def render_audio_player(texto):
    try:
        audio_path = generar_voz(texto)

        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mpeg")

        st.download_button(
            "⬇️ Descargar audio",
            data=audio_bytes,
            file_name="respuesta_av_mentorai.mp3",
            mime="audio/mpeg"
        )

    except Exception as e:
        st.warning(f"No se pudo generar el audio: {e}")

        # =========================================
# LOGIN / LANDING
# =========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown(f"""
    <div class="hero-card">
        <div class="av-logo">{APP_NAME}</div>
        <div class="av-subtitle">{APP_TAGLINE}</div>
        <p class="small-text">
        Aprendé negocios, ventas, marketing y disciplina con un mentor de IA personalizado.
        </p>
        <p class="small-text"><b>{APP_VERSION}</b></p>
    </div>
    """, unsafe_allow_html=True)

    l1, l2, l3 = st.columns(3)

    with l1:
        st.markdown("""
        <div class="card">
            <h3>🧠 Mentor personalizado</h3>
            <p class="small-text">Consejos según tu objetivo, negocio y nivel.</p>
        </div>
        """, unsafe_allow_html=True)

    with l2:
        st.markdown("""
        <div class="card">
            <h3>🔥 Desafíos diarios</h3>
            <p class="small-text">Ganá XP, mantené racha y avanzá todos los días.</p>
        </div>
        """, unsafe_allow_html=True)

    with l3:
        st.markdown("""
        <div class="card">
            <h3>💎 Premium</h3>
            <p class="small-text">Funciones avanzadas, voz, memoria profunda y más.</p>
        </div>
        """, unsafe_allow_html=True)

    login_tab, register_tab = st.tabs([
        "Iniciar sesión",
        "Crear cuenta"
    ])

    with login_tab:
        email_login = st.text_input("Gmail", placeholder="tuemail@gmail.com")
        password_login = st.text_input("Contraseña", type="password")

        if st.button("Entrar"):
            user_login = login(email_login, password_login)

            if user_login:
                st.session_state.logged_in = True
                st.session_state.user_data = user_login
                st.rerun()
            else:
                st.error("Gmail o contraseña incorrectos.")

    with register_tab:
        nombre_reg = st.text_input("Nombre", placeholder="Valentino")
        email_reg = st.text_input("Gmail para crear cuenta", placeholder="tuemail@gmail.com")
        password_reg = st.text_input("Crear contraseña", type="password")

        if st.button("Crear cuenta"):
            if not nombre_reg or not email_reg or not password_reg:
                st.warning("Completá todos los campos.")
            elif "@gmail.com" not in email_reg.lower():
                st.warning("Usá un Gmail válido.")
            elif len(password_reg) < 6:
                st.warning("La contraseña debe tener al menos 6 caracteres.")
            else:
                ok = crear_usuario(nombre_reg, email_reg, password_reg)

                if ok:
                    st.success("Cuenta creada. Ahora iniciá sesión.")
                else:
                    st.error("Ese Gmail ya existe.")

    st.stop()

# =========================================
# USER
# =========================================

user = st.session_state.user_data

default_user = usuario_default(
    user.get("nombre", ""),
    user.get("email", ""),
    "123456"
)

for key, value in default_user.items():
    if key not in user:
        user[key] = value

guardar_usuario(user)

desafio = generar_desafio(user)

hoy = str(date.today())

if user.get("fecha_preguntas", "") != hoy:
    user["fecha_preguntas"] = hoy
    user["preguntas_hoy"] = 0
    guardar_usuario(user)

if "modo" not in st.session_state:
    st.session_state.modo = "Mentor de Negocios"

# =========================================
# ONBOARDING INICIAL
# =========================================

if not user.get("onboarding_completo", False):

    st.markdown(f"""
    <div class="hero-card">
        <div class="av-logo">{APP_NAME}</div>
        <div class="av-subtitle">Configurá tu mentor en 1 minuto</div>
        <p class="small-text">
        Esto ayuda a que AV MentorAI te responda de forma más personalizada.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user["objetivo"] = st.text_area(
        "¿Cuál es tu objetivo principal?",
        value=user["objetivo"],
        placeholder="Ej: vender más, crear un negocio, mejorar mi disciplina..."
    )

    user["negocio"] = st.text_input(
        "¿Tenés un negocio o idea?",
        value=user["negocio"],
        placeholder="Ej: tienda de ropa, supermercado, ecommerce, todavía no tengo..."
    )

    user["tipo_negocio"] = st.selectbox(
        "Tipo de negocio o interés:",
        [
            "Todavía no tengo negocio",
            "Supermercado / mayorista",
            "E-commerce",
            "Reventa",
            "Restaurante / comida",
            "Servicios",
            "Inmobiliaria",
            "Otro"
        ],
        index=[
            "Todavía no tengo negocio",
            "Supermercado / mayorista",
            "E-commerce",
            "Reventa",
            "Restaurante / comida",
            "Servicios",
            "Inmobiliaria",
            "Otro"
        ].index(user["tipo_negocio"]) if user["tipo_negocio"] in [
            "Todavía no tengo negocio",
            "Supermercado / mayorista",
            "E-commerce",
            "Reventa",
            "Restaurante / comida",
            "Servicios",
            "Inmobiliaria",
            "Otro"
        ] else 0
    )

    user["nivel_usuario"] = st.selectbox(
        "Tu nivel actual:",
        ["Principiante", "Intermedio", "Avanzado"],
        index=["Principiante", "Intermedio", "Avanzado"].index(user["nivel_usuario"])
    )

    user["tiempo_diario"] = st.selectbox(
        "¿Cuánto tiempo podés dedicar por día?",
        ["15 minutos", "30 minutos", "1 hora", "Más de 1 hora"],
        index=["15 minutos", "30 minutos", "1 hora", "Más de 1 hora"].index(user["tiempo_diario"]) if user["tiempo_diario"] in ["15 minutos", "30 minutos", "1 hora", "Más de 1 hora"] else 0
    )

    user["principal_dificultad"] = st.text_area(
        "¿Qué es lo que más te cuesta hoy?",
        value=user["principal_dificultad"],
        placeholder="Ej: vender, organizarme, conseguir clientes, crear contenido..."
    )

    if st.button("🚀 Entrar a AV MentorAI"):
        user["onboarding_completo"] = True
        guardar_usuario(user)
        st.rerun()

    st.stop()

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.markdown(f"## ⚡ {APP_NAME}")
    st.caption(user["email"])
    st.caption(APP_VERSION)

    if st.button("🚪 Cerrar sesión"):
        guardar_usuario(user)
        st.session_state.logged_in = False
        st.rerun()

    st.divider()

    st.session_state.modo = st.selectbox(
        "Modo del mentor:",
        [
            "Mentor de Negocios",
            "Entrenador de Ventas",
            "Marketing LATAM",
            "Disciplina y Hábitos",
            "Ideas de Negocio",
            "Simulación con Cliente Difícil",
            "Planificador de Objetivos",
            "Modo Empresario Exigente",
            "Modo Mentor Millonario",
            "Especialista Supermercados",
            "Especialista E-commerce",
            "Especialista Reventa",
            "Especialista Restaurante",
            "Especialista Inmobiliaria"
        ]
    )

    st.divider()

    st.markdown("### 🧠 Memoria")

    user["nombre"] = st.text_input(
        "Tu nombre:",
        value=user["nombre"]
    )

    user["objetivo"] = st.text_area(
        "Objetivo principal:",
        value=user["objetivo"]
    )

    user["negocio"] = st.text_input(
        "Tu negocio o idea:",
        value=user["negocio"]
    )

    user["tipo_negocio"] = st.text_input(
        "Tipo de negocio:",
        value=user["tipo_negocio"]
    )

    st.divider()

    st.markdown("### 📊 Panel empresario")

    user["meta_mensual"] = st.text_input(
        "Meta mensual:",
        value=user["meta_mensual"],
        placeholder="Ej: conseguir 20 clientes"
    )

    user["ingresos_objetivo"] = st.number_input(
        "Objetivo de ingresos:",
        value=int(user["ingresos_objetivo"]),
        min_value=0
    )

    user["habito_clave"] = st.text_input(
        "Hábito clave:",
        value=user["habito_clave"],
        placeholder="Ej: vender 1 hora por día"
    )

    if st.button("💾 Guardar datos"):
        guardar_usuario(user)
        st.success("Datos guardados.")

    if st.button("🧹 Borrar conversación"):
        user["messages"] = []
        guardar_usuario(user)
        st.rerun()

    if st.button("🔁 Rehacer onboarding"):
        user["onboarding_completo"] = False
        guardar_usuario(user)
        st.rerun()

# =========================================
# HEADER / DASHBOARD
# =========================================

st.markdown(f"""
<div class="hero-card">
    <div class="av-logo">{APP_NAME}</div>
    <div class="av-subtitle">{APP_TAGLINE}</div>
    <p class="small-text"><b>{APP_VERSION}</b></p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown(f"""
    <div class="metric-card">
    <h3>👤 Usuario</h3>
    <h2>{user["nombre"]}</h2>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
    <h3>⭐ XP</h3>
    <h2>{user["xp"]}</h2>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
    <h3>🔥 Racha</h3>
    <h2>{user["racha"]} días</h2>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
    <h3>📈 Nivel</h3>
    <h2>{calcular_nivel(user["xp"])}</h2>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class="metric-card">
    <h3>💎 Plan</h3>
    <h2>{user["plan"]}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Progreso al próximo nivel")
st.progress(progreso_nivel(user["xp"]))

# =========================================
# TABS PRINCIPALES
# =========================================

tab_mentor, tab_progreso, tab_desafios, tab_premium, tab_ranking, tab_feedback = st.tabs([
    "🧠 Mentor",
    "📈 Progreso",
    "🔥 Desafíos",
    "💎 Premium",
    "🏆 Ranking",
    "💬 Feedback"
])

# =========================================
# TAB MENTOR
# =========================================

with tab_mentor:

    st.markdown("## 🧠 Chat principal")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    quick_prompt = None

    with c1:
        if st.button("💡 Idea"):
            quick_prompt = "Dame una idea de negocio rentable para empezar con pocos recursos."

    with c2:
        if st.button("📈 Vender"):
            quick_prompt = "Quiero vender más. Dame un plan práctico."

    with c3:
        if st.button("📱 Marketing"):
            quick_prompt = "Quiero aprender marketing desde cero para vender por redes sociales."

    with c4:
        if st.button("🎭 Cliente difícil"):
            quick_prompt = "Hagamos una simulación. Vos sos un cliente difícil y yo tengo que venderte."

    with c5:
        if st.button("🔥 Desafío"):
            quick_prompt = f"Quiero hacer este desafío diario: {desafio}. Guiame paso a paso."

    with c6:
        if st.button("💎 Mentor fuerte"):
            quick_prompt = "Háblame como mentor exigente y dime qué debería mejorar hoy."

    st.write("")

    audio = st.audio_input("🎤 Grabá tu pregunta por voz")
    voice_prompt = None

    if audio:
        with st.spinner("Transcribiendo audio..."):
            try:
                voice_prompt = transcribir_audio(audio)
                st.success(f"Escuché: {voice_prompt}")
            except Exception as e:
                st.warning(f"No pude transcribir el audio: {e}")

    st.write("")
    st.markdown("### Conversación")

    for msg in user["messages"]:
        render_chat_message(msg["role"], msg["content"])

    ultima_respuesta_audio = obtener_ultima_respuesta(user)

    if ultima_respuesta_audio:
        if st.button("🔊 Escuchar última respuesta"):
            render_audio_player(ultima_respuesta_audio)

    user_input = st.chat_input("Escribí tu pregunta...")

    if quick_prompt:
        user_input = quick_prompt

    if voice_prompt:
        user_input = voice_prompt

    if user_input:

        if "last_prompt" not in st.session_state:
            st.session_state.last_prompt = ""

        if user_input == st.session_state.last_prompt:
            st.stop()

        st.session_state.last_prompt = user_input

        if not MODO_DEV:
            if user["plan"] == "Gratis" and user["preguntas_hoy"] >= 10:
                st.warning("Llegaste al límite diario del plan Gratis. Activá Premium demo para seguir.")
                st.stop()

        user["preguntas_hoy"] += 1

        user["messages"].append({
            "role": "user",
            "content": user_input
        })

        user["memoria_larga"].append(f"El usuario dijo: {user_input}")

        sumar_xp(10)

        with st.spinner("AV MentorAI está pensando..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": crear_system_prompt(
                                user,
                                st.session_state.modo,
                                desafio
                            )
                        },
                        *user["messages"]
                    ],
                    temperature=0.85
                )

                respuesta = response.choices[0].message.content

            except Exception as e:
                respuesta = f"Hubo un problema de conexión con OpenAI: {e}"

        user["messages"].append({
            "role": "assistant",
            "content": respuesta
        })

        guardar_usuario(user)

        render_chat_message("assistant", respuesta)

        st.info("Respuesta guardada. Tocá “🔊 Escuchar última respuesta” para generar audio.")
if st.button("🔊 Escuchar última respuesta", key="audio_btn"):
    try:
        audio_path = generar_audio_openai(respuesta)

        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")

    except Exception as e:
        st.error(f"Error audio: {e}")
# =========================================
# TAB PROGRESO
# =========================================

with tab_progreso:

    st.markdown("## 📈 Progreso y hábitos")

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown(f"""
        <div class="metric-card">
        <h3>⭐ XP total</h3>
        <h2>{user["xp"]}</h2>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown(f"""
        <div class="metric-card">
        <h3>🔥 Racha</h3>
        <h2>{user["racha"]} días</h2>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown(f"""
        <div class="metric-card">
        <h3>🎯 Objetivos</h3>
        <h2>{user["objetivos_completados"]}</h2>
        </div>
        """, unsafe_allow_html=True)

    if user["xp_history"]:
        df_xp = pd.DataFrame(user["xp_history"])
        st.line_chart(df_xp.set_index("fecha")["xp"])
    else:
        st.info("Todavía no hay progreso suficiente.")

    if st.button("🧠 Generar memoria inteligente"):
        resumen = generar_resumen_inteligente(user)
        st.success(resumen)

    if user["logros"]:
        st.markdown("### 🏆 Logros desbloqueados")
        st.markdown(
            "".join([f'<span class="badge">🏆 {logro}</span>' for logro in user["logros"]]),
            unsafe_allow_html=True
        )

    st.markdown("### 📊 Panel empresario")

    st.markdown(f"""
    <div class="card">
        <p><b>Meta mensual:</b> {user["meta_mensual"] or "Sin definir"}</p>
        <p><b>Objetivo de ingresos:</b> ${user["ingresos_objetivo"]}</p>
        <p><b>Hábito clave:</b> {user["habito_clave"] or "Sin definir"}</p>
        <p><b>Tipo de negocio:</b> {user["tipo_negocio"] or "Sin definir"}</p>
        <p><b>Principal dificultad:</b> {user["principal_dificultad"] or "Sin definir"}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# TAB DESAFÍOS
# =========================================

with tab_desafios:

    st.markdown("## 🔥 Desafío diario")

    st.markdown(f"""
    <div class="challenge-card">
        <h2>Tu misión de hoy</h2>
        <h3>{desafio}</h3>
        <p class="small-text">Completarlo suma XP, mejora tu racha y te mantiene en movimiento.</p>
    </div>
    """, unsafe_allow_html=True)

    d1, d2 = st.columns(2)

    with d1:
        if st.button("✅ Completé el desafío"):
            user["desafios_completados"] += 1
            sumar_xp(40)
            guardar_usuario(user)
            st.success("Desafío completado. Sumaste 40 XP.")
            st.rerun()

    with d2:
        if st.button("🎯 Marcar objetivo completado"):
            user["objetivos_completados"] += 1
            sumar_xp(60)
            guardar_usuario(user)
            st.success("Objetivo completado. Sumaste 60 XP.")
            st.rerun()

    st.markdown("### Estado actual")

    st.markdown(f"""
    <div class="card">
        <p><b>Desafíos completados:</b> {user["desafios_completados"]}</p>
        <p><b>Objetivos completados:</b> {user["objetivos_completados"]}</p>
        <p><b>Racha actual:</b> {user["racha"]} días</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# TAB PREMIUM
# =========================================

with tab_premium:

    st.markdown("## 💎 Planes y pagos")

    plan1, plan2, plan3 = st.columns(3)

    with plan1:
        st.markdown("""
        <div class="plan-card">
            <h2>Gratis</h2>
            <p>✅ Mentor básico</p>
            <p>✅ Desafíos diarios</p>
            <p>✅ XP y racha</p>
            <p>⚠️ 10 preguntas por día</p>
            <h1>$0</h1>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Usar Gratis"):
            user["plan"] = "Gratis"
            guardar_usuario(user)
            st.rerun()

    with plan2:
        st.markdown("""
        <div class="plan-card">
            <h2>Pro</h2>
            <p>🚀 Mentor ilimitado</p>
            <p>🔊 Voz premium</p>
            <p>🧠 Memoria profunda</p>
            <p>📊 Panel avanzado</p>
            <h1>$4.99 USD</h1>
        </div>
        """, unsafe_allow_html=True)

        if st.button("💳 Activar Pro demo"):
            user["plan"] = "Premium"
            guardar_usuario(user)
            st.success("Plan Pro activado en modo demo.")
            st.rerun()

    with plan3:
        st.markdown("""
        <div class="plan-card">
            <h2>Empresarial 🔒</h2>
            <p>🏢 Para equipos</p>
            <p>📈 Métricas de negocio</p>
            <p>📂 Carga de archivos</p>
            <p>🤖 IA personalizada</p>
            <h1>Consultar</h1>
        </div>
        """, unsafe_allow_html=True)

        st.info("Más adelante se puede conectar con Mercado Pago o Stripe.")

    st.markdown("### Estado de tu plan")

    st.markdown(f"""
    <div class="card">
        <p><b>Plan actual:</b> {user["plan"]}</p>
        <p><b>Preguntas usadas hoy:</b> {user["preguntas_hoy"]}</p>
        <p><b>Modo desarrollo:</b> {"Activado" if MODO_DEV else "Desactivado"}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# TAB RANKING
# =========================================

with tab_ranking:

    st.markdown("## 🏆 Ranking demo")

    ranking = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".json"):
            try:
                with open(
                    os.path.join(DATA_DIR, file),
                    "r",
                    encoding="utf-8"
                ) as f:
                    u = json.load(f)

                    ranking.append({
                        "Usuario": u.get("nombre", "Usuario"),
                        "XP": u.get("xp", 0),
                        "Racha": u.get("racha", 0),
                        "Plan": u.get("plan", "Gratis")
                    })

            except Exception:
                pass

    ranking = sorted(ranking, key=lambda x: x["XP"], reverse=True)

    if ranking:
        df_ranking = pd.DataFrame(ranking)
        st.dataframe(df_ranking, width="stretch")
    else:
        st.info("Todavía no hay usuarios en el ranking.")

# =========================================
# TAB FEEDBACK
# =========================================

with tab_feedback:

    st.markdown("## 💬 Feedback de usuarios")

    st.info("Esta sección sirve para probar la app con amigos, familiares o vendedores y guardar opiniones.")

    calificacion = st.slider("¿Qué tan útil te parece AV MentorAI?", 1, 10, 8)

    comentario = st.text_area(
        "Comentario:",
        placeholder="Ej: qué te gustó, qué te confundió, qué pagarías, qué mejorarías..."
    )

    pagaria = st.selectbox(
        "¿Pagarías por usar esta app?",
        ["No sé", "Sí", "No"]
    )

    if st.button("Enviar feedback"):
        user["feedback"].append({
            "fecha": str(date.today()),
            "calificacion": calificacion,
            "comentario": comentario,
            "pagaria": pagaria
        })

        guardar_usuario(user)
        st.success("Feedback guardado. Esto te sirve para validar la app.")

    if user["feedback"]:
        st.markdown("### Feedback guardado")

        df_feedback = pd.DataFrame(user["feedback"])
        st.dataframe(df_feedback, width="stretch")
