import groq
from typing import Dict, Any, Optional
from datetime import datetime
import time
from .base_inference import BaseInferenceProvider, InferenceMetrics

class GroqProvider(BaseInferenceProvider):
    """Proveedor de inferencia usando Groq"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = groq.Client(api_key=self.api_key)
        self.default_model = config.get('default_model', 'mixtral-8x7b-32768')
        self.cost_per_token = config.get('cost_per_token', 0.0001)
    
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
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            
            end_time = time.time()
            latency = end_time - start_time
            tokens_used = response.usage.total_tokens
            cost = tokens_used * self.cost_per_token
            
            # Registrar métricas
            self.track_metrics(InferenceMetrics(
                latency=latency,
                tokens_used=tokens_used,
                cost=cost,
                model_name=model
            ))
            
            return {
                'text': response.choices[0].message.content,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
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
    
    async def embed_text(
        self,
        text: str,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        start_time = time.time()
        model = model or 'embed-english-v3'
        
        try:
            response = await self.client.embeddings.create(
                model=model,
                input=text,
                **kwargs
            )
            
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
                'embeddings': response.data[0].embedding,
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