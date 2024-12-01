from typing import Dict, Any, List
from src.core.base_components import BaseComponent
from src.engines.base_engine import BaseAIEngine

class AIEngineManager(BaseComponent):
    """Gestor de motores de IA"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.engines: Dict[str, BaseAIEngine] = {}
        self.fallback_strategy = config.get('fallback_strategy', 'round_robin')
        self.load_engines()
    
    def load_engines(self):
        """Carga los motores configurados"""
        for engine_name, engine_config in self.config.get('engines', {}).items():
            engine_class = self._get_engine_class(engine_config['type'])
            self.engines[engine_name] = engine_class(
                api_key=engine_config['api_key'],
                config=engine_config
            )
    
    def _get_engine_class(self, engine_type: str) -> type:
        """Obtiene la clase del motor según el tipo"""
        from src.engines.openai_engine import OpenAIEngine
        from src.engines.anthropic_engine import AnthropicEngine
        from src.engines.google_engine import GoogleEngine
        
        engine_classes = {
            'openai': OpenAIEngine,
            'anthropic': AnthropicEngine,
            'google': GoogleEngine
        }
        
        return engine_classes.get(engine_type)
    
    def select_best_engine(
        self, 
        task: str, 
        criteria: List[str] = ["cost", "speed", "quality"]
    ) -> BaseAIEngine:
        """Selecciona el mejor motor para una tarea"""
        scored_engines = [
            (engine, self._evaluate_engine(engine, task, criteria))
            for engine in self.engines.values()
        ]
        
        return max(scored_engines, key=lambda x: x[1])[0]
    
    def _evaluate_engine(
        self, 
        engine: BaseAIEngine, 
        task: str, 
        criteria: List[str]
    ) -> float:
        """Evalúa un motor según criterios"""
        score = 0.0
        metrics = engine.get_usage_report()
        
        if "cost" in criteria:
            # Menor costo = mejor puntuación
            cost_score = 1.0 / (metrics['total_cost'] + 1.0)
            score += cost_score * 0.4
        
        if "speed" in criteria:
            # Menor latencia = mejor puntuación
            speed_score = 1.0 / (metrics.get('avg_latency', 1.0) + 1.0)
            score += speed_score * 0.3
        
        if "quality" in criteria:
            # Mayor tasa de éxito = mejor puntuación
            quality_score = metrics.get('success_rate', 0.5)
            score += quality_score * 0.3
        
        return score
    
    def execute_with_fallback(
        self, 
        task: str, 
        prompt: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Ejecuta una tarea con manejo de fallback"""
        primary_engine = self.select_best_engine(task)
        
        try:
            result = primary_engine.generate_text(prompt, **kwargs)
            return {
                'result': result,
                'engine': primary_engine.__class__.__name__,
                'success': True
            }
        except Exception as e:
            # Si falla, intenta con el siguiente mejor motor
            backup_engines = [
                engine for engine in self.engines.values()
                if engine != primary_engine
            ]
            
            for engine in backup_engines:
                try:
                    result = engine.generate_text(prompt, **kwargs)
                    return {
                        'result': result,
                        'engine': engine.__class__.__name__,
                        'success': True,
                        'fallback_used': True
                    }
                except:
                    continue
            
            return {
                'result': None,
                'error': str(e),
                'success': False
            } 