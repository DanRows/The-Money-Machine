import streamlit as st
from src.interfaces.streamlit.main_interface import MainInterface
from src.utils.initialization import initialize_app

def main():
    try:
        # Inicializar la aplicación
        app_context = initialize_app()
        
        if not app_context.get('initialized', False):
            st.error(f"Error al inicializar la aplicación: {app_context.get('error', 'Error desconocido')}")
            return
        
        # Configurar la página
        st.set_page_config(
            page_title="The Money Machine",
            page_icon="💰",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Cargar y ejecutar la interfaz principal
        interface = MainInterface(app_context)
        interface.run()
        
    except Exception as e:
        st.error(f"Error en la aplicación: {str(e)}")

if __name__ == "__main__":
    main() 