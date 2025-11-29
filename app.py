import streamlit as st
import google.generativeai as genai
import datetime
import time
import json

# ==============================================================================
# 1. CONFIGURACIÓN Y CREDENCIALES
# ==============================================================================
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# ==============================================================================
# 2. MOTOR DE IA CON SISTEMA ANTI-CAÍDAS (Estabilidad)
# ==============================================================================

model = None
modelos_prioritarios = [
    "gemini-2.5-flash",        
    "gemini-2.5-flash-latest", 
    "gemini-pro"               
]

for nombre in modelos_prioritarios:
    try:
        model = genai.GenerativeModel(nombre)
        break 
    except:
        continue

if model is None:
    st.error("Error crítico: No se pudo conectar con los servidores de Google AI. Verifica tu conexión.")
    st.stop()

st.set_page_config(page_title="BiblioBot UCB", page_icon="🎓", layout="centered")

# ==============================================================================
# 3. BASE DE DATOS LOCAL (CATÁLOGO FÍSICO SIMULADO - 10 ÍTEMS)
# ==============================================================================

db_items = [
 
    {
        "id": "101",
        "tipo": "libro",
        "titulo": "Bioreactors: Design and Operation",
        "autor": "Mandenius, Carl-Fredrik",
        "editorial": "Wiley-VCH",
        "anio": "2016",
        "isbn": "978-3527337682",
        "signatura": "660.63 B518b",
        "estado": "Disponible",
        "img_url": "https://m.media-amazon.com/images/I/51+t-F-gQIL._SX342_SY445_.jpg",
        "keywords": ["bioreactors", "biotecnologia", "ingenieria"]
    },
    {
        "id": "102",
        "tipo": "libro",
        "titulo": "Metodología de la Investigación",
        "autor": "Hernández Sampieri, Roberto",
        "editorial": "McGraw-Hill",
        "anio": "2018",
        "isbn": "978-1456260965",
        "signatura": "001.42 H557m",
        "estado": "Disponible",
        "img_url": "https://m.media-amazon.com/images/I/51i6X3M-t+L._SX342_SY445_.jpg",
        "keywords": ["sampieri", "tesis", "metodologia", "investigacion"]
    },
    {
        "id": "103",
        "tipo": "libro",
        "titulo": "Clean Code",
        "autor": "Martin, Robert C.",
        "editorial": "Prentice Hall",
        "anio": "2008",
        "isbn": "978-0132350884",
        "signatura": "005.1 M379c",
        "estado": "Disponible",
        "img_url": "https://m.media-amazon.com/images/I/41xShlnTZTL._SX342_SY445_.jpg",
        "keywords": ["clean", "codigo", "programacion", "software"]
    },
    {
        "id": "104",
        "tipo": "libro",
        "titulo": "Tratado de Fisiología Médica",
        "autor": "Guyton y Hall",
        "editorial": "Elsevier",
        "anio": "2021",
        "isbn": "978-8491138222",
        "signatura": "612 G98",
        "estado": "Disponible",
        "img_url": "https://m.media-amazon.com/images/I/51+F+8A7pJL._SX342_SY445_.jpg",
        "keywords": ["fisiologia", "medicina", "anatomia", "salud"]
    },
    {
        "id": "105",
        "tipo": "libro",
        "titulo": "Constitución Política del Estado",
        "autor": "Gaceta Oficial",
        "editorial": "Gaceta",
        "anio": "2009",
        "isbn": "N/A",
        "signatura": "342.84 B69c",
        "estado": "Disponible",
        "img_url": "https://m.media-amazon.com/images/I/51y8S2w+G7L._SX342_SY445_.jpg",
        "keywords": ["constitucion", "derecho", "leyes", "politica"]
    },
    {
        "id": "901",
        "tipo": "juego",
        "titulo": "Catan: El Juego",
        "autor": "Teuber, Klaus",
        "editorial": "Devir",
        "anio": "2023",
        "isbn": "N/A",
        "signatura": "LUD-01",
        "estado": "Disponible",
        "img_url": "https://m.media-amazon.com/images/I/81XHjR5+tGL._AC_SX679_.jpg",
        "keywords": ["catan", "juego", "ludoteca", "mesa"]
    },
    {
        "id": "902",
        "tipo": "juego",
        "titulo": "Jenga Clásico",
        "autor": "Hasbro",
        "editorial": "Hasbro",
        "anio": "2015",
        "isbn": "N/A",
        "signatura": "LUD-02",
        "estado": "Disponible",
        "img_url": "https://m.media-amazon.com/images/I/7180qj19orL._AC_SX679_.jpg",
        "keywords": ["jenga", "torre", "ludoteca", "destreza"]
    },

    # --- LIBROS PRESTADOS (3 ÍTEMS) ---
    {
        "id": "201",
        "tipo": "libro",
        "titulo": "Marketing 4.0",
        "autor": "Kotler, Philip",
        "editorial": "Lid Editorial",
        "anio": "2018",
        "isbn": "978-8416894762",
        "signatura": "658.8 K87m",
        "estado": "Prestado",
        "devolucion": "05/12/2026",
        "img_url": "https://m.media-amazon.com/images/I/81+5JK3-uUL._SY466_.jpg",
        "keywords": ["marketing", "kotler", "ventas", "digital"]
    },
    {
        "id": "202", "tipo": "libro", "titulo": "Inteligencia Artificial",
        "autor": "Russell, Stuart",
        "editorial": "Pearson",
        "anio": "2020",
        "isbn": "978-129240",
        "signatura": "006.3 R961i",
        "estado": "Prestado",
        "devolucion": "15/12/2026",
        "img_url": "https://m.media-amazon.com/images/I/51L-2+8+W+L._SX342_SY445_.jpg",
        "keywords": ["inteligencia artificial", "russell", "tecnologia"]
    },
    {
        "id": "903", "tipo": "juego", "titulo": "UNO - Cartas",
        "autor": "Mattel",
        "editorial": "Mattel",
        "anio": "2019",
        "isbn": "N/A",
        "signatura": "LUD-03",
        "estado": "En Uso",
        "devolucion": "1 hora",
        "img_url": "https://m.media-amazon.com/images/I/71wF7M9kXhL._AC_SX679_.jpg",
        "keywords": ["uno", "cartas", "ludoteca"]
    }
]
catalogo_str = json.dumps(db_items, indent=2)

# ==============================================================================
# 4. CEREBRO IA (DATOS REALES + REGLAS DE NEGOCIO + SIMULACIÓN)
# ==============================================================================
fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y")
contexto = f"""
ERES: BiblioBot, el asistente experto oficial de la Biblioteca Central UCB Sede La Paz.
HOY ES: {fecha_hoy}.

--- PARTE 1: INFORMACIÓN INSTITUCIONAL REAL (Fuente: ucb.edu.bo) ---
1.  **HORARIOS DE ATENCIÓN:**
    * Lunes a Viernes: 08:00 a 20:30 (Horario Continuo).
    * Sábados: 09:00 a 12:30.
    * Sala VIP (Piso 3): Lun-Vie 08:30 a 16:30.

2.  **INFRAESTRUCTURA Y SERVICIOS:**
    * **Piso 4:** Sala Virtual (Computadoras), Sala Audiovisual.
    * **Piso 3:** Sala VIP (Sillones) y Terraza.
    * **Piso 2:** Cargadores Solares (Fotovoltaicos) y Salas de estudio.
    * **Planta Baja:** Mostrador de Referencia, Estantería Abierta.
    * **Sótano 1:** Salas grupales.

3.  **CONTACTO:**
    * WhatsApp Oficial (Inscripciones/Consultas): **75851671**.
    * Redes Sociales: **@bibliocato**.

--- PARTE 2: REGLAS DE NEGOCIO Y COBROS ---
1.  **INGRESO GRATUITO (CONVENIO CEUB):**
    * Estudiantes de **UCB**, **UMSA**, **UPEA**, **EMI**, **USFX**, **UMSS**.
    * Respuesta: "Tu ingreso es libre presentando matrícula vigente."

2.  **INGRESO DE PAGO (EXTERNOS/PRIVADAS):**
    * Estudiantes de **Salesiana**, **Univalle**, **UPB**, **Udabol**, **Unifranz**, etc.
    * Tarifa: **Bs 100 Semestrales** (Destaca que equivale a 17 Bs/mes).

--- PARTE 3: PROTOCOLOS TÉCNICOS ---
* **SOPORTE DE LOGIN:** Si el usuario dice "Error de Login" o "No puedo entrar", pídele su matrícula para validación manual.
* **TESIS:** Menciona que tenemos cerca de **14.000 tesis digitalizadas** en el Repositorio.

--- PARTE 4: INSTRUCCIONES DE BÚSQUEDA ---
* Tu catálogo físico prioritario es: {catalogo_str}
* Si piden un libro de esa lista, ofrécelo.
* **SI PIDEN UN LIBRO QUE NO ESTÁ:**
  * Busca en tu conocimiento general el libro REAL (Autor y Título verdaderos).
  * **SIMULA** que está en el "Depósito General".
  * Di si está Disponible o Prestado.
  * ¡No inventes autores falsos! Usa datos bibliográficos reales.

TONO: Profesional, tecnológico, amable y muy informado.
"""

# Función auxiliar para detectar intención de servicio
def detectar_intencion(texto):
    servicios = ["precio", "costo", "horario", "ubicacion", "login", "error", "falla", "hola", "gracias", "ayuda", "convenio", "umsa", "externo", "salesiana", "univalle", "tesis", "wifi"]
    return any(p in texto.lower() for p in servicios)

# ==============================================================================
# 5. INTERFAZ GRÁFICA (FRONTEND)
# ==============================================================================
st.title("📚 BiblioBot UCB")
st.caption("Plan Estratégico 2026 | Convenios CEUB & ISO 9001")

# --- 6. MÓDULO DE LOGIN VIP
if "reserva_activa" not in st.session_state: 
    st.session_state.reserva_activa = None

if st.session_state.reserva_activa:
    item_id = st.session_state.reserva_activa
    try: titulo = next(i['titulo'] for i in db_items if i['id'] == item_id)
    except: titulo = "Material Bibliográfico"
    
    with st.expander(f"🔐 Reservar: {titulo}", expanded=True):
        st.write("Ingresa credenciales para validar permisos:")
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        
        col1, col2 = st.columns([1,3])
        
        if col1.button("Confirmar"):
            # LÓGICA VIP
            if u == '6735384' and p == 'Sindrome12@':
                st.success("✅ **USUARIO VIP VERIFICADO:** Préstamo a Domicilio Autorizado (7 días).")
                st.info("Acceso Total a Colecciones y EBSCO Remoto.")
            elif u and p:
                st.success("✅ **ESTUDIANTE:** Reserva confirmada en sala.")
            else: 
                st.error("Faltan datos.")
            
            time.sleep(3)
            st.session_state.reserva_activa = None
            st.rerun()
            
        if col2.button("Cancelar"):
            st.session_state.reserva_activa = None
            st.rerun()

# --- 7. MÓDULO DE CHAT ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [{"role": "assistant", "content": "¡Hola! Soy BiblioBot. Conozco los horarios, servicios y convenios de la UCB. ¿En qué te ayudo?"}]

for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe aquí (Ej: 'Horarios', 'Soy de la EMI', 'Busco Catan')..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.chat_message("assistant"):
        with st.spinner("Procesando..."):
            try:

                res = model.generate_content(f"{contexto}\nUSUARIO: {prompt}").text
                st.markdown(res)
                st.session_state.mensajes.append({"role": "assistant", "content": res})

 
                if not detecting_intencion(prompt) if 'detecting_intencion' in globals() else detectar_intencion(prompt) == False:
                    # Búsqueda flexible en Base de Datos Local
                    for item in db_items:
                        match_titulo = item['titulo'].lower() in prompt.lower() or item['titulo'].lower() in res.lower()
                        match_keyword = any(k in prompt.lower() for k in item['keywords'])
                        
                        if match_titulo or match_keyword:
                            with st.container(border=True):
                                c1, c2 = st.columns([3,1])
                                c1.markdown(f"📖 **{item['titulo']}**")
                                c1.caption(f"{item['autor']} | {item['editorial']} ({item['anio']})")
                                c1.code(f"Sig: {item['signatura']}")
                                
                                if "Disponible" in item['estado']:
                                    if c2.button("Reservar", key=item['id']):
                                        st.session_state.reserva_activa = item['id']
                                        st.rerun()
                                else: 
                                    c2.error(item['estado'])
                                    c2.caption(f"Vuelve: {item.get('devolucion')}")

            except Exception as e:

                st.error(f"Error técnico: {e}")
