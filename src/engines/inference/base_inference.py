from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class InferenceMetrics:
    """Métricas de inferencia"""
    latency: float
    tokens_used: int
    cost: float
    model_name: str
    timestamp: datetime = datetime.now()

class BaseInferenceProvider(ABC):
    """Interfaz base para proveedores de inferencia"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_key = config['api_key']
        self.default_model = config.get('default_model')
        self.metrics: List[InferenceMetrics] = []
    
    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Genera texto usando el modelo especificado"""
        pass
    
    @abstractmethod
    async def embed_text(
        self,
        text: str,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Genera embeddings del texto"""
        pass
    
    def track_metrics(self, metrics: InferenceMetrics):
        """Registra métricas de inferencia"""
        self.metrics.append(metrics)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de métricas"""
        if not self.metrics:
            return {
                'total_cost': 0.0,
                'avg_latency': 0.0,
                'total_tokens': 0,
                'requests_count': 0
            }
        
        return {
            'total_cost': sum(m.cost for m in self.metrics),
            'avg_latency': sum(m.latency for m in self.metrics) / len(self.metrics),
            'total_tokens': sum(m.tokens_used for m in self.metrics),
            'requests_count': len(self.metrics)
        } 