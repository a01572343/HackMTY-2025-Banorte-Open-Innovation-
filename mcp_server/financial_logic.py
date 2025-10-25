import pandas as pd

def get_financial_summary(df):
    
    if df.empty:
        return {"error": "No hay datos"}

    # Filtrar por tipo
    ingresos_df = df[df['tipo'] == 'ingreso']
    gastos_df = df[df['tipo'] == 'gasto']

    total_ingresos = ingresos_df['monto'].sum()
    total_gastos = gastos_df['monto'].sum()
    flujo_neto = total_ingresos - total_gastos
    
    # Tasa de ahorro (respecto al ingreso)
    tasa_ahorro = (flujo_neto / total_ingresos) * 100 if total_ingresos > 0 else 0

    # Resumen de gastos por categoría
    gastos_por_categoria = gastos_df.groupby('categoria')['monto'].sum().sort_values(ascending=False)
    
    # Transacciones recientes
    transacciones_recientes = df.sort_values('fecha', ascending=False).head(5).copy()
    transacciones_recientes['fecha'] = transacciones_recientes['fecha'].dt.strftime('%Y-%m-%d')

    summary = {
        "total_ingresos": round(total_ingresos, 2),
        "total_gastos": round(total_gastos, 2),
        "flujo_neto_total": round(flujo_neto, 2),
        "tasa_ahorro_promedio_pct": round(tasa_ahorro, 2),
        "top_gastos_categoria": gastos_por_categoria.to_dict(),
        "conteo_transacciones": df.shape[0],
        "fecha_primera_transaccion": df['fecha'].min().strftime('%Y-%m-%d'),
        "fecha_ultima_transaccion": df['fecha'].max().strftime('%Y-%m-%d'),
        "transacciones_recientes_sample": transacciones_recientes[['fecha', 'descripcion', 'monto', 'tipo']].to_dict('records')
    }
    return summary

def apply_simulation(df, params):
    """
    Aplica cambios simulados a una *copia* del DataFrame.
    
    params: Es el objeto SimulationRequest con los cambios.
    """
    # ¡MUY IMPORTANTE! Copiamos el DF para no alterar el original (GLOBAL_DF)
    df_sim = df.copy()
    
    print(f"Iniciando simulación con params: {params.model_dump_json()}")

    # --- 1. Simular reducción de gastos ---
    # Verifica que ambos parámetros existan
    if params.category_to_reduce and params.reduction_percentage:
        reduction_factor = (1 - (params.reduction_percentage / 100.0))
        
        # Mascara para encontrar las filas correctas
        mask = (df_sim['categoria'] == params.category_to_reduce) & (df_sim['tipo'] == 'gasto')
        
        # Aplicamos el descuento al monto
        df_sim.loc[mask, 'monto'] = df_sim.loc[mask, 'monto'] * reduction_factor
        
        print(f"Simulación: Reduciendo '{params.category_to_reduce}' en {params.reduction_percentage}%")

    # --- 2. Simular aumento de ingresos ---
    # Verifica que ambos parámetros existan
    if params.income_to_increase and params.increase_amount:
        # Mascara para encontrar la 'descripcion' (es más específico que 'categoria')
        mask = (df_sim['descripcion'] == params.income_to_increase) & (df_sim['tipo'] == 'ingreso')
        
        # Asumimos que el aumento es por CADA transacción de ese tipo
        df_sim.loc[mask, 'monto'] = df_sim.loc[mask, 'monto'] + params.increase_amount
        
        print(f"Simulación: Aumentando '{params.income_to_increase}' en ${params.increase_amount}")

    return df_sim