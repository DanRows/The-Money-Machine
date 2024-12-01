from typing import Dict, Any, List
from src.workflows.base_workflow import BaseWorkflow

class PymeWorkflow(BaseWorkflow):
    """Workflow para creación y gestión de PYMES"""
    
    async def execute(self) -> Dict[str, Any]:
        try:
            # 1. Análisis de oportunidad de negocio
            market_opportunity = await self._analyze_opportunity()
            
            # 2. Plan de negocio
            business_plan = await self._create_business_plan(market_opportunity)
            
            # 3. Análisis financiero
            financial_analysis = await self._analyze_financials(business_plan)
            
            # 4. Plan de implementación
            implementation_plan = await self._create_implementation_plan(
                business_plan,
                financial_analysis
            )
            
            # 5. Plan de marketing
            marketing_plan = await self._create_marketing_plan(business_plan)
            
            return {
                'opportunity_analysis': market_opportunity,
                'business_plan': business_plan,
                'financial_analysis': financial_analysis,
                'implementation_plan': implementation_plan,
                'marketing_plan': marketing_plan,
                'metrics': self.metrics
            }
            
        except Exception as e:
            self.metrics['errors'].append({
                'step': 'workflow_execution',
                'error': str(e)
            })
            raise

    async def _analyze_opportunity(self) -> Dict[str, Any]:
        """Analiza la oportunidad de negocio"""
        engine = self.get_best_engine_for_task('opportunity_analysis')
        
        prompt = f"""
        Analiza la oportunidad de negocio para una PYME en el sector {self.config['sector']} considerando:
        
        1. Análisis de Mercado:
           - Tamaño del mercado
           - Tendencias del sector
           - Necesidades no cubiertas
           - Segmentos de clientes
        
        2. Análisis Competitivo:
           - Competidores principales
           - Barreras de entrada
           - Ventajas competitivas potenciales
        
        3. Viabilidad:
           - Recursos necesarios
           - Regulaciones y requisitos legales
           - Riesgos potenciales
        
        Ubicación: {self.config['location']}
        Inversión inicial disponible: {self.config['initial_investment']}
        
        Proporciona un análisis detallado y estructurado.
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'opportunity_analysis',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content']

    async def _create_business_plan(self, market_opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Genera un plan de negocio detallado"""
        engine = self.get_best_engine_for_task('business_planning')
        
        prompt = f"""
        Basado en el análisis de oportunidad:
        {market_opportunity}
        
        Desarrolla un plan de negocio completo incluyendo:
        
        1. Resumen Ejecutivo
        2. Descripción del Negocio:
           - Propuesta de valor
           - Modelo de negocio
           - Productos/servicios
        
        3. Análisis de Mercado:
           - Público objetivo
           - Estrategia de precios
           - Canales de distribución
        
        4. Plan Operativo:
           - Procesos clave
           - Recursos necesarios
           - Proveedores y partners
        
        5. Estructura Organizacional:
           - Equipo necesario
           - Roles y responsabilidades
           - Políticas de RRHH
        
        Considera:
        - Inversión inicial: {self.config['initial_investment']}
        - Ubicación: {self.config['location']}
        - Sector: {self.config['sector']}
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'business_planning',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content']

    async def _analyze_financials(self, business_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza un análisis financiero detallado"""
        engine = self.get_best_engine_for_task('financial_analysis')
        
        prompt = f"""
        Basado en el plan de negocio:
        {business_plan}
        
        Realiza un análisis financiero detallado incluyendo:
        
        1. Inversión Inicial:
           - Activos fijos
           - Capital de trabajo
           - Gastos pre-operativos
        
        2. Proyecciones Financieras (3 años):
           - Ingresos proyectados
           - Costos operativos
           - Flujo de caja
           - Estado de resultados
        
        3. Análisis de Rentabilidad:
           - ROI esperado
           - Punto de equilibrio
           - Margen de beneficio
        
        4. Indicadores Financieros:
           - VAN
           - TIR
           - Periodo de recuperación
        
        Inversión disponible: {self.config['initial_investment']}
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'financial_analysis',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content']

    async def _create_implementation_plan(
        self,
        business_plan: Dict[str, Any],
        financial_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Desarrolla un plan de implementación detallado"""
        engine = self.get_best_engine_for_task('implementation_planning')
        
        prompt = f"""
        Basado en:
        Plan de Negocio: {business_plan}
        Análisis Financiero: {financial_analysis}
        
        Desarrolla un plan de implementación detallado incluyendo:
        
        1. Cronograma de Implementación:
           - Fases y etapas
           - Hitos clave
           - Plazos estimados
        
        2. Plan de Acción:
           - Tareas específicas
           - Responsables
           - Recursos necesarios
        
        3. Gestión de Riesgos:
           - Riesgos identificados
           - Estrategias de mitigación
           - Plan de contingencia
        
        4. Indicadores de Seguimiento:
           - KPIs clave
           - Métricas de éxito
           - Sistema de monitoreo
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'implementation_planning',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content']

    async def _create_marketing_plan(self, business_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Desarrolla un plan de marketing completo"""
        engine = self.get_best_engine_for_task('marketing_planning')
        
        prompt = f"""
        Basado en el plan de negocio:
        {business_plan}
        
        Desarrolla un plan de marketing detallado incluyendo:
        
        1. Estrategia de Marketing:
           - Posicionamiento
           - Propuesta de valor
           - Mensajes clave
        
        2. Marketing Mix:
           - Producto/Servicio
           - Precio
           - Plaza
           - Promoción
        
        3. Marketing Digital:
           - Estrategia de contenidos
           - Redes sociales
           - SEO/SEM
           - Email marketing
        
        4. Presupuesto y ROI:
           - Inversión en marketing
           - ROI esperado
           - Métricas de seguimiento
        
        Considera:
        - Sector: {self.config['sector']}
        - Ubicación: {self.config['location']}
        - Público objetivo definido
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'marketing_planning',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content'] 