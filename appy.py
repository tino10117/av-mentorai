# =========================================
# AV MentorAI - VERSION DEMO PRIVADA COMPLETA v2.0
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
import uuid
import base64

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

APP_NAME = "AV MentorAI"
APP_TAGLINE = "Tu mentor personal premium para negocios, ventas y crecimiento."

DATA_DIR = "usuarios_av_mentorai"
os.makedirs(DATA_DIR, exist_ok=True)

MODO_DEV = True
APP_VERSION = "Demo privada v2.0"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚡",
    layout="wide"
)

# =========================================
# CSS
# =========================================

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: radial-gradient(circle at top left, #1f2937 0%, #0b1120 45%, #020617 100%);
    color: white;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 5rem;
    max-width: 860px;
}

h1, h2, h3, h4, p, label, span {
    color: #f8fafc !important;
}

.av-logo {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(90deg, #facc15, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.av-subtitle {
    font-size: 16px;
    color: #cbd5e1 !important;
    margin-bottom: 10px;
}

.hero-card, .card, .plan-card, .challenge-card {
    background: rgba(15, 23, 42, 0.88);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.30);
    margin-bottom: 14px;
}

.hero-card {
    background: linear-gradient(135deg, rgba(250,204,21,0.16), rgba(56,189,248,0.10));
    border: 1px solid rgba(250,204,21,0.35);
    padding: 16px 20px;
}

.challenge-card {
    background: linear-gradient(135deg, rgba(249,115,22,0.18), rgba(250,204,21,0.10));
    border: 1px solid rgba(250,204,21,0.45);
}

/* MÉTRICAS COMPACTAS */
.metrics-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 14px;
}

.metric-chip {
    background: rgba(15, 23, 42, 0.88);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 14px;
    padding: 8px 14px;
    text-align: center;
    flex: 1;
    min-width: 70px;
}

.metric-chip .metric-label {
    font-size: 11px;
    color: #94a3b8 !important;
    margin: 0;
}

.metric-chip .metric-value {
    font-size: 16px;
    font-weight: 800;
    color: #facc15 !important;
    margin: 2px 0 0 0;
}

/* CHAT */
.chat-user {
    background: rgba(30, 41, 59, 0.95);
    border-left: 4px solid #facc15;
    padding: 14px 16px;
    border-radius: 16px;
    margin-bottom: 12px;
}

.chat-ai {
    background: rgba(15, 23, 42, 0.96);
    border-left: 4px solid #38bdf8;
    padding: 14px 16px;
    border-radius: 16px;
    margin-bottom: 12px;
}

.chat-name {
    font-weight: 900;
    font-size: 13px;
    color: #facc15 !important;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.chat-name-ai {
    font-weight: 900;
    font-size: 13px;
    color: #38bdf8 !important;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.chat-text {
    color: #f1f5f9 !important;
    line-height: 1.65;
    font-size: 15px;
    white-space: pre-wrap;
}

.badge {
    display: inline-block;
    background: linear-gradient(90deg, #facc15, #f97316);
    color: #111827 !important;
    padding: 6px 12px;
    border-radius: 12px;
    font-weight: 800;
    margin: 3px;
    font-size: 13px;
}

.small-text {
    color: #cbd5e1 !important;
    font-size: 14px;
}

.guide-text {
    color: #94a3b8 !important;
    font-size: 14px;
    text-align: center;
    padding: 10px;
    border: 1px dashed rgba(148,163,184,0.3);
    border-radius: 12px;
    margin-bottom: 12px;
}

/* BOTONES */
.stButton>button {
    border-radius: 12px;
    border: 1px solid rgba(250,204,21,0.45);
    background: linear-gradient(90deg, #facc15, #f97316);
    color: #111827;
    font-weight: 800;
    font-size: 14px;
}

.stButton>button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

/* INPUTS */
.stTextInput input, .stTextArea textarea {
    background-color: #0f172a !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
    border: 1px solid rgba(250,204,21,0.3) !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #0f172a !important;
    color: #f8fafc !important;
    border: 1px solid rgba(250,204,21,0.35) !important;
    border-radius: 14px !important;
}

/* EXPANDER */
[data-testid="stExpander"] {
    background: rgba(15, 23, 42, 0.88) !important;
    border: 1px solid rgba(250,204,21,0.25) !important;
    border-radius: 16px !important;
}

/* MOBILE */
@media (max-width: 768px) {
    .av-logo { font-size: 32px; }
    .av-subtitle { font-size: 14px; }
    .chat-text { font-size: 14px; }
    .block-container { padding-left: 0.8rem; padding-right: 0.8rem; }
    .metric-chip .metric-value { font-size: 14px; }
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
        default = usuario_default(data.get("nombre", ""), data.get("email", email), "123456")
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
    if xp < 100: return "Nivel 1 - Inicial"
    if xp < 300: return "Nivel 2 - En crecimiento"
    if xp < 700: return "Nivel 3 - Estratega"
    if xp < 1200: return "Nivel 4 - Empresario Pro"
    return "Nivel 5 - Élite"

def progreso_nivel(xp):
    if xp < 100: return xp / 100
    if xp < 300: return (xp - 100) / 200
    if xp < 700: return (xp - 300) / 400
    if xp < 1200: return (xp - 700) / 500
    return 1.0

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
    user["xp_history"].append({"fecha": hoy, "xp": user["xp"]})
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

def plural_dias(n):
    return f"{n} día" if n == 1 else f"{n} días"

def transcribir_audio(audio_file):
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

def generar_audio_bytes(texto):
    audio_path = f"respuesta_av_{uuid.uuid4().hex}.mp3"
    with client.audio.speech.with_streaming_response.create(
        model="tts-1", voice="alloy", input=texto[:1200]
    ) as response:
        response.stream_to_file(audio_path)
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    try:
        os.remove(audio_path)
    except Exception:
        pass
    return audio_bytes

def render_audio_player(texto):
    try:
        audio_bytes = generar_audio_bytes(texto)
        st.audio(audio_bytes, format="audio/mpeg")
        st.download_button("⬇️ Descargar audio", data=audio_bytes,
                           file_name="respuesta_mentor.mp3", mime="audio/mpeg")
    except Exception as e:
        st.warning(f"No se pudo generar el audio: {e}")

def imagen_a_base64(uploaded_file):
    bytes_data = uploaded_file.read()
    b64 = base64.b64encode(bytes_data).decode("utf-8")
    mime = uploaded_file.type
    return b64, mime

def obtener_ultima_respuesta(user):
    for msg in reversed(user["messages"]):
        if msg["role"] == "assistant":
            return msg["content"]
    return None

def crear_system_prompt(user, modo, desafio):
    memoria_larga = "\n".join(user.get("memoria_larga", [])[-6:])
    return f"""
Eres AV MentorAI, un mentor personal premium de negocios, ventas, marketing y disciplina.

Datos del usuario:
Nombre: {user["nombre"]}
Plan: {user["plan"]}
Objetivo principal: {user["objetivo"]}
Negocio o idea: {user["negocio"]}
Tipo de negocio: {user["tipo_negocio"]}
Nivel del usuario: {user["nivel_usuario"]}
Tiempo diario disponible: {user["tiempo_diario"]}
Principal dificultad: {user["principal_dificultad"]}
XP: {user["xp"]} | Racha: {user["racha"]} días
Meta mensual: {user["meta_mensual"]}
Objetivo de ingresos: {user["ingresos_objetivo"]}
Hábito clave: {user["habito_clave"]}
Modo actual: {modo}
Desafío diario: {desafio}

Memoria:
{memoria_larga}

Identidad:
- Sos AV MentorAI: moderno, directo, motivador y estratégico.
- Sonás como mentor real, no como IA genérica.
- Frases propias: "No lo pienses tanto, ejecutalo.", "La claridad aparece cuando te movés.", "El negocio no premia al que sabe más, premia al que acciona mejor."

Estilo:
- Español latino. Claro, humano y práctico.
- Respuestas concretas, no eternas.
- Ejemplos de WhatsApp, Instagram, TikTok, Mercado Libre, kioscos, supermercados, comida, ropa, servicios, reventa.
- Siempre terminá con una acción concreta para hacer HOY.

Si el usuario sube una imagen o archivo:
- Analizá lo que ves con criterio empresarial.
- Identificá oportunidades, problemas o mejoras concretas.
- Sé específico y práctico.

Especialidades según modo:
- Especialista Supermercados: stock, rotación, márgenes, clientes.
- Especialista E-commerce: tienda online, fotos, catálogo, conversión.
- Especialista Reventa: comprar barato, vender con margen, conseguir clientes.
- Especialista Restaurante: menú, costos, delivery, experiencia.
- Especialista Inmobiliaria: captación, negociación, objeciones, cierres.
- Simulación Cliente Difícil: actuá como cliente complicado con objeciones reales.
- Modo Empresario Exigente: más duro, directo y desafiante.
- Modo Mentor Millonario: visión grande, mentalidad de crecimiento y estrategia.
"""

def generar_resumen_inteligente(user):
    if not user["messages"]:
        return "Todavía no hay suficiente conversación para crear una memoria inteligente."
    ultimos = user["messages"][-8:]
    texto = "\n".join([f'{m["role"]}: {m["content"]}' for m in ultimos])
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Resume datos importantes del usuario para memoria futura. Sé breve y práctico."},
                {"role": "user", "content": texto}
            ]
        )
        resumen = response.choices[0].message.content
        user["memoria_larga"].append(resumen)
        if len(user["memoria_larga"]) > 20:
            user["memoria_larga"] = user["memoria_larga"][-20:]
        guardar_usuario(user)
        return resumen
    except Exception as e:
        return f"No se pudo generar memoria inteligente: {e}"

def render_chat_message(role, content):
    if role == "user":
        st.markdown(f"""
        <div class="chat-user">
            <div class="chat-name">Vos</div>
            <div class="chat-text">{content}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-ai">
            <div class="chat-name-ai">⚡ AV MentorAI</div>
            <div class="chat-text">{content}</div>
        </div>""", unsafe_allow_html=True)
        # Botón copiar en cada respuesta del mentor
        st.code(content, language=None)

def enviar_mensaje(user_input, desafio, imagen_b64=None, imagen_mime=None, nombre_archivo=None):
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = ""

    prompt_key = user_input + (imagen_b64[:20] if imagen_b64 else "")
    if prompt_key == st.session_state.last_prompt:
        return
    st.session_state.last_prompt = prompt_key

    if not MODO_DEV:
        if user["plan"] == "Gratis" and user["preguntas_hoy"] >= 10:
            st.warning("Llegaste al límite diario del plan Gratis. Activá Premium para seguir.")
            return

    user = st.session_state.user_data
    user["preguntas_hoy"] += 1

    # Construir contenido del mensaje con imagen si hay
    if imagen_b64 and imagen_mime:
        content_user = [
            {"type": "text", "text": user_input or "Analizá esta imagen y dame consejos de negocio."},
            {"type": "image_url", "image_url": {"url": f"data:{imagen_mime};base64,{imagen_b64}"}}
        ]
        display_text = f"[Imagen adjunta: {nombre_archivo}]\n{user_input}" if user_input else f"[Imagen adjunta: {nombre_archivo}]"
    else:
        content_user = user_input
        display_text = user_input

    user["messages"].append({"role": "user", "content": display_text})
    user["memoria_larga"].append(f"El usuario dijo: {display_text}")
    if len(user["memoria_larga"]) > 20:
        user["memoria_larga"] = user["memoria_larga"][-20:]

    sumar_xp(10)

    # Armar historial para API (solo texto para historial, imagen solo en mensaje actual)
    historial_api = []
    for m in user["messages"][:-1]:
        historial_api.append({"role": m["role"], "content": m["content"]})

    # Agregar mensaje actual con imagen si aplica
    historial_api.append({"role": "user", "content": content_user})

    with st.spinner("⚡ AV MentorAI está pensando..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": crear_system_prompt(user, st.session_state.modo, desafio)},
                    *historial_api
                ],
                temperature=0.85,
                max_tokens=1000
            )
            respuesta = response.choices[0].message.content
        except Exception as e:
            respuesta = f"Hubo un problema de conexión: {e}"

    user["messages"].append({"role": "assistant", "content": respuesta})
    guardar_usuario(user)
    st.rerun()

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
        <p class="small-text">Aprendé negocios, ventas, marketing y disciplina con un mentor de IA personalizado.</p>
        <p class="small-text"><b>{APP_VERSION}</b></p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><h3>🧠 Mentor personalizado</h3><p class="small-text">Consejos según tu objetivo, negocio y nivel.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><h3>🔥 Desafíos diarios</h3><p class="small-text">Ganá XP, mantené racha y avanzá todos los días.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><h3>📸 Analizá fotos</h3><p class="small-text">Subí fotos de tu local, producto o catálogo y recibí consejos.</p></div>', unsafe_allow_html=True)

    login_tab, register_tab = st.tabs(["Iniciar sesión", "Crear cuenta"])

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
# USER SESSION
# =========================================

user = st.session_state.user_data
default_user = usuario_default(user.get("nombre", ""), user.get("email", ""), "123456")
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
# ONBOARDING
# =========================================

if not user.get("onboarding_completo", False):
    st.markdown(f"""
    <div class="hero-card">
        <div class="av-logo">{APP_NAME}</div>
        <div class="av-subtitle">Configurá tu mentor en 1 minuto</div>
        <p class="small-text">Esto ayuda a que AV MentorAI te responda de forma más personalizada.</p>
    </div>
    """, unsafe_allow_html=True)

    user["objetivo"] = st.text_area("¿Cuál es tu objetivo principal?", value=user["objetivo"],
        placeholder="Ej: vender más, crear un negocio, mejorar mi disciplina...")
    user["negocio"] = st.text_input("¿Tenés un negocio o idea?", value=user["negocio"],
        placeholder="Ej: tienda de ropa, supermercado, ecommerce...")

    tipos = ["Todavía no tengo negocio", "Supermercado / mayorista", "E-commerce",
             "Reventa", "Restaurante / comida", "Servicios", "Inmobiliaria", "Otro"]
    user["tipo_negocio"] = st.selectbox("Tipo de negocio:", tipos,
        index=tipos.index(user["tipo_negocio"]) if user["tipo_negocio"] in tipos else 0)

    niveles = ["Principiante", "Intermedio", "Avanzado"]
    user["nivel_usuario"] = st.selectbox("Tu nivel actual:", niveles,
        index=niveles.index(user["nivel_usuario"]) if user["nivel_usuario"] in niveles else 0)

    tiempos = ["15 minutos", "30 minutos", "1 hora", "Más de 1 hora"]
    user["tiempo_diario"] = st.selectbox("¿Cuánto tiempo podés dedicar por día?", tiempos,
        index=tiempos.index(user["tiempo_diario"]) if user["tiempo_diario"] in tiempos else 0)

    user["principal_dificultad"] = st.text_area("¿Qué es lo que más te cuesta hoy?",
        value=user["principal_dificultad"],
        placeholder="Ej: vender, organizarme, conseguir clientes...")

    if st.button("🚀 Entrar a AV MentorAI"):
        user["onboarding_completo"] = True
        guardar_usuario(user)
        st.rerun()

    st.stop()

# =========================================
# HEADER COMPACTO
# =========================================

st.markdown(f"""
<div class="hero-card">
    <div class="av-logo">{APP_NAME}</div>
    <div class="av-subtitle">{APP_TAGLINE} &nbsp;|&nbsp; <b>{APP_VERSION}</b></div>
</div>
""", unsafe_allow_html=True)

# MÉTRICAS COMPACTAS EN UNA FILA
st.markdown(f"""
<div class="metrics-row">
    <div class="metric-chip">
        <p class="metric-label">👤 Usuario</p>
        <p class="metric-value">{user["nombre"]}</p>
    </div>
    <div class="metric-chip">
        <p class="metric-label">⭐ XP</p>
        <p class="metric-value">{user["xp"]}</p>
    </div>
    <div class="metric-chip">
        <p class="metric-label">🔥 Racha</p>
        <p class="metric-value">{plural_dias(user["racha"])}</p>
    </div>
    <div class="metric-chip">
        <p class="metric-label">📈 Nivel</p>
        <p class="metric-value">{calcular_nivel(user["xp"]).split(" - ")[0]}</p>
    </div>
    <div class="metric-chip">
        <p class="metric-label">💎 Plan</p>
        <p class="metric-value">{user["plan"]}</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.progress(progreso_nivel(user["xp"]))
st.caption(f"Nivel: {calcular_nivel(user['xp'])} — Progreso al siguiente nivel")

# =========================================
# CONFIGURACIÓN (reemplaza sidebar, funciona en mobile)
# =========================================

with st.expander("⚙️ Configuración y perfil", expanded=False):

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**🔧 Modo del mentor**")
        st.session_state.modo = st.selectbox("Modo:", [
            "Mentor de Negocios", "Entrenador de Ventas", "Marketing LATAM",
            "Disciplina y Hábitos", "Ideas de Negocio", "Simulación con Cliente Difícil",
            "Planificador de Objetivos", "Modo Empresario Exigente", "Modo Mentor Millonario",
            "Especialista Supermercados", "Especialista E-commerce",
            "Especialista Reventa", "Especialista Restaurante", "Especialista Inmobiliaria"
        ], label_visibility="collapsed")

        st.markdown("**🧠 Memoria**")
        user["nombre"] = st.text_input("Nombre:", value=user["nombre"])
        user["objetivo"] = st.text_area("Objetivo principal:", value=user["objetivo"])
        user["negocio"] = st.text_input("Negocio o idea:", value=user["negocio"])
        user["tipo_negocio"] = st.text_input("Tipo de negocio:", value=user["tipo_negocio"])

    with col_b:
        st.markdown("**📊 Panel empresario**")
        user["meta_mensual"] = st.text_input("Meta mensual:", value=user["meta_mensual"],
            placeholder="Ej: conseguir 20 clientes")
        user["ingresos_objetivo"] = st.number_input("Objetivo de ingresos ($):",
            value=int(user["ingresos_objetivo"]), min_value=0)
        user["habito_clave"] = st.text_input("Hábito clave:", value=user["habito_clave"],
            placeholder="Ej: vender 1 hora por día")

        st.markdown("**⚙️ Acciones**")
        if st.button("💾 Guardar datos"):
            guardar_usuario(user)
            st.success("Datos guardados.")

        if st.button("🧹 Borrar conversación"):
            st.session_state.confirmar_borrar = True

        if st.session_state.get("confirmar_borrar", False):
            st.warning("¿Estás seguro? Se borra todo el historial.")
            c_si, c_no = st.columns(2)
            with c_si:
                if st.button("✅ Sí, borrar"):
                    user["messages"] = []
                    guardar_usuario(user)
                    st.session_state.confirmar_borrar = False
                    st.rerun()
            with c_no:
                if st.button("❌ Cancelar"):
                    st.session_state.confirmar_borrar = False
                    st.rerun()

        if st.button("🔁 Rehacer onboarding"):
            user["onboarding_completo"] = False
            guardar_usuario(user)
            st.rerun()

        if st.button("🚪 Cerrar sesión"):
            guardar_usuario(user)
            st.session_state.logged_in = False
            st.rerun()

# =========================================
# TABS
# =========================================

tab_mentor, tab_progreso, tab_desafios, tab_premium, tab_ranking, tab_feedback = st.tabs([
    "🧠 Mentor", "📈 Progreso", "🔥 Desafíos", "💎 Premium", "🏆 Ranking", "💬 Feedback"
])

# =========================================
# TAB MENTOR
# =========================================

with tab_mentor:

    # Mensaje de bienvenida automático si no hay conversación
    if not user["messages"]:
        nombre = user["nombre"] or "emprendedor"
        negocio_txt = f" sobre tu negocio de {user['negocio']}" if user["negocio"] else ""
        objetivo_txt = f" Tu objetivo es: {user['objetivo']}." if user["objetivo"] else ""
        bienvenida = f"¡Hola {nombre}! Soy AV MentorAI, tu mentor personal de negocios y ventas.{objetivo_txt} Estoy listo para ayudarte{negocio_txt}. ¿Por dónde empezamos? Podés tocar uno de los botones de abajo o escribirme directamente."
        st.markdown(f"""
        <div class="chat-ai">
            <div class="chat-name-ai">⚡ AV MentorAI</div>
            <div class="chat-text">{bienvenida}</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Mostrar conversación
        for msg in user["messages"]:
            render_chat_message(msg["role"], msg["content"])

        # Botón audio última respuesta
        ultima = obtener_ultima_respuesta(user)
        if ultima:
            if st.button("🔊 Escuchar última respuesta", key="audio_btn"):
                with st.spinner("Generando audio..."):
                    render_audio_player(ultima)

    st.divider()

    # TEXTO GUÍA si no hay mensajes
    if not user["messages"]:
        st.markdown('<div class="guide-text">👇 Tocá un botón o escribí tu primera pregunta abajo</div>', unsafe_allow_html=True)

    # BOTONES RÁPIDOS — 3 columnas, 2 por columna
    c1, c2, c3 = st.columns(3)
    quick_prompt = None
    with c1:
        if st.button("💡 Idea de negocio"):
            quick_prompt = "Dame una idea de negocio rentable para empezar con pocos recursos."
        if st.button("🎭 Cliente difícil"):
            quick_prompt = "Hagamos una simulación. Vos sos un cliente difícil y yo tengo que venderte."
    with c2:
        if st.button("📈 Quiero vender más"):
            quick_prompt = "Quiero vender más. Dame un plan práctico para empezar hoy."
        if st.button("🔥 Desafío de hoy"):
            quick_prompt = f"Quiero hacer este desafío: {desafio}. Guiame paso a paso."
    with c3:
        if st.button("📱 Marketing en redes"):
            quick_prompt = "Quiero aprender marketing desde cero para vender por redes sociales."
        if st.button("💎 Mentor exigente"):
            quick_prompt = "Háblame como mentor exigente y decime qué debería mejorar hoy."

    st.write("")

    # ---- SUBIR IMAGEN O ARCHIVO ----
    with st.expander("📎 Adjuntar imagen o archivo (opcional)", expanded=False):
        st.caption("Subí una foto de tu local, producto, catálogo, captura de ventas o un PDF y el mentor lo analiza.")

        archivo_subido = st.file_uploader(
            "Subí tu archivo:",
            type=["jpg", "jpeg", "png", "webp", "pdf", "txt"],
            label_visibility="collapsed"
        )

        contexto_archivo = st.text_input(
            "¿Qué querés saber sobre este archivo? (opcional)",
            placeholder="Ej: ¿Cómo mejoraría la presentación de este producto?"
        )

        if archivo_subido:
            if archivo_subido.type in ["image/jpeg", "image/png", "image/webp", "image/jpg"]:
                st.image(archivo_subido, caption="Vista previa", use_container_width=True)
            elif archivo_subido.type == "application/pdf":
                st.info(f"📄 PDF adjunto: {archivo_subido.name}")
            elif archivo_subido.type == "text/plain":
                contenido_txt = archivo_subido.read().decode("utf-8")
                st.text_area("Contenido del archivo:", value=contenido_txt[:500] + "..." if len(contenido_txt) > 500 else contenido_txt, height=100)
                archivo_subido.seek(0)

    # ---- VOZ ----
    audio = st.audio_input("🎤 Grabá tu pregunta por voz (opcional)")
    voice_prompt = None
    if audio:
        with st.spinner("Transcribiendo..."):
            try:
                voice_prompt = transcribir_audio(audio)
                st.success(f"Escuché: *{voice_prompt}*")
            except Exception as e:
                st.warning(f"No pude transcribir el audio: {e}")

    # ---- INPUT DE TEXTO ----
    user_input = st.chat_input("Escribí tu pregunta al mentor...")

    # Prioridad: voz > quick_prompt > texto
    if voice_prompt:
        user_input = voice_prompt
    elif quick_prompt:
        user_input = quick_prompt

    # ---- PROCESAR ENVÍO ----
    if user_input or (archivo_subido and st.session_state.get("enviar_archivo", False)):

        imagen_b64 = None
        imagen_mime = None
        nombre_archivo = None

        if archivo_subido:
            if archivo_subido.type in ["image/jpeg", "image/png", "image/webp", "image/jpg"]:
                imagen_b64, imagen_mime = imagen_a_base64(archivo_subido)
                nombre_archivo = archivo_subido.name
            elif archivo_subido.type == "text/plain":
                contenido = archivo_subido.read().decode("utf-8")
                user_input = (user_input or "") + f"\n\n[Contenido del archivo {archivo_subido.name}]:\n{contenido[:3000]}"
            elif archivo_subido.type == "application/pdf":
                user_input = (user_input or "") + f"\n\n[El usuario subió un PDF llamado: {archivo_subido.name}. No podés leerlo directamente pero podés pedirle que te cuente el contenido o que lo copie.]"

        if user_input or imagen_b64:
            enviar_mensaje(
                user_input=user_input or "",
                desafio=desafio,
                imagen_b64=imagen_b64,
                imagen_mime=imagen_mime,
                nombre_archivo=nombre_archivo
            )

# =========================================
# TAB PROGRESO
# =========================================

with tab_progreso:
    st.markdown("## 📈 Progreso y hábitos")

    p1, p2, p3 = st.columns(3)
    with p1:
        st.metric("⭐ XP total", user["xp"])
    with p2:
        st.metric("🔥 Racha", plural_dias(user["racha"]))
    with p3:
        st.metric("🎯 Objetivos completados", user["objetivos_completados"])

    if user["xp_history"]:
        df_xp = pd.DataFrame(user["xp_history"])
        st.markdown("### Evolución de XP")
        st.line_chart(df_xp.set_index("fecha")["xp"])
    else:
        st.info("Todavía no hay progreso para mostrar en el gráfico.")

    if st.button("🧠 Generar memoria inteligente"):
        with st.spinner("Generando resumen..."):
            resumen = generar_resumen_inteligente(user)
        st.success(resumen)

    if user["logros"]:
        st.markdown("### 🏆 Logros desbloqueados")
        st.markdown("".join([f'<span class="badge">🏆 {logro}</span>' for logro in user["logros"]]),
                    unsafe_allow_html=True)

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
            st.success("Desafío completado. Sumaste 40 XP. 🎉")
            st.rerun()
    with d2:
        if st.button("🎯 Marcar objetivo completado"):
            user["objetivos_completados"] += 1
            sumar_xp(60)
            guardar_usuario(user)
            st.success("Objetivo completado. Sumaste 60 XP. 🏆")
            st.rerun()

    st.markdown(f"""
    <div class="card">
        <p><b>Desafíos completados:</b> {user["desafios_completados"]}</p>
        <p><b>Objetivos completados:</b> {user["objetivos_completados"]}</p>
        <p><b>Racha actual:</b> {plural_dias(user["racha"])}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# TAB PREMIUM
# =========================================

with tab_premium:
    st.markdown("## 💎 Planes")
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
        </div>""", unsafe_allow_html=True)
        if st.button("Usar Gratis"):
            user["plan"] = "Gratis"
            guardar_usuario(user)
            st.rerun()

    with plan2:
        st.markdown("""
        <div class="plan-card">
            <h2>Pro</h2>
            <p>🚀 Mentor ilimitado</p>
            <p>🔊 Respuestas por voz</p>
            <p>📸 Análisis de fotos</p>
            <p>🧠 Memoria profunda</p>
            <h1>$4.99 USD</h1>
        </div>""", unsafe_allow_html=True)
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
            <p>📈 Métricas avanzadas</p>
            <p>📂 Carga de archivos</p>
            <p>🤖 IA personalizada</p>
            <h1>Consultar</h1>
        </div>""", unsafe_allow_html=True)
        st.info("Próximamente: Mercado Pago / Stripe.")

    st.markdown(f"""
    <div class="card">
        <p><b>Plan actual:</b> {user["plan"]}</p>
        <p><b>Preguntas usadas hoy:</b> {user["preguntas_hoy"]}</p>
    </div>""", unsafe_allow_html=True)

# =========================================
# TAB RANKING
# =========================================

with tab_ranking:
    st.markdown("## 🏆 Ranking")
    ranking = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".json"):
            try:
                with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
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
        st.dataframe(df_ranking, use_container_width=True)
    else:
        st.info("Todavía no hay usuarios en el ranking.")

# =========================================
# TAB FEEDBACK
# =========================================

with tab_feedback:
    st.markdown("## 💬 Feedback")
    st.info("Usá esta sección para guardar opiniones de quienes prueban la app.")

    calificacion = st.slider("¿Qué tan útil te parece AV MentorAI?", 1, 10, 8)
    comentario = st.text_area("Comentario:", placeholder="Qué te gustó, qué te confundió, qué pagarías, qué mejorarías...")
    pagaria = st.selectbox("¿Pagarías por usar esta app?", ["No sé", "Sí", "No"])

    if st.button("Enviar feedback"):
        user["feedback"].append({
            "fecha": str(date.today()),
            "calificacion": calificacion,
            "comentario": comentario,
            "pagaria": pagaria
        })
        guardar_usuario(user)
        st.success("Feedback guardado. ✅")

    if user["feedback"]:
        st.markdown("### Feedback guardado")
        df_feedback = pd.DataFrame(user["feedback"])
        st.dataframe(df_feedback, use_container_width=True)
