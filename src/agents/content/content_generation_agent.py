from typing import Dict, Any, List
from src.agents.base.base_agent import BaseAgent

class ContentGenerationAgent(BaseAgent):
    """Agente especializado en generación de contenido"""
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta el proceso de generación de contenido"""
        # 1. Investigación y planificación
        content_plan = await self._create_content_plan(context)
        
        # 2. Generación de contenido
        content = await self._generate_content(context, content_plan)
        
        # 3. Optimización y adaptación
        optimized_content = await self._optimize_content(context, content)
        
        # 4. Validación de calidad
        validated_content = await self._validate_content(optimized_content)
        
        # Actualizar contexto
        self.update_context({
            'content_plan': content_plan,
            'content': content,
            'optimized_content': optimized_content,
            'validated_content': validated_content
        })
        
        return {
            'content': validated_content,
            'plan': content_plan,
            'metrics': self.get_metrics_summary()
        }
    
    async def _create_content_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un plan de contenido"""
        prompt = self._prepare_prompt(
            """Crea un plan de contenido para {topic} considerando:
            1. Objetivos principales
            2. Público objetivo
            3. Puntos clave a cubrir
            4. Estructura sugerida
            5. Tono y estilo
            
            Plataformas objetivo: {platforms}
            Tono deseado: {tone}
            Longitud aproximada: {length} palabras
            
            Proporciona un plan detallado y estructurado.""",
            topic=context['topic'],
            platforms=", ".join(context['platforms']),
            tone=context.get('tone', 'profesional'),
            length=context.get('max_length', 1000)
        )
        
        result = await self._execute_with_retry(
            task='content_planning',
            prompt=prompt,
            temperature=0.7
        )
        
        return {
            'plan': result['text'],
            'timestamp': result.get('timestamp'),
            'structure': self._extract_structure(result['text'])
        }
    
    async def _generate_content(
        self,
        context: Dict[str, Any],
        content_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Genera el contenido base"""
        prompt = self._prepare_prompt(
            """Basado en el siguiente plan:
            {content_plan}
            
            Genera contenido para {topic} con estas características:
            - Tono: {tone}
            - Longitud: {length} palabras
            - Plataformas: {platforms}
            
            Asegúrate de:
            1. Mantener coherencia
            2. Incluir datos relevantes
            3. Optimizar para SEO
            4. Usar un lenguaje persuasivo
            5. Incluir llamadas a la acción
            
            Genera el contenido completo.""",
            content_plan=content_plan['plan'],
            topic=context['topic'],
            tone=context.get('tone', 'profesional'),
            length=context.get('max_length', 1000),
            platforms=", ".join(context['platforms'])
        )
        
        result = await self._execute_with_retry(
            task='content_generation',
            prompt=prompt,
            temperature=0.8
        )
        
        return {
            'content': result['text'],
            'timestamp': result.get('timestamp'),
            'platform_versions': self._create_platform_versions(result['text'], context['platforms'])
        }
    
    async def _optimize_content(
        self,
        context: Dict[str, Any],
        content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimiza el contenido para cada plataforma"""
        optimized_versions = {}
        
        for platform, content_version in content['platform_versions'].items():
            prompt = self._prepare_prompt(
                """Optimiza el siguiente contenido para {platform}:
                {content}
                
                Considerando:
                1. Límites de caracteres
                2. Formato específico
                3. Hashtags relevantes
                4. Elementos multimedia
                5. Engagement típico
                
                Optimiza el contenido manteniendo el mensaje clave.""",
                platform=platform,
                content=content_version
            )
            
            result = await self._execute_with_retry(
                task='content_optimization',
                prompt=prompt,
                temperature=0.7
            )
            
            optimized_versions[platform] = {
                'content': result['text'],
                'hashtags': self._extract_hashtags(result['text']),
                'media_suggestions': self._suggest_media(result['text'])
            }
        
        return {
            'versions': optimized_versions,
            'timestamp': content['timestamp']
        }
    
    async def _validate_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Valida la calidad del contenido"""
        validated_versions = {}
        
        for platform, version in content['versions'].items():
            prompt = self._prepare_prompt(
                """Valida el siguiente contenido:
                {content}
                
                Verifica:
                1. Gramática y ortografía
                2. Tono y estilo
                3. Claridad del mensaje
                4. Llamadas a la acción
                5. Optimización SEO
                
                Proporciona una evaluación detallada y correcciones si son necesarias.""",
                content=version['content']
            )
            
            result = await self._execute_with_retry(
                task='content_validation',
                prompt=prompt,
                temperature=0.5
            )
            
            validated_versions[platform] = {
                'content': result['text'],
                'quality_score': self._calculate_quality_score(result['text']),
                'improvements': self._extract_improvements(result['text']),
                'hashtags': version['hashtags'],
                'media_suggestions': version['media_suggestions']
            }
        
        return validated_versions
    
    def _extract_structure(self, text: str) -> List[Dict[str, Any]]:
        """Extrae la estructura del plan de contenido"""
        # TODO: Implementar extracción de estructura
        return []
    
    def _create_platform_versions(
        self,
        text: str,
        platforms: List[str]
    ) -> Dict[str, str]:
        """Crea versiones específicas para cada plataforma"""
        # TODO: Implementar adaptación por plataforma
        return {platform: text for platform in platforms}
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extrae hashtags del contenido"""
        # TODO: Implementar extracción de hashtags
        return []
    
    def _suggest_media(self, text: str) -> List[Dict[str, Any]]:
        """Sugiere elementos multimedia"""
        # TODO: Implementar sugerencias de media
        return []
    
    def _calculate_quality_score(self, text: str) -> float:
        """Calcula score de calidad del contenido"""
        # TODO: Implementar cálculo de calidad
        return 0.0
    
    def _extract_improvements(self, text: str) -> List[Dict[str, Any]]:
        """Extrae sugerencias de mejora"""
        # TODO: Implementar extracción de mejoras
        return []