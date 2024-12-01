from abc import ABC, abstractmethod
from typing import Dict, Any
from src.core.engine_manager import AIEngineManager

class BaseWorkflow(ABC):
    """Clase base para todos los workflows"""
    
    def __init__(self, engine_manager: AIEngineManager, config: Dict[str, Any]):
        self.engine_manager = engine_manager
        self.config = config
        self.metrics = {
            'steps_completed': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'errors': []
        }

    @abstractmethod
    async def execute(self) -> Dict[str, Any]:
        """Ejecuta el workflow completo"""
        pass

    def update_metrics(self, step_metrics: Dict[str, Any]):
        """Actualiza las métricas del workflow"""
        self.metrics['steps_completed'] += 1
        self.metrics['total_tokens'] += step_metrics.get('tokens', 0)
        self.metrics['total_cost'] += step_metrics.get('cost', 0.0)
        
        if 'error' in step_metrics:
            self.metrics['errors'].append({
                'step': step_metrics.get('step_name', 'unknown'),
                'error': str(step_metrics['error'])
            })

    def get_best_engine_for_task(self, task: str) -> str:
        """Selecciona el mejor motor para una tarea específica"""
        return self.engine_manager.select_best_engine(task) 