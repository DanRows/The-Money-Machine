import streamlit as st
import asyncio
from src.workflows.content.content_workflow import ContentWorkflow

def render_content_dashboard(engine_manager):
    st.subheader("Generador de Contenido Automatizado")
    
    with st.expander("Configuración de Contenido", expanded=True):
        # Configuración básica
        topic = st.text_input(
            "Tema del contenido",
            placeholder="Ej: Inteligencia Artificial en Negocios"
        )
        
        content_type = st.selectbox(
            "Tipo de Contenido",
            [
                "Artículo de Blog",
                "Post de Redes Sociales",
                "Newsletter",
                "Guía Técnica",
                "Caso de Estudio"
            ]
        )
        
        # Configuración de plataformas
        col1, col2 = st.columns(2)
        with col1:
            platforms = st.multiselect(
                "Plataformas",
                ["LinkedIn", "Twitter", "Medium", "Instagram", "Blog"],
                ["LinkedIn", "Twitter"]
            )
        
        with col2:
            tone = st.select_slider(
                "Tono del contenido",
                options=["Formal", "Profesional", "Neutral", "Casual", "Informal"],
                value="Profesional"
            )
        
        # Configuración avanzada
        with st.expander("Configuración Avanzada", expanded=False):
            col3, col4 = st.columns(2)
            
            with col3:
                max_length = st.number_input(
                    "Longitud máxima (palabras)",
                    min_value=100,
                    max_value=5000,
                    value=1000,
                    step=100
                )
                
                keywords = st.text_input(
                    "Palabras clave (separadas por comas)",
                    placeholder="IA, negocios, automatización"
                )
            
            with col4:
                include_images = st.checkbox("Generar imágenes", value=True)
                include_stats = st.checkbox("Incluir estadísticas", value=True)
                include_quotes = st.checkbox("Incluir citas", value=True)
    
    # Métricas de contenido
    st.subheader("Métricas de Contenido")
    metrics = {
        "Contenido Generado": "125 piezas",
        "Engagement Promedio": "15.2%",
        "Mejor Plataforma": "LinkedIn",
        "ROI Estimado": "$250/mes"
    }
    
    cols = st.columns(len(metrics))
    for idx, (metric, value) in enumerate(metrics.items()):
        with cols[idx]:
            st.metric(metric, value)
    
    # Botón de generación
    if st.button("Generar Contenido"):
        workflow = ContentWorkflow(
            engine_manager=engine_manager,
            config={
                'topic': topic,
                'content_type': content_type,
                'platforms': platforms,
                'tone': tone,
                'max_length': max_length,
                'keywords': [k.strip() for k in keywords.split(',') if k.strip()],
                'include_images': include_images,
                'include_stats': include_stats,
                'include_quotes': include_quotes
            }
        )
        
        with st.spinner("Generando contenido..."):
            try:
                result = asyncio.run(workflow.execute())
                
                # Mostrar resultados
                st.success("Contenido generado exitosamente")
                
                # Vista previa del contenido
                with st.expander("Vista Previa", expanded=True):
                    for platform, content in result['content'].items():
                        st.subheader(f"Contenido para {platform}")
                        if isinstance(content, dict):
                            if 'text' in content:
                                st.write(content['text'])
                            if 'image_url' in content and content['image_url']:
                                st.image(content['image_url'])
                        else:
                            st.write(content)
                
                # Análisis y métricas
                with st.expander("Análisis de Contenido"):
                    st.write(result['analysis'])
                
                with st.expander("Métricas de Ejecución"):
                    st.json(result['metrics'])
                
                # Botones de acción
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Programar Publicación"):
                        st.info("Programador de publicaciones en desarrollo")
                with col2:
                    if st.button("Exportar Contenido"):
                        st.info("Exportación en desarrollo")
                with col3:
                    if st.button("Análisis Detallado"):
                        st.info("Análisis detallado en desarrollo")
                    
            except Exception as e:
                st.error(f"Error en la generación de contenido: {str(e)}") 