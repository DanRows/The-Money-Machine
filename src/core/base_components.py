from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TaskMetrics:
    tokens_used: int = 0
    cost: float = 0.0
    latency: float = 0.0
    success: bool = True
    error_message: Optional[str] = None
    timestamp: datetime = datetime.now()

class BaseComponent(ABC):
    """Componente base para todos los elementos del sistema"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metrics: List[TaskMetrics] = []
    
    def track_metrics(self, metrics: TaskMetrics):
        """Registra métricas de ejecución"""
        self.metrics.append(metrics)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de métricas"""
        return {
            'total_tokens': sum(m.tokens_used for m in self.metrics),
            'total_cost': sum(m.cost for m in self.metrics),
            'avg_latency': sum(m.latency for m in self.metrics) / len(self.metrics) if self.metrics else 0,
            'success_rate': sum(1 for m in self.metrics if m.success) / len(self.metrics) if self.metrics else 0,
            'total_tasks': len(self.metrics)
        } 