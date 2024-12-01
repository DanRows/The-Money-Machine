import together
from typing import Dict, Any, Optional
from datetime import datetime
import time
from .base_inference import BaseInferenceProvider, InferenceMetrics

class TogetherProvider(BaseInferenceProvider):
    """Proveedor de inferencia usando Together AI"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        together.api_key = self.api_key
        self.default_model = config.get('default_model', 'togethercomputer/llama-2-70b')
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
            response = await together.Complete.create(
                prompt=prompt,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            
            end_time = time.time()
            latency = end_time - start_time
            tokens_used = response.usage.total_tokens
            cost = tokens_used * self.cost_per_token
            
            self.track_metrics(InferenceMetrics(
                latency=latency,
                tokens_used=tokens_used,
                cost=cost,
                model_name=model
            ))
            
            return {
                'text': response.output.text,
                'usage': response.usage._asdict(),
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
        model = model or 'togethercomputer/m2-bert-80M-8k-base'
        
        try:
            response = await together.Embeddings.create(
                input=text,
                model=model,
                **kwargs
            )
            
            end_time = time.time()
            latency = end_time - start_time
            
            self.track_metrics(InferenceMetrics(
                latency=latency,
                tokens_used=len(text.split()),
                cost=0.0,
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