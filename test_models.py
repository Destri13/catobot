import google.generativeai as genai
import os

# TU CLAVE DIRECTA (Solo para esta prueba rápida)
GOOGLE_API_KEY = "PEGA_AQUI_TU_API_KEY_AIzaSy..."

genai.configure(api_key=GOOGLE_API_KEY)

print("🔍 Buscando modelos disponibles para tu clave...\n")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ DISPONIBLE: {m.name}")
except Exception as e:
    print(f"❌ ERROR DE CONEXIÓN: {e}")