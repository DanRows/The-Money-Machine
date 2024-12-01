from typing import Dict, Any, Optional
import httpx
from datetime import datetime
import time
from .base_inference import BaseInferenceProvider, InferenceMetrics

class SambanovaProvider(BaseInferenceProvider):
    """Proveedor de inferencia usando SambaNova"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config['base_url']
        self.default_model = config.get('default_model', 'sambanova-gpt')
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
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
                "/v1/completions",
                json={
                    "model": model,
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    **kwargs
                }
            )
            response.raise_for_status()
            data = response.json()
            
            end_time = time.time()
            latency = end_time - start_time
            
            # Registrar métricas
            self.track_metrics(InferenceMetrics(
                latency=latency,
                tokens_used=data.get('usage', {}).get('total_tokens', 0),
                cost=0.0,  # Ajustar según pricing
                model_name=model
            ))
            
            return {
                'text': data['choices'][0]['text'],
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
    
    async def embed_text(
        self,
        text: str,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        start_time = time.time()
        model = model or f"{self.default_model}-embed"
        
        try:
            response = await self.client.post(
                "/v1/embeddings",
                json={
                    "model": model,
                    "input": text,
                    **kwargs
                }
            )
            response.raise_for_status()
            data = response.json()
            
            end_time = time.time()
            latency = end_time - start_time
            
            # Registrar métricas
            self.track_metrics(InferenceMetrics(
                latency=latency,
                tokens_used=len(text.split()),  # Aproximación
                cost=0.0,  # Ajustar según pricing
                model_name=model
            ))
            
            return {
                'embeddings': data['data'][0]['embedding'],
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