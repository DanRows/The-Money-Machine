import streamlit as st
import asyncio
from src.workflows.pyme.pyme_workflow import PymeWorkflow

def render_pyme_dashboard(engine_manager):
    st.subheader("Creador de PYMES")
    
    with st.expander("Configuración del Negocio", expanded=True):
        sector = st.selectbox(
            "Sector",
            ["Comercio", "Servicios", "Tecnología", "Manufactura", "Hostelería", "Otro"]
        )
        
        location = st.text_input(
            "Ubicación",
            "Madrid, España"
        )
        
        initial_investment = st.number_input(
            "Inversión Inicial Disponible (€)",
            min_value=1000,
            max_value=1000000,
            value=50000,
            step=1000
        )
        
        business_type = st.radio(
            "Tipo de Negocio",
            ["Nuevo Negocio", "Franquicia", "Adquisición"]
        )
        
        risk_profile = st.select_slider(
            "Perfil de Riesgo",
            options=["Muy Conservador", "Conservador", "Moderado", "Agresivo", "Muy Agresivo"],
            value="Moderado"
        )
    
    # Métricas clave
    st.subheader("Indicadores Clave")
    metrics = {
        "ROI Estimado": "15-20%",
        "Tiempo Break-Even": "12-18 meses",
        "Riesgo": "Moderado",
        "Potencial de Mercado": "Alto"
    }
    
    cols = st.columns(len(metrics))
    for idx, (metric, value) in enumerate(metrics.items()):
        with cols[idx]:
            st.metric(metric, value)
    
    # Botón de ejecución
    if st.button("Generar Plan de Negocio"):
        workflow = PymeWorkflow(
            engine_manager=engine_manager,
            config={
                'sector': sector,
                'location': location,
                'initial_investment': initial_investment,
                'business_type': business_type,
                'risk_profile': risk_profile
            }
        )
        
        with st.spinner("Analizando y generando plan de negocio..."):
            try:
                result = asyncio.run(workflow.execute())
                
                # Mostrar resultados
                st.success("Plan de negocio generado exitosamente")
                
                with st.expander("Análisis de Oportunidad", expanded=True):
                    st.write(result['opportunity_analysis'])
                
                with st.expander("Plan de Negocio"):
                    st.write(result['business_plan'])
                
                with st.expander("Análisis Financiero"):
                    st.write(result['financial_analysis'])
                
                with st.expander("Plan de Implementación"):
                    st.write(result['implementation_plan'])
                
                with st.expander("Plan de Marketing"):
                    st.write(result['marketing_plan'])
                
                with st.expander("Métricas de Ejecución"):
                    st.json(result['metrics'])
                    
            except Exception as e:
                st.error(f"Error en la generación del plan: {str(e)}") 