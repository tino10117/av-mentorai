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
[data-testid="stChatInput"] textarea{background-color:#0f172a!important;color:#f8fafc!important;border:1px solid rgba(250,204,21,.35)!important;border-radius:14px!important;}
[data-testid="stExpander"]{background:rgba(15,23,42,.88)!important;border:1px solid rgba(250,204,21,.25)!important;border-radius:16px!important;}
@media(max-width:768px){.av-logo{font-size:32px;}.chat-text{font-size:14px;}.block-container{padding-left:.8rem;padding-right:.8rem;}.metric-chip .metric-value{font-size:14px;}}
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
        st.markdown(f'<div class="chat-user"><div class="chat-name">Vos</div><div class="chat-text">{content}</div></div>',unsafe_allow_html=True)
    elif tipo=="english":
        st.markdown(f'<div class="chat-english"><div class="chat-name-english">🎓 Alex — Profesor de Inglés</div><div class="chat-text">{content}</div></div>',unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-ai"><div class="chat-name-ai">⚡ AV MentorAI</div><div class="chat-text">{content}</div></div>',unsafe_allow_html=True)

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
    st.markdown(f'<div class="hero-card"><div class="av-logo">{APP_NAME}</div><div class="av-subtitle">{APP_TAGLINE}</div><p class="small-text">Mentor de negocios + Inglés desde cero + Roleplay + Diario. Todo en uno.</p><p class="small-text"><b>{APP_VERSION}</b></p></div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: st.markdown('<div class="card"><h3>🧠 Mentor de negocios</h3><p class="small-text">Consejos según tu objetivo y nivel.</p></div>',unsafe_allow_html=True)
    with c2: st.markdown('<div class="card"><h3>📚 Inglés completo</h3><p class="small-text">Lecciones, quiz, roleplay, diario y certificado.</p></div>',unsafe_allow_html=True)
    with c3: st.markdown('<div class="card"><h3>🔥 Gamificación</h3><p class="small-text">XP, rachas, niveles y desafíos diarios.</p></div>',unsafe_allow_html=True)
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
st.markdown(f"""<div class="metrics-row">
  <div class="metric-chip"><p class="metric-label">👤 Usuario</p><p class="metric-value">{user['nombre']}</p></div>
  <div class="metric-chip"><p class="metric-label">⭐ XP</p><p class="metric-value">{user['xp']}</p></div>
  <div class="metric-chip"><p class="metric-label">🔥 Racha</p><p class="metric-value">{plural_dias(user['racha'])}</p></div>
  <div class="metric-chip"><p class="metric-label">📈 Nivel</p><p class="metric-value">{calcular_nivel(user['xp']).split(' - ')[0]}</p></div>
  <div class="metric-chip"><p class="metric-label">📚 Inglés</p><p class="metric-value">{loks} lecc.</p></div>
  <div class="metric-chip"><p class="metric-label">📓 Diario</p><p class="metric-value">{diary_count} entr.</p></div>
  <div class="metric-chip"><p class="metric-label">💎 Plan</p><p class="metric-value">{user['plan']}</p></div>
</div>""",unsafe_allow_html=True)
st.progress(progreso_nivel(user["xp"]))
st.caption(f"{calcular_nivel(user['xp'])} — Progreso al siguiente nivel")

# Configuración
with st.expander("⚙️ Configuración y perfil",expanded=False):
    ca,cb=st.columns(2)
    with ca:
        st.markdown("**🔧 Modo del mentor**")
        st.session_state.modo=st.selectbox("Modo:",["Mentor de Negocios","Entrenador de Ventas","Marketing LATAM","Disciplina y Hábitos","Ideas de Negocio","Simulación con Cliente Difícil","Planificador de Objetivos","Modo Empresario Exigente","Modo Mentor Millonario","Especialista Supermercados","Especialista E-commerce","Especialista Reventa","Especialista Restaurante","Especialista Inmobiliaria"],label_visibility="collapsed")
        st.markdown("**🧠 Memoria**")
        user["nombre"]=st.text_input("Nombre:",value=user["nombre"])
        user["objetivo"]=st.text_area("Objetivo:",value=user["objetivo"])
        user["negocio"]=st.text_input("Negocio:",value=user["negocio"])
        user["tipo_negocio"]=st.text_input("Tipo:",value=user["tipo_negocio"])
    with cb:
        st.markdown("**📊 Panel empresario**")
        user["meta_mensual"]=st.text_input("Meta mensual:",value=user["meta_mensual"])
        user["ingresos_objetivo"]=st.number_input("Ingresos objetivo ($):",value=int(user["ingresos_objetivo"]),min_value=0)
        user["habito_clave"]=st.text_input("Hábito clave:",value=user["habito_clave"])
        st.markdown("**⚙️ Acciones**")
        if st.button("💾 Guardar"): guardar_usuario(user); st.success("Guardado.")
        if st.button("🧹 Borrar conversación"): st.session_state.confirmar_borrar=True
        if st.session_state.get("confirmar_borrar",False):
            st.warning("¿Seguro? Se borra todo el historial.")
            cs,cn=st.columns(2)
            with cs:
                if st.button("✅ Sí"): user["messages"]=[]; guardar_usuario(user); st.session_state.confirmar_borrar=False; st.rerun()
            with cn:
                if st.button("❌ No"): st.session_state.confirmar_borrar=False; st.rerun()
        if st.button("🔁 Rehacer onboarding"): user["onboarding_completo"]=False; guardar_usuario(user); st.rerun()
        if st.button("🚪 Cerrar sesión"): guardar_usuario(user); st.session_state.logged_in=False; st.rerun()

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab_mentor,tab_english,tab_progreso,tab_desafios,tab_premium,tab_ranking,tab_feedback=st.tabs([
    "🧠 Mentor","📚 Aprender Inglés","📈 Progreso","🔥 Desafíos","💎 Premium","🏆 Ranking","💬 Feedback"
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

    c1,c2,c3=st.columns(3); qp=None
    with c1:
        if st.button("💡 Idea de negocio"): qp="Dame una idea de negocio rentable para empezar con pocos recursos."
        if st.button("🎭 Cliente difícil"): qp="Hagamos una simulación. Vos sos un cliente difícil y yo tengo que venderte."
    with c2:
        if st.button("📈 Quiero vender más"): qp="Quiero vender más. Dame un plan práctico para empezar hoy."
        if st.button("🔥 Desafío de hoy"): qp=f"Quiero hacer este desafío: {desafio}. Guiame paso a paso."
    with c3:
        if st.button("📱 Marketing en redes"): qp="Quiero aprender marketing desde cero para vender por redes sociales."
        if st.button("💎 Mentor exigente"): qp="Háblame como mentor exigente y decime qué debería mejorar hoy."

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

    ui=st.chat_input("Escribí tu pregunta al mentor...")
    if vp: ui=vp
    elif qp: ui=qp
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
    sub_tabs=st.tabs(["📖 Lecciones","🎭 Roleplay","📖 Traductor","📓 Diario","🏆 Certificado","💬 Chat con Alex"])

    # ── LECCIONES ──
    with sub_tabs[0]:
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
    with sub_tabs[1]:
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

            rp_input=st.chat_input("Escribí en inglés para el roleplay...")
            if ve_rp: rp_input=ve_rp
            if rp_input: enviar_english(rp_input,modo="roleplay",lista_msgs_key="english_roleplay_messages")

            if st.button("🔄 Cambiar situación"):
                user["english_roleplay_situacion"]=None; user["english_roleplay_messages"]=[]
                guardar_usuario(user); st.rerun()

    # ── TRADUCTOR INTELIGENTE ──
    with sub_tabs[2]:
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
    with sub_tabs[3]:
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
    with sub_tabs[4]:
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
    with sub_tabs[5]:
        st.markdown("### 💬 Chat con Alex, tu profesor de inglés")
        st.caption("Preguntale cualquier duda, pedile ejercicios o practicá conversación.")

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

        e1,e2,e3=st.columns(3); eq=None
        with e1:
            if st.button("🔤 Verbo To Be"): eq="Explicame el verbo To Be desde cero con ejemplos."
            if st.button("✍️ Corregí mi inglés"): eq="Voy a escribir algo en inglés, corregime si hay errores."
        with e2:
            if st.button("💬 Practicar conversación"): eq="Quiero practicar una conversación en inglés. Empezá vos."
            if st.button("📧 Emails en inglés"): eq="Enseñame a escribir un email en inglés con la estructura correcta."
        with e3:
            if st.button("🎯 Dame un ejercicio"): eq="Dame un ejercicio de inglés para mi nivel actual."
            if st.button("🗣️ Frases cotidianas"): eq="Enseñame frases que uso todos los días en inglés."

        audio_eng=st.audio_input("🎤 Grabá y Alex te corrige (opcional)",key="audio_alex")
        ve=None
        if audio_eng:
            with st.spinner("Transcribiendo..."):
                try: ve=transcribir_audio(audio_eng); st.info(f"Transcribí: *{ve}*")
                except: pass

        ei=st.chat_input("Escribile a Alex tu profesor de inglés...")
        if ve: ei=f"Grabé esto en inglés: '{ve}'. ¿Está bien dicho? Corregime si hay errores."
        elif eq: ei=eq
        if ei: enviar_english(ei,modo="chat",lista_msgs_key="english_messages")

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
