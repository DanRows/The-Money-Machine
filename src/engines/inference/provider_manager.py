from typing import Dict, Any, Optional, List
from .base_inference import BaseInferenceProvider
from .groq_provider import GroqProvider
from .anthropic_provider import AnthropicProvider
from .together_provider import TogetherProvider
from .anyscale_provider import AnyscaleProvider
from .replicate_provider import ReplicateProvider
from .deepinfra_provider import DeepInfraProvider
from .sambanova_provider import SambanovaProvider

class InferenceProviderManager:
    """Gestor de proveedores de inferencia"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.providers: Dict[str, BaseInferenceProvider] = {}
        self.load_providers()
    
    def load_providers(self):
        """Carga los proveedores configurados"""
        provider_classes = {
            'groq': GroqProvider,
            'anthropic': AnthropicProvider,
            'together': TogetherProvider,
            'anyscale': AnyscaleProvider,
            'replicate': ReplicateProvider,
            'deepinfra': DeepInfraProvider,
            'sambanova': SambanovaProvider
        }
        
        for name, provider_config in self.config.get('providers', {}).items():
            if provider_config.get('enabled', True):
                provider_class = provider_classes.get(provider_config['type'])
                if provider_class:
                    self.providers[name] = provider_class(provider_config)
    
    def get_provider(self, name: str) -> Optional[BaseInferenceProvider]:
        """Obtiene un proveedor específico"""
        return self.providers.get(name)
    
    def get_all_providers(self) -> Dict[str, BaseInferenceProvider]:
        """Obtiene todos los proveedores activos"""
        return self.providers
    
    def get_best_provider(self, task: str, criteria: List[str] = ["cost", "speed", "quality"]) -> BaseInferenceProvider:
        """Selecciona el mejor proveedor para una tarea"""
        scored_providers = [
            (provider, self._evaluate_provider(provider, task, criteria))
            for provider in self.providers.values()
        ]
        
        return max(scored_providers, key=lambda x: x[1])[0]
    
    def _evaluate_provider(
        self,
        provider: BaseInferenceProvider,
        task: str,
        criteria: List[str]
    ) -> float:
        """Evalúa un proveedor según criterios"""
        metrics = provider.get_metrics_summary()
        score = 0.0
        
        if "cost" in criteria:
            cost_score = 1.0 / (metrics['total_cost'] + 1.0)
            score += cost_score * 0.4
        
        if "speed" in criteria:
            speed_score = 1.0 / (metrics['avg_latency'] + 1.0)
            score += speed_score * 0.3
        
        if "quality" in criteria:
            success_rate = metrics['success_rate'] if 'success_rate' in metrics else 0.5
            score += success_rate * 0.3
        
        return score 