import google.generativeai as genai
import json
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash') # O el modelo que prefieras

def get_ai_recommendation(user_question, financial_context):

    # Convertimos el contexto de Python a un string JSON legible
    context_str = json.dumps(financial_context, indent=2, ensure_ascii=False)
    
    system_prompt = f"""
    Eres un "CFO Virtual" de Banorte, un asesor financiero experto, 
    amable y profesional. Tu objetivo es ayudar a un usuario a tomar 
    mejores decisiones financieras.
    
    NUNCA inventes información. Basa TODAS tus respuestas en el siguiente 
    contexto financiero del usuario. Si la pregunta no se puede responder 
    con el contexto, responde con información externa a la base de datos,
    sin desviarte mucho del te. Si el contexto es relevante, busca sugerencias
    alineadas con el desarrollo sustentable como opcion, pero recuerda que el
    proposito principal es el apoyo financiero.
    
    Contexto Financiero (Resumen):
    {context_str}
    
    Responde a la siguiente pregunta del usuario. Por default, sé claro, 
    calido, conciso y ofrece recomendaciones accionables. Si el usuario te
    pide que le hables de cierta forma sigue sus ordenes si es coherente.
    """
    
    try:
        # Genera la respuesta
        response = model.generate_content([system_prompt, user_question])
        return response.text
    
    except Exception as e:
        print(f"Error al llamar a la API de Gemini: {e}")
        return "Hubo un error al procesar tu solicitud con el asistente de IA."
    
def get_ai_simulation_analysis(context_real, context_simulado):
    """
    Genera un análisis de IA comparando el escenario real vs. el simulado.
    """
    
    # Convertir los diccionarios de contexto a texto JSON legible
    context_real_str = json.dumps(context_real, indent=2, ensure_ascii=False)
    context_simulado_str = json.dumps(context_simulado, indent=2, ensure_ascii=False)
    
    system_prompt = f"""
    Eres un "CFO Virtual" de Banorte, un asesor financiero experto.
    Tu tarea es analizar el impacto de una simulación financiera para el usuario.
    
    Compara el "Contexto Real" con el "Contexto Simulado" que te proporciono.
    
    Explica claramente qué cambió (ej. "Veo que simulaste reducir tus gastos en 'Restaurantes' en un 20%...") 
    y cuál es el impacto directo en métricas clave como el "flujo_neto_total" 
    y la "tasa_ahorro_promedio_pct".
    
    Termina con una recomendación breve y accionable sobre si esta simulación
    parece ser un buen plan para el usuario. Sé directo y alentador.
    
    --- CONTEXTO REAL ---
    {context_real_str}
    ---------------------
    
    --- CONTEXTO SIMULADO ---
    {context_simulado_str}
    -----------------------
    """
    
    try:
        # Usamos el modelo ya definido (ej. 'gemini-pro')
        response = model.generate_content([system_prompt]) # El prompt ya contiene todo
        return response.text
    except Exception as e:
        print(f"Error al llamar a la API de Gemini para simulación: {e}")
        return "Hubo un error al procesar el análisis de la simulación."