import replicate
from typing import Dict, Any, Optional
from datetime import datetime
import time
from .base_inference import BaseInferenceProvider, InferenceMetrics

class ReplicateProvider(BaseInferenceProvider):
    """Proveedor de inferencia usando Replicate"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = replicate.Client(api_token=self.api_key)
        self.default_model = config.get('default_model', 'meta/llama-2-70b-chat')
        self.cost_per_token = config.get('cost_per_token', 0.0002)
    
    async def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        start_time = time.time()
        model = model or self.default_model
        
        try:
            output = await self.client.run(
                model,
                input={
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    **kwargs
                }
            )
            
            end_time = time.time()
            latency = end_time - start_time
            # Replicate no proporciona conteo de tokens directamente
            tokens_used = len(prompt.split()) + len(output.split())
            cost = tokens_used * self.cost_per_token
            
            self.track_metrics(InferenceMetrics(
                latency=latency,
                tokens_used=tokens_used,
                cost=cost,
                model_name=model
            ))
            
            return {
                'text': output,
                'usage': {
                    'total_tokens': tokens_used
                },
                'model': model,
                'metrics': {
                    'latency': latency,
                    'cost': cost
                }
            }
            
        except Exception as e:
            end_time = time.time()
            self.track_metrics(InferenceMetrics(
                latency=end_time - start_time,
                tokens_used=0,
                cost=0,
                model_name=model
            ))
            raise 