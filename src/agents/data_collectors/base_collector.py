from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from src.core.base_agent import BaseAgent
from src.core.error_handling import handle_error

@dataclass
class CollectorMetadata:
    source_name: str
    collection_timestamp: datetime
    records_count: int
    status: str
    error_message: Optional[str] = None

class BaseDataCollector(BaseAgent):
    """Clase base para todos los colectores de datos"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.source_name = config.get('source_name', 'unknown')
        self.retry_attempts = config.get('retry_attempts', 3)
        self.metadata: Optional[CollectorMetadata] = None

    @abstractmethod
    def connect(self) -> bool:
        """Establece conexión con la fuente de datos"""
        pass

    @abstractmethod
    def fetch_data(self) -> Dict[str, Any]:
        """Obtiene los datos de la fuente"""
        pass

    def process_input(self) -> Dict[str, Any]:
        """Procesa los datos recolectados"""
        try:
            if not self.connect():
                error_msg = "No se pudo conectar a la fuente de datos"
                handle_error(Exception(error_msg), error_msg)
                return self._create_error_response(error_msg)
            
            data = self.fetch_data()
            
            self.metadata = CollectorMetadata(
                source_name=self.source_name,
                collection_timestamp=datetime.now(),
                records_count=len(data) if isinstance(data, (list, dict)) else 0,
                status="success"
            )
            
            return {
                "data": data,
                "metadata": self.metadata.__dict__
            }
            
        except Exception as e:
            error_msg = f"Error en la recolección de datos: {str(e)}"
            handle_error(e, error_msg)
            return self._create_error_response(error_msg)

    def _create_error_response(self, error_msg: str) -> Dict[str, Any]:
        self.metadata = CollectorMetadata(
            source_name=self.source_name,
            collection_timestamp=datetime.now(),
            records_count=0,
            status="error",
            error_message=error_msg
        )
        return {
            "data": {},
            "metadata": self.metadata.__dict__
        } 