import streamlit as st
import asyncio
from src.workflows.trading.trading_workflow import TradingWorkflow

def render_trading_dashboard(engine_manager):
    st.subheader("Trading Automatizado")
    
    with st.expander("Configuración de Trading", expanded=True):
        market = st.selectbox(
            "Mercado",
            ["CRYPTO/BTC-USD", "FOREX/EUR-USD", "STOCKS/AAPL", "STOCKS/GOOGL"]
        )
        
        timeframe = st.select_slider(
            "Timeframe",
            options=["1m", "5m", "15m", "1h", "4h", "1d"]
        )
        
        risk_level = st.slider(
            "Nivel de Riesgo",
            min_value=1,
            max_value=10,
            value=5,
            help="1: Muy conservador, 10: Muy agresivo"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            max_positions = st.number_input(
                "Máximo de Posiciones",
                min_value=1,
                max_value=10,
                value=3
            )
        with col2:
            max_risk_per_trade = st.number_input(
                "Riesgo Máximo por Operación (%)",
                min_value=0.1,
                max_value=5.0,
                value=1.0,
                step=0.1
            )
    
    # Estado actual del portfolio
    st.subheader("Estado del Portfolio")
    portfolio_metrics = {
        "Balance Total": "$10,000",
        "P&L Diario": "+$150 (1.5%)",
        "Posiciones Abiertas": "2/3",
        "Riesgo Total": "2.5%"
    }
    
    cols = st.columns(len(portfolio_metrics))
    for idx, (metric, value) in enumerate(portfolio_metrics.items()):
        with cols[idx]:
            st.metric(metric, value)
    
    # Botón de ejecución
    if st.button("Ejecutar Análisis"):
        workflow = TradingWorkflow(
            engine_manager=engine_manager,
            config={
                'market': market,
                'timeframe': timeframe,
                'risk_level': risk_level,
                'max_positions': max_positions,
                'max_risk_per_trade': max_risk_per_trade,
                'current_portfolio': portfolio_metrics
            }
        )
        
        with st.spinner("Analizando mercado..."):
            try:
                result = asyncio.run(workflow.execute())
                
                # Mostrar resultados
                st.success("Análisis completado")
                
                with st.expander("Análisis de Mercado", expanded=True):
                    st.write(result['analysis'])
                
                with st.expander("Señales de Trading"):
                    st.write(result['signals'])
                
                with st.expander("Evaluación de Riesgo"):
                    st.write(result['risk_assessment'])
                
                with st.expander("Decisiones de Trading"):
                    st.write(result['decisions'])
                
                with st.expander("Métricas de Ejecución"):
                    st.json(result['metrics'])
                    
            except Exception as e:
                st.error(f"Error en el análisis: {str(e)}") 