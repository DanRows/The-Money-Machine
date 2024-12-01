import streamlit as st
from typing import Dict, Any
from dataclasses import dataclass
from src.core.engine_manager import AIEngineManager
from src.utils.metrics_manager import MetricsManager
from src.utils.initialization import initialize_app

@dataclass
class UIConfig:
    """Configuración de la interfaz de usuario"""
    title: str = "The Money Machine"
    icon: str = "💰"
    layout: str = "wide"
    theme: Dict[str, str] = None

class MainInterface:
    """Interfaz principal de la aplicación"""
    
    def __init__(self, app_context: Dict[str, Any]):
        self.app_context = app_context
        self.provider_manager = app_context['provider_manager']
        self.config = app_context['config']
        
        self.ui_config = UIConfig(
            theme={
                "primaryColor": "#FF4B4B",
                "backgroundColor": "#FFFFFF",
                "secondaryBackgroundColor": "#F0F2F6",
                "textColor": "#262730",
                "font": "sans serif"
            }
        )
        self.setup_page()
        self.initialize_session_state()
        
    def setup_page(self):
        """Configura la página principal"""
        st.set_page_config(
            page_title=self.ui_config.title,
            page_icon=self.ui_config.icon,
            layout=self.ui_config.layout,
            initial_sidebar_state="expanded"
        )
        
        # Aplicar estilos personalizados
        self.apply_custom_styles()
    
    def initialize_session_state(self):
        """Inicializa el estado de la sesión"""
        if 'engine_manager' not in st.session_state:
            st.session_state.engine_manager = AIEngineManager(self.load_engine_config())
        
        if 'metrics_manager' not in st.session_state:
            st.session_state.metrics_manager = MetricsManager()
        
        if 'current_workflow' not in st.session_state:
            st.session_state.current_workflow = None
    
    def apply_custom_styles(self):
        """Aplica estilos CSS personalizados"""
        st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .metric-card {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .success-message {
            padding: 1rem;
            border-radius: 5px;
            background-color: #D4EDDA;
            color: #155724;
            margin: 1rem 0;
        }
        
        .error-message {
            padding: 1rem;
            border-radius: 5px;
            background-color: #F8D7DA;
            color: #721C24;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Renderiza la barra lateral"""
        with st.sidebar:
            st.title(self.ui_config.title)
            st.markdown("---")
            
            # Selector de workflow
            workflow_type = st.selectbox(
                "Seleccionar Workflow",
                ["Generación de Contenido", "Trading", "Dropshipping", "PYME"]
            )
            
            # Métricas globales
            with st.expander("Métricas Globales", expanded=True):
                metrics = st.session_state.metrics_manager.get_metrics_display()
                for name, value in metrics.items():
                    st.metric(name, value)
            
            # Configuración
            with st.expander("Configuración", expanded=False):
                self.render_settings()
            
            st.markdown("---")
            st.markdown("Desarrollado con ❤️ por The Money Machine Team")
    
    def render_settings(self):
        """Renderiza la sección de configuración"""
        st.subheader("Configuración General")
        
        # Configuración de motores
        engines_enabled = {
            "OpenAI": st.checkbox("Habilitar OpenAI", value=True),
            "Anthropic": st.checkbox("Habilitar Anthropic", value=True),
            "Google": st.checkbox("Habilitar Google", value=False)
        }
        
        # Estrategia de fallback
        fallback_strategy = st.selectbox(
            "Estrategia de Fallback",
            ["round_robin", "cost_based", "quality_based"]
        )
        
        # Límites de costos
        st.number_input(
            "Límite de Costo Diario ($)",
            min_value=1.0,
            max_value=1000.0,
            value=50.0,
            step=1.0
        )
        
        if st.button("Guardar Configuración"):
            self.save_settings(engines_enabled, fallback_strategy)
            st.success("Configuración guardada exitosamente")
    
    def render_main_content(self, workflow_type: str):
        """Renderiza el contenido principal según el workflow seleccionado"""
        if workflow_type == "Generación de Contenido":
            from src.interfaces.streamlit.pages.content_dashboard import render_content_dashboard
            render_content_dashboard(st.session_state.engine_manager)
        
        elif workflow_type == "Trading":
            from src.interfaces.streamlit.pages.trading_dashboard import render_trading_dashboard
            render_trading_dashboard(st.session_state.engine_manager)
        
        elif workflow_type == "Dropshipping":
            from src.interfaces.streamlit.pages.dropshipping_dashboard import render_dropshipping_dashboard
            render_dropshipping_dashboard(st.session_state.engine_manager)
        
        else:  # PYME
            from src.interfaces.streamlit.pages.pyme_dashboard import render_pyme_dashboard
            render_pyme_dashboard(st.session_state.engine_manager)
    
    def load_engine_config(self) -> Dict[str, Any]:
        """Carga la configuración de los motores"""
        import yaml
        with open('config/engines.yaml', 'r') as f:
            return yaml.safe_load(f)
    
    def save_settings(self, engines_enabled: Dict[str, bool], fallback_strategy: str):
        """Guarda la configuración en el archivo"""
        import yaml
        config = {
            'engines': {
                name.lower(): {'enabled': enabled}
                for name, enabled in engines_enabled.items()
            },
            'fallback_strategy': fallback_strategy
        }
        
        with open('config/settings.yaml', 'w') as f:
            yaml.dump(config, f)
    
    def run(self):
        """Ejecuta la interfaz principal"""
        self.render_sidebar()
        workflow_type = st.session_state.get('workflow_type', "Generación de Contenido")
        self.render_main_content(workflow_type)

def main():
    interface = MainInterface()
    interface.run()

if __name__ == "__main__":
    main() 