from typing import Dict, Any, List
from src.workflows.base_workflow import BaseWorkflow

class ContentWorkflow(BaseWorkflow):
    """Workflow para generación y publicación de contenido"""
    
    async def execute(self) -> Dict[str, Any]:
        try:
            # 1. Planificación de contenido
            content_plan = await self._plan_content()
            
            # 2. Generación de contenido
            content = await self._generate_content(content_plan)
            
            # 3. Adaptación por plataforma
            platform_content = await self._adapt_for_platforms(content)
            
            # 4. Validación de calidad
            validated_content = await self._validate_content(platform_content)
            
            return {
                'content': validated_content,
                'metrics': self.metrics
            }
            
        except Exception as e:
            self.metrics['errors'].append({
                'step': 'workflow_execution',
                'error': str(e)
            })
            raise

    async def _plan_content(self) -> Dict[str, Any]:
        """Genera un plan de contenido basado en el tema"""
        engine = self.get_best_engine_for_task('content_planning')
        
        prompt = f"""
        Crea un plan de contenido para el tema: {self.config['topic']}
        Tono deseado: {self.config['tone']}
        Plataformas objetivo: {', '.join(self.config['platforms'])}
        
        El plan debe incluir:
        1. Puntos clave a cubrir
        2. Estructura sugerida
        3. Referencias o datos relevantes
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'content_planning',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content']

    async def _generate_content(self, content_plan: Dict[str, Any]) -> str:
        """Genera el contenido base"""
        engine = self.get_best_engine_for_task('content_generation')
        
        prompt = f"""
        Basado en el siguiente plan de contenido:
        {content_plan}
        
        Genera contenido con estas características:
        - Tema: {self.config['topic']}
        - Tono: {self.config['tone']}
        - Longitud: Adaptada para múltiples plataformas
        """
        
        response = await engine.generate_text(prompt)
        
        self.update_metrics({
            'step_name': 'content_generation',
            'tokens': response.get('usage', {}).get('total_tokens', 0),
            'cost': response.get('cost', 0.0)
        })
        
        return response['content']

    async def _adapt_for_platforms(self, content: str) -> Dict[str, str]:
        """Adapta el contenido para cada plataforma"""
        adapted_content = {}
        
        for platform in self.config['platforms']:
            engine = self.get_best_engine_for_task('content_adaptation')
            
            prompt = f"""
            Adapta el siguiente contenido para {platform}:
            {content}
            
            Considera:
            - Límites de caracteres de la plataforma
            - Formato y estilo típico
            - Hashtags relevantes
            """
            
            response = await engine.generate_text(prompt)
            
            self.update_metrics({
                'step_name': f'content_adaptation_{platform.lower()}',
                'tokens': response.get('usage', {}).get('total_tokens', 0),
                'cost': response.get('cost', 0.0)
            })
            
            adapted_content[platform] = response['content']
        
        return adapted_content

    async def _validate_content(self, platform_content: Dict[str, str]) -> Dict[str, Any]:
        """Valida la calidad del contenido generado"""
        validated_content = {}
        
        for platform, content in platform_content.items():
            engine = self.get_best_engine_for_task('content_validation')
            
            prompt = f"""
            Valida el siguiente contenido para {platform}:
            {content}
            
            Verifica:
            1. Gramática y ortografía
            2. Tono apropiado
            3. Longitud adecuada
            4. Cumplimiento de políticas de la plataforma
            
            Retorna el contenido corregido si es necesario.
            """
            
            response = await engine.generate_text(prompt)
            
            self.update_metrics({
                'step_name': f'content_validation_{platform.lower()}',
                'tokens': response.get('usage', {}).get('total_tokens', 0),
                'cost': response.get('cost', 0.0)
            })
            
            validated_content[platform] = response['content']
        
        return validated_content 