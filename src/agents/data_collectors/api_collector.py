from typing import Dict, Any, Optional
import requests
from urllib.parse import urljoin
from src.core.logging_system import logger
from .base_collector import BaseDataCollector

class APIDataCollector(BaseDataCollector):
    """Colector de datos desde APIs REST"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get('base_url', config.get('api_url'))  # Compatibilidad con versión anterior
        self.endpoints = config.get('endpoints', {})
        self.headers = config.get('headers', {})
        self.params = config.get('params', {})
        self.session: Optional[requests.Session] = None

    def connect(self) -> bool:
        try:
            self.session = requests.Session()
            self.session.headers.update(self.headers)
            
            # Verificar conectividad
            response = self.session.get(self.base_url)
            response.raise_for_status()
            logger.info(f"Conexión exitosa a {self.base_url}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al conectar con {self.base_url}: {str(e)}")
            return False

    def fetch_data(self) -> Dict[str, Any]:
        if not self.session:
            raise Exception("No hay una sesión activa")
            
        if not self.endpoints:
            # Modo compatible con versión anterior
            response = self.session.get(self.base_url, params=self.params)
            response.raise_for_status()
            return response.json()
            
        collected_data = {}
        for endpoint_name, endpoint_config in self.endpoints.items():
            url = urljoin(self.base_url, endpoint_config['path'])
            method = endpoint_config.get('method', 'GET')
            params = endpoint_config.get('params', {})
            
            logger.info(f"Obteniendo datos de {url}")
            response = self.session.request(method, url, params=params)
            response.raise_for_status()
            
            collected_data[endpoint_name] = response.json()
            
        return collected_data 