import streamlit as st
from src.core.engine_manager import AIEngineManager
from src.utils.metrics_manager import MetricsManager

def initialize_engine_manager():
    if 'engine_manager' not in st.session_state:
        st.session_state.engine_manager = AIEngineManager()
    return st.session_state.engine_manager

def render_main_dashboard(engine_manager):
    st.set_page_config(
        page_title="The Money Machine",
        page_icon="💰",
        layout="wide"
    )
    
    # Selector de workflow
    workflow_type = st.sidebar.selectbox(
        "Seleccionar Workflow",
        ["Generación de Contenido", "Trading", "Dropshipping", "PYME"]
    )
    
    # Métricas globales
    metrics_manager = MetricsManager.load_metrics('data/metrics.json')
    with st.sidebar.expander("Métricas Globales"):
        metrics_display = metrics_manager.get_metrics_display()
        for metric_name, metric_value in metrics_display.items():
            st.metric(metric_name, metric_value)
    
    try:
        # Renderizar el dashboard correspondiente
        if workflow_type == "Generación de Contenido":
            result = render_content_dashboard(engine_manager)
        elif workflow_type == "Trading":
            result = render_trading_dashboard(engine_manager)
        elif workflow_type == "Dropshipping":
            result = render_dropshipping_dashboard(engine_manager)
        else:  # PYME
            result = render_pyme_dashboard(engine_manager)
        
        # Actualizar métricas si el workflow se ejecutó
        if result and 'metrics' in result:
            metrics_manager.update_metrics(result['metrics'])
            metrics_manager.save_metrics('data/metrics.json')
            
    except Exception as e:
        st.error(f"Error en la ejecución del workflow: {str(e)}")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Desarrollado con ❤️ por The Money Machine Team") 