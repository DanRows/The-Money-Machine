import streamlit as st
import asyncio
from src.core.engine_manager import AIEngineManager
from src.engines.openai_engine import OpenAIEngine
from src.engines.anthropic_engine import AnthropicEngine
from src.workflows.content.content_workflow import ContentWorkflow

class OrquestratorDashboard:
    def __init__(self):
        self.engine_manager = AIEngineManager()
        self._initialize_engines()
        
    def _initialize_engines(self):
        if 'engines_initialized' not in st.session_state:
            # Inicializar motores de IA
            openai_engine = OpenAIEngine(
                api_key=st.secrets["OPENAI_API_KEY"],
                model="gpt-4"
            )
            
            anthropic_engine = AnthropicEngine(
                api_key=st.secrets["ANTHROPIC_API_KEY"],
                model="claude-2"
            )
            
            self.engine_manager.register_engine("openai", openai_engine)
            self.engine_manager.register_engine("anthropic", anthropic_engine)
            
            st.session_state.engines_initialized = True
            st.session_state.engine_manager = self.engine_manager
        else:
            self.engine_manager = st.session_state.engine_manager

    def render_dashboard(self):
        st.title("The Money Machine - Panel de Control")
        
        # Sección de configuración
        with st.expander("Configuración de Workflow", expanded=False):
            st.subheader("Parámetros del Workflow")
            workflow_type = st.selectbox(
                "Tipo de Workflow",
                ["Generación de Contenido", "Trading", "Dropshipping"]
            )
            
            if workflow_type == "Generación de Contenido":
                topic = st.text_input("Tema del contenido", "Innovación en IA")
                platforms = st.multiselect(
                    "Plataformas objetivo",
                    ["Twitter", "LinkedIn", "Medium", "Instagram"],
                    ["Twitter", "LinkedIn"]
                )
                tone = st.select_slider(
                    "Tono del contenido",
                    options=["Formal", "Neutral", "Casual"]
                )
        
        # Estado de los motores
        st.subheader("Estado de los Motores de IA")
        cols = st.columns(len(self.engine_manager.engines))
        
        for idx, (name, engine) in enumerate(self.engine_manager.engines.items()):
            with cols[idx]:
                st.markdown(f"**{name.upper()}**")
                metrics = engine.get_usage_report()
                st.metric("Tokens Usados", metrics['total_tokens'])
                st.metric("Costo Total", f"${metrics['total_cost']:.2f}")
        
        # Botón de ejecución
        if st.button("Ejecutar Workflow"):
            if workflow_type == "Generación de Contenido":
                workflow = ContentWorkflow(
                    engine_manager=self.engine_manager,
                    config={
                        "topic": topic,
                        "platforms": platforms,
                        "tone": tone
                    }
                )
                
                st.info("Iniciando workflow de contenido...")
                
                try:
                    # Ejecutar workflow
                    result = asyncio.run(workflow.execute())
                    
                    # Mostrar resultados
                    st.success("Workflow completado exitosamente")
                    
                    with st.expander("Contenido Generado", expanded=True):
                        st.write(result['content'])
                        
                    with st.expander("Métricas de Ejecución"):
                        st.json(result['metrics'])
                        
                except Exception as e:
                    st.error(f"Error en la ejecución del workflow: {str(e)}")

def main():
    dashboard = OrquestratorDashboard()
    dashboard.render_dashboard()

if __name__ == "__main__":
    main() 