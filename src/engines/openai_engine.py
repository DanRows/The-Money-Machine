import openai
from typing import Dict, Any, Optional
from datetime import datetime
import time
from src.core.base_components import BaseComponent, TaskMetrics

class OpenAIEngine(BaseComponent):
    """Motor de IA basado en OpenAI"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        openai.api_key = config['api_key']
        self.model = config.get('model', 'gpt-4')
        self.default_params = {
            'temperature': config.get('temperature', 0.7),
            'max_tokens': config.get('max_tokens', 2000),
            'top_p': config.get('top_p', 1.0),
            'frequency_penalty': config.get('frequency_penalty', 0.0),
            'presence_penalty': config.get('presence_penalty', 0.0)
        }
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Genera texto usando OpenAI"""
        start_time = time.time()
        
        try:
            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Combinar parámetros por defecto con los proporcionados
            params = {**self.default_params, **kwargs}
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                **params
            )
            
            # Calcular métricas
            end_time = time.time()
            latency = end_time - start_time
            tokens_used = response['usage']['total_tokens']
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
                'text': response.choices[0].message['content'],
                'usage': response['usage'],
                'model': self.model,
                'finish_reason': response.choices[0].finish_reason,
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
    
    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        style: str = "natural",
        **kwargs
    ) -> Dict[str, Any]:
        """Genera imágenes usando DALL-E"""
        start_time = time.time()
        
        try:
            response = await openai.Image.acreate(
                prompt=prompt,
                size=size,
                quality=quality,
                style=style,
                **kwargs
            )
            
            # Calcular métricas
            end_time = time.time()
            latency = end_time - start_time
            cost = self._calculate_image_cost(size, quality)
            
            # Registrar métricas
            self.track_metrics(TaskMetrics(
                cost=cost,
                latency=latency,
                success=True,
                timestamp=datetime.now()
            ))
            
            return {
                'urls': [img['url'] for img in response['data']],
                'metrics': {
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
            'gpt-4': 0.03,  # $0.03 por 1K tokens
            'gpt-4-32k': 0.06,
            'gpt-3.5-turbo': 0.002,
            'gpt-3.5-turbo-16k': 0.004
        }
        
        cost_per_1k = costs.get(self.model, 0.03)
        return (tokens / 1000) * cost_per_1k
    
    def _calculate_image_cost(self, size: str, quality: str) -> float:
        """Calcula el costo de generación de imágenes"""
        costs = {
            '1024x1024': {'standard': 0.020, 'hd': 0.080},
            '512x512': {'standard': 0.018, 'hd': 0.070},
            '256x256': {'standard': 0.016, 'hd': 0.060}
        }
        
        return costs.get(size, {}).get(quality, 0.020) 