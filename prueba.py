import google.generativeai as genai

# --- PEGA TU CLAVE AQUÍ CON CUIDADO ---
TU_CLAVE = "AIzaSyAbGJuVdE0Fks29IC1fNIsVC1woZ-41cNM"
# --------------------------------------

print(f"1. Probando clave que empieza con: {TU_CLAVE[:5]}...")

genai.configure(api_key=TU_CLAVE)

print("2. Intentando conectar con Google...")

try:
    # Intentamos listar modelos. Si esto falla, la clave está mal o bloqueada.
    modelos = list(genai.list_models())
    print("✅ ¡ÉXITO! La clave funciona correctamente.")
    print(f"   Se encontraron {len(modelos)} modelos disponibles.")
    print("   El primero es:", modelos[0].name)
except Exception as e:
    print("\n❌ FALLÓ LA CONEXIÓN.")
    print("   El error exacto es:")
    print(e)