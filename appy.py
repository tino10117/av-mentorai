# =========================================
# AV MentorAI - VERSION DEMO PRIVADA v3.0
# Con módulo de Aprender Inglés integrado
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
APP_VERSION = "Demo privada v3.0"

LECCIONES = {
    "Principiante": [
        {
            "id": "p1",
            "titulo": "Saludos básicos",
            "descripcion": "Hello, Hi, Good morning, Good night",
            "xp": 20,
            "contenido": """**Saludos formales:**
- Hello → Hola
- Good morning → Buenos días
- Good afternoon → Buenas tardes
- Good evening → Buenas noches (al llegar)
- Good night → Buenas noches (al irse a dormir)

**Saludos informales:**
- Hi → Hola (casual)
- Hey → Ey / Hola (muy informal)
- What's up? → ¿Qué onda?
- How are you? → ¿Cómo estás?
- I'm fine, thanks → Estoy bien, gracias

**Despedidas:**
- Goodbye / Bye → Adiós / Chau
- See you later → Nos vemos después
- Take care → Cuídate
- Have a good day → Que tengas un buen día

**Ejercicio:** Escribile un saludo al profesor como si lo encontraras por primera vez en el día."""
        },
        {
            "id": "p2",
            "titulo": "El verbo To Be",
            "descripcion": "I am, You are, He/She is...",
            "xp": 25,
            "contenido": """El verbo **To Be** significa "ser" o "estar". Es el más importante del inglés.

**Forma afirmativa:**
- I am / I'm → Yo soy/estoy
- You are / You're → Vos sos/estás
- He is / He's → Él es/está
- She is / She's → Ella es/está
- It is / It's → Eso es/está
- We are / We're → Nosotros somos/estamos
- They are / They're → Ellos son/están

**Ejemplos:**
- I'm Valentino → Yo soy Valentino
- She's my friend → Ella es mi amiga
- We're from Argentina → Somos de Argentina

**Negativa:** agrega "not"
- I'm not → Yo no soy/estoy
- He isn't → Él no es/está

**Preguntas:** se invierte el orden
- Are you okay? → ¿Estás bien?
- Is she your sister? → ¿Es tu hermana?

**Ejercicio:** Escribí 3 oraciones sobre vos usando I am / I'm."""
        },
        {
            "id": "p3",
            "titulo": "Números del 1 al 100",
            "descripcion": "One, two, three... hasta one hundred",
            "xp": 20,
            "contenido": """**Del 1 al 20:**
1-one, 2-two, 3-three, 4-four, 5-five, 6-six, 7-seven, 8-eight, 9-nine, 10-ten
11-eleven, 12-twelve, 13-thirteen, 14-fourteen, 15-fifteen
16-sixteen, 17-seventeen, 18-eighteen, 19-nineteen, 20-twenty

**Las decenas:**
30-thirty, 40-forty, 50-fifty, 60-sixty, 70-seventy, 80-eighty, 90-ninety, 100-one hundred

**Combinaciones:**
- 21 → twenty-one
- 45 → forty-five
- 99 → ninety-nine

**En contexto:**
- It costs fifty dollars → Cuesta cincuenta dólares
- I have thirty products → Tengo treinta productos

**Ejercicio:** ¿Cómo se dice 27, 53 y 88 en inglés?"""
        },
        {
            "id": "p4",
            "titulo": "Presentarse en inglés",
            "descripcion": "My name is, I'm from, I work...",
            "xp": 25,
            "contenido": """**Frases básicas:**
- My name is... → Mi nombre es...
- I'm... → Soy... (informal)
- Nice to meet you → Mucho gusto

**De dónde sos:**
- I'm from Argentina → Soy de Argentina
- I live in Buenos Aires → Vivo en Buenos Aires

**Tu trabajo:**
- I work at... → Trabajo en...
- I own a business → Tengo un negocio
- I'm an entrepreneur → Soy emprendedor/a

**Tu edad:**
- I'm 25 years old → Tengo 25 años
- How old are you? → ¿Cuántos años tenés?

**Ejemplo completo:**
"Hi! My name is Valentino. I'm from Argentina. I'm 25 years old and I own a small business. Nice to meet you!"

**Ejercicio:** Escribí tu propia presentación completa en inglés."""
        },
        {
            "id": "p5",
            "titulo": "Vocabulario esencial",
            "descripcion": "Las palabras más usadas en inglés",
            "xp": 30,
            "contenido": """**Palabras básicas:**
- Yes/No/Maybe → Sí/No/Quizás
- Please → Por favor
- Thank you → Gracias
- Sorry → Perdón
- Help → Ayuda

**Preguntas clave:**
- What? → ¿Qué? | Who? → ¿Quién?
- Where? → ¿Dónde? | When? → ¿Cuándo?
- Why? → ¿Por qué? | How? → ¿Cómo?
- How much? → ¿Cuánto cuesta?

**Palabras de tiempo:**
- Today/Yesterday/Tomorrow → Hoy/Ayer/Mañana
- Now/Later → Ahora/Después
- Always/Never/Sometimes → Siempre/Nunca/A veces

**Colores:**
Red-rojo, Blue-azul, Green-verde, Yellow-amarillo, Black-negro, White-blanco

**Ejercicio:** Usá 5 de estas palabras en oraciones propias."""
        },
    ],
    "Intermedio": [
        {
            "id": "i1",
            "titulo": "Presente simple",
            "descripcion": "I work, She works, They play...",
            "xp": 35,
            "contenido": """**Cuándo usarlo:** rutinas, hábitos, hechos.

**Estructura:**
- Afirmativa: Sujeto + verbo (+ s en 3ra persona)
- Negativa: Sujeto + don't/doesn't + verbo
- Pregunta: Do/Does + sujeto + verbo?

**Ejemplos:**
- I sell products every day → Vendo productos todos los días
- She works in the morning → Ella trabaja por la mañana
- I don't have time → No tengo tiempo
- Do you have a store? → ¿Tenés una tienda?

**Palabras clave:** always, usually, often, sometimes, never, every day

**Ejercicio:** Describí tu rutina de trabajo usando presente simple (mínimo 4 oraciones)."""
        },
        {
            "id": "i2",
            "titulo": "Pasado simple",
            "descripcion": "I worked, She bought, They went...",
            "xp": 35,
            "contenido": """**Cuándo usarlo:** acciones ya terminadas.

**Verbos regulares:** agrega -ed
- work → worked | call → called | open → opened

**Verbos irregulares más usados:**
- go → went | buy → bought | sell → sold
- have → had | make → made | come → came
- see → saw | get → got

**Ejemplos:**
- Yesterday I sold 10 products → Ayer vendí 10 productos
- We had a great month → Tuvimos un mes excelente

**Negativa:** didn't + verbo base
- I didn't sell anything → No vendí nada

**Pregunta:** Did + sujeto + verbo?
- Did you make money? → ¿Hiciste plata?

**Ejercicio:** Contá qué hiciste ayer en tu negocio usando pasado simple."""
        },
        {
            "id": "i3",
            "titulo": "Inglés para ventas",
            "descripcion": "Frases clave para vender en inglés",
            "xp": 40,
            "contenido": """**Presentar un producto:**
- This product is... → Este producto es...
- It helps you to... → Te ayuda a...
- This is our best seller → Este es nuestro más vendido

**Preguntar al cliente:**
- What are you looking for? → ¿Qué estás buscando?
- What's your budget? → ¿Cuál es tu presupuesto?
- Would you like to try it? → ¿Querés probarlo?

**Manejar objeciones:**
- I understand your concern → Entiendo tu preocupación
- Let me explain... → Dejame explicarte...

**Cerrar la venta:**
- Shall we close the deal? → ¿Cerramos el trato?
- I'll give you a discount → Te hago un descuento
- It's a great investment → Es una gran inversión

**Ejercicio:** Presentá un producto tuyo en inglés usando estas frases."""
        },
        {
            "id": "i4",
            "titulo": "Emails en inglés",
            "descripcion": "Cómo escribir emails profesionales",
            "xp": 40,
            "contenido": """**Estructura de un email:**
1. Saludo → Dear / Hi + nombre
2. Introducción → quién sos y por qué escribís
3. Cuerpo → el mensaje
4. Cierre → despedida

**Saludos:**
- Dear Mr./Ms. [apellido] → formal
- Hi [nombre] → informal

**Frases útiles:**
- I'm writing to... → Le escribo para...
- Could you please...? → ¿Podría por favor...?
- Please find attached... → Adjunto encontrará...
- I look forward to hearing from you → Quedo a la espera

**Cierres:**
- Best regards → Saludos cordiales
- Kind regards → Atentamente
- Thanks → Gracias (informal)

**Ejemplo:**
"Hi John, I'm writing to ask about your product prices. Could you please send me your catalogue? Best regards, Valentino."

**Ejercicio:** Escribí un email a un proveedor pidiendo precios."""
        },
    ],
    "Avanzado": [
        {
            "id": "a1",
            "titulo": "Negociación en inglés",
            "descripcion": "Cómo negociar precios, condiciones y contratos",
            "xp": 50,
            "contenido": """**Abrir una negociación:**
- I'd like to discuss the terms → Me gustaría discutir los términos
- Let's talk about pricing → Hablemos de precios
- I have a proposal for you → Tengo una propuesta

**Hacer ofertas:**
- We can offer you... → Podemos ofrecerte...
- Our best price is... → Nuestro mejor precio es...
- If you order more, we can lower the price → Si pedís más, bajamos el precio

**Contraofertas:**
- That's a bit high for us → Eso es un poco alto
- Could you do better? → ¿Podría mejorar eso?
- Let's meet in the middle → Encontrémonos en el medio

**Cerrar el trato:**
- We have a deal → Tenemos un trato
- I'll send you the contract → Te mando el contrato
- When can we start? → ¿Cuándo empezamos?

**Ejercicio:** Hacé un roleplay de negociación con Alex."""
        },
        {
            "id": "a2",
            "titulo": "Presentaciones de negocio",
            "descripcion": "Cómo presentar tu negocio en inglés",
            "xp": 50,
            "contenido": """**Estructura de una presentación:**
1. Hook → ganchar la atención
2. El problema que resolvés
3. Tu solución
4. Por qué vos
5. Call to action

**Frases por sección:**

Hook:
- Did you know that...? → ¿Sabías que...?
- Imagine a world where... → Imaginate un mundo donde...

El problema:
- The main challenge is... → El principal desafío es...
- Most people struggle with... → La mayoría lucha con...

Tu solución:
- We've developed... → Desarrollamos...
- Unlike competitors, we... → A diferencia de los competidores...

Call to action:
- Let's work together → Trabajemos juntos
- Contact us today → Contactanos hoy

**Ejercicio:** Preparate una presentación de 1 minuto de tu negocio en inglés."""
        },
        {
            "id": "a3",
            "titulo": "Phrasal verbs de negocios",
            "descripcion": "Los verbos compuestos más usados",
            "xp": 45,
            "contenido": """Los **phrasal verbs** son verbos + preposición que cambian de significado. Son muy usados en inglés real.

**Los más importantes en negocios:**
- Set up → Establecer, crear (I set up my business last year)
- Take over → Tomar control (They took over the company)
- Scale up → Crecer, escalar (We need to scale up)
- Cut down → Reducir (We cut down costs)
- Follow up → Hacer seguimiento (I'll follow up with the client)
- Break even → Cubrir costos (We finally broke even)
- Run out of → Quedarse sin (We ran out of stock)
- Put off → Posponer (Don't put off that meeting)
- Turn down → Rechazar (They turned down our offer)
- Come up with → Idear (She came up with a great plan)

**En contexto:**
- "We need to follow up with that client from Monday."
- "The new product line helped us scale up quickly."
- "Don't put off calling your best customer."

**Ejercicio:** Usá 5 phrasal verbs de esta lista en oraciones sobre tu negocio."""
        },
    ]
}

st.set_page_config(page_title=APP_NAME, page_icon="⚡", layout="wide")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: radial-gradient(circle at top left, #1f2937 0%, #0b1120 45%, #020617 100%);
    color: white;
}
.block-container { padding-top: 1.2rem; padding-bottom: 5rem; max-width: 860px; }
h1, h2, h3, h4, p, label, span { color: #f8fafc !important; }

.av-logo {
    font-size: 48px; font-weight: 900;
    background: linear-gradient(90deg, #facc15, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.av-subtitle { font-size: 16px; color: #cbd5e1 !important; margin-bottom: 10px; }

.hero-card, .card, .plan-card, .challenge-card {
    background: rgba(15,23,42,0.88); border: 1px solid rgba(148,163,184,0.22);
    border-radius: 20px; padding: 18px; box-shadow: 0px 8px 24px rgba(0,0,0,0.30); margin-bottom: 14px;
}
.hero-card {
    background: linear-gradient(135deg, rgba(250,204,21,0.16), rgba(56,189,248,0.10));
    border: 1px solid rgba(250,204,21,0.35); padding: 16px 20px;
}
.challenge-card {
    background: linear-gradient(135deg, rgba(249,115,22,0.18), rgba(250,204,21,0.10));
    border: 1px solid rgba(250,204,21,0.45);
}
.english-card {
    background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(99,102,241,0.10));
    border: 1px solid rgba(56,189,248,0.35); border-radius: 20px; padding: 18px; margin-bottom: 14px;
}
.lesson-card {
    background: rgba(15,23,42,0.88); border: 1px solid rgba(56,189,248,0.25);
    border-radius: 16px; padding: 14px; margin-bottom: 8px;
}
.lesson-card-done {
    background: rgba(15,23,42,0.88); border: 1px solid rgba(34,197,94,0.5);
    border-radius: 16px; padding: 14px; margin-bottom: 8px;
}
.lesson-content {
    background: rgba(15,23,42,0.95); border: 1px solid rgba(56,189,248,0.3);
    border-radius: 16px; padding: 20px; margin-bottom: 14px;
    color: #f1f5f9 !important; line-height: 1.7; white-space: pre-wrap;
}

.metrics-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
.metric-chip {
    background: rgba(15,23,42,0.88); border: 1px solid rgba(148,163,184,0.22);
    border-radius: 14px; padding: 8px 14px; text-align: center; flex: 1; min-width: 70px;
}
.metric-chip .metric-label { font-size: 11px; color: #94a3b8 !important; margin: 0; }
.metric-chip .metric-value { font-size: 16px; font-weight: 800; color: #facc15 !important; margin: 2px 0 0 0; }

.chat-user {
    background: rgba(30,41,59,0.95); border-left: 4px solid #facc15;
    padding: 14px 16px; border-radius: 16px; margin-bottom: 12px;
}
.chat-ai {
    background: rgba(15,23,42,0.96); border-left: 4px solid #38bdf8;
    padding: 14px 16px; border-radius: 16px; margin-bottom: 12px;
}
.chat-english {
    background: rgba(15,23,42,0.96); border-left: 4px solid #a855f7;
    padding: 14px 16px; border-radius: 16px; margin-bottom: 12px;
}
.chat-name { font-weight: 900; font-size: 13px; color: #facc15 !important; margin-bottom: 6px; text-transform: uppercase; }
.chat-name-ai { font-weight: 900; font-size: 13px; color: #38bdf8 !important; margin-bottom: 6px; text-transform: uppercase; }
.chat-name-english { font-weight: 900; font-size: 13px; color: #a855f7 !important; margin-bottom: 6px; text-transform: uppercase; }
.chat-text { color: #f1f5f9 !important; line-height: 1.65; font-size: 15px; white-space: pre-wrap; }

.badge {
    display: inline-block; background: linear-gradient(90deg, #facc15, #f97316);
    color: #111827 !important; padding: 6px 12px; border-radius: 12px;
    font-weight: 800; margin: 3px; font-size: 13px;
}
.small-text { color: #cbd5e1 !important; font-size: 14px; }
.guide-text {
    color: #94a3b8 !important; font-size: 14px; text-align: center; padding: 10px;
    border: 1px dashed rgba(148,163,184,0.3); border-radius: 12px; margin-bottom: 12px;
}

.stButton>button {
    border-radius: 12px; border: 1px solid rgba(250,204,21,0.45);
    background: linear-gradient(90deg, #facc15, #f97316);
    color: #111827; font-weight: 800; font-size: 14px;
}
.stTextInput input, .stTextArea textarea {
    background-color: #0f172a !important; color: #f8fafc !important;
    border-radius: 12px !important; border: 1px solid rgba(250,204,21,0.3) !important;
}
[data-testid="stChatInput"] textarea {
    background-color: #0f172a !important; color: #f8fafc !important;
    border: 1px solid rgba(250,204,21,0.35) !important; border-radius: 14px !important;
}
[data-testid="stExpander"] {
    background: rgba(15,23,42,0.88) !important;
    border: 1px solid rgba(250,204,21,0.25) !important; border-radius: 16px !important;
}
@media (max-width: 768px) {
    .av-logo { font-size: 32px; }
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
    return email.lower().strip().replace("@","_at_").replace(".","_")

def archivo_usuario(email):
    return os.path.join(DATA_DIR, f"{limpiar_email(email)}.json")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def usuario_default(nombre, email, password):
    return {
        "nombre": nombre, "email": email, "password": hash_password(password),
        "plan": "Gratis", "xp": 0, "racha": 0, "messages": [], "memoria_larga": [],
        "onboarding_completo": False, "objetivo": "", "negocio": "", "tipo_negocio": "",
        "nivel_usuario": "Principiante", "tiempo_diario": "", "principal_dificultad": "",
        "meta_mensual": "", "ingresos_objetivo": 0, "habito_clave": "",
        "desafios_completados": 0, "objetivos_completados": 0, "logros": [], "xp_history": [],
        "ultima_fecha": "", "fecha_desafio": "", "desafio_actual": "",
        "preguntas_hoy": 0, "fecha_preguntas": "", "feedback": [],
        "english_nivel": "Principiante", "english_lecciones_completadas": [],
        "english_messages": [], "english_xp": 0,
    }

def guardar_usuario(data):
    with open(archivo_usuario(data["email"]), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def cargar_usuario(email):
    path = archivo_usuario(email)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        default = usuario_default(data.get("nombre",""), data.get("email",email), "123456")
        for k, v in default.items():
            if k not in data:
                data[k] = v
        return data
    return None

def crear_usuario(nombre, email, password):
    if cargar_usuario(email): return False
    guardar_usuario(usuario_default(nombre, email, password))
    return True

def login(email, password):
    user = cargar_usuario(email)
    if not user: return None
    if (user.get("password") or user.get("password_hash")) == hash_password(password):
        return user
    return None

# =========================================
# FUNCIONES
# =========================================

def calcular_nivel(xp):
    if xp < 100: return "Nivel 1 - Inicial"
    if xp < 300: return "Nivel 2 - En crecimiento"
    if xp < 700: return "Nivel 3 - Estratega"
    if xp < 1200: return "Nivel 4 - Empresario Pro"
    return "Nivel 5 - Élite"

def progreso_nivel(xp):
    if xp < 100: return xp/100
    if xp < 300: return (xp-100)/200
    if xp < 700: return (xp-300)/400
    if xp < 1200: return (xp-700)/500
    return 1.0

def desbloquear_logros(user):
    reglas = [
        (user["xp"] >= 100, "Primeros 100 XP"),
        (user["xp"] >= 300, "Mente en crecimiento"),
        (user["xp"] >= 700, "Estratega en formación"),
        (user["racha"] >= 3, "Racha de 3 días"),
        (user["racha"] >= 7, "Semana imparable"),
        (user["desafios_completados"] >= 5, "5 desafíos completados"),
        (user["objetivos_completados"] >= 3, "Constructor de objetivos"),
        (len(user.get("english_lecciones_completadas",[])) >= 3, "Estudiante de inglés"),
        (len(user.get("english_lecciones_completadas",[])) >= 8, "Angloparlante en progreso"),
    ]
    for condicion, logro in reglas:
        if condicion and logro not in user["logros"]:
            user["logros"].append(logro)

def sumar_xp(cantidad):
    user = st.session_state.user_data
    user["xp"] += cantidad
    hoy = str(date.today())
    if user.get("ultima_fecha","") != hoy:
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
    if user.get("fecha_desafio","") != hoy:
        user["desafio_actual"] = random.choice(desafios)
        user["fecha_desafio"] = hoy
        guardar_usuario(user)
    return user["desafio_actual"]

def plural_dias(n):
    return f"{n} día" if n == 1 else f"{n} días"

def transcribir_audio(audio_file):
    return client.audio.transcriptions.create(model="whisper-1", file=audio_file).text

def generar_audio_bytes(texto):
    audio_path = f"resp_{uuid.uuid4().hex}.mp3"
    with client.audio.speech.with_streaming_response.create(model="tts-1", voice="alloy", input=texto[:1200]) as r:
        r.stream_to_file(audio_path)
    with open(audio_path,"rb") as f:
        b = f.read()
    try: os.remove(audio_path)
    except: pass
    return b

def render_audio_player(texto):
    try:
        b = generar_audio_bytes(texto)
        st.audio(b, format="audio/mpeg")
        st.download_button("⬇️ Descargar audio", data=b, file_name="respuesta.mp3", mime="audio/mpeg")
    except Exception as e:
        st.warning(f"No se pudo generar el audio: {e}")

def imagen_a_base64(f):
    b64 = base64.b64encode(f.read()).decode("utf-8")
    return b64, f.type

def obtener_ultima_respuesta(msgs):
    for m in reversed(msgs):
        if m["role"] == "assistant": return m["content"]
    return None

def system_negocio(user, modo, desafio):
    mem = "\n".join(user.get("memoria_larga",[])[-6:])
    return f"""Eres AV MentorAI, mentor premium de negocios, ventas y marketing para LATAM.
Usuario: {user['nombre']} | Plan: {user['plan']} | Objetivo: {user['objetivo']}
Negocio: {user['negocio']} | Tipo: {user['tipo_negocio']} | Nivel: {user['nivel_usuario']}
XP: {user['xp']} | Racha: {user['racha']} días | Modo: {modo} | Desafío: {desafio}
Memoria: {mem}
Identidad: Moderno, directo, motivador. Frases: "No lo pienses tanto, ejecutalo.", "El negocio premia al que acciona mejor."
Estilo: Español latino, claro, práctico. Ejemplos de WhatsApp, Instagram, Mercado Libre, kioscos, reventa.
Siempre terminá con una acción concreta para HOY. Si hay imagen, analizala con criterio empresarial."""

def system_english(user, leccion=None):
    nivel = user.get("english_nivel","Principiante")
    loks = len(user.get("english_lecciones_completadas",[]))
    lec = f"\nLección actual: {leccion}" if leccion else ""
    return f"""Sos Alex, el profesor de inglés de AV MentorAI. Enseñás inglés de forma divertida y moderna, como un amigo que sabe mucho inglés.
Estudiante: {user['nombre']} | Nivel: {nivel} | Lecciones completadas: {loks}{lec}
Estilo: Divertido, con energía, usás emojis. Explicás en ESPAÑOL pero enseñás INGLÉS.
Siempre corregís errores así: "✅ Correcto sería: [forma correcta]" y explicás por qué.
Celebrás logros. Si preguntan algo fuera del inglés, redirigís amablemente.
Frases tuyas: "¡Genial! Casi perfecto...", "You're killing it! 🔥", "Let's practice!"
Si el estudiante graba audio en inglés, corregís pronunciación y gramática."""

def render_msg(role, content, tipo="negocio"):
    if role == "user":
        st.markdown(f'<div class="chat-user"><div class="chat-name">Vos</div><div class="chat-text">{content}</div></div>', unsafe_allow_html=True)
    elif tipo == "english":
        st.markdown(f'<div class="chat-english"><div class="chat-name-english">🎓 Alex — Profesor de Inglés</div><div class="chat-text">{content}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-ai"><div class="chat-name-ai">⚡ AV MentorAI</div><div class="chat-text">{content}</div></div>', unsafe_allow_html=True)

def enviar_negocio(user_input, desafio, imagen_b64=None, imagen_mime=None, nombre_archivo=None):
    user = st.session_state.user_data
    key = user_input + (imagen_b64[:20] if imagen_b64 else "")
    if key == st.session_state.get("last_neg",""): return
    st.session_state.last_neg = key

    if not MODO_DEV and user["plan"]=="Gratis" and user["preguntas_hoy"]>=10:
        st.warning("Límite diario alcanzado. Activá Premium."); return

    user["preguntas_hoy"] += 1
    if imagen_b64:
        content_api = [{"type":"text","text": user_input or "Analizá esta imagen."},
                       {"type":"image_url","image_url":{"url":f"data:{imagen_mime};base64,{imagen_b64}"}}]
        display = f"[Imagen: {nombre_archivo}]\n{user_input}" if user_input else f"[Imagen: {nombre_archivo}]"
    else:
        content_api = user_input
        display = user_input

    user["messages"].append({"role":"user","content":display})
    user["memoria_larga"].append(f"Usuario: {display}")
    if len(user["memoria_larga"])>20: user["memoria_larga"] = user["memoria_larga"][-20:]
    sumar_xp(10)

    hist = [{"role":m["role"],"content":m["content"]} for m in user["messages"][:-1]]
    hist.append({"role":"user","content":content_api})

    with st.spinner("⚡ AV MentorAI está pensando..."):
        try:
            r = client.chat.completions.create(model="gpt-4o",
                messages=[{"role":"system","content":system_negocio(user,st.session_state.modo,desafio)},*hist],
                temperature=0.85, max_tokens=1000)
            resp = r.choices[0].message.content
        except Exception as e:
            resp = f"Error de conexión: {e}"

    user["messages"].append({"role":"assistant","content":resp})
    guardar_usuario(user)
    st.rerun()

def enviar_english(user_input, leccion=None):
    user = st.session_state.user_data
    if user_input == st.session_state.get("last_eng",""): return
    st.session_state.last_eng = user_input

    if "english_messages" not in user: user["english_messages"] = []
    user["english_messages"].append({"role":"user","content":user_input})
    hist = [{"role":m["role"],"content":m["content"]} for m in user["english_messages"][-12:]]

    with st.spinner("🎓 Alex está respondiendo..."):
        try:
            r = client.chat.completions.create(model="gpt-4o",
                messages=[{"role":"system","content":system_english(user,leccion)},*hist],
                temperature=0.8, max_tokens=800)
            resp = r.choices[0].message.content
        except Exception as e:
            resp = f"Error: {e}"

    user["english_messages"].append({"role":"assistant","content":resp})
    if len(user["english_messages"])>40: user["english_messages"] = user["english_messages"][-40:]
    guardar_usuario(user)
    st.rerun()

def generar_resumen(user):
    if not user["messages"]: return "No hay conversación aún."
    texto = "\n".join([f'{m["role"]}: {m["content"]}' for m in user["messages"][-8:]])
    try:
        r = client.chat.completions.create(model="gpt-4o-mini",
            messages=[{"role":"system","content":"Resume datos del usuario para memoria futura. Breve y práctico."},
                      {"role":"user","content":texto}])
        resumen = r.choices[0].message.content
        user["memoria_larga"].append(resumen)
        if len(user["memoria_larga"])>20: user["memoria_larga"] = user["memoria_larga"][-20:]
        guardar_usuario(user)
        return resumen
    except Exception as e:
        return f"Error: {e}"

# =========================================
# LOGIN
# =========================================

if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown(f'<div class="hero-card"><div class="av-logo">{APP_NAME}</div><div class="av-subtitle">{APP_TAGLINE}</div><p class="small-text">Mentor de negocios + Aprendé inglés desde cero. Todo en uno.</p><p class="small-text"><b>{APP_VERSION}</b></p></div>', unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown('<div class="card"><h3>🧠 Mentor de negocios</h3><p class="small-text">Consejos según tu objetivo y nivel.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="card"><h3>📚 Aprender inglés</h3><p class="small-text">Desde cero hasta avanzado con Alex, tu profe IA.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="card"><h3>🔥 Gamificación</h3><p class="small-text">XP, rachas, niveles y desafíos diarios.</p></div>', unsafe_allow_html=True)

    lt, rt = st.tabs(["Iniciar sesión","Crear cuenta"])
    with lt:
        el = st.text_input("Gmail", placeholder="tuemail@gmail.com")
        pl = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            ul = login(el, pl)
            if ul: st.session_state.logged_in=True; st.session_state.user_data=ul; st.rerun()
            else: st.error("Gmail o contraseña incorrectos.")
    with rt:
        nr = st.text_input("Nombre", placeholder="Valentino")
        er = st.text_input("Gmail para crear cuenta", placeholder="tuemail@gmail.com")
        pr = st.text_input("Crear contraseña", type="password")
        if st.button("Crear cuenta"):
            if not nr or not er or not pr: st.warning("Completá todos los campos.")
            elif "@gmail.com" not in er.lower(): st.warning("Usá un Gmail válido.")
            elif len(pr)<6: st.warning("Mínimo 6 caracteres.")
            else:
                ok = crear_usuario(nr,er,pr)
                st.success("Cuenta creada. Iniciá sesión.") if ok else st.error("Ese Gmail ya existe.")
    st.stop()

# =========================================
# SESSION
# =========================================

user = st.session_state.user_data
dfu = usuario_default(user.get("nombre",""), user.get("email",""), "123456")
for k,v in dfu.items():
    if k not in user: user[k] = v
guardar_usuario(user)

desafio = generar_desafio(user)
hoy = str(date.today())
if user.get("fecha_preguntas","") != hoy:
    user["fecha_preguntas"]=hoy; user["preguntas_hoy"]=0; guardar_usuario(user)

if "modo" not in st.session_state: st.session_state.modo = "Mentor de Negocios"
if "leccion_seleccionada" not in st.session_state: st.session_state.leccion_seleccionada = None

# =========================================
# ONBOARDING
# =========================================

if not user.get("onboarding_completo", False):
    st.markdown(f'<div class="hero-card"><div class="av-logo">{APP_NAME}</div><div class="av-subtitle">Configurá tu mentor en 1 minuto</div></div>', unsafe_allow_html=True)
    user["objetivo"] = st.text_area("¿Cuál es tu objetivo principal?", value=user["objetivo"], placeholder="Ej: vender más, crear un negocio...")
    user["negocio"] = st.text_input("¿Tenés un negocio o idea?", value=user["negocio"], placeholder="Ej: tienda de ropa, supermercado...")
    tipos = ["Todavía no tengo negocio","Supermercado / mayorista","E-commerce","Reventa","Restaurante / comida","Servicios","Inmobiliaria","Otro"]
    user["tipo_negocio"] = st.selectbox("Tipo de negocio:", tipos, index=tipos.index(user["tipo_negocio"]) if user["tipo_negocio"] in tipos else 0)
    niv = ["Principiante","Intermedio","Avanzado"]
    user["nivel_usuario"] = st.selectbox("Tu nivel:", niv, index=niv.index(user["nivel_usuario"]) if user["nivel_usuario"] in niv else 0)
    tps = ["15 minutos","30 minutos","1 hora","Más de 1 hora"]
    user["tiempo_diario"] = st.selectbox("Tiempo por día:", tps, index=tps.index(user["tiempo_diario"]) if user["tiempo_diario"] in tps else 0)
    user["principal_dificultad"] = st.text_area("¿Qué te cuesta más?", value=user["principal_dificultad"])
    if st.button("🚀 Entrar a AV MentorAI"):
        user["onboarding_completo"]=True; guardar_usuario(user); st.rerun()
    st.stop()

# =========================================
# HEADER
# =========================================

st.markdown(f'<div class="hero-card"><div class="av-logo">{APP_NAME}</div><div class="av-subtitle">{APP_TAGLINE} &nbsp;|&nbsp; <b>{APP_VERSION}</b></div></div>', unsafe_allow_html=True)

loks = len(user.get("english_lecciones_completadas",[]))
st.markdown(f"""
<div class="metrics-row">
  <div class="metric-chip"><p class="metric-label">👤 Usuario</p><p class="metric-value">{user['nombre']}</p></div>
  <div class="metric-chip"><p class="metric-label">⭐ XP</p><p class="metric-value">{user['xp']}</p></div>
  <div class="metric-chip"><p class="metric-label">🔥 Racha</p><p class="metric-value">{plural_dias(user['racha'])}</p></div>
  <div class="metric-chip"><p class="metric-label">📈 Nivel</p><p class="metric-value">{calcular_nivel(user['xp']).split(' - ')[0]}</p></div>
  <div class="metric-chip"><p class="metric-label">📚 Inglés</p><p class="metric-value">{loks} lecc.</p></div>
  <div class="metric-chip"><p class="metric-label">💎 Plan</p><p class="metric-value">{user['plan']}</p></div>
</div>""", unsafe_allow_html=True)
st.progress(progreso_nivel(user["xp"]))
st.caption(f"{calcular_nivel(user['xp'])} — Progreso al siguiente nivel")

# =========================================
# CONFIGURACIÓN
# =========================================

with st.expander("⚙️ Configuración y perfil", expanded=False):
    ca, cb = st.columns(2)
    with ca:
        st.markdown("**🔧 Modo del mentor**")
        st.session_state.modo = st.selectbox("Modo:", ["Mentor de Negocios","Entrenador de Ventas","Marketing LATAM","Disciplina y Hábitos","Ideas de Negocio","Simulación con Cliente Difícil","Planificador de Objetivos","Modo Empresario Exigente","Modo Mentor Millonario","Especialista Supermercados","Especialista E-commerce","Especialista Reventa","Especialista Restaurante","Especialista Inmobiliaria"], label_visibility="collapsed")
        st.markdown("**🧠 Memoria**")
        user["nombre"] = st.text_input("Nombre:", value=user["nombre"])
        user["objetivo"] = st.text_area("Objetivo:", value=user["objetivo"])
        user["negocio"] = st.text_input("Negocio:", value=user["negocio"])
        user["tipo_negocio"] = st.text_input("Tipo:", value=user["tipo_negocio"])
    with cb:
        st.markdown("**📊 Panel empresario**")
        user["meta_mensual"] = st.text_input("Meta mensual:", value=user["meta_mensual"])
        user["ingresos_objetivo"] = st.number_input("Ingresos objetivo ($):", value=int(user["ingresos_objetivo"]), min_value=0)
        user["habito_clave"] = st.text_input("Hábito clave:", value=user["habito_clave"])
        st.markdown("**⚙️ Acciones**")
        if st.button("💾 Guardar"): guardar_usuario(user); st.success("Guardado.")
        if st.button("🧹 Borrar conversación"): st.session_state.confirmar_borrar = True
        if st.session_state.get("confirmar_borrar",False):
            st.warning("¿Seguro? Se borra todo el historial.")
            cs,cn = st.columns(2)
            with cs:
                if st.button("✅ Sí"):
                    user["messages"]=[]; guardar_usuario(user); st.session_state.confirmar_borrar=False; st.rerun()
            with cn:
                if st.button("❌ No"): st.session_state.confirmar_borrar=False; st.rerun()
        if st.button("🔁 Rehacer onboarding"): user["onboarding_completo"]=False; guardar_usuario(user); st.rerun()
        if st.button("🚪 Cerrar sesión"): guardar_usuario(user); st.session_state.logged_in=False; st.rerun()

# =========================================
# TABS
# =========================================

tab_mentor, tab_english, tab_progreso, tab_desafios, tab_premium, tab_ranking, tab_feedback = st.tabs([
    "🧠 Mentor", "📚 Aprender Inglés", "📈 Progreso", "🔥 Desafíos", "💎 Premium", "🏆 Ranking", "💬 Feedback"
])

# --- TAB MENTOR ---
with tab_mentor:
    if not user["messages"]:
        n = user['nombre'] or 'emprendedor'
        obj = f" Tu objetivo: {user['objetivo']}." if user["objetivo"] else ""
        neg = f" sobre tu negocio de {user['negocio']}" if user["negocio"] else ""
        bienvenida = f"¡Hola {n}! Soy AV MentorAI, tu mentor personal.{obj} Estoy listo para ayudarte{neg}. ¿Por dónde empezamos?"
        st.markdown(f'<div class="chat-ai"><div class="chat-name-ai">⚡ AV MentorAI</div><div class="chat-text">{bienvenida}</div></div>', unsafe_allow_html=True)
    else:
        for m in user["messages"]: render_msg(m["role"], m["content"], "negocio")
        ul = obtener_ultima_respuesta(user["messages"])
        if ul and st.button("🔊 Escuchar última respuesta", key="aud_neg"):
            with st.spinner("Generando audio..."): render_audio_player(ul)

    st.divider()
    if not user["messages"]: st.markdown('<div class="guide-text">👇 Tocá un botón o escribí tu primera pregunta abajo</div>', unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    qp = None
    with c1:
        if st.button("💡 Idea de negocio"): qp="Dame una idea de negocio rentable para empezar con pocos recursos."
        if st.button("🎭 Cliente difícil"): qp="Hagamos una simulación. Vos sos un cliente difícil y yo tengo que venderte."
    with c2:
        if st.button("📈 Quiero vender más"): qp="Quiero vender más. Dame un plan práctico para empezar hoy."
        if st.button("🔥 Desafío de hoy"): qp=f"Quiero hacer este desafío: {desafio}. Guiame paso a paso."
    with c3:
        if st.button("📱 Marketing en redes"): qp="Quiero aprender marketing desde cero para vender por redes sociales."
        if st.button("💎 Mentor exigente"): qp="Háblame como mentor exigente y decime qué debería mejorar hoy."

    st.write("")
    with st.expander("📎 Adjuntar imagen o archivo (opcional)", expanded=False):
        st.caption("Subí foto de tu local, producto, catálogo o archivo de texto.")
        arch = st.file_uploader("Archivo:", type=["jpg","jpeg","png","webp","pdf","txt"], label_visibility="collapsed")
        if arch:
            if arch.type in ["image/jpeg","image/png","image/webp","image/jpg"]:
                st.image(arch, caption="Vista previa", use_container_width=True)
            elif arch.type=="application/pdf": st.info(f"📄 PDF: {arch.name}")

    audio = st.audio_input("🎤 Grabá tu pregunta por voz (opcional)")
    vp = None
    if audio:
        with st.spinner("Transcribiendo..."):
            try: vp = transcribir_audio(audio); st.success(f"Escuché: *{vp}*")
            except Exception as e: st.warning(f"No pude transcribir: {e}")

    ui = st.chat_input("Escribí tu pregunta al mentor...")
    if vp: ui = vp
    elif qp: ui = qp

    if ui:
        ib64=None; im=None; na=None
        if arch:
            if arch.type in ["image/jpeg","image/png","image/webp","image/jpg"]:
                ib64, im = imagen_a_base64(arch); na = arch.name
            elif arch.type=="text/plain":
                c = arch.read().decode("utf-8")
                ui = ui + f"\n\n[Archivo {arch.name}]:\n{c[:3000]}"
            elif arch.type=="application/pdf":
                ui = ui + f"\n\n[PDF adjunto: {arch.name}]"
        enviar_negocio(ui, desafio, ib64, im, na)

# --- TAB INGLÉS ---
with tab_english:
    st.markdown('<div class="english-card"><h2>📚 Aprender Inglés</h2><p class="small-text">Tu profesor personal Alex te enseña inglés desde cero, a tu ritmo.</p></div>', unsafe_allow_html=True)

    niv_ing = st.selectbox("Tu nivel de inglés:", ["Principiante","Intermedio","Avanzado"],
        index=["Principiante","Intermedio","Avanzado"].index(user.get("english_nivel","Principiante")))
    if niv_ing != user.get("english_nivel"):
        user["english_nivel"]=niv_ing; guardar_usuario(user)

    loks_list = user.get("english_lecciones_completadas",[])
    lecs_niv = LECCIONES.get(niv_ing,[])
    total = len(lecs_niv)
    comp_niv = sum(1 for l in lecs_niv if l["id"] in loks_list)
    if total>0:
        st.progress(comp_niv/total)
        st.caption(f"{comp_niv}/{total} lecciones completadas en {niv_ing}")

    st.markdown(f"### Lecciones — {niv_ing}")

    for lec in lecs_niv:
        done = lec["id"] in loks_list
        icono = "✅" if done else "📖"
        cl, cb2 = st.columns([4,1])
        with cl:
            card_class = "lesson-card-done" if done else "lesson-card"
            st.markdown(f'<div class="{card_class}"><b>{icono} {lec["titulo"]}</b><br><span class="small-text">{lec["descripcion"]}</span> <span style="color:#facc15;font-size:12px;font-weight:700">+{lec["xp"]} XP</span></div>', unsafe_allow_html=True)
        with cb2:
            lbl = "Repasar" if done else "Ver"
            if st.button(lbl, key=f"lec_{lec['id']}"):
                st.session_state.leccion_seleccionada = lec["id"]; st.rerun()

    # Mostrar lección seleccionada
    lsel = st.session_state.leccion_seleccionada
    if lsel:
        lobj = next((l for l in lecs_niv if l["id"]==lsel), None)
        if lobj:
            st.divider()
            st.markdown(f"## 📖 {lobj['titulo']}")
            st.markdown(f'<div class="lesson-content">{lobj["contenido"]}</div>', unsafe_allow_html=True)
            co1, co2 = st.columns(2)
            with co1:
                if lobj["id"] not in loks_list:
                    if st.button(f"✅ Completada (+{lobj['xp']} XP)"):
                        user["english_lecciones_completadas"].append(lobj["id"])
                        user["english_xp"] = user.get("english_xp",0)+lobj["xp"]
                        sumar_xp(lobj["xp"]); guardar_usuario(user)
                        st.success(f"¡Lección completada! +{lobj['xp']} XP 🎉")
                        st.session_state.leccion_seleccionada=None; st.rerun()
                else:
                    st.success("✅ Ya completaste esta lección")
            with co2:
                if st.button("❌ Cerrar lección"):
                    st.session_state.leccion_seleccionada=None; st.rerun()

    st.divider()
    st.markdown("### 🎓 Practicá con Alex, tu profesor")
    st.caption("Preguntale dudas, pedile ejercicios, practicá conversación o pedile que te corrija.")

    eng_msgs = user.get("english_messages",[])
    if not eng_msgs:
        n = user['nombre'] or 'estudiante'
        bv = f"¡Hola {n}! 👋 Soy Alex, tu profesor de inglés. Estoy acá para enseñarte inglés de forma divertida. ¿Querés empezar desde cero o ya sabés algo? Let's go! 🚀"
        st.markdown(f'<div class="chat-english"><div class="chat-name-english">🎓 Alex — Profesor de Inglés</div><div class="chat-text">{bv}</div></div>', unsafe_allow_html=True)
    else:
        for m in eng_msgs[-20:]: render_msg(m["role"], m["content"], "english")
        ul_eng = obtener_ultima_respuesta(eng_msgs)
        if ul_eng and st.button("🔊 Escuchar a Alex", key="aud_eng"):
            with st.spinner("Generando audio..."): render_audio_player(ul_eng)

    e1,e2,e3 = st.columns(3)
    eq = None
    with e1:
        if st.button("🔤 Verbo To Be"): eq="Explicame el verbo To Be desde cero con ejemplos."
        if st.button("✍️ Corregí mi inglés"): eq="Voy a escribir algo en inglés, corregime si hay errores."
    with e2:
        if st.button("💬 Practicar conversación"): eq="Quiero practicar una conversación en inglés. Empezá vos."
        if st.button("📧 Emails en inglés"): eq="Enseñame a escribir un email en inglés con la estructura correcta."
    with e3:
        if st.button("🎯 Dame un ejercicio"): eq="Dame un ejercicio de inglés para mi nivel actual."
        if st.button("🗣️ Frases cotidianas"): eq="Enseñame frases que uso todos los días en inglés."

    st.write("")
    audio_eng = st.audio_input("🎤 Grabá en inglés y Alex te corrige (opcional)")
    ve = None
    if audio_eng:
        with st.spinner("Transcribiendo..."):
            try: ve=transcribir_audio(audio_eng); st.info(f"Transcribí: *{ve}*")
            except Exception as e: st.warning(f"Error: {e}")

    ei = st.chat_input("Escribile a Alex tu profesor de inglés...")
    if ve: ei=f"Grabé esto en inglés: '{ve}'. ¿Está bien dicho? Corregime si hay errores."
    elif eq: ei=eq

    if ei:
        lec_ctx = None
        if lsel:
            lo = next((l for l in lecs_niv if l["id"]==lsel), None)
            if lo: lec_ctx = lo["titulo"]
        enviar_english(ei, lec_ctx)

    if st.button("🗑️ Borrar chat de inglés"):
        user["english_messages"]=[]; guardar_usuario(user); st.rerun()

# --- TAB PROGRESO ---
with tab_progreso:
    st.markdown("## 📈 Progreso")
    p1,p2,p3,p4 = st.columns(4)
    with p1: st.metric("⭐ XP total", user["xp"])
    with p2: st.metric("🔥 Racha", plural_dias(user["racha"]))
    with p3: st.metric("🎯 Objetivos", user["objetivos_completados"])
    with p4: st.metric("📚 Lecciones inglés", len(user.get("english_lecciones_completadas",[])))

    if user["xp_history"]:
        df = pd.DataFrame(user["xp_history"])
        st.markdown("### Evolución de XP")
        st.line_chart(df.set_index("fecha")["xp"])
    else: st.info("Todavía no hay progreso para mostrar.")

    if st.button("🧠 Generar memoria inteligente"):
        with st.spinner("Generando..."): resumen = generar_resumen(user)
        st.success(resumen)

    if user["logros"]:
        st.markdown("### 🏆 Logros")
        st.markdown("".join([f'<span class="badge">🏆 {l}</span>' for l in user["logros"]]), unsafe_allow_html=True)

    st.markdown("### 📊 Panel empresario")
    st.markdown(f'<div class="card"><p><b>Meta mensual:</b> {user["meta_mensual"] or "Sin definir"}</p><p><b>Ingresos objetivo:</b> ${user["ingresos_objetivo"]}</p><p><b>Hábito clave:</b> {user["habito_clave"] or "Sin definir"}</p><p><b>Tipo de negocio:</b> {user["tipo_negocio"] or "Sin definir"}</p><p><b>Principal dificultad:</b> {user["principal_dificultad"] or "Sin definir"}</p></div>', unsafe_allow_html=True)

# --- TAB DESAFÍOS ---
with tab_desafios:
    st.markdown("## 🔥 Desafío diario")
    st.markdown(f'<div class="challenge-card"><h2>Tu misión de hoy</h2><h3>{desafio}</h3><p class="small-text">Completarlo suma XP y mejora tu racha.</p></div>', unsafe_allow_html=True)
    d1,d2 = st.columns(2)
    with d1:
        if st.button("✅ Completé el desafío"):
            user["desafios_completados"]+=1; sumar_xp(40); guardar_usuario(user)
            st.success("Desafío completado. +40 XP 🎉"); st.rerun()
    with d2:
        if st.button("🎯 Objetivo completado"):
            user["objetivos_completados"]+=1; sumar_xp(60); guardar_usuario(user)
            st.success("Objetivo completado. +60 XP 🏆"); st.rerun()
    st.markdown(f'<div class="card"><p><b>Desafíos:</b> {user["desafios_completados"]}</p><p><b>Objetivos:</b> {user["objetivos_completados"]}</p><p><b>Racha:</b> {plural_dias(user["racha"])}</p></div>', unsafe_allow_html=True)

# --- TAB PREMIUM ---
with tab_premium:
    st.markdown("## 💎 Planes")
    p1,p2,p3 = st.columns(3)
    with p1:
        st.markdown('<div class="plan-card"><h2>Gratis</h2><p>✅ Mentor básico</p><p>✅ Inglés básico</p><p>✅ Desafíos diarios</p><p>⚠️ 10 preguntas/día</p><h1>$0</h1></div>', unsafe_allow_html=True)
        if st.button("Usar Gratis"): user["plan"]="Gratis"; guardar_usuario(user); st.rerun()
    with p2:
        st.markdown('<div class="plan-card"><h2>Pro</h2><p>🚀 Mentor ilimitado</p><p>📚 Inglés completo</p><p>🔊 Voz premium</p><p>📸 Análisis de fotos</p><h1>$4.99 USD</h1></div>', unsafe_allow_html=True)
        if st.button("💳 Activar Pro demo"): user["plan"]="Premium"; guardar_usuario(user); st.success("Plan Pro activado."); st.rerun()
    with p3:
        st.markdown('<div class="plan-card"><h2>Empresarial 🔒</h2><p>🏢 Para equipos</p><p>📈 Métricas avanzadas</p><p>🤖 IA personalizada</p><h1>Consultar</h1></div>', unsafe_allow_html=True)
        st.info("Próximamente: Mercado Pago / Stripe.")
    st.markdown(f'<div class="card"><p><b>Plan actual:</b> {user["plan"]}</p><p><b>Preguntas hoy:</b> {user["preguntas_hoy"]}</p></div>', unsafe_allow_html=True)

# --- TAB RANKING ---
with tab_ranking:
    st.markdown("## 🏆 Ranking")
    rk=[]
    for f in os.listdir(DATA_DIR):
        if f.endswith(".json"):
            try:
                with open(os.path.join(DATA_DIR,f),"r",encoding="utf-8") as fl:
                    u=json.load(fl)
                rk.append({"Usuario":u.get("nombre","?"),"XP":u.get("xp",0),"Racha":u.get("racha",0),"Lecciones inglés":len(u.get("english_lecciones_completadas",[])),"Plan":u.get("plan","Gratis")})
            except: pass
    rk = sorted(rk, key=lambda x:x["XP"], reverse=True)
    st.dataframe(pd.DataFrame(rk), use_container_width=True) if rk else st.info("Todavía no hay usuarios.")

# --- TAB FEEDBACK ---
with tab_feedback:
    st.markdown("## 💬 Feedback")
    cal = st.slider("¿Qué tan útil es AV MentorAI?", 1, 10, 8)
    com = st.text_area("Comentario:", placeholder="Qué te gustó, qué mejorarías...")
    pag = st.selectbox("¿Pagarías por esta app?", ["No sé","Sí","No"])
    if st.button("Enviar feedback"):
        user["feedback"].append({"fecha":str(date.today()),"calificacion":cal,"comentario":com,"pagaria":pag})
        guardar_usuario(user); st.success("Feedback guardado. ✅")
    if user["feedback"]:
        st.markdown("### Feedback guardado")
        st.dataframe(pd.DataFrame(user["feedback"]), use_container_width=True)
