import streamlit as st
import asyncio
from src.workflows.dropshipping.dropshipping_workflow import DropshippingWorkflow

def render_dropshipping_dashboard(engine_manager):
    st.subheader("Dropshipping Automatizado")
    
    with st.expander("Configuración de Producto", expanded=True):
        category = st.selectbox(
            "Categoría de Producto",
            [
                "Electrónica",
                "Hogar y Jardín",
                "Moda y Accesorios",
                "Salud y Belleza",
                "Deportes",
                "Mascotas",
                "Niños y Bebés"
            ]
        )
        
        target_market = st.multiselect(
            "Mercados Objetivo",
            ["España", "Europa", "Estados Unidos", "Latinoamérica"],
            ["España"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input(
                "Presupuesto Inicial (€)",
                min_value=500,
                max_value=50000,
                value=2000,
                step=500
            )
        with col2:
            marketing_budget = st.number_input(
                "Presupuesto Marketing (€)",
                min_value=100,
                max_value=10000,
                value=1000,
                step=100
            )
        
        min_margin = st.slider(
            "Margen Mínimo Deseado (%)",
            min_value=20,
            max_value=80,
            value=30,
            help="Margen de beneficio mínimo aceptable"
        )
        
        platform = st.selectbox(
            "Plataforma de Venta Principal",
            ["Shopify", "WooCommerce", "Amazon", "eBay", "Marketplace Propio"]
        )
    
    # Métricas de rendimiento esperado
    st.subheader("Métricas Estimadas")
    metrics = {
        "ROI Esperado": "150-200%",
        "Tiempo a Beneficio": "2-3 meses",
        "Ventas Mensuales": "€5,000-8,000",
        "Conversión Estimada": "2-3%"
    }
    
    cols = st.columns(len(metrics))
    for idx, (metric, value) in enumerate(metrics.items()):
        with cols[idx]:
            st.metric(metric, value)
    
    # Configuración avanzada
    with st.expander("Configuración Avanzada", expanded=False):
        shipping_strategy = st.radio(
            "Estrategia de Envío",
            ["Envío Estándar", "Envío Express", "Mixta"]
        )
        
        inventory_strategy = st.radio(
            "Estrategia de Inventario",
            ["Bajo Demanda", "Stock Mínimo", "Híbrida"]
        )
        
        pricing_strategy = st.selectbox(
            "Estrategia de Precios",
            ["Competitiva", "Premium", "Penetración", "Dinámica"]
        )
    
    # Botón de ejecución
    if st.button("Generar Plan de Dropshipping"):
        workflow = DropshippingWorkflow(
            engine_manager=engine_manager,
            config={
                'category': category,
                'target_market': target_market,
                'budget': budget,
                'marketing_budget': marketing_budget,
                'min_margin': f"{min_margin}%",
                'platform': platform,
                'shipping_strategy': shipping_strategy,
                'inventory_strategy': inventory_strategy,
                'pricing_strategy': pricing_strategy
            }
        )
        
        with st.spinner("Analizando mercado y generando plan..."):
            try:
                result = asyncio.run(workflow.execute())
                
                # Mostrar resultados
                st.success("Plan de dropshipping generado exitosamente")
                
                with st.expander("Análisis de Productos", expanded=True):
                    st.write(result['product_analysis'])
                
                with st.expander("Análisis de Proveedores"):
                    st.write(result['supplier_analysis'])
                
                with st.expander("Análisis de Mercado"):
                    st.write(result['market_analysis'])
                
                with st.expander("Estrategia de Precios"):
                    st.write(result['pricing_strategy'])
                
                with st.expander("Plan de Marketing"):
                    st.write(result['marketing_plan'])
                
                with st.expander("Métricas de Ejecución"):
                    st.json(result['metrics'])
                
                # Botones de acción
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Exportar Plan (PDF)"):
                        st.info("Funcionalidad de exportación en desarrollo")
                with col2:
                    if st.button("Conectar con Proveedores"):
                        st.info("Integración con proveedores en desarrollo")
                with col3:
                    if st.button("Configurar Tienda"):
                        st.info("Asistente de configuración en desarrollo")
                    
            except Exception as e:
                st.error(f"Error en la generación del plan: {str(e)}") 