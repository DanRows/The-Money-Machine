from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from src.core.base_components import BaseComponent, TaskMetrics
from src.core.engine_manager import AIEngineManager

class BaseAgent(BaseComponent):
    """Agente base para todos los agentes del sistema"""
    
    def __init__(self, engine_manager: AIEngineManager, config: Dict[str, Any]):
        super().__init__(config)
        self.engine_manager = engine_manager
        self.context: Dict[str, Any] = {}
        self.last_execution: Optional[datetime] = None
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la tarea principal del agente"""
        pass
    
    async def _execute_with_retry(
        self,
        task: str,
        prompt: str,
        max_retries: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """Ejecuta una tarea con reintentos"""
        for attempt in range(max_retries):
            try:
                start_time = datetime.now()
                result = await self.engine_manager.execute_with_fallback(
                    task=task,
                    prompt=prompt,
                    **kwargs
                )
                
                # Registrar métricas
                self.track_metrics(TaskMetrics(
                    tokens_used=result.get('metrics', {}).get('tokens', 0),
                    cost=result.get('metrics', {}).get('cost', 0.0),
                    latency=(datetime.now() - start_time).total_seconds(),
                    success=True,
                    timestamp=datetime.now()
                ))
                
                return result
                
            except Exception as e:
                if attempt == max_retries - 1:
                    self.track_metrics(TaskMetrics(
                        success=False,
                        error_message=str(e),
                        timestamp=datetime.now()
                    ))
                    raise
                continue
    
    def _prepare_prompt(self, template: str, **kwargs) -> str:
        """Prepara un prompt usando un template"""
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Falta el parámetro requerido: {e}")
    
    def update_context(self, new_context: Dict[str, Any]):
        """Actualiza el contexto del agente"""
        self.context.update(new_context)
        self.last_execution = datetime.now()
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del agente"""
        metrics = self.get_metrics_summary()
        return {
            'last_execution': self.last_execution,
            'success_rate': metrics['success_rate'],
            'total_cost': metrics['total_cost'],
            'total_executions': metrics['total_tasks'],
            'context_size': len(self.context)
        } 