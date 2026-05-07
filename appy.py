# =========================================
# AV MentorAI - v4.0
# Nuevas features: Roleplay, Traductor, Diario, Certificado, Offline
# =========================================

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os, json, hashlib, random, uuid, base64, io
from datetime import date
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

APP_NAME    = "AV MentorAI"
APP_TAGLINE = "Tu mentor personal premium para negocios, ventas y crecimiento."
DATA_DIR    = "usuarios_av_mentorai"
APP_VERSION = "Demo privada v4.0"
MODO_DEV    = True
os.makedirs(DATA_DIR, exist_ok=True)

# ─────────────────────────────────────────
# LECCIONES  (offline — no necesitan IA)
# ─────────────────────────────────────────
LECCIONES = {
    "Principiante": [
        {"id":"p1","titulo":"Saludos básicos","descripcion":"Hello, Hi, Good morning...","xp":20,
         "contenido":"""**Saludos formales:**
- Hello → Hola  |  Good morning → Buenos días
- Good afternoon → Buenas tardes  |  Good night → Buenas noches

**Saludos informales:**
- Hi / Hey → Hola  |  What's up? → ¿Qué onda?
- How are you? → ¿Cómo estás?  |  I'm fine, thanks → Estoy bien

**Despedidas:**
- Bye / Goodbye → Chau  |  See you later → Nos vemos
- Take care → Cuídate  |  Have a good day → Buen día

📝 **Ejercicio:** Escribile un saludo a Alex como si lo encontraras por primera vez hoy.""",
         "quiz":[
             {"pregunta":"¿Cómo se dice 'Buenos días' en inglés?","opciones":["Good night","Good morning","Good evening","Hello"],"correcta":1},
             {"pregunta":"¿Qué significa 'How are you?'","opciones":["¿Cómo te llamás?","¿De dónde sos?","¿Cómo estás?","¿Cuántos años tenés?"],"correcta":2},
             {"pregunta":"¿Cuál es la forma más informal de decir 'Hola'?","opciones":["Hello","Good morning","Hey","Greetings"],"correcta":2},
             {"pregunta":"¿Cómo se dice 'Nos vemos después'?","opciones":["Goodbye","Take care","See you later","Good night"],"correcta":2},
             {"pregunta":"'I'm fine, thanks' significa:","opciones":["Estoy cansado","Estoy bien, gracias","Mucho gusto","Hasta luego"],"correcta":1},
         ]},
        {"id":"p2","titulo":"El verbo To Be","descripcion":"I am, You are, He/She is...","xp":25,
         "contenido":"""El verbo **To Be** = ser / estar. El más importante del inglés.

**Afirmativa:**
I am / I'm → Yo soy  |  You are / You're → Vos sos
He is / He's → Él es  |  She is / She's → Ella es
We are / We're → Somos  |  They are / They're → Ellos son

**Negativa:** agrega "not"
I'm not → No soy  |  He isn't → Él no es

**Preguntas:** invierte el orden
Are you okay? → ¿Estás bien?  |  Is she your sister? → ¿Es tu hermana?

📝 **Ejercicio:** Escribí 3 oraciones sobre vos usando I am / I'm.""",
         "quiz":[
             {"pregunta":"¿Cómo se dice 'Ella es mi amiga'?","opciones":["She am my friend","She is my friend","She are my friend","Her is my friend"],"correcta":1},
             {"pregunta":"La contracción de 'I am' es:","opciones":["I'm","Im","I'am","Iam"],"correcta":0},
             {"pregunta":"¿Cómo se hace una pregunta con To Be?","opciones":["You are okay?","Are you okay?","Is you okay?","Am you okay?"],"correcta":1},
             {"pregunta":"'We are from Argentina' en negativo es:","opciones":["We not are from Argentina","We are not from Argentina","We isn't from Argentina","We aren't from Argentina"],"correcta":3},
             {"pregunta":"¿Cuál es la forma correcta?","opciones":["They is ready","They am ready","They are ready","They be ready"],"correcta":2},
         ]},
        {"id":"p3","titulo":"Números del 1 al 100","descripcion":"One, two, three... one hundred","xp":20,
         "contenido":"""**Del 1 al 20:**
1-one  2-two  3-three  4-four  5-five  6-six  7-seven  8-eight  9-nine  10-ten
11-eleven  12-twelve  13-thirteen  14-fourteen  15-fifteen
16-sixteen  17-seventeen  18-eighteen  19-nineteen  20-twenty

**Decenas:**
30-thirty  40-forty  50-fifty  60-sixty  70-seventy  80-eighty  90-ninety  100-one hundred

**Combinaciones:**
21 → twenty-one  |  45 → forty-five  |  99 → ninety-nine

**En el negocio:**
It costs fifty dollars → Cuesta $50
I have thirty products → Tengo 30 productos

📝 **Ejercicio:** ¿Cómo se dice 27, 53 y 88 en inglés?""",
         "quiz":[
             {"pregunta":"¿Cómo se dice '15' en inglés?","opciones":["Fifty","Fiveteen","Fifteen","Fiftieth"],"correcta":2},
             {"pregunta":"¿Cómo se escribe '40'?","opciones":["Fourty","Forty","Fourtee","Fority"],"correcta":1},
             {"pregunta":"'Eighty-seven' es el número:","opciones":["78","87","88","76"],"correcta":1},
             {"pregunta":"¿Cómo se dice 'Cuesta veinte dólares'?","opciones":["It costs twenty dollars","It cost twenty dollar","It costs twenty dollar","Its cost twenty dollars"],"correcta":0},
             {"pregunta":"'Thirty-three' es:","opciones":["23","43","33","34"],"correcta":2},
         ]},
        {"id":"p4","titulo":"Presentarse en inglés","descripcion":"My name is, I'm from, I work...","xp":25,
         "contenido":"""**Frases básicas:**
My name is... → Mi nombre es...
I'm... → Soy... (informal)  |  Nice to meet you → Mucho gusto

**De dónde sos:**
I'm from Argentina → Soy de Argentina
I live in Buenos Aires → Vivo en Buenos Aires

**Tu trabajo:**
I own a business → Tengo un negocio
I'm an entrepreneur → Soy emprendedor/a

**Edad:**
I'm 25 years old → Tengo 25 años

**Ejemplo completo:**
"Hi! My name is Valentino. I'm from Argentina. I'm 25 and I own a business. Nice to meet you!"

📝 **Ejercicio:** Escribí tu propia presentación completa.""",
         "quiz":[
             {"pregunta":"¿Cómo se dice 'Mi nombre es Ana'?","opciones":["My name are Ana","I name is Ana","My name is Ana","I'm name Ana"],"correcta":2},
             {"pregunta":"'Nice to meet you' significa:","opciones":["Hasta luego","Mucho gusto","¿Cómo estás?","Bienvenido"],"correcta":1},
             {"pregunta":"¿Cómo decís 'Soy de Argentina'?","opciones":["I am from of Argentina","I'm Argentina","I'm from Argentina","I come Argentina"],"correcta":2},
             {"pregunta":"'I'm 30 years old' significa:","opciones":["Tengo 13 años","Tengo 30 años","Soy de los 30","Vivo hace 30 años"],"correcta":1},
             {"pregunta":"'I own a business' significa:","opciones":["Busco un negocio","Vendo negocios","Tengo un negocio","Trabajo en negocios"],"correcta":2},
         ]},
        {"id":"p5","titulo":"Vocabulario esencial","descripcion":"Las palabras más usadas en inglés","xp":30,
         "contenido":"""**Palabras básicas:**
Yes/No/Maybe → Sí/No/Quizás  |  Please → Por favor  |  Thank you → Gracias
Sorry → Perdón  |  Help → Ayuda  |  Stop → Para  |  Go → Ir/Andá

**Preguntas:**
What? → ¿Qué?  |  Who? → ¿Quién?  |  Where? → ¿Dónde?
When? → ¿Cuándo?  |  Why? → ¿Por qué?  |  How? → ¿Cómo?
How much? → ¿Cuánto cuesta?

**Tiempo:**
Today/Yesterday/Tomorrow → Hoy/Ayer/Mañana
Now/Later → Ahora/Después  |  Always/Never/Sometimes → Siempre/Nunca/A veces

**Colores:**
Red-rojo  Blue-azul  Green-verde  Yellow-amarillo  Black-negro  White-blanco

📝 **Ejercicio:** Usá 5 de estas palabras en oraciones propias.""",
         "quiz":[
             {"pregunta":"¿Cómo se dice 'Por favor' en inglés?","opciones":["Thank you","Sorry","Please","Excuse me"],"correcta":2},
             {"pregunta":"'How much?' pregunta sobre:","opciones":["Cantidad","Precio","Tiempo","Lugar"],"correcta":1},
             {"pregunta":"'Yesterday' significa:","opciones":["Hoy","Mañana","Ayer","Después"],"correcta":2},
             {"pregunta":"¿Cómo se dice 'A veces'?","opciones":["Always","Never","Sometimes","Usually"],"correcta":2},
             {"pregunta":"'Blue' es el color:","opciones":["Rojo","Verde","Amarillo","Azul"],"correcta":3},
         ]},
    ],
    "Intermedio": [
        {"id":"i1","titulo":"Presente simple","descripcion":"I work, She works, They play...","xp":35,
         "contenido":"""**Cuándo usarlo:** rutinas, hábitos, hechos permanentes.

**Estructura:**
Afirmativa: Sujeto + verbo (+ s en 3ra persona)
Negativa: Sujeto + don't / doesn't + verbo
Pregunta: Do / Does + sujeto + verbo?

**Ejemplos:**
I sell products every day → Vendo productos todos los días
She works in the morning → Ella trabaja por la mañana
I don't have time → No tengo tiempo
Do you have a store? → ¿Tenés una tienda?

**Palabras clave:** always, usually, often, sometimes, never, every day/week

📝 **Ejercicio:** Describí tu rutina de trabajo (mínimo 4 oraciones).""",
         "quiz":[
             {"pregunta":"¿Cuál es correcta para 3ra persona?","opciones":["She work here","She works here","She working here","She do work here"],"correcta":1},
             {"pregunta":"La negativa de 'I work' es:","opciones":["I not work","I don't work","I doesn't work","I no work"],"correcta":1},
             {"pregunta":"¿Cómo se pregunta '¿Él trabaja acá?'","opciones":["He works here?","Does he work here?","Do he works here?","Is he work here?"],"correcta":1},
             {"pregunta":"'She doesn't sell online' en afirmativo es:","opciones":["She sells online","She do sell online","She selling online","She sold online"],"correcta":0},
             {"pregunta":"¿Cuál palabra indica presente simple?","opciones":["Yesterday","Tomorrow","Every day","Right now"],"correcta":2},
         ]},
        {"id":"i2","titulo":"Pasado simple","descripcion":"I worked, She bought, They went...","xp":35,
         "contenido":"""**Cuándo usarlo:** acciones ya terminadas.

**Verbos regulares:** agrega -ed
work→worked  |  call→called  |  open→opened

**Irregulares más usados:**
go→went  |  buy→bought  |  sell→sold  |  have→had
make→made  |  come→came  |  see→saw  |  get→got

**Ejemplos:**
Yesterday I sold 10 products → Ayer vendí 10 productos
We had a great month → Tuvimos un mes excelente

**Negativa:** didn't + verbo base
I didn't sell anything → No vendí nada

**Pregunta:** Did + sujeto + verbo?
Did you make money? → ¿Hiciste plata?

📝 **Ejercicio:** Contá qué hiciste ayer en tu negocio.""",
         "quiz":[
             {"pregunta":"¿Cuál es el pasado de 'buy'?","opciones":["Buyed","Buyd","Bought","Boughted"],"correcta":2},
             {"pregunta":"La negativa de 'I went' es:","opciones":["I didn't went","I didn't go","I don't went","I not went"],"correcta":1},
             {"pregunta":"¿Cómo se pregunta '¿Fuiste al mercado?'","opciones":["Did you go to the market?","You went to the market?","Did you went to the market?","Were you go to the market?"],"correcta":0},
             {"pregunta":"El pasado de 'make' es:","opciones":["Maked","Makes","Made","Maden"],"correcta":2},
             {"pregunta":"'She saw the client yesterday' significa:","opciones":["Ella verá al cliente mañana","Ella vio al cliente ayer","Ella ve al cliente siempre","Ella llamó al cliente ayer"],"correcta":1},
         ]},
        {"id":"i3","titulo":"Inglés para ventas","descripcion":"Frases clave para vender en inglés","xp":40,
         "contenido":"""**Presentar un producto:**
This product is... → Este producto es...
It helps you to... → Te ayuda a...
This is our best seller → Este es nuestro más vendido

**Preguntar al cliente:**
What are you looking for? → ¿Qué buscás?
What's your budget? → ¿Cuál es tu presupuesto?
Would you like to try it? → ¿Querés probarlo?

**Manejar objeciones:**
I understand your concern → Entiendo tu preocupación
Let me explain... → Dejame explicarte...
Actually, the quality is... → En realidad la calidad es...

**Cerrar la venta:**
Shall we close the deal? → ¿Cerramos el trato?
I'll give you a discount → Te hago un descuento
It's a great investment → Es una gran inversión

📝 **Ejercicio:** Presentá un producto tuyo en inglés.""",
         "quiz":[
             {"pregunta":"'What are you looking for?' pregunta:","opciones":["El precio","El presupuesto","Qué busca el cliente","Si quiere probar el producto"],"correcta":2},
             {"pregunta":"¿Cómo se dice 'Cerramos el trato'?","opciones":["Let's close the deal","Shall we close the deal?","We close the deal","Close the deal now"],"correcta":1},
             {"pregunta":"'I'll give you a discount' significa:","opciones":["No hay descuento","El precio es fijo","Te hago un descuento","El descuento ya aplicó"],"correcta":2},
             {"pregunta":"Para manejar una objeción usás:","opciones":["Shall we close?","I understand your concern","What's your budget?","This is our best seller"],"correcta":1},
             {"pregunta":"'This is our best seller' significa:","opciones":["Este es el más caro","Este es el más nuevo","Este es el más vendido","Este es el mejor precio"],"correcta":2},
         ]},
        {"id":"i4","titulo":"Emails en inglés","descripcion":"Cómo escribir emails profesionales","xp":40,
         "contenido":"""**Estructura:**
1. Saludo  2. Por qué escribís  3. Cuerpo  4. Cierre

**Saludos:**
Dear Mr./Ms. [apellido] → formal
Hi [nombre] → informal

**Frases útiles:**
I'm writing to... → Le escribo para...
Could you please...? → ¿Podría por favor...?
Please find attached... → Adjunto encontrará...
I look forward to hearing from you → Quedo a la espera

**Cierres:**
Best regards → Saludos cordiales
Kind regards → Atentamente
Thanks → Gracias (informal)

**Ejemplo:**
"Hi John, I'm writing to ask about your prices. Could you send me your catalogue? Best regards, Valentino."

📝 **Ejercicio:** Escribí un email a un proveedor pidiendo precios.""",
         "quiz":[
             {"pregunta":"¿Cuál es el cierre más formal?","opciones":["Thanks","Bye","Kind regards","See you"],"correcta":2},
             {"pregunta":"'I'm writing to...' se usa para:","opciones":["Despedirse","Presentarse","Explicar por qué escribís","Pedir un descuento"],"correcta":2},
             {"pregunta":"¿Cómo se saluda formalmente en un email?","opciones":["Hey John","Hi there","Dear Mr. Smith","Hello buddy"],"correcta":2},
             {"pregunta":"'Please find attached' indica:","opciones":["Que hay un archivo adjunto","Que el precio está adjunto","Que encontraste algo","Que adjuntás la respuesta"],"correcta":0},
             {"pregunta":"'I look forward to hearing from you' significa:","opciones":["No espero tu respuesta","Quedo a la espera de tu respuesta","Escucho tu música","Miro hacia adelante"],"correcta":1},
         ]},
    ],
    "Avanzado": [
        {"id":"a1","titulo":"Negociación en inglés","descripcion":"Negociar precios, condiciones y contratos","xp":50,
         "contenido":"""**Abrir:**
I'd like to discuss the terms → Quiero hablar de los términos
I have a proposal for you → Tengo una propuesta

**Hacer ofertas:**
We can offer you... → Podemos ofrecerte...
If you order more, we can lower the price → Si pedís más, bajamos el precio

**Contraofertas:**
That's a bit high for us → Eso es un poco alto
Could you do better? → ¿Podría mejorar eso?
Let's meet in the middle → Encontrémonos en el medio

**Cerrar:**
We have a deal → Tenemos un trato
I'll send you the contract → Te mando el contrato
When can we start? → ¿Cuándo empezamos?

📝 **Ejercicio:** Hacé un roleplay de negociación con Alex.""",
         "quiz":[
             {"pregunta":"'We have a deal' significa:","opciones":["Tenemos un problema","Tenemos un trato","Hacemos un trato","Hacemos negocios"],"correcta":1},
             {"pregunta":"'Let's meet in the middle' propone:","opciones":["Reunirse en el centro","Llegar a un punto medio","Encontrarse a mitad de camino","Hablar en el centro"],"correcta":1},
             {"pregunta":"¿Cómo propones bajar el precio si compran más?","opciones":["If you buy more, price go down","If you order more, we can lower the price","We lower price if more order","More order, less price"],"correcta":1},
             {"pregunta":"'Could you do better?' es una:","opciones":["Oferta inicial","Contraoferta","Aceptación","Cierre"],"correcta":1},
             {"pregunta":"'I'd like to discuss the terms' se usa para:","opciones":["Cerrar el trato","Rechazar la oferta","Abrir una negociación","Pedir un descuento"],"correcta":2},
         ]},
        {"id":"a2","titulo":"Presentaciones de negocio","descripcion":"Presentar tu negocio en inglés","xp":50,
         "contenido":"""**Estructura:**
1. Hook  2. El problema  3. Tu solución  4. Por qué vos  5. Call to action

**Hook:**
Did you know that...? → ¿Sabías que...?
Imagine a world where... → Imaginate un mundo donde...

**El problema:**
The main challenge is... → El principal desafío es...
Most people struggle with... → La mayoría lucha con...

**Tu solución:**
We've developed... → Desarrollamos...
Unlike competitors, we... → A diferencia de los competidores...

**Call to action:**
Let's work together → Trabajemos juntos
Contact us today → Contactanos hoy

📝 **Ejercicio:** Prepará una presentación de 1 minuto de tu negocio.""",
         "quiz":[
             {"pregunta":"¿Qué es un 'Hook' en una presentación?","opciones":["El cierre","La solución","Lo que engancha la atención","El problema"],"correcta":2},
             {"pregunta":"'Unlike competitors, we...' sirve para:","opciones":["Criticar a la competencia","Diferenciarte de los competidores","Hablar del precio","Presentar el problema"],"correcta":1},
             {"pregunta":"'Let's work together' es un:","opciones":["Hook","Call to action","Presentación del problema","Introducción"],"correcta":1},
             {"pregunta":"¿Qué va después del Hook?","opciones":["La solución","El call to action","El problema","Por qué vos"],"correcta":2},
             {"pregunta":"'Most people struggle with...' presenta:","opciones":["La solución","El equipo","El problema","El precio"],"correcta":2},
         ]},
        {"id":"a3","titulo":"Phrasal verbs de negocios","descripcion":"Los verbos compuestos más usados","xp":45,
         "contenido":"""Los **phrasal verbs** = verbo + preposición. Muy usados en inglés real.

**Los más importantes:**
Set up → Establecer (I set up my business last year)
Take over → Tomar control (They took over the company)
Scale up → Escalar (We need to scale up)
Cut down → Reducir (We cut down costs)
Follow up → Hacer seguimiento (I'll follow up with the client)
Break even → Cubrir costos (We finally broke even)
Run out of → Quedarse sin (We ran out of stock)
Put off → Posponer (Don't put off that meeting)
Turn down → Rechazar (They turned down our offer)
Come up with → Idear (She came up with a great plan)

📝 **Ejercicio:** Usá 5 phrasal verbs en oraciones sobre tu negocio.""",
         "quiz":[
             {"pregunta":"'Follow up' en negocios significa:","opciones":["Seguir en redes","Hacer seguimiento","Seguir comprando","Seguir al cliente"],"correcta":1},
             {"pregunta":"'We ran out of stock' significa:","opciones":["Corrimos al almacén","Nos quedamos sin stock","Llenamos el stock","Vendimos todo el stock"],"correcta":1},
             {"pregunta":"'Put off' significa:","opciones":["Pagar","Posponer","Rechazar","Apagar"],"correcta":1},
             {"pregunta":"'Break even' en negocios significa:","opciones":["Romper un acuerdo","Hacer una pausa","Cubrir los costos","Ganar mucho"],"correcta":2},
             {"pregunta":"'She came up with a great plan' significa:","opciones":["Ella llegó con un plan","Ella ideó un gran plan","Ella siguió el plan","Ella vendió el plan"],"correcta":1},
         ]},
    ],
}

SITUACIONES_ROLEPLAY = [
    {"id":"r1","emoji":"✈️","titulo":"En el aeropuerto","descripcion":"Check-in, migraciones, preguntas básicas"},
    {"id":"r2","emoji":"🤝","titulo":"Negociación con proveedor","descripcion":"Precios, condiciones, cierre de trato"},
    {"id":"r3","emoji":"💼","titulo":"Entrevista de trabajo","descripcion":"Preguntas típicas de una entrevista en inglés"},
    {"id":"r4","emoji":"🍽️","titulo":"En un restaurante","descripcion":"Pedir comida, preguntar al mozo, pagar"},
    {"id":"r5","emoji":"🏪","titulo":"Atender a un cliente extranjero","descripcion":"Venderle algo a alguien que solo habla inglés"},
    {"id":"r6","emoji":"📞","titulo":"Llamada de negocios","descripcion":"Concertar reuniones, presentarse por teléfono"},
    {"id":"r7","emoji":"🛒","titulo":"Comprar en una tienda","descripcion":"Preguntar precios, tallas, disponibilidad"},
    {"id":"r8","emoji":"🏨","titulo":"En el hotel","descripcion":"Check-in, pedir servicios, hacer reclamos"},
]

# ─────────────────────────────────────────
# PAGE CONFIG + CSS
# ─────────────────────────────────────────
st.set_page_config(page_title=APP_NAME, page_icon="⚡", layout="wide")

st.markdown("""
<style>
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
.stApp{background:radial-gradient(circle at top left,#1f2937 0%,#0b1120 45%,#020617 100%);color:white;}
.block-container{padding-top:1.2rem;padding-bottom:5rem;max-width:880px;}
h1,h2,h3,h4,p,label,span{color:#f8fafc!important;}
.av-logo{font-size:48px;font-weight:900;background:linear-gradient(90deg,#facc15,#38bdf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.av-subtitle{font-size:16px;color:#cbd5e1!important;margin-bottom:10px;}
.hero-card,.card,.plan-card,.challenge-card{background:rgba(15,23,42,.88);border:1px solid rgba(148,163,184,.22);border-radius:20px;padding:18px;box-shadow:0 8px 24px rgba(0,0,0,.3);margin-bottom:14px;}
.hero-card{background:linear-gradient(135deg,rgba(250,204,21,.16),rgba(56,189,248,.10));border:1px solid rgba(250,204,21,.35);padding:16px 20px;}
.challenge-card{background:linear-gradient(135deg,rgba(249,115,22,.18),rgba(250,204,21,.10));border:1px solid rgba(250,204,21,.45);}
.english-card{background:linear-gradient(135deg,rgba(56,189,248,.15),rgba(99,102,241,.10));border:1px solid rgba(56,189,248,.35);border-radius:20px;padding:18px;margin-bottom:14px;}
.lesson-card{background:rgba(15,23,42,.88);border:1px solid rgba(56,189,248,.25);border-radius:16px;padding:14px;margin-bottom:8px;}
.lesson-card-done{background:rgba(15,23,42,.88);border:1px solid rgba(34,197,94,.5);border-radius:16px;padding:14px;margin-bottom:8px;}
.lesson-content{background:rgba(15,23,42,.95);border:1px solid rgba(56,189,248,.3);border-radius:16px;padding:20px;margin-bottom:14px;line-height:1.7;white-space:pre-wrap;}
.quiz-card{background:rgba(15,23,42,.95);border:1px solid rgba(250,204,21,.3);border-radius:16px;padding:18px;margin-bottom:14px;}
.roleplay-card{background:linear-gradient(135deg,rgba(168,85,247,.15),rgba(56,189,248,.10));border:1px solid rgba(168,85,247,.35);border-radius:16px;padding:16px;margin-bottom:10px;}
.diary-card{background:rgba(15,23,42,.95);border:1px solid rgba(34,197,94,.3);border-radius:16px;padding:18px;margin-bottom:12px;}
.metrics-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;}
.metric-chip{background:rgba(15,23,42,.88);border:1px solid rgba(148,163,184,.22);border-radius:14px;padding:8px 14px;text-align:center;flex:1;min-width:70px;}
.metric-chip .metric-label{font-size:11px;color:#94a3b8!important;margin:0;}
.metric-chip .metric-value{font-size:16px;font-weight:800;color:#facc15!important;margin:2px 0 0 0;}
.chat-user{background:rgba(30,41,59,.95);border-left:4px solid #facc15;padding:14px 16px;border-radius:16px;margin-bottom:12px;}
.chat-ai{background:rgba(15,23,42,.96);border-left:4px solid #38bdf8;padding:14px 16px;border-radius:16px;margin-bottom:12px;}
.chat-english{background:rgba(15,23,42,.96);border-left:4px solid #a855f7;padding:14px 16px;border-radius:16px;margin-bottom:12px;}
.chat-name{font-weight:900;font-size:13px;color:#facc15!important;margin-bottom:6px;text-transform:uppercase;}
.chat-name-ai{font-weight:900;font-size:13px;color:#38bdf8!important;margin-bottom:6px;text-transform:uppercase;}
.chat-name-english{font-weight:900;font-size:13px;color:#a855f7!important;margin-bottom:6px;text-transform:uppercase;}
.chat-text{color:#f1f5f9!important;line-height:1.65;font-size:15px;white-space:pre-wrap;}
.badge{display:inline-block;background:linear-gradient(90deg,#facc15,#f97316);color:#111827!important;padding:6px 12px;border-radius:12px;font-weight:800;margin:3px;font-size:13px;}
.small-text{color:#cbd5e1!important;font-size:14px;}
.guide-text{color:#94a3b8!important;font-size:14px;text-align:center;padding:10px;border:1px dashed rgba(148,163,184,.3);border-radius:12px;margin-bottom:12px;}
.stButton>button{border-radius:12px;border:1px solid rgba(250,204,21,.45);background:linear-gradient(90deg,#facc15,#f97316);color:#111827;font-weight:800;font-size:14px;}
.stTextInput input,.stTextArea textarea{background-color:#0f172a!important;color:#f8fafc!important;border-radius:12px!important;border:1px solid rgba(250,204,21,.3)!important;}
/* CHAT INPUT */
[data-testid="stChatInput"]{background:#1e293b!important;border:2px solid #facc15!important;border-radius:16px!important;padding:4px!important;}
[data-testid="stChatInput"] > div{background:#1e293b!important;border-radius:14px!important;}
[data-testid="stChatInput"] textarea{background:#1e293b!important;color:#f8fafc!important;font-size:15px!important;border:none!important;}
[data-testid="stChatInput"] textarea::placeholder{color:#facc15!important;opacity:0.8!important;font-size:14px!important;}

/* AUDIO INPUT — fondo oscuro */
[data-testid="stAudioInput"]{background:#1e293b!important;border:1px solid rgba(250,204,21,.3)!important;border-radius:14px!important;}
[data-testid="stAudioInput"] > div{background:#1e293b!important;border-radius:14px!important;}
[data-testid="stAudioInput"] button{background:#1e293b!important;}
[data-testid="stAudioInput"] *{background:#1e293b!important;color:#f8fafc!important;}
[data-testid="stExpander"]{background:rgba(15,23,42,.88)!important;border:1px solid rgba(250,204,21,.25)!important;border-radius:16px!important;}

/* RADIO BUTTONS COMO TABS */
div[data-testid="stRadio"] > div {
    gap: 8px !important;
    flex-wrap: wrap !important;
}
div[data-testid="stRadio"] label {
    background: rgba(15,23,42,.88) !important;
    border: 1px solid rgba(148,163,184,.25) !important;
    border-radius: 10px !important;
    padding: 6px 12px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    color: #cbd5e1 !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: rgba(250,204,21,.15) !important;
    border-color: #facc15 !important;
    color: #facc15 !important;
}

/* FORZAR BOTÓN HAMBURGUESA VISIBLE EN MOBILE */
[data-testid="stSidebarCollapsedControl"]{
    display:block!important;
    visibility:visible!important;
    opacity:1!important;
    background:rgba(250,204,21,.15)!important;
    border:1px solid rgba(250,204,21,.4)!important;
    border-radius:10px!important;
    padding:4px!important;
}
[data-testid="stSidebarCollapsedControl"] svg{
    fill:#facc15!important;
    width:24px!important;
    height:24px!important;
}
section[data-testid="stSidebarContent"]{
    padding-top:1rem!important;
}

/* SIDEBAR NAVIGATION */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#020617 0%,#0b1120 100%)!important;border-right:1px solid rgba(250,204,21,.2)!important;}
[data-testid="stSidebar"] .stButton>button{
    background:transparent!important;border:none!important;color:#cbd5e1!important;
    font-size:15px!important;font-weight:600!important;text-align:left!important;
    width:100%!important;padding:12px 16px!important;border-radius:12px!important;
    margin-bottom:4px!important;transition:all .2s!important;
}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(250,204,21,.1)!important;color:#facc15!important;}
.nav-active>button{background:rgba(250,204,21,.15)!important;color:#facc15!important;border-left:3px solid #facc15!important;}
.nav-section{color:#64748b!important;font-size:11px!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:1px!important;padding:12px 16px 4px!important;}
@media(max-width:768px){
    .av-logo{font-size:28px;}
    .chat-text{font-size:13px;}
    .block-container{padding-left:.6rem;padding-right:.6rem;padding-top:.5rem;}
    h1{font-size:20px!important;}
    h2{font-size:17px!important;}
    h3{font-size:15px!important;}
    .hero-card,.card,.plan-card,.challenge-card{padding:12px;}
    [data-testid="stTabs"] [data-baseweb="tab"]{font-size:11px!important;padding:6px 8px!important;}
    .stButton>button{font-size:13px!important;padding:6px 10px!important;}
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# USUARIOS
# ─────────────────────────────────────────
def limpiar_email(e): return e.lower().strip().replace("@","_at_").replace(".","_")
def archivo_usuario(e): return os.path.join(DATA_DIR, f"{limpiar_email(e)}.json")
def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()

def usuario_default(nombre, email, password):
    return {"nombre":nombre,"email":email,"password":hash_pw(password),"plan":"Gratis",
            "xp":0,"racha":0,"messages":[],"memoria_larga":[],"onboarding_completo":False,
            "objetivo":"","negocio":"","tipo_negocio":"","nivel_usuario":"Principiante",
            "tiempo_diario":"","principal_dificultad":"","meta_mensual":"","ingresos_objetivo":0,
            "habito_clave":"","desafios_completados":0,"objetivos_completados":0,"logros":[],
            "xp_history":[],"ultima_fecha":"","fecha_desafio":"","desafio_actual":"",
            "preguntas_hoy":0,"fecha_preguntas":"","feedback":[],
            "english_nivel":"Principiante","english_lecciones_completadas":[],
            "english_messages":[],"english_xp":0,
            "english_roleplay_messages":[],"english_roleplay_situacion":None,
            "english_diary":[],"english_quiz_scores":{}}

def guardar_usuario(data):
    with open(archivo_usuario(data["email"]),"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

def cargar_usuario(email):
    path = archivo_usuario(email)
    if not os.path.exists(path): return None
    with open(path,"r",encoding="utf-8") as f: data=json.load(f)
    dft = usuario_default(data.get("nombre",""),data.get("email",email),"x")
    for k,v in dft.items():
        if k not in data: data[k]=v
    return data

def crear_usuario(nombre,email,password):
    if cargar_usuario(email): return False
    guardar_usuario(usuario_default(nombre,email,password)); return True

def login(email,password):
    u=cargar_usuario(email)
    if not u: return None
    if (u.get("password") or u.get("password_hash"))==hash_pw(password): return u
    return None

# ─────────────────────────────────────────
# FUNCIONES APP
# ─────────────────────────────────────────
def calcular_nivel(xp):
    if xp<100: return "Nivel 1 - Inicial"
    if xp<300: return "Nivel 2 - En crecimiento"
    if xp<700: return "Nivel 3 - Estratega"
    if xp<1200: return "Nivel 4 - Empresario Pro"
    return "Nivel 5 - Élite"

def progreso_nivel(xp):
    if xp<100: return xp/100
    if xp<300: return (xp-100)/200
    if xp<700: return (xp-300)/400
    if xp<1200: return (xp-700)/500
    return 1.0

def plural_dias(n): return f"{n} día" if n==1 else f"{n} días"

def desbloquear_logros(user):
    loks=len(user.get("english_lecciones_completadas",[]))
    diary=len(user.get("english_diary",[]))
    reglas=[
        (user["xp"]>=100,"Primeros 100 XP"),(user["xp"]>=300,"Mente en crecimiento"),
        (user["xp"]>=700,"Estratega en formación"),(user["racha"]>=3,"Racha de 3 días"),
        (user["racha"]>=7,"Semana imparable"),(user["desafios_completados"]>=5,"5 desafíos completados"),
        (user["objetivos_completados"]>=3,"Constructor de objetivos"),
        (loks>=3,"Estudiante de inglés"),(loks>=8,"Angloparlante en progreso"),
        (loks>=12,"Inglés dominado 🏆"),(diary>=7,"Diario de 7 días"),
        (diary>=30,"Escritor constante 📝"),
    ]
    for cond,logro in reglas:
        if cond and logro not in user["logros"]: user["logros"].append(logro)

def sumar_xp(cantidad):
    user=st.session_state.user_data; user["xp"]+=cantidad
    hoy=str(date.today())
    if user.get("ultima_fecha","")!=hoy: user["racha"]+=1; user["ultima_fecha"]=hoy
    user["xp_history"].append({"fecha":hoy,"xp":user["xp"]})
    desbloquear_logros(user); guardar_usuario(user)

def generar_desafio(user):
    desafios=["Mandá mensajes a 3 clientes potenciales.","Publicá un producto o servicio hoy.",
        "Analizá un negocio local y anotá qué harías mejor.",
        "Pensá una oferta irresistible: producto + beneficio + urgencia.",
        "Grabá un video corto vendiendo algo.","Diseñá una promoción simple por WhatsApp.",
        "Buscá 3 competidores en Instagram y analizá qué hacen bien.",
        "Mejorá la descripción de un producto o servicio.",
        "Creá una lista de 10 productos o servicios que podrías vender.",
        "Armá una estrategia para vender más sin bajar demasiado el margen."]
    hoy=str(date.today())
    if user.get("fecha_desafio","")!=hoy:
        user["desafio_actual"]=random.choice(desafios); user["fecha_desafio"]=hoy; guardar_usuario(user)
    return user["desafio_actual"]

def transcribir_audio(audio_file):
    return client.audio.transcriptions.create(model="whisper-1",file=audio_file).text

def generar_audio_bytes(texto):
    ap=f"tmp_{uuid.uuid4().hex}.mp3"
    with client.audio.speech.with_streaming_response.create(model="tts-1",voice="alloy",input=texto[:1200]) as r:
        r.stream_to_file(ap)
    with open(ap,"rb") as f: b=f.read()
    try: os.remove(ap)
    except: pass
    return b

def render_audio_player(texto):
    try:
        b=generar_audio_bytes(texto)
        st.audio(b,format="audio/mpeg")
        st.download_button("⬇️ Descargar audio",data=b,file_name="respuesta.mp3",mime="audio/mpeg")
    except Exception as e: st.warning(f"No se pudo generar el audio: {e}")

def imagen_a_base64(f):
    return base64.b64encode(f.read()).decode("utf-8"), f.type

def obtener_ultima_respuesta(msgs):
    for m in reversed(msgs):
        if m["role"]=="assistant": return m["content"]
    return None

def render_msg(role,content,tipo="negocio"):
    if role=="user":
        st.markdown(f'''<div class="chat-user">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#facc15,#f97316);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0">😊</div>
            <div class="chat-name" style="margin:0">Vos</div>
        </div>
        <div class="chat-text" style="padding-left:44px">{content}</div>
        </div>''',unsafe_allow_html=True)
    elif tipo=="english":
        st.markdown(f'''<div class="chat-english">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#a855f7,#6366f1);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0">🎓</div>
            <div class="chat-name-english" style="margin:0">Alex — Profesor de Inglés</div>
        </div>
        <div class="chat-text" style="padding-left:44px">{content}</div>
        </div>''',unsafe_allow_html=True)
    else:
        st.markdown(f'''<div class="chat-ai">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#38bdf8,#6366f1);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0">⚡</div>
            <div class="chat-name-ai" style="margin:0">AV MentorAI</div>
        </div>
        <div class="chat-text" style="padding-left:44px">{content}</div>
        </div>''',unsafe_allow_html=True)

# ─── System prompts ───
def system_negocio(user,modo,desafio):
    mem="\n".join(user.get("memoria_larga",[])[-6:])
    return f"""Eres AV MentorAI, mentor premium de negocios, ventas y marketing para LATAM.
Usuario: {user['nombre']} | Plan: {user['plan']} | Objetivo: {user['objetivo']}
Negocio: {user['negocio']} | Tipo: {user['tipo_negocio']} | Nivel: {user['nivel_usuario']}
XP: {user['xp']} | Racha: {user['racha']} días | Modo: {modo} | Desafío: {desafio}
Memoria: {mem}
Identidad: Moderno, directo, motivador. "No lo pienses tanto, ejecutalo." "El negocio premia al que acciona mejor."
Estilo: Español latino, claro, práctico. Ejemplos de WhatsApp, Instagram, Mercado Libre.
Siempre terminá con una acción concreta para HOY. Si hay imagen, analizala con criterio empresarial."""

def system_english(user,leccion=None,modo="chat"):
    nivel=user.get("english_nivel","Principiante")
    loks=len(user.get("english_lecciones_completadas",[]))
    lec=f"\nLección actual: {leccion}" if leccion else ""
    modo_extra=""
    if modo=="roleplay":
        sit=user.get("english_roleplay_situacion","")
        modo_extra=f"\n\nESTÁS EN MODO ROLEPLAY. Situación: {sit}. Actuá el rol del personaje en esa situación (mozo, entrevistador, proveedor, etc). Hablá en inglés. Si el estudiante comete errores, después de responder en el personaje, agregá una nota de corrección al final separada con ---."
    if modo=="traductor":
        modo_extra="\n\nESTÁS EN MODO TRADUCTOR INTELIGENTE. El usuario te va a dar texto en inglés. Vos: 1) Traducís al español 2) Explicás palabra por palabra las más importantes 3) Explicás la gramática usada 4) Dás el contexto de uso."
    if modo=="diario":
        modo_extra="\n\nESTÁS EN MODO DIARIO EN INGLÉS. El usuario escribió una entrada de diario en inglés. Vos: 1) Corregís todos los errores con amabilidad 2) Mostrás la versión corregida 3) Explicás los errores principales 4) Lo felicitás por practicar."
    return f"""Sos Alex, el profesor de inglés de AV MentorAI. Divertido, moderno, como un amigo que sabe mucho inglés.
Estudiante: {user['nombre']} | Nivel: {nivel} | Lecciones completadas: {loks}{lec}
Explicás en ESPAÑOL pero enseñás INGLÉS. Usás emojis. Corregís errores así: "✅ Correcto sería: [forma correcta]".
Celebrás logros. Frases tuyas: "¡Genial!", "You're killing it! 🔥", "Let's practice!"{modo_extra}"""

# ─── Enviar mensajes ───
def enviar_negocio(ui,desafio,ib64=None,im=None,na=None):
    user=st.session_state.user_data
    key=ui+(ib64[:20] if ib64 else "")
    if key==st.session_state.get("last_neg",""): return
    st.session_state.last_neg=key
    if not MODO_DEV and user["plan"]=="Gratis" and user["preguntas_hoy"]>=10:
        st.warning("Límite diario alcanzado."); return
    user["preguntas_hoy"]+=1
    if ib64:
        ca=[{"type":"text","text":ui or "Analizá esta imagen."},{"type":"image_url","image_url":{"url":f"data:{im};base64,{ib64}"}}]
        disp=f"[Imagen: {na}]\n{ui}" if ui else f"[Imagen: {na}]"
    else: ca=ui; disp=ui
    user["messages"].append({"role":"user","content":disp})
    user["memoria_larga"].append(f"Usuario: {disp}")
    if len(user["memoria_larga"])>20: user["memoria_larga"]=user["memoria_larga"][-20:]
    sumar_xp(10)
    hist=[{"role":m["role"],"content":m["content"]} for m in user["messages"][:-1]]
    hist.append({"role":"user","content":ca})
    with st.spinner("⚡ AV MentorAI está pensando..."):
        try:
            r=client.chat.completions.create(model="gpt-4o",messages=[{"role":"system","content":system_negocio(user,st.session_state.modo,desafio)},*hist],temperature=0.85,max_tokens=1000)
            resp=r.choices[0].message.content
        except Exception as e: resp=f"Error: {e}"
    user["messages"].append({"role":"assistant","content":resp}); guardar_usuario(user); st.rerun()

def enviar_english(ui,leccion=None,modo="chat",lista_msgs_key="english_messages"):
    user=st.session_state.user_data
    lkey=f"last_{lista_msgs_key}"
    if ui==st.session_state.get(lkey,""): return
    st.session_state[lkey]=ui
    if lista_msgs_key not in user: user[lista_msgs_key]=[]
    user[lista_msgs_key].append({"role":"user","content":ui})
    hist=[{"role":m["role"],"content":m["content"]} for m in user[lista_msgs_key][-12:]]
    spinner_txt={"chat":"🎓 Alex está respondiendo...","roleplay":"🎭 Roleplay en curso...","traductor":"📖 Traduciendo...","diario":"📝 Corrigiendo tu diario..."}.get(modo,"⏳ Procesando...")
    with st.spinner(spinner_txt):
        try:
            r=client.chat.completions.create(model="gpt-4o",messages=[{"role":"system","content":system_english(user,leccion,modo)},*hist],temperature=0.8,max_tokens=900)
            resp=r.choices[0].message.content
        except Exception as e: resp=f"Error: {e}"
    user[lista_msgs_key].append({"role":"assistant","content":resp})
    if len(user[lista_msgs_key])>40: user[lista_msgs_key]=user[lista_msgs_key][-40:]
    guardar_usuario(user); st.rerun()

def enviar_mate(ui, leccion=None):
    user=st.session_state.user_data
    if ui==st.session_state.get("last_mate",""): return
    st.session_state.last_mate=ui
    if "mate_messages" not in user: user["mate_messages"]=[]
    user["mate_messages"].append({"role":"user","content":ui})
    hist=[{"role":m["role"],"content":m["content"]} for m in user["mate_messages"][-12:]]
    with st.spinner("🔢 Bruno está calculando..."):
        try:
            r=client.chat.completions.create(model="gpt-4o",
                messages=[{"role":"system","content":system_mate(user,leccion)},*hist],
                temperature=0.8,max_tokens=800)
            resp=r.choices[0].message.content
        except Exception as e: resp=f"Error: {e}"
    user["mate_messages"].append({"role":"assistant","content":resp})
    if len(user["mate_messages"])>40: user["mate_messages"]=user["mate_messages"][-40:]
    guardar_usuario(user); st.rerun()

def generar_resumen(user):
    if not user["messages"]: return "No hay conversación aún."
    texto="\n".join([f'{m["role"]}: {m["content"]}' for m in user["messages"][-8:]])
    try:
        r=client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"system","content":"Resume datos del usuario para memoria futura. Breve y práctico."},{"role":"user","content":texto}])
        res=r.choices[0].message.content; user["memoria_larga"].append(res)
        if len(user["memoria_larga"])>20: user["memoria_larga"]=user["memoria_larga"][-20:]
        guardar_usuario(user); return res
    except Exception as e: return f"Error: {e}"

# ─── Certificado PDF ───
def generar_certificado_pdf(nombre, nivel, lecciones_completadas, fecha):
    buf=io.BytesIO()
    w,h=A4; c=canvas.Canvas(buf,pagesize=A4)

    # Fondo
    c.setFillColor(colors.HexColor("#020617")); c.rect(0,0,w,h,fill=1,stroke=0)

    # Borde dorado
    c.setStrokeColor(colors.HexColor("#facc15")); c.setLineWidth(3)
    c.rect(30,30,w-60,h-60,fill=0,stroke=1)
    c.setLineWidth(1); c.setStrokeColor(colors.HexColor("#38bdf8"))
    c.rect(38,38,w-76,h-76,fill=0,stroke=1)

    # Logo / Título
    c.setFillColor(colors.HexColor("#facc15")); c.setFont("Helvetica-Bold",32)
    c.drawCentredString(w/2, h-110, "AV MentorAI")
    c.setFillColor(colors.HexColor("#38bdf8")); c.setFont("Helvetica",16)
    c.drawCentredString(w/2, h-140, "Certificado de Nivel de Ingles")

    # Línea decorativa
    c.setStrokeColor(colors.HexColor("#facc15")); c.setLineWidth(2)
    c.line(80, h-160, w-80, h-160)

    # Cuerpo
    c.setFillColor(colors.white); c.setFont("Helvetica",14)
    c.drawCentredString(w/2, h-200, "Este certificado acredita que")

    c.setFillColor(colors.HexColor("#facc15")); c.setFont("Helvetica-Bold",28)
    c.drawCentredString(w/2, h-245, nombre)

    c.setFillColor(colors.white); c.setFont("Helvetica",14)
    c.drawCentredString(w/2, h-285, "ha completado exitosamente todas las lecciones del nivel")

    nivel_colors={"Principiante":"#22c55e","Intermedio":"#facc15","Avanzado":"#ef4444"}
    c.setFillColor(colors.HexColor(nivel_colors.get(nivel,"#facc15")))
    c.setFont("Helvetica-Bold",26)
    c.drawCentredString(w/2, h-325, nivel)

    c.setFillColor(colors.white); c.setFont("Helvetica",12)
    c.drawCentredString(w/2, h-365, f"Lecciones completadas: {lecciones_completadas}")
    c.drawCentredString(w/2, h-390, f"Fecha: {fecha}")

    # Línea final
    c.setStrokeColor(colors.HexColor("#38bdf8")); c.setLineWidth(1.5)
    c.line(80, h-430, w-80, h-430)

    c.setFillColor(colors.HexColor("#94a3b8")); c.setFont("Helvetica",10)
    c.drawCentredString(w/2, h-455, "AV MentorAI — Tu mentor personal de negocios y aprendizaje")
    c.drawCentredString(w/2, h-472, "avmentorai.streamlit.app")

    # Sello / estrella
    c.setFillColor(colors.HexColor("#facc15")); c.setFont("Helvetica-Bold",40)
    c.drawCentredString(w/2, h-530, "★")
    c.setFont("Helvetica-Bold",11)
    c.drawCentredString(w/2, h-555, "CERTIFICADO OFICIAL")

    c.save(); buf.seek(0); return buf



# ─────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────
if "logged_in" not in st.session_state: st.session_state.logged_in=False



if not st.session_state.logged_in:
    # HERO
    st.markdown(f'''<div style="text-align:center;padding:36px 16px 16px">
        <div style="font-size:48px;font-weight:900;background:linear-gradient(90deg,#facc15,#f97316,#38bdf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.1;margin-bottom:10px">⚡ {APP_NAME}</div>
        <div style="font-size:17px;color:#cbd5e1;margin-bottom:6px">{APP_TAGLINE}</div>
        <div style="font-size:13px;color:#64748b">Mentor de negocios · Inglés · Matemáticas · Herramientas · Todo con IA</div>
    </div>''', unsafe_allow_html=True)

    st.markdown('''<div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:16px 0 24px">
        <div style="background:rgba(250,204,21,.1);border:1px solid rgba(250,204,21,.3);border-radius:12px;padding:10px 16px;text-align:center">
            <div style="font-size:20px;font-weight:800;color:#facc15">14</div><div style="font-size:11px;color:#94a3b8">Modos mentor</div></div>
        <div style="background:rgba(168,85,247,.1);border:1px solid rgba(168,85,247,.3);border-radius:12px;padding:10px 16px;text-align:center">
            <div style="font-size:20px;font-weight:800;color:#a855f7">12</div><div style="font-size:11px;color:#94a3b8">Lecciones inglés</div></div>
        <div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);border-radius:12px;padding:10px 16px;text-align:center">
            <div style="font-size:20px;font-weight:800;color:#22c55e">10</div><div style="font-size:11px;color:#94a3b8">Lecciones mate</div></div>
        <div style="background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.3);border-radius:12px;padding:10px 16px;text-align:center">
            <div style="font-size:20px;font-weight:800;color:#38bdf8">8</div><div style="font-size:11px;color:#94a3b8">Roleplay</div></div>
        <div style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.3);border-radius:12px;padding:10px 16px;text-align:center">
            <div style="font-size:20px;font-weight:800;color:#f97316">8</div><div style="font-size:11px;color:#94a3b8">Herramientas</div></div>
    </div>''', unsafe_allow_html=True)

    st.markdown("### ¿Qué tiene AV MentorAI?")
    fa,fb=st.columns(2)
    with fa:
        st.markdown('''
        <div style="background:linear-gradient(135deg,rgba(250,204,21,.12),rgba(249,115,22,.08));border:1px solid rgba(250,204,21,.3);border-radius:16px;padding:14px;margin-bottom:10px">
            <b style="color:#facc15">🧠 Mentor de Negocios</b><br><span style="color:#cbd5e1;font-size:12px">14 modos: ventas, marketing, e-commerce, supermercado y más. Analizá fotos de tu negocio.</span></div>
        <div style="background:linear-gradient(135deg,rgba(168,85,247,.12),rgba(99,102,241,.08));border:1px solid rgba(168,85,247,.3);border-radius:16px;padding:14px;margin-bottom:10px">
            <b style="color:#a855f7">📚 Inglés con Alex</b><br><span style="color:#cbd5e1;font-size:12px">12 lecciones, quiz, roleplay, traductor, diario y certificado PDF.</span></div>
        <div style="background:linear-gradient(135deg,rgba(56,189,248,.12),rgba(99,102,241,.08));border:1px solid rgba(56,189,248,.3);border-radius:16px;padding:14px;margin-bottom:10px">
            <b style="color:#38bdf8">🔍 Análisis de Competencia</b><br><span style="color:#cbd5e1;font-size:12px">Plan de 5 pasos para superar a cualquier competidor.</span></div>
        ''', unsafe_allow_html=True)
    with fb:
        st.markdown('''
        <div style="background:linear-gradient(135deg,rgba(34,197,94,.12),rgba(16,185,129,.08));border:1px solid rgba(34,197,94,.3);border-radius:16px;padding:14px;margin-bottom:10px">
            <b style="color:#22c55e">🔢 Matemáticas con Bruno</b><br><span style="color:#cbd5e1;font-size:12px">10 lecciones + calculadora de márgenes, ROI y proyecciones.</span></div>
        <div style="background:linear-gradient(135deg,rgba(249,115,22,.12),rgba(239,68,68,.08));border:1px solid rgba(249,115,22,.3);border-radius:16px;padding:14px;margin-bottom:10px">
            <b style="color:#f97316">✍️ Generador de Contenido</b><br><span style="color:#cbd5e1;font-size:12px">Posts de Instagram, WhatsApp, Mercado Libre y TikTok listos para publicar.</span></div>
        <div style="background:linear-gradient(135deg,rgba(250,204,21,.12),rgba(34,197,94,.08));border:1px solid rgba(250,204,21,.3);border-radius:16px;padding:14px;margin-bottom:10px">
            <b style="color:#facc15">🔥 Gamificación</b><br><span style="color:#cbd5e1;font-size:12px">XP, rachas, niveles, desafíos diarios, logros y ranking.</span></div>
        ''', unsafe_allow_html=True)

    st.markdown('''<div style="text-align:center;padding:18px;background:linear-gradient(135deg,rgba(250,204,21,.1),rgba(56,189,248,.08));border:1px solid rgba(250,204,21,.25);border-radius:18px;margin:12px 0 20px">
        <div style="font-size:17px;font-weight:800;color:#f8fafc;margin-bottom:4px">¿Listo para empezar?</div>
        <div style="font-size:13px;color:#94a3b8">Creá tu cuenta gratis en 30 segundos. Sin tarjeta de crédito.</div>
    </div>''', unsafe_allow_html=True)
    lt,rt=st.tabs(["Iniciar sesión","Crear cuenta"])
    with lt:
        el=st.text_input("Gmail",placeholder="tuemail@gmail.com",key="login_email")
        pl=st.text_input("Contraseña",type="password",key="login_pass")
        if st.button("Entrar",key="btn_entrar"):
            ul=login(el,pl)
            if ul: st.session_state.logged_in=True; st.session_state.user_data=ul; st.rerun()
            else: st.error("Gmail o contraseña incorrectos.")
    with rt:
        nr=st.text_input("Nombre",placeholder="Valentino",key="reg_nombre")
        er=st.text_input("Gmail",placeholder="tuemail@gmail.com",key="reg_email")
        pr=st.text_input("Crear contraseña",type="password",key="reg_pass")
        if st.button("Crear cuenta"):
            if not nr or not er or not pr: st.warning("Completá todos los campos.")
            elif "@gmail.com" not in er.lower(): st.warning("Usá un Gmail válido.")
            elif len(pr)<6: st.warning("Mínimo 6 caracteres.")
            else:
                ok=crear_usuario(nr,er,pr)
                st.success("Cuenta creada. Iniciá sesión.") if ok else st.error("Ese Gmail ya existe.")
    st.stop()

# ─────────────────────────────────────────
# SESSION
# ─────────────────────────────────────────
user=st.session_state.user_data
dfu=usuario_default(user.get("nombre",""),user.get("email",""),"x")
for k,v in dfu.items():
    if k not in user: user[k]=v
guardar_usuario(user)

desafio=generar_desafio(user)
hoy=str(date.today())
if user.get("fecha_preguntas","")!=hoy: user["fecha_preguntas"]=hoy; user["preguntas_hoy"]=0; guardar_usuario(user)
if "modo" not in st.session_state: st.session_state.modo="Mentor de Negocios"
if "leccion_sel" not in st.session_state: st.session_state.leccion_sel=None
if "english_tab" not in st.session_state: st.session_state.english_tab="lecciones"

# ─────────────────────────────────────────
# ONBOARDING
# ─────────────────────────────────────────
if not user.get("onboarding_completo",False):
    st.markdown(f'<div class="hero-card"><div class="av-logo">{APP_NAME}</div><div class="av-subtitle">Configurá tu mentor en 1 minuto</div></div>',unsafe_allow_html=True)
    user["objetivo"]=st.text_area("¿Cuál es tu objetivo principal?",value=user["objetivo"],placeholder="Ej: vender más, crear un negocio...")
    user["negocio"]=st.text_input("¿Tenés un negocio o idea?",value=user["negocio"],placeholder="Ej: tienda de ropa, supermercado...")
    tipos=["Todavía no tengo negocio","Supermercado / mayorista","E-commerce","Reventa","Restaurante / comida","Servicios","Inmobiliaria","Otro"]
    user["tipo_negocio"]=st.selectbox("Tipo:",tipos,index=tipos.index(user["tipo_negocio"]) if user["tipo_negocio"] in tipos else 0)
    niv=["Principiante","Intermedio","Avanzado"]
    user["nivel_usuario"]=st.selectbox("Tu nivel:",niv,index=niv.index(user["nivel_usuario"]) if user["nivel_usuario"] in niv else 0)
    tps=["15 minutos","30 minutos","1 hora","Más de 1 hora"]
    user["tiempo_diario"]=st.selectbox("Tiempo por día:",tps,index=tps.index(user["tiempo_diario"]) if user["tiempo_diario"] in tps else 0)
    user["principal_dificultad"]=st.text_area("¿Qué te cuesta más?",value=user["principal_dificultad"])
    if st.button("🚀 Entrar a AV MentorAI"): user["onboarding_completo"]=True; guardar_usuario(user); st.rerun()
    st.stop()

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown(f'<div class="hero-card"><div class="av-logo">{APP_NAME}</div><div class="av-subtitle">{APP_TAGLINE} &nbsp;|&nbsp; <b>{APP_VERSION}</b></div></div>',unsafe_allow_html=True)

loks=len(user.get("english_lecciones_completadas",[]))
diary_count=len(user.get("english_diary",[]))
nivel_txt=calcular_nivel(user["xp"])
prog=progreso_nivel(user["xp"])
prog_pct=int(prog*100)
m1,m2,m3,m4=st.columns(4)
with m1:
    st.markdown(f'''<div style="background:linear-gradient(135deg,rgba(250,204,21,.2),rgba(250,204,21,.05));border:1px solid rgba(250,204,21,.4);border-radius:16px;padding:14px;text-align:center">
    <div style="font-size:28px">👤</div>
    <div style="font-size:11px;color:#94a3b8;margin:4px 0">USUARIO</div>
    <div style="font-size:16px;font-weight:800;color:#facc15">{user["nombre"]}</div>
    </div>''',unsafe_allow_html=True)
with m2:
    st.markdown(f'''<div style="background:linear-gradient(135deg,rgba(249,115,22,.2),rgba(249,115,22,.05));border:1px solid rgba(249,115,22,.4);border-radius:16px;padding:14px;text-align:center">
    <div style="font-size:28px">⭐</div>
    <div style="font-size:11px;color:#94a3b8;margin:4px 0">XP TOTAL</div>
    <div style="font-size:20px;font-weight:800;color:#f97316">{user["xp"]}</div>
    </div>''',unsafe_allow_html=True)
with m3:
    st.markdown(f'''<div style="background:linear-gradient(135deg,rgba(239,68,68,.2),rgba(239,68,68,.05));border:1px solid rgba(239,68,68,.4);border-radius:16px;padding:14px;text-align:center">
    <div style="font-size:28px">🔥</div>
    <div style="font-size:11px;color:#94a3b8;margin:4px 0">RACHA</div>
    <div style="font-size:20px;font-weight:800;color:#ef4444">{plural_dias(user["racha"])}</div>
    </div>''',unsafe_allow_html=True)
with m4:
    st.markdown(f'''<div style="background:linear-gradient(135deg,rgba(56,189,248,.2),rgba(56,189,248,.05));border:1px solid rgba(56,189,248,.4);border-radius:16px;padding:14px;text-align:center">
    <div style="font-size:28px">💎</div>
    <div style="font-size:11px;color:#94a3b8;margin:4px 0">PLAN</div>
    <div style="font-size:16px;font-weight:800;color:#38bdf8">{user["plan"]}</div>
    </div>''',unsafe_allow_html=True)
st.write("")
st.markdown(f'''<div style="background:rgba(15,23,42,.88);border:1px solid rgba(148,163,184,.2);border-radius:14px;padding:14px">
<div style="display:flex;justify-content:space-between;margin-bottom:6px">
  <span style="color:#f8fafc;font-size:13px;font-weight:700">{nivel_txt}</span>
  <span style="color:#facc15;font-size:13px;font-weight:700">{prog_pct}%</span>
</div>
<div style="background:rgba(148,163,184,.15);border-radius:8px;height:10px;overflow:hidden">
  <div style="background:linear-gradient(90deg,#facc15,#f97316);height:100%;width:{prog_pct}%;border-radius:8px;transition:width .3s"></div>
</div>
<div style="display:flex;justify-content:space-between;margin-top:8px">
  <span style="color:#94a3b8;font-size:11px">📚 {loks} lecciones inglés</span>
  <span style="color:#94a3b8;font-size:11px">📓 {diary_count} entradas diario</span>
  <span style="color:#94a3b8;font-size:11px">🎯 {user.get("objetivos_completados",0)} objetivos</span>
</div>
</div>''',unsafe_allow_html=True)
st.write("")

# Configuración
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
        if st.session_state.get("confirmar_borrar", False):
            st.warning("¿Seguro? Se borra todo el historial.")
            cs, cn = st.columns(2)
            with cs:
                if st.button("✅ Sí"): user["messages"] = []; guardar_usuario(user); st.session_state.confirmar_borrar = False; st.rerun()
            with cn:
                if st.button("❌ No"): st.session_state.confirmar_borrar = False; st.rerun()
        if st.button("🔁 Rehacer onboarding"): user["onboarding_completo"] = False; guardar_usuario(user); st.rerun()
        if st.button("🚪 Cerrar sesión"): guardar_usuario(user); st.session_state.logged_in = False; st.rerun()

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab_mentor, tab_english, tab_mate, tab_herramientas, tab_progreso, tab_desafios, tab_premium, tab_ranking, tab_feedback = st.tabs([
    "🧠 Mentor", "📚 Inglés", "🔢 Mate", "🛠️ Herramientas",
    "📈 Progreso", "🔥 Desafíos", "💎 Premium", "🏆 Ranking", "💬 Feedback"
])

# ════════════════════════════════════════
# TAB MENTOR
# ════════════════════════════════════════
with tab_mentor:
    if not user["messages"]:
        n=user['nombre'] or 'emprendedor'
        obj=f" Tu objetivo: {user['objetivo']}." if user["objetivo"] else ""
        neg=f" sobre tu negocio de {user['negocio']}" if user["negocio"] else ""
        bv=f"¡Hola {n}! Soy AV MentorAI.{obj} Listo para ayudarte{neg}. ¿Por dónde empezamos?"
        st.markdown(f'<div class="chat-ai"><div class="chat-name-ai">⚡ AV MentorAI</div><div class="chat-text">{bv}</div></div>',unsafe_allow_html=True)
    else:
        for m in user["messages"]: render_msg(m["role"],m["content"],"negocio")
        ul=obtener_ultima_respuesta(user["messages"])
        if ul and st.button("🔊 Escuchar última respuesta",key="aud_neg"):
            with st.spinner("Generando audio..."): render_audio_player(ul)

    st.divider()
    if not user["messages"]: st.markdown('<div class="guide-text">👇 Tocá un botón o escribí tu primera pregunta abajo</div>',unsafe_allow_html=True)

    # Botones rápidos con colores individuales via CSS
    st.markdown("""<style>
    div[data-testid="column"]:nth-child(1) .stButton>button{background:linear-gradient(90deg,#f59e0b,#d97706)!important;color:#111!important;}
    div[data-testid="column"]:nth-child(2) .stButton>button{background:linear-gradient(90deg,#10b981,#059669)!important;color:#fff!important;}
    div[data-testid="column"]:nth-child(3) .stButton>button{background:linear-gradient(90deg,#6366f1,#4f46e5)!important;color:#fff!important;}
    div[data-testid="column"]:nth-child(4) .stButton>button{background:linear-gradient(90deg,#ef4444,#dc2626)!important;color:#fff!important;}
    div[data-testid="column"]:nth-child(5) .stButton>button{background:linear-gradient(90deg,#8b5cf6,#7c3aed)!important;color:#fff!important;}
    div[data-testid="column"]:nth-child(6) .stButton>button{background:linear-gradient(90deg,#0ea5e9,#0284c7)!important;color:#fff!important;}
    </style>""", unsafe_allow_html=True)
    c1,c2,c3,c4,c5,c6=st.columns(6); qp=None
    with c1:
        if st.button("💡 Idea", use_container_width=True, key="qb1"): qp="Dame una idea de negocio rentable para empezar con pocos recursos."
    with c2:
        if st.button("📈 Vender", use_container_width=True, key="qb2"): qp="Quiero vender más. Dame un plan práctico para empezar hoy."
    with c3:
        if st.button("📱 Marketing", use_container_width=True, key="qb3"): qp="Quiero aprender marketing desde cero para vender por redes sociales."
    with c4:
        if st.button("🎭 Cliente", use_container_width=True, key="qb4"): qp="Hagamos una simulación. Vos sos un cliente difícil y yo tengo que venderte."
    with c5:
        if st.button("🔥 Desafío", use_container_width=True, key="qb5"): qp=f"Quiero hacer este desafío: {desafio}. Guiame paso a paso."
    with c6:
        if st.button("💎 Mentor", use_container_width=True, key="qb6"): qp="Háblame como mentor exigente y decime qué debería mejorar hoy."

    with st.expander("📎 Adjuntar imagen o archivo (opcional)",expanded=False):
        arch=st.file_uploader("Archivo:",type=["jpg","jpeg","png","webp","pdf","txt"],label_visibility="collapsed")
        if arch:
            if arch.type in ["image/jpeg","image/png","image/webp","image/jpg"]: st.image(arch,use_container_width=True)
            elif arch.type=="application/pdf": st.info(f"📄 PDF: {arch.name}")

    audio=st.audio_input("🎤 Grabá tu pregunta por voz (opcional)")
    vp=None
    if audio:
        with st.spinner("Transcribiendo..."):
            try: vp=transcribir_audio(audio); st.success(f"Escuché: *{vp}*")
            except Exception as e: st.warning(f"Error: {e}")

    # Procesar botón rápido ANTES del chat_input
    if st.session_state.get("neg_quick"):
        _nq = st.session_state.neg_quick
        st.session_state.neg_quick = None
        enviar_negocio(_nq, desafio)

    # Procesar audio
    if vp:
        enviar_negocio(vp, desafio)

    ui=st.chat_input("✍️ Escribí tu pregunta acá...")
    if ui:
        ib64=im=na=None
        if arch:
            if arch.type in ["image/jpeg","image/png","image/webp","image/jpg"]: ib64,im=imagen_a_base64(arch); na=arch.name
            elif arch.type=="text/plain": c2=arch.read().decode("utf-8"); ui=ui+f"\n\n[Archivo {arch.name}]:\n{c2[:3000]}"
            elif arch.type=="application/pdf": ui=ui+f"\n\n[PDF adjunto: {arch.name}]"
        enviar_negocio(ui,desafio,ib64,im,na)

# ════════════════════════════════════════
# TAB INGLÉS
# ════════════════════════════════════════
with tab_english:
    st.markdown('<div class="english-card"><h2>📚 Aprender Inglés</h2><p class="small-text">Lecciones offline + Quiz + Roleplay + Traductor + Diario + Certificado</p></div>',unsafe_allow_html=True)

    # Sub-navegación
    ing_sel = st.radio("", 
        ["Lecciones", "Roleplay", "Traductor", "Diario", "Certificado", "Chat con Alex"],
        key="ing_sel", horizontal=True, label_visibility="collapsed")
    st.divider()

    # ── LECCIONES ──
    if ing_sel == "Lecciones":
        niv_ing=st.selectbox("Tu nivel de inglés:",["Principiante","Intermedio","Avanzado"],
            index=["Principiante","Intermedio","Avanzado"].index(user.get("english_nivel","Principiante")))
        if niv_ing!=user.get("english_nivel"): user["english_nivel"]=niv_ing; guardar_usuario(user)

        loks_list=user.get("english_lecciones_completadas",[])
        lecs_niv=LECCIONES.get(niv_ing,[])
        total=len(lecs_niv); comp_niv=sum(1 for l in lecs_niv if l["id"] in loks_list)
        if total>0: st.progress(comp_niv/total); st.caption(f"{comp_niv}/{total} lecciones completadas en {niv_ing}")

        # Lista de lecciones
        for lec in lecs_niv:
            done=lec["id"] in loks_list; icono="✅" if done else "📖"
            cl2,cb2=st.columns([4,1])
            with cl2: st.markdown(f'<div class="{"lesson-card-done" if done else "lesson-card"}"><b>{icono} {lec["titulo"]}</b><br><span class="small-text">{lec["descripcion"]}</span> <span style="color:#facc15;font-size:12px;font-weight:700">+{lec["xp"]} XP</span></div>',unsafe_allow_html=True)
            with cb2:
                if st.button("Repasar" if done else "Ver",key=f"lec_{lec['id']}"):
                    st.session_state.leccion_sel=lec["id"]; st.rerun()

        # Mostrar lección seleccionada + quiz
        lsel=st.session_state.leccion_sel
        if lsel:
            lobj=next((l for l in lecs_niv if l["id"]==lsel),None)
            if lobj:
                st.divider()
                st.markdown(f"## 📖 {lobj['titulo']}")
                # Lección offline — no necesita IA
                st.markdown(f'<div class="lesson-content">{lobj["contenido"]}</div>',unsafe_allow_html=True)

                # Quiz
                st.markdown("### 🧠 Quiz de la lección")
                st.caption("Respondé las 5 preguntas para completar la lección.")
                quiz_key=f"quiz_{lobj['id']}"
                if quiz_key not in st.session_state: st.session_state[quiz_key]={}

                quiz_data=lobj.get("quiz",[])
                respuestas=st.session_state[quiz_key]
                for i,q in enumerate(quiz_data):
                    st.markdown(f'<div class="quiz-card"><b>Pregunta {i+1}:</b> {q["pregunta"]}</div>',unsafe_allow_html=True)
                    sel=st.radio("",q["opciones"],key=f"q_{lobj['id']}_{i}",index=None,label_visibility="collapsed")
                    if sel is not None: respuestas[i]=q["opciones"].index(sel)

                if len(respuestas)==len(quiz_data):
                    correctas=sum(1 for i,q in enumerate(quiz_data) if respuestas.get(i)==q["correcta"])
                    pct=int(correctas/len(quiz_data)*100)
                    if pct>=80:
                        st.success(f"✅ {correctas}/{len(quiz_data)} correctas ({pct}%). ¡Excelente!")
                        if lobj["id"] not in loks_list:
                            if st.button(f"🏆 Marcar como completada (+{lobj['xp']} XP)"):
                                user["english_lecciones_completadas"].append(lobj["id"])
                                user["english_xp"]=user.get("english_xp",0)+lobj["xp"]
                                qs=user.get("english_quiz_scores",{}); qs[lobj["id"]]=pct
                                user["english_quiz_scores"]=qs
                                sumar_xp(lobj["xp"]); guardar_usuario(user)
                                st.success(f"¡Lección completada! +{lobj['xp']} XP 🎉")
                                st.session_state.leccion_sel=None; st.rerun()
                        else: st.info("✅ Ya completaste esta lección.")
                    else:
                        st.warning(f"⚠️ {correctas}/{len(quiz_data)} correctas ({pct}%). Necesitás 80% para completarla. Repasá la lección y volvé a intentarlo.")

                col_c=st.columns(2)
                with col_c[1]:
                    if st.button("❌ Cerrar lección"): st.session_state.leccion_sel=None; st.rerun()

    # ── ROLEPLAY ──
    if ing_sel == "Roleplay":
        st.markdown("### 🎭 Roleplay de situaciones reales")
        st.caption("Elegí una situación y practicá inglés real como si estuvieras ahí.")

        sit_actual=user.get("english_roleplay_situacion")
        rp_msgs=user.get("english_roleplay_messages",[])

        if not sit_actual:
            st.markdown("**Elegí tu situación:**")
            cols=st.columns(2)
            for i,sit in enumerate(SITUACIONES_ROLEPLAY):
                with cols[i%2]:
                    st.markdown(f'<div class="roleplay-card"><b>{sit["emoji"]} {sit["titulo"]}</b><br><span class="small-text">{sit["descripcion"]}</span></div>',unsafe_allow_html=True)
                    if st.button(f"Empezar →",key=f"sit_{sit['id']}"):
                        user["english_roleplay_situacion"]=f"{sit['emoji']} {sit['titulo']}: {sit['descripcion']}"
                        user["english_roleplay_messages"]=[]
                        guardar_usuario(user); st.rerun()
        else:
            st.info(f"**Situación actual:** {sit_actual}")
            st.caption("Hablá en inglés. Alex actúa el personaje y te corrige al final de cada respuesta.")

            if not rp_msgs:
                st.markdown('<div class="chat-english"><div class="chat-name-english">🎭 Roleplay</div><div class="chat-text">Cuando quieras, empezá la conversación en inglés. Yo actúo el personaje y al final de cada respuesta te corrijo si hay errores. Let\'s go! 🎭</div></div>',unsafe_allow_html=True)
            else:
                for m in rp_msgs[-16:]: render_msg(m["role"],m["content"],"english")
                ul_rp=obtener_ultima_respuesta(rp_msgs)
                if ul_rp and st.button("🔊 Escuchar",key="aud_rp"):
                    with st.spinner("..."): render_audio_player(ul_rp)

            audio_rp=st.audio_input("🎤 Grabá en inglés",key="audio_rp")
            ve_rp=None
            if audio_rp:
                with st.spinner("Transcribiendo..."):
                    try: ve_rp=transcribir_audio(audio_rp); st.info(f"Dijiste: *{ve_rp}*")
                    except: pass

            rp_input=st.chat_input("✍️ Escribí en inglés acá...")
            if ve_rp: rp_input=ve_rp
            if rp_input: enviar_english(rp_input,modo="roleplay",lista_msgs_key="english_roleplay_messages")

            if st.button("🔄 Cambiar situación"):
                user["english_roleplay_situacion"]=None; user["english_roleplay_messages"]=[]
                guardar_usuario(user); st.rerun()

    # ── TRADUCTOR INTELIGENTE ──
    if ing_sel == "Traductor":
        st.markdown("### 📖 Traductor inteligente")
        st.caption("Pegá cualquier texto en inglés y Alex lo traduce, explica palabra por palabra y enseña la gramática.")

        texto_traducir=st.text_area("Pegá tu texto en inglés acá:",placeholder="Ej: The quarterly results exceeded our expectations significantly.",height=120)
        if st.button("🔍 Traducir y explicar") and texto_traducir.strip():
            prompt=f"Traducí y explicá este texto en inglés: '{texto_traducir}'"
            enviar_english(prompt,modo="traductor",lista_msgs_key="english_messages")

        # Mostrar últimas respuestas del traductor (del chat general de alex)
        msgs_alex=user.get("english_messages",[])
        if msgs_alex:
            ultimas=msgs_alex[-4:]
            for m in ultimas: render_msg(m["role"],m["content"],"english")

    # ── DIARIO EN INGLÉS ──
    if ing_sel == "Diario":
        st.markdown("### 📓 Diario en inglés")
        st.caption("Escribí todos los días aunque sea 3 oraciones. Alex las corrige y guardás tu progreso.")

        diary=user.get("english_diary",[])
        entrada_hoy=next((e for e in diary if e.get("fecha")==hoy),None)

        if not entrada_hoy:
            st.markdown(f"**Entrada de hoy — {hoy}**")
            texto_diario=st.text_area("Escribí tu entrada de hoy en inglés:",placeholder="Today I worked on my business. I talked to 3 clients and sold 2 products. I feel good about my progress.",height=150)
            if st.button("✍️ Enviar y corregir") and texto_diario.strip():
                # Guardar entrada
                entrada={"fecha":hoy,"texto":texto_diario,"correccion":None}
                user["english_diary"].append(entrada)
                guardar_usuario(user)
                # Pedir corrección a Alex
                prompt=f"Acá está mi entrada de diario en inglés de hoy: '{texto_diario}'"
                enviar_english(prompt,modo="diario",lista_msgs_key="english_messages")
                sumar_xp(15)
        else:
            st.success(f"✅ Ya escribiste tu entrada de hoy — {hoy}")
            st.markdown(f'<div class="diary-card"><b>Tu entrada:</b><br>{entrada_hoy["texto"]}</div>',unsafe_allow_html=True)
            msgs_alex=user.get("english_messages",[])
            ul_diary=obtener_ultima_respuesta(msgs_alex)
            if ul_diary: render_msg("assistant",ul_diary,"english")

        # Historial del diario
        if len(diary)>1:
            st.markdown("### Historial de entradas")
            st.caption(f"Total: {len(diary)} entradas escritas")
            for e in reversed(diary[-10:]):
                if e.get("fecha")!=hoy:
                    with st.expander(f"📅 {e['fecha']}"):
                        st.write(e["texto"])

    # ── CERTIFICADO ──
    if ing_sel == "Certificado":
        st.markdown("### 🏆 Certificado de nivel")
        st.caption("Completá todas las lecciones de un nivel para descargar tu certificado oficial.")

        for nivel_cert,lecs_cert in LECCIONES.items():
            total_cert=len(lecs_cert)
            loks_cert=sum(1 for l in lecs_cert if l["id"] in user.get("english_lecciones_completadas",[]))
            pct_cert=int(loks_cert/total_cert*100) if total_cert>0 else 0
            nivel_colors_ui={"Principiante":"🟢","Intermedio":"🟡","Avanzado":"🔴"}

            st.markdown(f"#### {nivel_colors_ui.get(nivel_cert,'')} Nivel {nivel_cert}")
            st.progress(loks_cert/total_cert if total_cert>0 else 0)
            st.caption(f"{loks_cert}/{total_cert} lecciones ({pct_cert}%)")

            if loks_cert==total_cert:
                st.success(f"✅ ¡Completaste el nivel {nivel_cert}! Tu certificado está listo.")
                if st.button(f"📜 Descargar certificado {nivel_cert}",key=f"cert_{nivel_cert}"):
                    pdf_buf=generar_certificado_pdf(user["nombre"],nivel_cert,loks_cert,hoy)
                    st.download_button(
                        label=f"⬇️ Descargar PDF — Certificado {nivel_cert}",
                        data=pdf_buf,
                        file_name=f"certificado_ingles_{nivel_cert.lower()}_{user['nombre'].lower().replace(' ','_')}.pdf",
                        mime="application/pdf",
                        key=f"dl_cert_{nivel_cert}"
                    )
            else:
                faltantes=total_cert-loks_cert
                st.info(f"Te faltan {faltantes} lección{'es' if faltantes!=1 else ''} para desbloquear el certificado.")
            st.write("")

    # ── CHAT CON ALEX ──
    if ing_sel == "Chat con Alex":
        st.markdown("<p style='font-size:16px;font-weight:800;color:#a855f7;margin:8px 0 2px'>💬 Chat con Alex</p>", unsafe_allow_html=True)
        st.caption("Preguntale dudas, pedile ejercicios o practicá conversación.")

        eng_msgs=user.get("english_messages",[])
        if not eng_msgs:
            n=user['nombre'] or 'estudiante'
            bv=f"¡Hola {n}! 👋 Soy Alex. Estoy acá para enseñarte inglés de forma divertida. ¿Qué querés practicar hoy? Let's go! 🚀"
            st.markdown(f'<div class="chat-english"><div class="chat-name-english">🎓 Alex — Profesor de Inglés</div><div class="chat-text">{bv}</div></div>',unsafe_allow_html=True)
        else:
            for m in eng_msgs[-20:]: render_msg(m["role"],m["content"],"english")
            ul_eng=obtener_ultima_respuesta(eng_msgs)
            if ul_eng and st.button("🔊 Escuchar a Alex",key="aud_eng"):
                with st.spinner("..."): render_audio_player(ul_eng)

        e1,e2,e3=st.columns(3)
        with e1:
            if st.button("🔤 Verbo To Be", key="eng_b1"): st.session_state.eng_quick="Explicame el verbo To Be desde cero con ejemplos."
            if st.button("✍️ Corregí mi inglés", key="eng_b2"): st.session_state.eng_quick="Voy a escribir algo en inglés, corregime si hay errores."
        with e2:
            if st.button("💬 Practicar conversación", key="eng_b3"): st.session_state.eng_quick="Quiero practicar una conversación en inglés. Empezá vos."
            if st.button("📧 Emails en inglés", key="eng_b4"): st.session_state.eng_quick="Enseñame a escribir un email en inglés con la estructura correcta."
        with e3:
            if st.button("🎯 Dame un ejercicio", key="eng_b5"): st.session_state.eng_quick="Dame un ejercicio de inglés para mi nivel actual."
            if st.button("🗣️ Frases cotidianas", key="eng_b6"): st.session_state.eng_quick="Enseñame frases que uso todos los días en inglés."

        audio_eng=st.audio_input("🎤 Grabá y Alex te corrige (opcional)",key="audio_alex")
        ve=None
        if audio_eng:
            with st.spinner("Transcribiendo..."):
                try: ve=transcribir_audio(audio_eng); st.info(f"Transcribí: *{ve}*")
                except: pass

        # Procesar botón rápido ANTES del chat_input
        if st.session_state.get("eng_quick"):
            _eq = st.session_state.eng_quick
            st.session_state.eng_quick = None
            enviar_english(_eq, modo="chat", lista_msgs_key="english_messages")

        # Procesar audio ANTES del chat_input
        if ve:
            enviar_english(f"Grabé esto en inglés: '{ve}'. ¿Está bien dicho? Corregime si hay errores.", modo="chat", lista_msgs_key="english_messages")

        ei=st.chat_input("✍️ Escribile a Alex acá...")
        if ei: enviar_english(ei, modo="chat", lista_msgs_key="english_messages")

        if st.button("🗑️ Borrar chat de Alex"): user["english_messages"]=[]; guardar_usuario(user); st.rerun()

# ════════════════════════════════════════
# TAB PROGRESO
# ════════════════════════════════════════
with tab_progreso:
    st.markdown("## 📈 Progreso")
    p1,p2,p3,p4,p5=st.columns(5)
    with p1: st.metric("⭐ XP total",user["xp"])
    with p2: st.metric("🔥 Racha",plural_dias(user["racha"]))
    with p3: st.metric("🎯 Objetivos",user["objetivos_completados"])
    with p4: st.metric("📚 Lecciones",len(user.get("english_lecciones_completadas",[])))
    with p5: st.metric("📓 Diario",len(user.get("english_diary",[])))

    if user["xp_history"]:
        df=pd.DataFrame(user["xp_history"]); st.markdown("### Evolución de XP")
        st.line_chart(df.set_index("fecha")["xp"])
    else: st.info("Todavía no hay progreso para mostrar.")

    if st.button("🧠 Generar memoria inteligente"):
        with st.spinner("Generando..."): resumen=generar_resumen(user)
        st.success(resumen)

    if user["logros"]:
        st.markdown("### 🏆 Logros")
        st.markdown("".join([f'<span class="badge">🏆 {l}</span>' for l in user["logros"]]),unsafe_allow_html=True)

    st.markdown("### 📊 Panel empresario")
    st.markdown(f'<div class="card"><p><b>Meta mensual:</b> {user["meta_mensual"] or "Sin definir"}</p><p><b>Ingresos objetivo:</b> ${user["ingresos_objetivo"]}</p><p><b>Hábito clave:</b> {user["habito_clave"] or "Sin definir"}</p><p><b>Tipo de negocio:</b> {user["tipo_negocio"] or "Sin definir"}</p><p><b>Principal dificultad:</b> {user["principal_dificultad"] or "Sin definir"}</p></div>',unsafe_allow_html=True)

# ════════════════════════════════════════
# TAB DESAFÍOS
# ════════════════════════════════════════
with tab_desafios:
    st.markdown("## 🔥 Desafío diario")
    st.markdown(f'<div class="challenge-card"><h2>Tu misión de hoy</h2><h3>{desafio}</h3><p class="small-text">Completarlo suma XP y mejora tu racha.</p></div>',unsafe_allow_html=True)
    d1,d2=st.columns(2)
    with d1:
        if st.button("✅ Completé el desafío"): user["desafios_completados"]+=1; sumar_xp(40); guardar_usuario(user); st.success("+40 XP 🎉"); st.rerun()
    with d2:
        if st.button("🎯 Objetivo completado"): user["objetivos_completados"]+=1; sumar_xp(60); guardar_usuario(user); st.success("+60 XP 🏆"); st.rerun()
    st.markdown(f'<div class="card"><p><b>Desafíos:</b> {user["desafios_completados"]}</p><p><b>Objetivos:</b> {user["objetivos_completados"]}</p><p><b>Racha:</b> {plural_dias(user["racha"])}</p></div>',unsafe_allow_html=True)

# ════════════════════════════════════════
# TAB PREMIUM
# ════════════════════════════════════════
with tab_premium:
    st.markdown("## 💎 Planes")
    p1,p2,p3=st.columns(3)
    with p1:
        st.markdown('<div class="plan-card"><h2>Gratis</h2><p>✅ Mentor básico</p><p>✅ Lecciones offline</p><p>✅ Quiz interactivo</p><p>⚠️ 10 preguntas/día con IA</p><h1>$0</h1></div>',unsafe_allow_html=True)
        if st.button("Usar Gratis"): user["plan"]="Gratis"; guardar_usuario(user); st.rerun()
    with p2:
        st.markdown('<div class="plan-card"><h2>Pro</h2><p>🚀 Mentor ilimitado</p><p>🎭 Roleplay completo</p><p>📓 Diario con IA</p><p>📜 Certificados PDF</p><p>🔊 Voz premium</p><h1>$4.99 USD</h1></div>',unsafe_allow_html=True)
        if st.button("💳 Activar Pro demo"): user["plan"]="Premium"; guardar_usuario(user); st.success("Plan Pro activado."); st.rerun()
    with p3:
        st.markdown('<div class="plan-card"><h2>Empresarial 🔒</h2><p>🏢 Para equipos</p><p>📈 Métricas avanzadas</p><p>🤖 IA personalizada</p><h1>Consultar</h1></div>',unsafe_allow_html=True)
        st.info("Próximamente: Mercado Pago / Stripe.")
    st.markdown(f'<div class="card"><p><b>Plan actual:</b> {user["plan"]}</p><p><b>Preguntas hoy:</b> {user["preguntas_hoy"]}</p></div>',unsafe_allow_html=True)

# ════════════════════════════════════════
# TAB RANKING
# ════════════════════════════════════════
with tab_ranking:
    st.markdown("## 🏆 Ranking")
    rk=[]
    for f in os.listdir(DATA_DIR):
        if f.endswith(".json"):
            try:
                with open(os.path.join(DATA_DIR,f),"r",encoding="utf-8") as fl: u=json.load(fl)
                rk.append({"Usuario":u.get("nombre","?"),"XP":u.get("xp",0),"Racha":u.get("racha",0),"Lecciones":len(u.get("english_lecciones_completadas",[])),"Diario":len(u.get("english_diary",[])),"Plan":u.get("plan","Gratis")})
            except: pass
    rk=sorted(rk,key=lambda x:x["XP"],reverse=True)
    st.dataframe(pd.DataFrame(rk),use_container_width=True) if rk else st.info("Todavía no hay usuarios.")

# ════════════════════════════════════════
# TAB FEEDBACK
# ════════════════════════════════════════
with tab_feedback:
    st.markdown("## 💬 Feedback")
    cal=st.slider("¿Qué tan útil es AV MentorAI?",1,10,8)
    com=st.text_area("Comentario:",placeholder="Qué te gustó, qué mejorarías...")
    pag=st.selectbox("¿Pagarías por esta app?",["No sé","Sí","No"])
    if st.button("Enviar feedback"):
        user["feedback"].append({"fecha":hoy,"calificacion":cal,"comentario":com,"pagaria":pag})
        guardar_usuario(user); st.success("Feedback guardado. ✅")
    if user["feedback"]:
        st.markdown("### Feedback guardado")
        st.dataframe(pd.DataFrame(user["feedback"]),use_container_width=True)

# ════════════════════════════════════════
# LECCIONES DE MATEMÁTICAS
# ════════════════════════════════════════

LECCIONES_MATE = {
    "Básico": [
        {"id":"m1","titulo":"Números y operaciones básicas","descripcion":"Suma, resta, multiplicación y división","xp":20,
         "contenido":"""**Números naturales:** 1, 2, 3, 4, 5... son los que usamos para contar.

**Las 4 operaciones:**
- Suma (+): 5 + 3 = 8 → Juntás cantidades
- Resta (-): 10 - 4 = 6 → Quitás cantidades
- Multiplicación (×): 4 × 3 = 12 → Suma repetida (4 veces el 3)
- División (÷): 12 ÷ 4 = 3 → Repartís en partes iguales

**En el negocio:**
- Vendiste 5 remeras a $2000 cada una → 5 × 2000 = $10.000
- Tenías $50.000 y gastaste $18.000 → 50.000 - 18.000 = $32.000
- Compraste 24 productos para 4 locales → 24 ÷ 4 = 6 por local

**Orden de operaciones (PEMDAS):**
Primero: paréntesis → potencias → × y ÷ → + y -
Ejemplo: 2 + 3 × 4 = 2 + 12 = 14 (NO 20)

📝 **Ejercicio:** Si vendés 8 productos a $1.500 cada uno y pagaste $7.000 de costo, ¿cuánto ganás?""",
         "quiz":[
             {"pregunta":"¿Cuánto es 15 × 4?","opciones":["54","60","45","70"],"correcta":1},
             {"pregunta":"Vendiste 6 productos a $500 cada uno. ¿Cuánto juntaste?","opciones":["$2.500","$3.000","$3.500","$2.000"],"correcta":1},
             {"pregunta":"¿Cuánto es 100 ÷ 5?","opciones":["15","25","20","30"],"correcta":2},
             {"pregunta":"2 + 3 × 4 es igual a:","opciones":["20","14","18","12"],"correcta":1},
             {"pregunta":"Tenías $80.000 y gastaste $35.000. ¿Cuánto te queda?","opciones":["$55.000","$40.000","$45.000","$50.000"],"correcta":2},
         ]},
        {"id":"m2","titulo":"Porcentajes","descripcion":"El % más útil para cualquier negocio","xp":25,
         "contenido":"""El **porcentaje** es una parte de 100. Es lo más usado en negocios.

**¿Cómo calcular un porcentaje?**
Fórmula: (porcentaje ÷ 100) × número
Ejemplo: 20% de $5.000 = (20 ÷ 100) × 5.000 = 0.20 × 5.000 = $1.000

**Casos más comunes:**

Descuento: Precio original - (% descuento × precio)
→ Remera de $3.000 con 30% off = 3.000 - 900 = $2.100

Aumento de precio: Precio original × (1 + % aumento)
→ Producto de $1.000 con 15% de aumento = 1.000 × 1.15 = $1.150

IVA (21%): Precio sin IVA × 1.21
→ Producto de $1.000 + IVA = $1.210

**Calcular qué % representa algo:**
Fórmula: (parte ÷ total) × 100
→ Ganaste $300 sobre una venta de $1.500 = (300 ÷ 1500) × 100 = 20%

📝 **Ejercicio:** Tenés un producto que costó $2.000 y lo vendés a $3.000. ¿Qué porcentaje de ganancia tenés?""",
         "quiz":[
             {"pregunta":"¿Cuánto es el 25% de $4.000?","opciones":["$800","$1.000","$1.200","$900"],"correcta":1},
             {"pregunta":"Un producto de $5.000 tiene 20% de descuento. ¿Cuánto pagás?","opciones":["$3.500","$4.500","$4.000","$3.000"],"correcta":2},
             {"pregunta":"Si comprás a $1.000 y vendés a $1.500, ¿qué % ganás?","opciones":["40%","60%","50%","45%"],"correcta":2},
             {"pregunta":"¿Cuánto es el 10% de $7.500?","opciones":["$650","$750","$700","$800"],"correcta":1},
             {"pregunta":"Un producto sin IVA cuesta $2.000. Con IVA del 21% cuesta:","opciones":["$2.100","$2.420","$2.210","$2.300"],"correcta":1},
         ]},
        {"id":"m3","titulo":"Fracciones y decimales","descripcion":"Mitades, tercios, cuartos y números con coma","xp":20,
         "contenido":"""**Fracciones:** representan partes de un todo.
- 1/2 = la mitad → 0.5
- 1/4 = un cuarto → 0.25
- 3/4 = tres cuartos → 0.75
- 1/3 = un tercio → 0.333...

**Decimales:** números con coma (o punto)
- 0.5 = 5/10 = 50%
- 0.25 = 25/100 = 25%
- 1.5 = uno y medio

**Operar con decimales:**
- 2.5 + 1.3 = 3.8
- 4.0 - 1.7 = 2.3
- 3.5 × 2 = 7.0
- 9.0 ÷ 4 = 2.25

**En el negocio:**
- Vendiste media docena de algo → 6 × 0.5 = 3 unidades
- Tu ganancia fue 1.5 veces el costo → costo × 1.5
- Repartís ganancias en 3 → dividís por 3

📝 **Ejercicio:** Si tu ganancia por producto es $750 y vendés 8 productos, ¿cuánto ganás en total?""",
         "quiz":[
             {"pregunta":"¿Cuánto es 1/4 en decimal?","opciones":["0.4","0.14","0.25","0.50"],"correcta":2},
             {"pregunta":"¿Cuánto es 2.5 × 4?","opciones":["8","9","10","7"],"correcta":2},
             {"pregunta":"3/4 equivale a qué porcentaje?","opciones":["34%","73%","70%","75%"],"correcta":3},
             {"pregunta":"¿Cuánto es 7.5 ÷ 3?","opciones":["2","2.5","3","2.25"],"correcta":1},
             {"pregunta":"Si tenés $1.000 y gastás la mitad, ¿cuánto te queda?","opciones":["$400","$600","$500","$450"],"correcta":2},
         ]},
        {"id":"m4","titulo":"Proporciones y regla de tres","descripcion":"Si X entonces Y, ¿y si tengo más?","xp":25,
         "contenido":"""La **regla de tres** sirve para calcular cantidades proporcionales.

**Fórmula directa:**
Si A → B, entonces C → X
X = (C × B) ÷ A

**Ejemplo directo:**
Si 5 productos cuestan $10.000, ¿cuánto cuestan 8?
X = (8 × 10.000) ÷ 5 = 80.000 ÷ 5 = $16.000

**Ejemplo inverso (relación contraria):**
Si 4 personas terminan un trabajo en 6 días, ¿cuánto tardan 3 personas?
X = (4 × 6) ÷ 3 = 24 ÷ 3 = 8 días

**En el negocio:**
Si con $50.000 comprás 25 unidades, ¿cuántas comprás con $80.000?
X = (80.000 × 25) ÷ 50.000 = 40 unidades

Si 1 vendedor hace 20 ventas por día, ¿cuántas hacen 3 vendedores?
X = 3 × 20 = 60 ventas

📝 **Ejercicio:** Si 10 productos te generan $15.000 de ganancia, ¿cuánto generan 35 productos?""",
         "quiz":[
             {"pregunta":"Si 3 productos cuestan $6.000, ¿cuánto cuestan 7?","opciones":["$12.000","$14.000","$13.000","$15.000"],"correcta":1},
             {"pregunta":"Si 1 empleado hace 15 cajas por hora, ¿cuántas hacen 4 empleados?","opciones":["45","50","60","55"],"correcta":2},
             {"pregunta":"Si con $20.000 comprás 10 unidades, ¿cuántas comprás con $50.000?","opciones":["20","25","30","22"],"correcta":1},
             {"pregunta":"Si 5 trabajadores terminan en 8 días, ¿cuánto tardan 10 trabajadores?","opciones":["4 días","6 días","3 días","5 días"],"correcta":0},
             {"pregunta":"Si 4 productos generan $2.000 de ganancia, ¿cuánto generan 10 productos?","opciones":["$4.000","$5.000","$6.000","$4.500"],"correcta":1},
         ]},
    ],
    "Intermedio": [
        {"id":"m5","titulo":"Margen de ganancia","descripcion":"Cómo calcular cuánto ganás realmente","xp":35,
         "contenido":"""El **margen de ganancia** es fundamental para cualquier negocio.

**Ganancia bruta:**
Ganancia = Precio de venta - Costo
Ejemplo: Vendés a $5.000, costó $3.000 → Ganancia = $2.000

**Margen de ganancia (%):**
Margen = (Ganancia ÷ Precio de venta) × 100
Ejemplo: (2.000 ÷ 5.000) × 100 = 40%

**Markup (% sobre el costo):**
Markup = (Ganancia ÷ Costo) × 100
Ejemplo: (2.000 ÷ 3.000) × 100 = 66.7%

**¿Cuál usar?**
- Margen → para saber qué % de lo que vendés es ganancia
- Markup → para saber cuánto le sumás al costo

**Fijar precio desde el margen:**
Si querés 40% de margen y el costo es $3.000:
Precio = Costo ÷ (1 - margen decimal) = 3.000 ÷ 0.60 = $5.000

**Fijar precio desde el markup:**
Si querés 50% de markup sobre costo de $3.000:
Precio = 3.000 × 1.50 = $4.500

📝 **Ejercicio:** Un producto te cuesta $1.800. ¿A qué precio lo vendés para tener un margen del 40%?""",
         "quiz":[
             {"pregunta":"Comprás a $2.000 y vendés a $3.000. ¿Cuál es tu margen?","opciones":["33%","40%","50%","45%"],"correcta":0},
             {"pregunta":"Si el costo es $5.000 y querés 50% de markup, ¿a qué precio vendés?","opciones":["$7.000","$7.500","$8.000","$6.500"],"correcta":1},
             {"pregunta":"Ganancia = $800, Precio de venta = $2.000. ¿Cuál es el margen?","opciones":["35%","40%","45%","30%"],"correcta":1},
             {"pregunta":"¿Cuál es la diferencia entre margen y markup?","opciones":["Son lo mismo","Margen se calcula sobre el precio, markup sobre el costo","Markup se calcula sobre el precio, margen sobre el costo","Ninguna"],"correcta":1},
             {"pregunta":"Costo $3.000, margen deseado 25%. ¿Cuál es el precio?","opciones":["$3.750","$4.000","$3.800","$4.200"],"correcta":1},
         ]},
        {"id":"m6","titulo":"Punto de equilibrio","descripcion":"¿Cuánto tenés que vender para no perder?","xp":35,
         "contenido":"""El **punto de equilibrio** es cuando tus ingresos igualan tus costos — ni ganás ni perdés.

**Tipos de costos:**
- Costos fijos: alquiler, sueldos, servicios → no cambian con las ventas
- Costos variables: materia prima, empaques → cambian con la producción

**Fórmula del punto de equilibrio (en unidades):**
PE = Costos Fijos ÷ (Precio de venta - Costo variable por unidad)

**Ejemplo:**
Costos fijos mensuales: $50.000 (alquiler + servicios)
Precio de venta por producto: $5.000
Costo variable por producto: $3.000
Margen de contribución: 5.000 - 3.000 = $2.000

PE = 50.000 ÷ 2.000 = 25 unidades

→ Necesitás vender 25 productos por mes para cubrir todos los costos.

**En pesos:**
PE en pesos = PE unidades × Precio de venta = 25 × 5.000 = $125.000

**¿Para qué sirve?**
Para saber cuál es tu meta mínima de ventas cada mes.

📝 **Ejercicio:** Tus costos fijos son $80.000. Vendés a $4.000 y el costo variable es $2.500. ¿Cuántas unidades necesitás vender?""",
         "quiz":[
             {"pregunta":"¿Qué es el punto de equilibrio?","opciones":["Cuando ganás el máximo","Cuando ingresos = costos","Cuando vendés la mitad","Cuando cubrís solo costos variables"],"correcta":1},
             {"pregunta":"Costos fijos $30.000, precio $3.000, costo variable $1.500. ¿Cuál es el PE?","opciones":["15 unidades","20 unidades","25 unidades","18 unidades"],"correcta":1},
             {"pregunta":"¿Cuál es un costo fijo?","opciones":["Materia prima","Empaques","Alquiler","Comisiones de vendedores"],"correcta":2},
             {"pregunta":"Si el PE son 40 unidades y vendés 50, ¿qué significa?","opciones":["Estás perdiendo","Estás en equilibrio","Estás ganando","No se puede saber"],"correcta":2},
             {"pregunta":"El margen de contribución es:","opciones":["Precio - Costo fijo","Precio - Costo variable","Ganancia total","Costo variable - Precio"],"correcta":1},
         ]},
        {"id":"m7","titulo":"Estadística básica","descripcion":"Promedio, mediana y datos para decidir mejor","xp":30,
         "contenido":"""La estadística te ayuda a entender tus números de negocio.

**Promedio (media aritmética):**
Promedio = Suma de todos los valores ÷ Cantidad de valores
Ventas de la semana: 10, 15, 8, 20, 12 → Suma = 65 ÷ 5 = 13 ventas/día

**Mediana:**
El valor del medio cuando los datos están ordenados.
Datos: 8, 10, 12, 15, 20 → Mediana = 12
Si hay cantidad par: promedio de los dos del medio.

**Moda:**
El valor que más se repite.
Ventas: 5, 8, 8, 10, 12, 8 → Moda = 8

**¿Cuándo usar cada uno?**
- Promedio → rendimiento general
- Mediana → cuando hay valores muy extremos que distorsionan
- Moda → el producto más vendido, la hora pico, etc.

**En el negocio:**
Promedio de ventas diarias → meta diaria
Mediana de precios → precio más representativo
Moda de productos vendidos → tu estrella

📝 **Ejercicio:** Tus ventas esta semana fueron: $15.000, $22.000, $8.000, $18.000, $12.000, $25.000, $20.000. ¿Cuál es el promedio diario?""",
         "quiz":[
             {"pregunta":"Ventas: 5, 10, 15, 20, 25. ¿Cuál es el promedio?","opciones":["13","14","15","16"],"correcta":2},
             {"pregunta":"Datos: 3, 7, 9, 12, 18. ¿Cuál es la mediana?","opciones":["7","9","12","10"],"correcta":1},
             {"pregunta":"Ventas: 4, 6, 6, 8, 6, 10. ¿Cuál es la moda?","opciones":["4","8","6","10"],"correcta":2},
             {"pregunta":"¿Cuándo conviene usar la mediana en lugar del promedio?","opciones":["Siempre","Cuando hay valores extremos que distorsionan","Cuando todos los datos son iguales","Nunca"],"correcta":1},
             {"pregunta":"Si vendés 0, 0, 0, 0, 100 productos, el promedio es 20. ¿Es representativo?","opciones":["Sí, siempre","No, la mediana (0) sería más representativa","Sí, el promedio siempre es correcto","No importa"],"correcta":1},
         ]},
    ],
    "Negocios": [
        {"id":"mn1","titulo":"Flujo de caja","descripcion":"Controlá cuánto entra y cuánto sale","xp":40,
         "contenido":"""El **flujo de caja** (cash flow) registra todo el dinero que entra y sale de tu negocio.

**Fórmula:**
Flujo de caja = Ingresos - Egresos

**Ingresos:** todo lo que entra
- Ventas en efectivo
- Cobros de deudas
- Préstamos recibidos

**Egresos:** todo lo que sale
- Compra de mercadería
- Alquiler, servicios
- Sueldos
- Impuestos

**Ejemplo mensual:**
Ingresos: $200.000 (ventas) + $30.000 (cobro deuda) = $230.000
Egresos: $100.000 (mercadería) + $40.000 (alquiler) + $30.000 (sueldos) = $170.000
Flujo de caja = $230.000 - $170.000 = +$60.000 ✅

Si el resultado es negativo → estás gastando más de lo que entra 🚨

**Flujo de caja acumulado:**
Suma mes a mes para ver la tendencia del negocio.

📝 **Ejercicio:** En enero vendiste $150.000, pagaste $80.000 de costos fijos y $40.000 de mercadería. ¿Cuál es tu flujo de caja?""",
         "quiz":[
             {"pregunta":"¿Qué es el flujo de caja?","opciones":["Las ganancias del negocio","La diferencia entre ingresos y egresos","El dinero en la caja registradora","El capital del negocio"],"correcta":1},
             {"pregunta":"Ingresos $300.000, egresos $250.000. ¿Cuál es el flujo de caja?","opciones":["$50.000","$30.000","$40.000","$60.000"],"correcta":0},
             {"pregunta":"Un flujo de caja negativo significa:","opciones":["El negocio está creciendo","Estás ganando mucho","Gastás más de lo que entra","El negocio está en equilibrio"],"correcta":2},
             {"pregunta":"¿Cuál de estos es un egreso?","opciones":["Venta en efectivo","Cobro de deuda","Pago de alquiler","Préstamo recibido"],"correcta":2},
             {"pregunta":"¿Para qué sirve el flujo de caja acumulado?","opciones":["Para saber el precio de venta","Para ver la tendencia del negocio mes a mes","Para calcular el margen","Para fijar sueldos"],"correcta":1},
         ]},
        {"id":"mn2","titulo":"Rentabilidad y ROI","descripcion":"¿Vale la pena la inversión?","xp":45,
         "contenido":"""El **ROI** (Return on Investment) mide qué tan rentable fue una inversión.

**Fórmula del ROI:**
ROI = ((Ganancia - Inversión) ÷ Inversión) × 100

**Ejemplo:**
Invertiste $50.000 en mercadería y la vendiste por $80.000
Ganancia = 80.000 - 50.000 = $30.000
ROI = (30.000 ÷ 50.000) × 100 = 60%

→ Por cada $100 que invertiste, ganaste $60. ¡Muy bueno!

**¿Qué ROI es bueno?**
- Menos de 10% → bajo
- 10% - 30% → aceptable
- 30% - 50% → bueno
- Más de 50% → excelente

**ROI en publicidad:**
Gastaste $5.000 en publicidad y generaste $20.000 en ventas adicionales
ROI = ((20.000 - 5.000) ÷ 5.000) × 100 = 300%

→ Por cada $100 invertidos en publicidad, ganaste $300.

**Período de recupero:**
¿En cuánto tiempo recuperás la inversión?
Período = Inversión ÷ Ganancia mensual

📝 **Ejercicio:** Invertiste $100.000 en una mejora del local y tus ventas aumentaron $20.000 por mes. ¿En cuántos meses recuperás la inversión?""",
         "quiz":[
             {"pregunta":"Invertiste $20.000 y ganaste $30.000. ¿Cuál es el ROI?","opciones":["40%","50%","60%","45%"],"correcta":1},
             {"pregunta":"Un ROI de 80% es:","opciones":["Bajo","Aceptable","Bueno","Excelente"],"correcta":3},
             {"pregunta":"Si gastaste $10.000 en publicidad y generaste $25.000 adicionales, el ROI es:","opciones":["100%","150%","200%","250%"],"correcta":1},
             {"pregunta":"¿Para qué sirve el período de recupero?","opciones":["Para calcular el margen","Para saber cuándo recuperás la inversión","Para fijar precios","Para calcular el ROI"],"correcta":1},
             {"pregunta":"Invertiste $50.000 y ganás $10.000 por mes. ¿En cuántos meses recuperás?","opciones":["3 meses","4 meses","5 meses","6 meses"],"correcta":2},
         ]},
        {"id":"mn3","titulo":"Proyecciones de ventas","descripcion":"Cómo proyectar el futuro de tu negocio","xp":40,
         "contenido":"""Las **proyecciones** te ayudan a planificar y anticipar el futuro del negocio.

**Proyección simple (crecimiento fijo):**
Si vendés $100.000 este mes y crecés 10% mensual:
Mes 1: $100.000
Mes 2: 100.000 × 1.10 = $110.000
Mes 3: 110.000 × 1.10 = $121.000
Mes 4: 121.000 × 1.10 = $133.100

**Proyección anual:**
Ventas anuales = Ventas mensuales promedio × 12
Si vendés $150.000/mes → $150.000 × 12 = $1.800.000 anuales

**Meta regresiva (de atrás para adelante):**
Si querés ganar $500.000 en el año y tu margen es 40%:
Ventas necesarias = 500.000 ÷ 0.40 = $1.250.000 anuales
Por mes = 1.250.000 ÷ 12 = $104.167/mes

**Escenarios:**
Siempre hacé 3 proyecciones:
- Pesimista: -20% de lo esperado
- Normal: lo que esperás
- Optimista: +20% de lo esperado

📝 **Ejercicio:** Querés ganar $200.000 netos en 6 meses. Tu margen es del 30%. ¿Cuánto necesitás vender por mes?""",
         "quiz":[
             {"pregunta":"Si vendés $80.000 y crecés 10% mensual, ¿cuánto vendés el mes siguiente?","opciones":["$85.000","$88.000","$90.000","$82.000"],"correcta":1},
             {"pregunta":"Ventas mensuales $200.000. ¿Cuánto proyectás en el año?","opciones":["$1.800.000","$2.000.000","$2.400.000","$2.200.000"],"correcta":2},
             {"pregunta":"Querés ganar $600.000 con un margen del 25%. ¿Cuánto necesitás vender?","opciones":["$2.000.000","$2.400.000","$1.800.000","$2.200.000"],"correcta":1},
             {"pregunta":"¿Por qué conviene hacer 3 escenarios (pesimista, normal, optimista)?","opciones":["Para confundirse más","Para estar preparado para diferentes resultados","Porque es obligatorio","Para impresionar a los inversores"],"correcta":1},
             {"pregunta":"La 'meta regresiva' sirve para:","opciones":["Calcular pérdidas","Partir de la ganancia deseada y calcular las ventas necesarias","Proyectar el pasado","Calcular el ROI"],"correcta":1},
         ]},
    ],
}

def system_mate(user, leccion=None, modo="chat"):
    nivel = user.get("mate_nivel", "Básico")
    loks = len(user.get("mate_lecciones_completadas", []))
    lec = f"\nLección actual: {leccion}" if leccion else ""
    modo_extra = ""
    if modo == "calculadora":
        modo_extra = "\n\nESTÁS EN MODO CALCULADORA. El usuario te da un problema numérico de su negocio. Vos: 1) Identificás qué fórmula usar 2) Mostrás el cálculo paso a paso 3) Das el resultado claro 4) Explicás qué significa para su negocio."
    return f"""Sos Bruno, el profesor de matemáticas de AV MentorAI. Motivador, con ejemplos de la vida real, explicás todo con situaciones del negocio y la vida cotidiana.
Estudiante: {user['nombre']} | Nivel: {nivel} | Lecciones completadas: {loks}{lec}
Explicás en español simple. Usás ejemplos de negocios, precios, ventas, ganancias, productos.
Nunca usás jerga matemática innecesaria. Siempre terminás con "¿Lo entendiste? ¿Querés que practiquemos más?" 🔢
Frases tuyas: "Los números no mienten, y tampoco son difíciles si los entendés así:", "Esto en tu negocio significa:", "¡Muy bien! Eso es exactamente correcto 💪"{modo_extra}"""

# ════════════════════════════════════════
# TAB MATEMÁTICAS
# ════════════════════════════════════════
with tab_mate:
    st.markdown('<div style="background:linear-gradient(135deg,rgba(34,197,94,.15),rgba(16,185,129,.10));border:1px solid rgba(34,197,94,.35);border-radius:16px;padding:12px 16px;margin-bottom:12px"><span style="font-size:20px;font-weight:800;color:#22c55e">🔢 Aprender Matemáticas</span><br><span style="font-size:12px;color:#94a3b8">Lecciones · Quiz · Calculadora de negocios · Certificado</span></div>', unsafe_allow_html=True)

    # Inicializar datos de mate en usuario si no existen
    if "mate_nivel" not in user: user["mate_nivel"] = "Básico"
    if "mate_lecciones_completadas" not in user: user["mate_lecciones_completadas"] = []
    if "mate_messages" not in user: user["mate_messages"] = []

    mate_sel = st.radio("",
        ["Lecciones", "Calculadora de negocios", "Chat con Bruno"],
        key="mate_sel", horizontal=True, label_visibility="collapsed")
    st.divider()

    # ── LECCIONES DE MATEMÁTICAS ──
    if mate_sel == "Lecciones":
        niv_mate = st.selectbox("Tu nivel de matemáticas:", ["Básico", "Intermedio", "Negocios"],
            index=["Básico", "Intermedio", "Negocios"].index(user.get("mate_nivel", "Básico")),
            key="sel_mate_nivel")
        if niv_mate != user.get("mate_nivel"):
            user["mate_nivel"] = niv_mate; guardar_usuario(user)

        mate_loks_list = user.get("mate_lecciones_completadas", [])
        lecs_mate_niv = LECCIONES_MATE.get(niv_mate, [])
        total_mate = len(lecs_mate_niv)
        comp_mate = sum(1 for l in lecs_mate_niv if l["id"] in mate_loks_list)
        if total_mate > 0:
            st.progress(comp_mate / total_mate)
            st.caption(f"{comp_mate}/{total_mate} lecciones completadas en nivel {niv_mate}")

        for lec in lecs_mate_niv:
            done = lec["id"] in mate_loks_list
            icono = "✅" if done else "📖"
            cl2, cb2 = st.columns([4, 1])
            with cl2:
                st.markdown(f'<div class="{"lesson-card-done" if done else "lesson-card"}"><b>{icono} {lec["titulo"]}</b><br><span class="small-text">{lec["descripcion"]}</span> <span style="color:#facc15;font-size:12px;font-weight:700">+{lec["xp"]} XP</span></div>', unsafe_allow_html=True)
            with cb2:
                if st.button("Repasar" if done else "Ver", key=f"mate_{lec['id']}"):
                    st.session_state.mate_leccion_sel = lec["id"]; st.rerun()

        # Lección seleccionada
        mate_lsel = st.session_state.get("mate_leccion_sel", None)
        if mate_lsel:
            lobj = next((l for l in lecs_mate_niv if l["id"] == mate_lsel), None)
            if lobj:
                st.divider()
                st.markdown(f"## 📖 {lobj['titulo']}")
                st.markdown(f'<div class="lesson-content">{lobj["contenido"]}</div>', unsafe_allow_html=True)

                # Quiz
                st.markdown("### 🧠 Quiz de la lección")
                st.caption("Respondé las preguntas para completar la lección (necesitás 80%).")
                quiz_key = f"mate_quiz_{lobj['id']}"
                if quiz_key not in st.session_state: st.session_state[quiz_key] = {}
                respuestas = st.session_state[quiz_key]
                for i, q in enumerate(lobj.get("quiz", [])):
                    st.markdown(f'<div class="quiz-card"><b>Pregunta {i+1}:</b> {q["pregunta"]}</div>', unsafe_allow_html=True)
                    sel = st.radio("", q["opciones"], key=f"mq_{lobj['id']}_{i}", index=None, label_visibility="collapsed")
                    if sel is not None: respuestas[i] = q["opciones"].index(sel)

                if len(respuestas) == len(lobj.get("quiz", [])):
                    correctas = sum(1 for i, q in enumerate(lobj["quiz"]) if respuestas.get(i) == q["correcta"])
                    pct = int(correctas / len(lobj["quiz"]) * 100)
                    if pct >= 80:
                        st.success(f"✅ {correctas}/{len(lobj['quiz'])} correctas ({pct}%). ¡Excelente Bruno estaría orgulloso! 💪")
                        if lobj["id"] not in mate_loks_list:
                            if st.button(f"🏆 Completar lección (+{lobj['xp']} XP)", key=f"comp_mate_{lobj['id']}"):
                                user["mate_lecciones_completadas"].append(lobj["id"])
                                sumar_xp(lobj["xp"]); guardar_usuario(user)
                                st.success(f"¡Lección completada! +{lobj['xp']} XP 🎉")
                                st.session_state.mate_leccion_sel = None; st.rerun()
                        else:
                            st.info("✅ Ya completaste esta lección.")
                    else:
                        st.warning(f"⚠️ {correctas}/{len(lobj['quiz'])} correctas ({pct}%). Necesitás 80% para completarla.")

                if st.button("❌ Cerrar", key=f"cerrar_mate_{mate_lsel}"):
                    st.session_state.mate_leccion_sel = None; st.rerun()

        # Certificado de mate
        st.divider()
        st.markdown("### 🏆 Certificado de Matemáticas")
        for nivel_cert, lecs_cert in LECCIONES_MATE.items():
            total_c = len(lecs_cert)
            loks_c = sum(1 for l in lecs_cert if l["id"] in user.get("mate_lecciones_completadas", []))
            st.progress(loks_c / total_c if total_c > 0 else 0)
            st.caption(f"Nivel {nivel_cert}: {loks_c}/{total_c}")
            if loks_c == total_c:
                st.success(f"✅ ¡Completaste el nivel {nivel_cert}!")
                if st.button(f"📜 Certificado {nivel_cert}", key=f"cert_mate_{nivel_cert}"):
                    pdf_buf = generar_certificado_pdf(user["nombre"], f"Matemáticas — {nivel_cert}", loks_c, hoy)
                    st.download_button(f"⬇️ Descargar PDF", data=pdf_buf,
                        file_name=f"certificado_mate_{nivel_cert.lower()}_{user['nombre'].lower().replace(' ','_')}.pdf",
                        mime="application/pdf", key=f"dl_mate_{nivel_cert}")

    # ── CALCULADORA DE NEGOCIOS ──
    if mate_sel == "Calculadora de negocios":
        st.markdown("### 🧮 Calculadora de negocios")
        st.caption("Ingresá tus números y Bruno te explica el resultado paso a paso.")

        calc_tipo = st.selectbox("¿Qué querés calcular?", [
            "💰 Margen de ganancia",
            "⚖️ Punto de equilibrio",
            "📈 ROI de una inversión",
            "🏷️ Precio de venta ideal",
            "📊 Proyección de ventas",
            "🔢 Problema personalizado"
        ], key="calc_tipo")

        if calc_tipo == "💰 Margen de ganancia":
            costo = st.number_input("Costo del producto ($):", min_value=0.0, step=100.0, key="calc_costo")
            precio = st.number_input("Precio de venta ($):", min_value=0.0, step=100.0, key="calc_precio")
            if st.button("Calcular 🔢", key="btn_margen") and precio > 0:
                ganancia = precio - costo
                margen = (ganancia / precio) * 100
                markup = (ganancia / costo) * 100 if costo > 0 else 0
                st.success(f"**Ganancia:** ${ganancia:,.0f}")
                st.success(f"**Margen:** {margen:.1f}%")
                st.success(f"**Markup:** {markup:.1f}%")
                prompt = f"Mi producto cuesta ${costo} y lo vendo a ${precio}. La ganancia es ${ganancia:.0f}, el margen es {margen:.1f}% y el markup es {markup:.1f}%. Explicame si esto está bien para mi negocio y qué me recomendás."
                enviar_mate(prompt, leccion="Calculadora de negocios")

        elif calc_tipo == "⚖️ Punto de equilibrio":
            cf = st.number_input("Costos fijos mensuales ($):", min_value=0.0, step=1000.0, key="calc_cf")
            pv = st.number_input("Precio de venta por unidad ($):", min_value=0.0, step=100.0, key="calc_pv")
            cv = st.number_input("Costo variable por unidad ($):", min_value=0.0, step=100.0, key="calc_cv")
            if st.button("Calcular 🔢", key="btn_pe") and pv > cv:
                mc = pv - cv
                pe = cf / mc
                pe_pesos = pe * pv
                st.success(f"**Punto de equilibrio:** {pe:.0f} unidades por mes")
                st.success(f"**En pesos:** ${pe_pesos:,.0f} por mes")
                prompt = f"Mis costos fijos son ${cf}, vendo a ${pv} y el costo variable es ${cv}. Mi punto de equilibrio es {pe:.0f} unidades (${pe_pesos:,.0f}). Explicame qué significa y si mi negocio está bien."
                enviar_mate(prompt, leccion="Calculadora de negocios")

        elif calc_tipo == "📈 ROI de una inversión":
            inversion = st.number_input("Inversión realizada ($):", min_value=0.0, step=1000.0, key="calc_inv")
            retorno = st.number_input("Retorno obtenido ($):", min_value=0.0, step=1000.0, key="calc_ret")
            if st.button("Calcular 🔢", key="btn_roi") and inversion > 0:
                ganancia_roi = retorno - inversion
                roi = (ganancia_roi / inversion) * 100
                st.success(f"**Ganancia neta:** ${ganancia_roi:,.0f}")
                st.success(f"**ROI:** {roi:.1f}%")
                if roi > 50: st.success("🔥 ¡Excelente ROI!")
                elif roi > 20: st.info("👍 Buen ROI")
                else: st.warning("⚠️ ROI bajo, revisá la estrategia")
                prompt = f"Invertí ${inversion} y obtuve ${retorno}. Mi ganancia fue ${ganancia_roi:.0f} y el ROI es {roi:.1f}%. ¿Es bueno esto para mi negocio?"
                enviar_mate(prompt, leccion="Calculadora de negocios")

        elif calc_tipo == "🏷️ Precio de venta ideal":
            costo_p = st.number_input("Costo del producto ($):", min_value=0.0, step=100.0, key="calc_costo_p")
            margen_d = st.slider("Margen de ganancia deseado (%):", 5, 80, 40, key="calc_margen_d")
            if st.button("Calcular 🔢", key="btn_precio") and costo_p > 0:
                precio_ideal = costo_p / (1 - margen_d / 100)
                ganancia_p = precio_ideal - costo_p
                st.success(f"**Precio ideal:** ${precio_ideal:,.0f}")
                st.success(f"**Ganancia por unidad:** ${ganancia_p:,.0f}")
                prompt = f"Mi producto cuesta ${costo_p} y quiero un margen del {margen_d}%. El precio ideal es ${precio_ideal:.0f} con una ganancia de ${ganancia_p:.0f} por unidad. ¿Me das consejos para fijar este precio?"
                enviar_mate(prompt, leccion="Calculadora de negocios")

        elif calc_tipo == "📊 Proyección de ventas":
            ventas_act = st.number_input("Ventas actuales mensuales ($):", min_value=0.0, step=1000.0, key="calc_vact")
            crec = st.slider("Crecimiento mensual esperado (%):", 1, 50, 10, key="calc_crec")
            meses = st.slider("Proyección en meses:", 1, 24, 6, key="calc_meses")
            if st.button("Proyectar 🔢", key="btn_proy") and ventas_act > 0:
                st.markdown("**Proyección mes a mes:**")
                v = ventas_act
                total_proy = 0
                for i in range(1, meses + 1):
                    v = v * (1 + crec / 100)
                    total_proy += v
                    st.write(f"Mes {i}: ${v:,.0f}")
                st.success(f"**Total proyectado {meses} meses:** ${total_proy:,.0f}")

        else:  # Problema personalizado
            problema = st.text_area("Describí tu problema o cálculo:", placeholder="Ej: Compré 50 remeras a $1.500 cada una, las quiero vender con 45% de margen. ¿A qué precio las pongo?", height=100, key="calc_problema")
            if st.button("Resolver con Bruno 🔢", key="btn_problema") and problema.strip():
                enviar_mate(problema, leccion="Calculadora de negocios")

        # Mostrar respuesta de Bruno
        mate_msgs = user.get("mate_messages", [])
        if mate_msgs:
            ul_mate = obtener_ultima_respuesta(mate_msgs)
            if ul_mate:
                st.divider()
                st.markdown("**Bruno dice:**")
                st.markdown(f'<div class="chat-english" style="border-left-color:#22c55e"><div class="chat-name-english" style="color:#22c55e!important">🔢 Bruno — Profesor de Matemáticas</div><div class="chat-text">{ul_mate}</div></div>', unsafe_allow_html=True)

    # ── CHAT CON BRUNO ──
    if mate_sel == "Chat con Bruno":
        st.markdown("<p style='font-size:16px;font-weight:800;color:#22c55e;margin:8px 0 2px'>💬 Chat con Bruno</p>", unsafe_allow_html=True)
        st.caption("Preguntale dudas o pedile ejercicios con ejemplos de tu negocio.")

        mate_msgs = user.get("mate_messages", [])
        if not mate_msgs:
            n = user['nombre'] or 'estudiante'
            bv_mate = f"¡Hola {n}! 💪 Soy Bruno, tu profesor de matemáticas. Te prometo que con ejemplos reales de negocios, los números se vuelven simples. ¿Por dónde empezamos? ¿Querés aprender algo nuevo o tenés un cálculo para hacer?"
            st.markdown(f'<div class="chat-english" style="border-left-color:#22c55e"><div class="chat-name-english" style="color:#22c55e!important">🔢 Bruno — Profesor de Matemáticas</div><div class="chat-text">{bv_mate}</div></div>', unsafe_allow_html=True)
        else:
            for m in mate_msgs[-20:]:
                if m["role"] == "user":
                    st.markdown(f'<div class="chat-user"><div class="chat-name">Vos</div><div class="chat-text">{m["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-english" style="border-left-color:#22c55e"><div class="chat-name-english" style="color:#22c55e!important">🔢 Bruno</div><div class="chat-text">{m["content"]}</div></div>', unsafe_allow_html=True)

            ul_mate2 = obtener_ultima_respuesta(mate_msgs)
            if ul_mate2 and st.button("🔊 Escuchar a Bruno", key="aud_mate"):
                with st.spinner("..."): render_audio_player(ul_mate2)

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("% Porcentajes", key="bmate1"): st.session_state.mate_quick="Explicame cómo calcular porcentajes con ejemplos de precios y descuentos."
            if st.button("📊 Margen de ganancia", key="bmate2"): st.session_state.mate_quick="¿Cómo calculo el margen de ganancia de un producto? Dame ejemplos."
        with b2:
            if st.button("⚖️ Punto de equilibrio", key="bmate3"): st.session_state.mate_quick="Explicame qué es el punto de equilibrio y cómo calcularlo para mi negocio."
            if st.button("📈 ROI", key="bmate4"): st.session_state.mate_quick="¿Qué es el ROI y cómo sé si una inversión vale la pena?"
        with b3:
            if st.button("🎯 Dame un ejercicio", key="bmate5"): st.session_state.mate_quick="Dame un ejercicio de matemáticas de negocios para practicar."
            if st.button("🔢 Regla de tres", key="bmate6"): st.session_state.mate_quick="Explicame la regla de tres con ejemplos de ventas y productos."

        # Procesar botón rápido ANTES del chat_input
        if st.session_state.get("mate_quick"):
            _mq = st.session_state.mate_quick
            st.session_state.mate_quick = None
            enviar_mate(_mq)

        mate_input = st.chat_input("✍️ Preguntale a Bruno acá...")
        if mate_input:
            enviar_mate(mate_input)
        if False:
            mate_lsel2 = st.session_state.get("mate_leccion_sel", None)
            lec_ctx = None
            if mate_lsel2:
                lo2 = next((l for l in lecs_mate_niv if l["id"] == mate_lsel2), None)
                if lo2: lec_ctx = lo2["titulo"]
            enviar_mate(mate_input, leccion=lec_ctx)

        if st.button("🗑️ Borrar chat de Bruno", key="borrar_mate"):
            user["mate_messages"] = []; guardar_usuario(user); st.rerun()

# ════════════════════════════════════════
# TAB HERRAMIENTAS
# ════════════════════════════════════════
with tab_herramientas:
    st.markdown('<div class="hero-card"><h2>🛠️ Herramientas</h2><p class="small-text">Analizá tu competencia, generá contenido listo para publicar y descubrí herramientas para crecer.</p></div>', unsafe_allow_html=True)

    herr_sel = st.radio("",
        ["Analizar competencia", "Generar contenido", "Afiliados",
         "Plantillas", "Marca personal", "Finanzas"],
        key="herr_sel", horizontal=True, label_visibility="collapsed")
    st.divider()

    # ── ANÁLISIS DE COMPETENCIA ──
    if herr_sel == "Analizar competencia":
        st.markdown("### 🔍 Análisis de competencia")
        st.caption("Describí a tu competidor y el mentor te dice cómo superarlo con un plan concreto.")

        comp_nombre = st.text_input("Nombre del competidor:", placeholder="Ej: Tienda Ropa Valentino, Supermercado El Barrio...", key="comp_nombre")
        comp_rubro = st.text_input("Rubro o tipo de negocio:", placeholder="Ej: ropa, supermercado, ecommerce, comida...", key="comp_rubro")
        comp_ig = st.text_input("Instagram o web (opcional):", placeholder="Ej: @tiendaropa o www.tienda.com", key="comp_ig")
        comp_desc = st.text_area("¿Qué sabés de este competidor? Describilo:", 
            placeholder="Ej: Tiene mucha clientela, sus precios son más bajos que los míos, publica mucho en Instagram, tiene local en el centro...",
            height=120, key="comp_desc")
        comp_mi_negocio = st.text_area("¿Cómo es tu negocio en comparación?",
            placeholder="Ej: Yo vendo online, tengo precios similares pero menos clientes, mi producto es de mejor calidad...",
            height=100, key="comp_mi_negocio")

        if st.button("🔍 Analizar y crear plan para superarlo", key="btn_comp"):
            if comp_nombre.strip() and comp_desc.strip():
                prompt_comp = f"""Analizá este competidor y dame un plan concreto para superarlo:

COMPETIDOR:
- Nombre: {comp_nombre}
- Rubro: {comp_rubro}
- Instagram/web: {comp_ig or 'No especificado'}
- Descripción: {comp_desc}

MI NEGOCIO EN COMPARACIÓN:
{comp_mi_negocio or 'No especificado'}

Dame:
1. Análisis de qué hace bien este competidor (sus fortalezas)
2. Sus debilidades o puntos débiles que puedo aprovechar
3. Mis ventajas competitivas reales
4. Plan concreto de 5 acciones para superarlo
5. Una estrategia de diferenciación clara

Sé específico y práctico. Sin vaguedades."""

                user = st.session_state.user_data
                with st.spinner("🔍 Analizando competidor..."):
                    try:
                        r = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": system_negocio(user, st.session_state.modo, "")},
                                {"role": "user", "content": prompt_comp}
                            ],
                            temperature=0.8, max_tokens=1200
                        )
                        resp_comp = r.choices[0].message.content
                        st.session_state.ultimo_analisis = resp_comp
                        sumar_xp(15)
                        guardar_usuario(user)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Completá al menos el nombre y la descripción del competidor.")

        if st.session_state.get("ultimo_analisis"):
            st.divider()
            st.markdown("### 📊 Análisis completo")
            st.markdown(f'<div class="card" style="border-color:rgba(56,189,248,.4)">{st.session_state.ultimo_analisis}</div>', unsafe_allow_html=True)
            st.download_button(
                "⬇️ Descargar análisis",
                data=st.session_state.ultimo_analisis,
                file_name=f"analisis_{comp_nombre.lower().replace(' ','_')}.txt",
                mime="text/plain",
                key="dl_analisis"
            )

    # ── GENERADOR DE CONTENIDO ──
    if herr_sel == "Generar contenido":
        st.markdown("### ✍️ Generador de contenido")
        st.caption("Describí tu producto y generamos el texto listo para copiar y publicar.")

        gen_tipo = st.selectbox("¿Dónde vas a publicar?", [
            "📸 Post de Instagram",
            "💬 Mensaje de WhatsApp para vender",
            "🛒 Descripción para Mercado Libre",
            "📱 Historia de Instagram (Story)",
            "🎵 Caption para TikTok",
            "📧 Email de venta a clientes",
            "🏷️ Título y descripción para producto online",
        ], key="gen_tipo")

        gen_producto = st.text_input("¿Qué producto o servicio querés promocionar?",
            placeholder="Ej: remeras de algodón, servicio de limpieza, empanadas caseras...", key="gen_producto")
        gen_precio = st.text_input("Precio (opcional):", placeholder="Ej: $5.000, 3x$10.000...", key="gen_precio")
        gen_beneficio = st.text_area("¿Qué lo hace especial o diferente?",
            placeholder="Ej: son de algodón 100% nacional, entrega en el día, hecho a mano, precio más bajo de la zona...",
            height=100, key="gen_beneficio")
        gen_tono = st.selectbox("Tono del mensaje:", [
            "Divertido y casual",
            "Profesional y serio",
            "Urgente (oferta limitada)",
            "Cercano y amigable",
            "Aspiracional y premium"
        ], key="gen_tono")
        gen_cantidad = st.slider("¿Cuántas versiones querés?", 1, 3, 2, key="gen_cantidad")

        if st.button("✍️ Generar contenido", key="btn_gen"):
            if gen_producto.strip():
                tipo_limpio = gen_tipo.split(" ", 1)[1]
                prompt_gen = f"""Generá {gen_cantidad} versión(es) de contenido para {tipo_limpio}.

PRODUCTO/SERVICIO: {gen_producto}
PRECIO: {gen_precio or 'No especificado'}
QUÉ LO HACE ESPECIAL: {gen_beneficio or 'No especificado'}
TONO: {gen_tono}

Reglas:
- Escribí en español latino argentino
- Incluí emojis si corresponde al canal
- Usá hashtags relevantes si es Instagram o TikTok
- Sé específico y persuasivo
- Incluí un call to action claro al final
- Cada versión separada claramente con "--- VERSIÓN X ---"
- Para WhatsApp: formato corto y directo, máximo 5 líneas
- Para Mercado Libre: incluí título optimizado + descripción detallada
- Para Instagram: incluí caption completo + hashtags

Generá contenido que realmente venda, no genérico."""

                user = st.session_state.user_data
                with st.spinner("✍️ Generando contenido..."):
                    try:
                        r = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": f"Sos un experto en marketing digital y copywriting para LATAM. Creás contenido que vende de verdad para redes sociales, WhatsApp y marketplaces. Conocés bien el mercado argentino."},
                                {"role": "user", "content": prompt_gen}
                            ],
                            temperature=0.9, max_tokens=1500
                        )
                        resp_gen = r.choices[0].message.content
                        st.session_state.ultimo_contenido = resp_gen
                        st.session_state.ultimo_gen_tipo = tipo_limpio
                        sumar_xp(10)
                        guardar_usuario(user)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Describí el producto o servicio primero.")

        if st.session_state.get("ultimo_contenido"):
            st.divider()
            st.markdown(f"### 📋 Contenido generado para {st.session_state.get('ultimo_gen_tipo','')}")
            
            versiones = st.session_state.ultimo_contenido.split("--- VERSIÓN")
            if len(versiones) > 1:
                for i, v in enumerate(versiones[1:], 1):
                    v_limpia = v.replace(f" {i} ---", "").strip()
                    with st.expander(f"📄 Versión {i}", expanded=True):
                        st.markdown(f'<div class="card" style="border-color:rgba(168,85,247,.4);white-space:pre-wrap">{v_limpia}</div>', unsafe_allow_html=True)
                        st.code(v_limpia, language=None)
            else:
                st.markdown(f'<div class="card" style="border-color:rgba(168,85,247,.4);white-space:pre-wrap">{st.session_state.ultimo_contenido}</div>', unsafe_allow_html=True)
                st.code(st.session_state.ultimo_contenido, language=None)

            st.download_button(
                "⬇️ Descargar contenido",
                data=st.session_state.ultimo_contenido,
                file_name=f"contenido_{gen_producto.lower().replace(' ','_')}.txt",
                mime="text/plain",
                key="dl_contenido"
            )

            if st.button("🔄 Generar nuevas versiones", key="btn_regen"):
                st.session_state.ultimo_contenido = None
                st.rerun()

    # ── AFILIADOS ──
    if herr_sel == "Afiliados":
        st.markdown("### 🤝 Herramientas recomendadas")
        st.caption("Las mejores herramientas para hacer crecer tu negocio. Usadas y recomendadas por AV MentorAI.")

        herramientas_afiliados = [
            {
                "nombre": "Tiendanube",
                "emoji": "🛍️",
                "categoria": "Tienda online",
                "descripcion": "La plataforma de e-commerce más popular de LATAM. Creás tu tienda online en minutos, sin saber programar. Ideal para vender ropa, accesorios, productos y más.",
                "para_quien": "Para quien quiere vender online sin complicarse",
                "precio": "Plan gratis disponible",
                "link": "https://www.tiendanube.com",
                "color": "#38bdf8"
            },
            {
                "nombre": "Canva",
                "emoji": "🎨",
                "categoria": "Diseño",
                "descripcion": "La herramienta de diseño más fácil del mundo. Creás posts de Instagram, logos, flyers, presentaciones y todo lo que necesitás para tu negocio sin ser diseñador.",
                "para_quien": "Para quien quiere contenido visual profesional sin contratar diseñador",
                "precio": "Plan gratis muy completo",
                "link": "https://www.canva.com",
                "color": "#a855f7"
            },
            {
                "nombre": "Mercado Pago",
                "emoji": "💳",
                "categoria": "Pagos",
                "descripcion": "El sistema de pagos más usado de Argentina y LATAM. Cobrás con QR, link de pago, tarjeta de crédito y débito. Sin necesitar local físico.",
                "para_quien": "Para cualquier negocio que quiera cobrar de forma profesional",
                "precio": "Gratis — cobra comisión por transacción",
                "link": "https://www.mercadopago.com.ar",
                "color": "#22c55e"
            },
            {
                "nombre": "WhatsApp Business",
                "emoji": "📱",
                "categoria": "Ventas",
                "descripcion": "La versión de WhatsApp para negocios. Tenés catálogo de productos, respuestas automáticas, etiquetas para organizar clientes y estadísticas de mensajes.",
                "para_quien": "Para quien vende por WhatsApp y quiere ser más profesional",
                "precio": "100% gratis",
                "link": "https://business.whatsapp.com",
                "color": "#facc15"
            },
            {
                "nombre": "Notion",
                "emoji": "📋",
                "categoria": "Organización",
                "descripcion": "La herramienta perfecta para organizar tu negocio. Anotás ideas, hacés listas de tareas, seguimiento de clientes, presupuestos y mucho más en un solo lugar.",
                "para_quien": "Para quien quiere tener todo su negocio organizado",
                "precio": "Plan gratis disponible",
                "link": "https://www.notion.so",
                "color": "#f97316"
            },
            {
                "nombre": "Mailchimp",
                "emoji": "📧",
                "categoria": "Email marketing",
                "descripcion": "Enviás emails masivos a tus clientes de forma profesional. Promociones, novedades, newsletter. Muy fácil de usar y con plantillas listas.",
                "para_quien": "Para quien tiene base de clientes y quiere fidelizarlos",
                "precio": "Gratis hasta 500 contactos",
                "link": "https://mailchimp.com",
                "color": "#38bdf8"
            },
            {
                "nombre": "Later",
                "emoji": "📅",
                "categoria": "Redes sociales",
                "descripcion": "Programás tus posts de Instagram, Facebook y TikTok con anticipación. Subís el contenido una vez por semana y se publica solo en el horario ideal.",
                "para_quien": "Para quien quiere ser constante en redes sin perder tiempo",
                "precio": "Plan gratis disponible",
                "link": "https://later.com",
                "color": "#a855f7"
            },
            {
                "nombre": "Google My Business",
                "emoji": "📍",
                "categoria": "Visibilidad local",
                "descripcion": "Aparecés en Google Maps y en las búsquedas de Google cuando alguien busca tu rubro en tu zona. Fundamental para negocios locales y con local físico.",
                "para_quien": "Para negocios con local físico o que atienden zona específica",
                "precio": "100% gratis",
                "link": "https://business.google.com",
                "color": "#22c55e"
            },
        ]

        # Filtro por categoría
        categorias = ["Todas"] + list(set(h["categoria"] for h in herramientas_afiliados))
        cat_sel = st.selectbox("Filtrar por categoría:", categorias, key="cat_afil")

        herramientas_filtradas = herramientas_afiliados if cat_sel == "Todas" else [h for h in herramientas_afiliados if h["categoria"] == cat_sel]

        for herr in herramientas_filtradas:
            st.markdown(f"""
            <div class="card" style="border-color:rgba({','.join(str(int(herr['color'].lstrip('#')[i:i+2], 16)) for i in (0,2,4))},.4);margin-bottom:16px">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                    <span style="font-size:28px">{herr['emoji']}</span>
                    <div>
                        <b style="font-size:18px;color:#f8fafc">{herr['nombre']}</b>
                        <span style="background:rgba(148,163,184,.2);padding:2px 10px;border-radius:10px;font-size:12px;margin-left:8px;color:#94a3b8">{herr['categoria']}</span>
                    </div>
                </div>
                <p style="color:#cbd5e1;font-size:14px;margin-bottom:8px">{herr['descripcion']}</p>
                <p style="color:#94a3b8;font-size:13px;margin-bottom:4px">✅ <b>Para quién:</b> {herr['para_quien']}</p>
                <p style="color:#94a3b8;font-size:13px;margin-bottom:12px">💰 <b>Precio:</b> {herr['precio']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.link_button(f"🔗 Ir a {herr['nombre']}", herr['link'], use_container_width=False)
            st.write("")

        st.divider()
        st.markdown('<div class="card"><p class="small-text">💡 <b>¿Usás alguna de estas herramientas?</b> Contale al mentor de negocios cuál usás y te ayuda a sacarle el máximo provecho.</p></div>', unsafe_allow_html=True)

    # ── PLANTILLAS ──
    if herr_sel == "Plantillas":
        st.markdown("### 📋 Plantillas descargables")
        st.caption("Copiá y usá estas plantillas hoy mismo. Están listas para adaptar a tu negocio.")
        plant_sel = st.selectbox("Elegí una plantilla:", list(PLANTILLAS.keys()), key="pl3_sel")
        if plant_sel:
            contenido_p = PLANTILLAS[plant_sel]
            st.markdown(f'<div style="background:rgba(15,23,42,.95);border:1px solid rgba(250,204,21,.3);border-radius:16px;padding:20px;white-space:pre-wrap;font-size:13px;color:#f1f5f9;line-height:1.6">{contenido_p}</div>', unsafe_allow_html=True)
            st.code(contenido_p, language=None)
            st.download_button("⬇️ Descargar plantilla", data=contenido_p,
                file_name="plantilla.txt", mime="text/plain", key="pl3_dl")
        st.divider()
        st.markdown("**✍️ Personalizar con IA**")
        mi_neg_p = st.text_area("Describí tu negocio:", placeholder="Ej: vendo ropa de mujer por Instagram", height=80, key="pl3_neg")
        if st.button("🪄 Personalizar", key="pl3_btn") and mi_neg_p.strip():
            prompt_p = f"Adaptá esta plantilla para el negocio: {mi_neg_p}. Plantilla: {PLANTILLAS[plant_sel]}. Adaptá todos los campos con info realista."
            with st.spinner("Personalizando..."):
                try:
                    r = client.chat.completions.create(model="gpt-4o-mini",
                        messages=[{"role":"system","content":"Experto en marketing LATAM. Adaptás plantillas de forma concreta."},
                                  {"role":"user","content":prompt_p}], max_tokens=600)
                    resp_p = r.choices[0].message.content
                    st.markdown(f'<div class="card" style="border-color:rgba(34,197,94,.4);white-space:pre-wrap">{resp_p}</div>', unsafe_allow_html=True)
                    st.code(resp_p, language=None)
                    st.download_button("⬇️ Descargar personalizada", data=resp_p, file_name="plantilla_personalizada.txt", mime="text/plain", key="pl3_dl2")
                    sumar_xp(10)
                except Exception as e: st.error(f"Error: {e}")

    # ── MARCA PERSONAL ──
    if herr_sel == "Marca personal":
        st.markdown("### 🎨 Creador de marca personal")
        st.caption("La IA te ayuda a crear tu identidad: nombre, bio, colores y estilo para Instagram.")
        c1m, c2m = st.columns(2)
        with c1m:
            marca_rubro = st.text_input("¿Qué vendés o a qué te dedicás?", placeholder="Ej: vendo ropa de mujer, soy fotógrafo", key="mp3_rubro")
            marca_publico = st.text_input("¿A quién le vendés?", placeholder="Ej: mujeres jóvenes, empresas pequeñas", key="mp3_pub")
        with c2m:
            marca_estilo = st.selectbox("Estilo de tu marca:", ["Moderno y minimalista","Divertido y colorido","Elegante y premium","Cercano y familiar","Joven y urbano"], key="mp3_estilo")
            marca_ciudad = st.text_input("¿De dónde sos?", placeholder="Ej: Buenos Aires, Córdoba", key="mp3_ciudad")
        if st.button("🎨 Crear mi marca", key="mp3_btn") and marca_rubro.strip():
            prompt_m = f"Creá una identidad de marca completa. Rubro: {marca_rubro}. Público: {marca_publico}. Estilo: {marca_estilo}. Ciudad: {marca_ciudad}. Dame: 5 nombres creativos, bio para Instagram (español e inglés), 3 colores con códigos hex, estilo visual, 10 hashtags en español + 5 en inglés, frase de marca, tono de comunicación."
            with st.spinner("🎨 Creando tu marca..."):
                try:
                    r = client.chat.completions.create(model="gpt-4o",
                        messages=[{"role":"system","content":"Experto en branding y marketing digital para LATAM. Creás identidades de marca modernas y auténticas."},
                                  {"role":"user","content":prompt_m}],
                        temperature=0.9, max_tokens=1200)
                    resp_m = r.choices[0].message.content
                    st.markdown(f'<div class="card" style="border-color:rgba(168,85,247,.4);white-space:pre-wrap;line-height:1.7">{resp_m}</div>', unsafe_allow_html=True)
                    st.download_button("⬇️ Descargar mi marca", data=resp_m, file_name="mi_marca.txt", mime="text/plain", key="mp3_dl")
                    sumar_xp(15)
                    guardar_usuario(st.session_state.user_data)
                except Exception as e: st.error(f"Error: {e}")

    # ── FINANZAS PERSONALES ──
    if herr_sel == "Finanzas":
        st.markdown("### 💰 Finanzas personales con IA")
        st.caption("Controlá tu plata, armá tu presupuesto y tomá mejores decisiones financieras.")
        fin_opcion = st.radio("¿Qué querés hacer?",
            ["Armar mi presupuesto", "Simulador de decisiones", "Calculadora de ahorro", "¿Cuánto necesito ganar?"],
            key="fin3_opcion", horizontal=True)

        if fin_opcion == "Armar mi presupuesto":
            fin_ingreso = st.number_input("💵 Ingreso mensual ($):", min_value=0, step=1000, key="fin3_ing")
            c1f, c2f = st.columns(2)
            with c1f:
                fin_alquiler = st.number_input("🏠 Alquiler:", min_value=0, step=1000, key="fin3_alq")
                fin_comida = st.number_input("🍕 Comida:", min_value=0, step=1000, key="fin3_com")
                fin_transporte = st.number_input("🚌 Transporte:", min_value=0, step=1000, key="fin3_trans")
            with c2f:
                fin_servicios = st.number_input("💡 Servicios:", min_value=0, step=1000, key="fin3_serv")
                fin_entretenimiento = st.number_input("🎬 Entretenimiento:", min_value=0, step=1000, key="fin3_ent")
                fin_otros = st.number_input("📦 Otros:", min_value=0, step=1000, key="fin3_otros")
            if st.button("📊 Analizar mis finanzas", key="fin3_btn"):
                total = fin_alquiler+fin_comida+fin_transporte+fin_servicios+fin_entretenimiento+fin_otros
                saldo = fin_ingreso - total
                pct = (saldo/fin_ingreso*100) if fin_ingreso > 0 else 0
                r1,r2,r3 = st.columns(3)
                with r1: st.metric("💵 Ingresos", f"${fin_ingreso:,.0f}")
                with r2: st.metric("💸 Gastos", f"${total:,.0f}")
                with r3: st.metric("💰 Saldo", f"${saldo:,.0f}", f"{pct:.1f}% ahorro")
                if saldo < 0: st.error(f"⚠️ Gastás ${abs(saldo):,.0f} más de lo que ganás.")
                elif pct < 10: st.warning("⚠️ Tu ahorro es bajo. Lo ideal es el 20%.")
                else: st.success(f"✅ Estás ahorrando {pct:.1f}% de tus ingresos.")
                prompt_fin = f"Ingresos: ${fin_ingreso}. Gastos: alquiler ${fin_alquiler}, comida ${fin_comida}, transporte ${fin_transporte}, servicios ${fin_servicios}, entretenimiento ${fin_entretenimiento}, otros ${fin_otros}. Saldo: ${saldo}. Dame diagnóstico, 3 gastos donde recortar y cómo llegar al 20% de ahorro."
                with st.spinner("Analizando..."):
                    try:
                        r = client.chat.completions.create(model="gpt-4o-mini",
                            messages=[{"role":"system","content":"Asesor financiero personal para Argentina. Consejos prácticos y directos."},
                                      {"role":"user","content":prompt_fin}], max_tokens=500)
                        st.markdown(f'<div class="card" style="border-color:rgba(34,197,94,.4)">{r.choices[0].message.content}</div>', unsafe_allow_html=True)
                    except Exception as e: st.error(f"Error: {e}")

        elif fin_opcion == "Simulador de decisiones":
            dilema = st.text_area("¿Qué decisión tenés que tomar?",
                placeholder="Ej: ¿Me conviene comprar un auto de $500.000 en cuotas o invertir en mi negocio?", height=100, key="fin3_dilema")
            ctx = st.text_input("Tu situación actual (opcional):", placeholder="Ej: gano $150.000/mes, tengo $80.000 ahorrados", key="fin3_ctx")
            if st.button("🤔 Analizar decisión", key="fin3_btn_dil") and dilema.strip():
                prompt_d = f"Analizá esta decisión: {dilema}. Situación: {ctx or 'no especificada'}. Dame: pros y contras de cada opción, qué pasa en 3/6/12 meses, tu recomendación clara y una acción concreta para HOY."
                with st.spinner("Analizando..."):
                    try:
                        r = client.chat.completions.create(model="gpt-4o",
                            messages=[{"role":"system","content":"Asesor financiero experto para Argentina. Análisis claros y honestos."},
                                      {"role":"user","content":prompt_d}], max_tokens=700)
                        st.markdown(f'<div class="card" style="border-color:rgba(250,204,21,.4)">{r.choices[0].message.content}</div>', unsafe_allow_html=True)
                        sumar_xp(10)
                    except Exception as e: st.error(f"Error: {e}")

        elif fin_opcion == "Calculadora de ahorro":
            meta_nom = st.text_input("Meta de ahorro:", placeholder="Ej: viaje, auto, negocio propio", key="fin3_meta")
            c1a, c2a = st.columns(2)
            with c1a: meta_mont = st.number_input("¿Cuánto necesitás? ($):", min_value=0, step=1000, key="fin3_mont")
            with c2a: aho_mens = st.number_input("¿Cuánto ahorrás por mes? ($):", min_value=0, step=1000, key="fin3_aho")
            if st.button("💸 Calcular", key="fin3_btn_aho") and meta_mont > 0 and aho_mens > 0:
                meses = meta_mont / aho_mens
                st.success(f"Para ahorrar ${meta_mont:,.0f} ahorrando ${aho_mens:,.0f}/mes necesitás **{meses:.0f} meses** ({meses/12:.1f} años).")
                if meses > 24: st.info(f"Para lograrlo en 1 año necesitarías ${meta_mont/12:,.0f}/mes.")

        elif fin_opcion == "¿Cuánto necesito ganar?":
            c1g, c2g = st.columns(2)
            with c1g:
                g_alq = st.number_input("🏠 Alquiler:", min_value=0, step=1000, key="fin3_galq")
                g_com = st.number_input("🍕 Comida:", min_value=0, step=1000, key="fin3_gcom")
                g_trans = st.number_input("🚌 Transporte:", min_value=0, step=1000, key="fin3_gtrans")
            with c2g:
                g_serv = st.number_input("💡 Servicios:", min_value=0, step=1000, key="fin3_gserv")
                g_ocio = st.number_input("🎬 Ocio:", min_value=0, step=1000, key="fin3_gocio")
                g_aho = st.number_input("💰 Ahorro deseado:", min_value=0, step=1000, key="fin3_gaho")
            if st.button("📈 Calcular", key="fin3_btn_gan"):
                total = g_alq+g_com+g_trans+g_serv+g_ocio+g_aho
                st.success(f"**Necesitás ganar al menos ${total:,.0f}/mes**")
                st.info(f"Con 30% de margen de seguridad: **${total*1.3:,.0f}/mes**")
                st.caption(f"Eso es ${total/22:,.0f} por día hábil.")

PLANTILLAS = {
    "📞 Guión de venta por WhatsApp": """Hola [Nombre]! 👋

Vi que podría interesarte [producto/servicio].

Te cuento en 3 líneas:
✅ [Beneficio 1]
✅ [Beneficio 2]  
✅ [Beneficio 3]

Precio: [precio] — y si querés te hago una oferta especial esta semana.

¿Te mando más info o preferís que te llame?""",

    "💼 Pitch de ventas de 60 segundos": """Hola, soy [nombre] de [empresa/negocio].

Nos especializamos en ayudar a [tipo de cliente] a [resultado que logran].

Lo que nos diferencia es [tu diferencial único].

Trabajamos con clientes como [ejemplo o tipo de cliente] y logramos [resultado concreto].

Me gustaría saber si esto podría ser útil para vos. ¿Tenés 10 minutos esta semana para charlar?""",

    "📄 CV básico en inglés": """FULL NAME
Email: | Phone: | LinkedIn: | City, Country

PROFESSIONAL SUMMARY
[2-3 sentences describing who you are and what you offer professionally]

WORK EXPERIENCE
[Job Title] | [Company] | [Dates]
• [Achievement or responsibility 1]
• [Achievement or responsibility 2]
• [Achievement or responsibility 3]

EDUCATION
[Degree/Course] | [Institution] | [Year]

SKILLS
Languages: Spanish (native), English (intermediate)
Technical: [list your skills]
Soft skills: [communication, teamwork, etc.]

LANGUAGES
Spanish: Native | English: [level]""",

    "📊 Plan de negocio simple": """PLAN DE NEGOCIO — [Nombre del negocio]

1. QUÉ VENDO
Producto/Servicio: [descripción]
Precio de venta: $[precio]
Costo de producción: $[costo]
Ganancia por unidad: $[ganancia]

2. A QUIÉN LE VENDO
Cliente ideal: [descripción]
Edad: | Ubicación: | Problema que resuelvo:

3. CÓMO LO VENDO
Canales: WhatsApp / Instagram / Local / Mercado Libre
Estrategia: [cómo vas a conseguir clientes]

4. NÚMEROS DEL MES
Meta de ventas: [X] unidades
Ingresos esperados: $[monto]
Costos fijos: $[monto]
Ganancia esperada: $[monto]

5. PRÓXIMOS 3 PASOS
1. [Acción concreta]
2. [Acción concreta]
3. [Acción concreta]""",

    "📱 Bio para Instagram": """[NOMBRE DEL NEGOCIO] ✨
[Qué hacés en 1 línea]
📍 [Ciudad] | 🚚 Envíos a todo el país
💬 Escribinos por DM o WhatsApp
👇 Ver catálogo / Ver precios""",

    "📧 Email a proveedor": """Asunto: Consulta de precios — [tu nombre/empresa]

Estimado/a equipo de [Proveedor],

Mi nombre es [nombre] y represento a [tu negocio/nombre].

Estoy interesado/a en adquirir los siguientes productos:
- [Producto 1]: [cantidad aproximada]
- [Producto 2]: [cantidad aproximada]

¿Podrían enviarme su lista de precios actualizada y condiciones de pago?

Quedo a la espera de su respuesta.

Saludos,
[Nombre]
[Teléfono]
[Email]""",
}

