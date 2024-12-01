import streamlit as st
from frontend.pages.orchestrator_dashboard import OrquestratorDashboard

def main():
    st.set_page_config(
        page_title="The Money Machine",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar
    st.sidebar.title("The Money Machine")
    st.sidebar.markdown("---")
    
    # Menú de navegación
    page = st.sidebar.selectbox(
        "Navegación",
        ["Dashboard", "Configuración", "Logs"]
    )
    
    if page == "Dashboard":
        dashboard = OrquestratorDashboard()
        dashboard.render_dashboard()
    elif page == "Configuración":
        st.title("Configuración")
        st.info("Página en construcción")
    else:
        st.title("Logs")
        st.info("Página en construcción")

if __name__ == "__main__":
    main() 