from typing import Dict, Any, List
from src.workflows.base_workflow import BaseWorkflow

class TradingWorkflow(BaseWorkflow):
    """Workflow para análisis y ejecución de operaciones de trading"""
    
    async def execute(self) -> Dict[str, Any]:
        try:
            # 1. Análisis de mercado
            market_analysis = await self._analyze_market()
            
            # 2. Generación de señales
            trading_signals = await self._generate_signals(market_analysis)
            
            # 3. Evaluación de riesgo
            risk_assessment = await self._assess_risk(trading_signals)
            
            # 4. Decisión de trading
            trading_decisions = await self._make_trading_decisions(
                trading_signals, 
                risk_assessment
            )
            
            return {
                'analysis': market_analysis,
                'signals': trading_signals,
                'risk_assessment': risk_assessment,
                'decisions': trading_decisions,
                'metrics': self.metrics
            }
            
        except Exception as e:
            self.metrics['errors'].append({
                'step': 'workflow_execution',
                'error': str(e)
            })
            raise

    async def _analyze_market(self) -> Dict[str, Any]:
        """Analiza las condiciones actuales del mercado"""
        engine = self.get_best_engine_for_task('market_analysis')
        
        prompt = f"""
        Analiza el mercado {self.config['market']} considerando:
        
        1. Condiciones Macroeconómicas:
           - Indicadores económicos clave
           - Eventos geopolíticos relevantes
           - Tendencias de mercado
        
        2. Análisis Técnico:
           - Patrones de precio
           - Indicadores técnicos principales
           - Niveles de soporte/resistencia
        
        3. Análisis Fundamental:
           - Métricas fundamentales clave
           - Noticias y eventos corporativos
           - Sentimiento del mercado
        
        Proporciona un análisis detallado y estructurado.
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'market_analysis',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content']

    async def _generate_signals(self, market_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Genera señales de trading basadas en el análisis"""
        engine = self.get_best_engine_for_task('signal_generation')
        
        prompt = f"""
        Basado en el siguiente análisis de mercado:
        {market_analysis}
        
        Genera señales de trading considerando:
        1. Dirección (largo/corto)
        2. Puntos de entrada
        3. Stop loss
        4. Take profit
        5. Timeframe
        6. Confianza de la señal (1-10)
        
        Proporciona señales específicas y accionables.
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'signal_generation',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content']

    async def _assess_risk(self, trading_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evalúa el riesgo de las señales generadas"""
        engine = self.get_best_engine_for_task('risk_assessment')
        
        prompt = f"""
        Evalúa el riesgo de las siguientes señales de trading:
        {trading_signals}
        
        Considera:
        1. Volatilidad del mercado
        2. Correlación con otros activos
        3. Exposición total
        4. Ratio riesgo/recompensa
        5. Liquidez del mercado
        
        Proporciona una evaluación detallada de riesgos y recomendaciones.
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'risk_assessment',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content']

    async def _make_trading_decisions(
        self, 
        trading_signals: List[Dict[str, Any]], 
        risk_assessment: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Toma decisiones finales de trading"""
        engine = self.get_best_engine_for_task('decision_making')
        
        prompt = f"""
        Basado en:
        Señales: {trading_signals}
        Evaluación de Riesgo: {risk_assessment}
        
        Toma decisiones de trading considerando:
        1. Tamaño de la posición
        2. Momento óptimo de entrada
        3. Gestión de la operación
        4. Plan de salida
        
        Portfolio actual: {self.config.get('current_portfolio', {})}
        Límites de riesgo: {self.config.get('risk_limits', {})}
        
        Proporciona decisiones específicas y ejecutables.
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'decision_making',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content'] 