import httpx
from typing import Dict, Any, Optional
from datetime import datetime
import time
from .base_inference import BaseInferenceProvider, InferenceMetrics

class DeepInfraProvider(BaseInferenceProvider):
    """Proveedor de inferencia usando DeepInfra"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = "https://api.deepinfra.com/v1/inference"
        self.default_model = config.get('default_model', 'meta-llama/Llama-2-70b-chat-hf')
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
    
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
            response = await self.client.post(
                f"{self.base_url}/{model}",
                json={
                    "input": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    **kwargs
                }
            )
            response.raise_for_status()
            data = response.json()
            
            end_time = time.time()
            latency = end_time - start_time
            
            self.track_metrics(InferenceMetrics(
                latency=latency,
                tokens_used=data.get('usage', {}).get('total_tokens', 0),
                cost=0.0,
                model_name=model
            ))
            
            return {
                'text': data['output'],
                'usage': data.get('usage', {}),
                'model': model,
                'metrics': {
                    'latency': latency
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