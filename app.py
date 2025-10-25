import streamlit as st
import requests
import plotly.express as px
import pandas as pd

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Aliado financiero Banorte",
    page_icon="🤖",
    layout="wide"
)

# URL de nuestro Servidor MCP
MCP_API_URL = "https://mi-mcp-server.onrender.com/"

# --- Funciones para llamar a la API ---

def get_api_summary():
    """Obtiene el resumen financiero del servidor MCP."""
    try:
        response = requests.get(f"{MCP_API_URL}/api/v1/summary")
        response.raise_for_status() # Lanza error si la API falla
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con el Servidor MCP: {e}")
        return None

def ask_api_cfo(question):
    """Envía una pregunta al asistente de IA en el servidor MCP."""
    try:
        response = requests.post(f"{MCP_API_URL}/api/v1/ask", json={"question": question})
        response.raise_for_status()
        return response.json()["ai_answer"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error al contactar al Asistente: {e}")
        return "Lo siento, no puedo responder en este momento."

def get_api_all_transactions():
    """Obtiene TODAS las transacciones del servidor MCP para gráficas."""
    try:
        response = requests.get(f"{MCP_API_URL}/api/v1/all_transactions")
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar datos de la línea de tiempo: {e}")
        return None

def post_api_simulation(params):
    """Envía parámetros de simulación al servidor MCP."""
    try:
        # params será un dict, ej: {"category_to_reduce": "Restaurantes", ...}
        response = requests.post(f"{MCP_API_URL}/api/v1/simulate", json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al contactar al Simulador: {e}")
        return None

# --- Carga de Datos ---
# Obtenemos los datos una sola vez
summary_data = get_api_summary()

# --- Creación de la Interfaz ---

# Custom CSS for banner (keep your existing CSS)
st.markdown("""
<style>
    
    
    .logo-placeholder img {
        max-width: 100%;
        height: auto;
        margin: auto;  /* This centers the image inside the container */
    }
            
    .banner-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .banner-subtitle {
        color: #e0e7ff;
        font-size: 1.3rem;
        margin-top: 1rem;
        font-weight: 300;
    }
</style>
""", unsafe_allow_html=True)

# BANNER SECTION
st.markdown("""
<div class="banner-container">
    <div class="logo-placeholder">""", 
    unsafe_allow_html=True
)

# Load and display image
try:
    st.image("assets/Banorte_Logo.png", width=180)
except:
    st.error("Error loading image. Make sure 'Banorte_Logo.png' exists in the assets folder.")
    
st.markdown("""
    </div>
    <h1 class="banner-title">Banorte</h1>
    <p class="banner-subtitle">Soluciones Financieras Inteligentes</p>
</div>
""", unsafe_allow_html=True)

st.title("Aliado financiero Banorte - 🤖")
st.caption("Una herramienta inteligente para tus finanzas personales.")

if summary_data:
    # Usamos pestañas para organizar
    tab_dashboard, tab_asistente, tab_simulacion = st.tabs([
        "Dashboard (Mi Situación)", 
        "Aliado financiero  Banorte", 
        "Simulador de Decisiones"
    ])

    

    # --- Pestaña 1: Dashboard ---
    with tab_dashboard:
        
        #Tabs de la primer pestaña
        tab_AnalisisGeneral, tab_LineaDelTiempo = st.tabs([
            "Análisis General",
            "Línea del Tiempo"
        ])

        with tab_AnalisisGeneral:
            
            st.header("Análisis de Salud Financiera")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Ingresos", f"${summary_data.get('total_ingresos', 0):,.2f}")
            col2.metric("Total Gastos", f"${summary_data.get('total_gastos', 0):,.2f}")
            col3.metric("Flujo Neto", f"${summary_data.get('flujo_neto_total', 0):,.2f}", 
                        delta_color="off" if summary_data.get('flujo_neto_total', 0) < 0 else "normal")
            
            st.divider()
            
        
            st.subheader("Top Gastos por Categoría")
            if "top_gastos_categoria" in summary_data:
                # Convertir dict a DataFrame para Plotly
                cat_df = pd.DataFrame(
                    summary_data["top_gastos_categoria"].items(), 
                    columns=['Categoria', 'Monto']
                )
                fig = px.pie(cat_df, values='Monto', names='Categoria', 
                            title='Distribución de Gastos')
                st.plotly_chart(fig, use_container_width=True)

        with tab_LineaDelTiempo:
            
            st.subheader("Ganancias y Costos diarios")

            timeline_data = get_api_all_transactions()

            if timeline_data:
                recientes_df = pd.DataFrame(timeline_data)


                recientes_df['fecha'] = pd.to_datetime(recientes_df['fecha'], errors='coerce')
                recientes_df['monto'] = pd.to_numeric(recientes_df['monto'], errors='coerce')
                recientes_df['descripcion'] = recientes_df['descripcion'].astype(str)
                recientes_df['tipo'] = recientes_df['tipo'].astype(str)
                
                st.markdown("**Filtros**")
                desc_options = sorted(recientes_df['descripcion'].dropna().unique().tolist())
                selected_desc = st.multiselect(
                    "Filtrar por descripción (ej: Walmart, Netflix, Farmacia)",
                    options=desc_options,
                    default=desc_options[:3]
                )
                
                tipo_option = st.selectbox("Tipo", options=['both', 'gasto', 'ingreso'], index=0)
                
                # Date range picker with proper default values
                min_date = None
                max_date = None
                if recientes_df['fecha'].notna().any():
                    ts_min = recientes_df['fecha'].min()
                    ts_max = recientes_df['fecha'].max()
                    if pd.notna(ts_min) and pd.notna(ts_max):
                        min_date = ts_min.date()
                        max_date = ts_max.date()
                        
                        # Set default dates within the valid range
                        # Use the last month of data or less if data span is shorter
                        date_span = (max_date - min_date).days
                        default_days = min(30, date_span)
                        default_start = max_date - pd.Timedelta(days=default_days)
                        
                        try:
                            date_range = st.date_input(
                                "Rango de fechas",
                                value=(default_start, max_date),
                                min_value=min_date,
                                max_value=max_date,
                                key="date_range_picker"
                            )
                            
                            # Handle both single date and date range returns
                            if isinstance(date_range, tuple):
                                start_date, end_date = date_range
                            else:
                                start_date = end_date = date_range
                        except Exception as e:
                            st.warning(f"Error al configurar fechas: {str(e)}")
                            start_date = min_date
                            end_date = max_date
                else:
                    start_date, end_date = None, None
                    st.warning("No hay fechas disponibles en los datos")
                
                mask = pd.Series(True, index=recientes_df.index)
                if selected_desc:
                    mask &= recientes_df['descripcion'].isin(selected_desc)
                if tipo_option != 'both':
                    mask &= recientes_df['tipo'] == tipo_option
                if start_date and end_date:
                    # compare using timestamps to match 'fecha' dtype
                    mask &= recientes_df['fecha'].between(pd.to_datetime(start_date), pd.to_datetime(end_date))
                
                plot_df = recientes_df[mask].sort_values('fecha')
                
                if plot_df.empty:
                    st.info("No hay transacciones con los filtros seleccionados.")
                else:
                    # Aggregate data by date and description
                    daily_totals = (plot_df
                        .groupby(['fecha', 'descripcion', 'tipo'])['monto']
                        .sum()
                        .reset_index())
                    
                    # Create scatter plot with aggregated data
                    px_kwargs = {
                        "x": "fecha",
                        "y": "monto",
                        "color": "descripcion",
                        "symbol": "tipo",
                        "title": "Total diario por descripción",
                        "labels": {
                            "fecha": "Fecha", 
                            "monto": "Monto Total ($)",
                            "descripcion": "Descripción",
                            "tipo": "Tipo"
                        },
                        "hover_data": {
                            "fecha": True,
                            "monto": ":.2f",
                            "descripcion": True,
                            "tipo": True
                        }
                    }

                    fig = px.scatter(
                        daily_totals,
                        **px_kwargs
                    )
                    
                    # Customize the plot appearance
                    fig.update_traces(
                        marker=dict(size=12, opacity=0.8),
                        selector=dict(mode='markers')
                    )
                    fig.update_layout(
                        hovermode='closest',
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show aggregated data table
                    st.divider()
                    st.subheader("Totales Diarios")
                    st.dataframe(
                        daily_totals.sort_values(['fecha', 'descripcion']),
                        use_container_width=True
                    )
            else:
                st.info("No hay transacciones recientes.")
            
            st.divider()

            st.subheader("Transacciones Recientes")
            if "transacciones_recientes_sample" in summary_data:
                recientes_df = pd.DataFrame(summary_data["transacciones_recientes_sample"])
                st.dataframe(recientes_df, use_container_width=True)
                
    # --- Pestaña 2: Asistente Conversacional ---
    with tab_asistente:
        st.title("Asistente virtual CFO")
        st.caption("Consulta tus dudas sobre tu estado financiero, de forma sencilla y rapida.")
        
        

        st.write("\n")
        st.write("\n")


        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        # Chat input (stays at bottom automatically)
        if prompt := st.chat_input("Type your message..."):
            # Add user 
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            # Add bot response
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    response = ask_api_cfo(prompt)
                st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

            st.rerun()
            
    

    # --- Pestaña 3: Simulación (Básico) ---
    with tab_simulacion:
        st.header("Simulador de Decisiones")

        with st.form(key="simulation_form"):
            st.subheader("Reducir Gastos")

            # Usamos las categorías reales (de los gastos) como opciones
            # Asumimos que summary_data['top_gastos_categoria'] es un dict
            categorias_gasto = list(summary_data.get("top_gastos_categoria", {}).keys())

            sim_category = st.selectbox(
                "Si reduzco gastos en...", 
                options=[""] + categorias_gasto, # Añadir opción vacía
                index=0,
                help="Elige una categoría de gasto de tus datos."
            )
            sim_percentage = st.slider(
                "...en este porcentaje (%):", 
                0.0, 100.0, 10.0, step=1.0
            )

            st.divider()
            st.subheader("Aumentar Ingresos")

            sim_income_desc = st.text_input(
                "Si mi ingreso por (descripción)...", 
                placeholder="Ej: Nómina mensual",
                help="Escribe la 'descripción' exacta de un ingreso, ej: 'Nómina mensual'"
            )
            sim_income_amount = st.number_input(
                "...aumenta en esta cantidad ($) por transacción:", 
                value=0.0, step=100.0
            )
            
            st.divider()

            submit_button = st.form_submit_button("Simular Impacto")

        # Lógica cuando el usuario presiona el botón
        if submit_button:
            # Construir el JSON para la API
            params_to_send = {
                "category_to_reduce": sim_category if sim_category else None,
                "reduction_percentage": sim_percentage if sim_category else None,
                "income_to_increase": sim_income_desc if sim_income_desc else None,
                "increase_amount": sim_income_amount if sim_income_desc else None
            }

            if not sim_category and not sim_income_desc:
                st.warning("Por favor, rellena al menos una simulación (gasto o ingreso).")
            else:
                with st.spinner("El CFO Virtual está calculando el futuro..."):
                    sim_response = post_api_simulation(params_to_send)

                if sim_response:
                    if "error" in sim_response:
                        st.error(sim_response["error"])
                    else:
                        st.subheader("Análisis del CFO Virtual")
                        st.markdown(sim_response.get("ai_analysis", "No se recibió análisis."))

                        st.divider()
                        st.subheader("Comparación de Escenarios")

                        original_neto = sim_response.get("original_summary", {}).get("flujo_neto_total", 0)
                        sim_neto = sim_response.get("simulated_summary", {}).get("flujo_neto_total", 0)

                        # Métrica de impacto
                        st.metric(
                            "Flujo Neto Simulado", 
                            f"${sim_neto:,.2f}", 
                            delta=f"{sim_neto - original_neto:,.2f} vs. Real"
                        )

                        with st.expander("Ver detalles completos (JSON)"):
                            st.json(sim_response)

else:
    st.error("No se pudo cargar la información financiera. Asegúrate de que el 'Servidor MCP' esté corriendo.")