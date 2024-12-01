import anthropic
from typing import Dict, Any, Optional
from datetime import datetime
import time
from src.core.base_components import BaseComponent, TaskMetrics

class AnthropicEngine(BaseComponent):
    """Motor de IA basado en Anthropic Claude"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = anthropic.Client(api_key=config['api_key'])
        self.model = config.get('model', 'claude-2')
        self.default_params = {
            'temperature': config.get('temperature', 0.7),
            'max_tokens': config.get('max_tokens', 2000),
            'top_p': config.get('top_p', 1.0)
        }
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Genera texto usando Claude"""
        start_time = time.time()
        
        try:
            # Preparar el mensaje
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nHuman: {prompt}\n\nAssistant:"
            else:
                full_prompt = f"Human: {prompt}\n\nAssistant:"
            
            # Combinar parámetros
            params = {**self.default_params, **kwargs}
            
            response = await self.client.completions.create(
                model=self.model,
                prompt=full_prompt,
                **params
            )
            
            # Calcular métricas
            end_time = time.time()
            latency = end_time - start_time
            tokens_used = response.usage.total_tokens
            cost = self._calculate_cost(tokens_used)
            
            # Registrar métricas
            self.track_metrics(TaskMetrics(
                tokens_used=tokens_used,
                cost=cost,
                latency=latency,
                success=True,
                timestamp=datetime.now()
            ))
            
            return {
                'text': response.completion,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': tokens_used
                },
                'model': self.model,
                'metrics': {
                    'tokens': tokens_used,
                    'cost': cost,
                    'latency': latency
                }
            }
            
        except Exception as e:
            end_time = time.time()
            self.track_metrics(TaskMetrics(
                success=False,
                error_message=str(e),
                latency=end_time - start_time,
                timestamp=datetime.now()
            ))
            raise
    
    def _calculate_cost(self, tokens: int) -> float:
        """Calcula el costo basado en el modelo y tokens usados"""
        costs = {
            'claude-2': 0.01,  # $0.01 por 1K tokens
            'claude-instant-1': 0.0015
        }
        
        cost_per_1k = costs.get(self.model, 0.01)
        return (tokens / 1000) * cost_per_1k 