from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import data_loader
import financial_logic
import gemini_client

app = FastAPI(
    title="Servidor MCP Financiero - Reto Banorte",
    description="Analiza datos, ejecuta cálculos y responde con IA."
)

# Cargar datos una vez al iniciar el servidor
try:
    GLOBAL_DF = data_loader.load_user_data()
    GLOBAL_CONTEXT = financial_logic.get_financial_summary(GLOBAL_DF)
except Exception as e:
    print(f"Error crítico al cargar datos: {e}")
    GLOBAL_DF = None
    GLOBAL_CONTEXT = {"error": "No se pudieron cargar los datos iniciales."}

# Modelo de entrada para las preguntas del chat
class ChatRequest(BaseModel):
    question: str

class SimulationRequest(BaseModel):
    category_to_reduce: Optional[str] = None
    reduction_percentage: Optional[float] = None
    income_to_increase: Optional[str] = None
    increase_amount: Optional[float] = None

@app.get("/api/v1/summary")
async def get_summary():
    """
    Endpoint para el dashboard.
    Retorna el resumen financiero completo (cálculos complejos).
    """
    if GLOBAL_CONTEXT is None:
        return {"error": "Los datos no están cargados."}
    return GLOBAL_CONTEXT

@app.post("/api/v1/ask")
async def ask_cfo(request: ChatRequest):
    """
    Endpoint para el asistente conversacional.
    Recibe una pregunta, la combina con el contexto y consulta a Gemini.
    """
    if GLOBAL_CONTEXT is None:
        return {"error": "Los datos no están cargados."}
    
    print(f"Pregunta recibida: {request.question}")
    
    # Aquí se ejecuta el "Model Context Protocol"
    # 1. Contexto: GLOBAL_CONTEXT
    # 2. Modelo: gemini_client
    # 3. Pregunta: request.question
    
    ai_response = gemini_client.get_ai_recommendation(
        user_question=request.question,
        financial_context=GLOBAL_CONTEXT
    )
    
    return {"user_question": request.question, "ai_answer": ai_response}

@app.post("/api/v1/simulate")
async def simulate_scenario(request: SimulationRequest):
    """
    Endpoint para simulación.
    Recalcula el resumen financiero basado en parámetros 
    y pide a Gemini que compare los escenarios.
    """
    if GLOBAL_DF is None or GLOBAL_CONTEXT is None:
        return {"error": "Los datos no están cargados."}
        
    print(f"Simulación recibida: {request.model_dump_json()}")

    try:
        # 1. Aplicar cambios al DataFrame (usando la nueva función)
        df_simulado = financial_logic.apply_simulation(GLOBAL_DF, request)
        
        # 2. Calcular nuevo resumen (re-usando la función existente)
        context_simulado = financial_logic.get_financial_summary(df_simulado)
        
        # 3. Pedir a Gemini que compare (Protocolo de Modelo)
        #    Compara el contexto REAL (GLOBAL_CONTEXT) con el SIMULADO
        ai_analysis = gemini_client.get_ai_simulation_analysis(
            context_real=GLOBAL_CONTEXT,
            context_simulado=context_simulado
        )
        
        # 4. Devolver todo para el frontend
        return {
            "simulation_params": request.model_dump(),
            "original_summary": GLOBAL_CONTEXT,
            "simulated_summary": context_simulado,
            "ai_analysis": ai_analysis
        }
        
    except Exception as e:
        print(f"Error grave durante la simulación: {e}")
        return {"error": f"Ocurrió un error al procesar la simulación: {e}"}
    
@app.get("/api/v1/all_transactions")
async def get_all_transactions():
    """
    Endpoint para el dashboard de línea de tiempo.
    Retorna TODAS las transacciones para las gráficas.
    """
    if GLOBAL_DF is None:
        return {"error": "Los datos no están cargados."}
    
    # Devolvemos todas las transacciones
    all_data = GLOBAL_DF.copy()
    
    # Convertimos fecha a string para que JSON funcione
    # (¡IMPORTANTE! Si no, da error 500)
    all_data['fecha'] = all_data['fecha'].dt.strftime('%Y-%m-%d')
    
    # Usamos .to_dict('records') para que sea un JSON array
    return all_data.to_dict('records')