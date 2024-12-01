
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    @abstractmethod
    def validate_input(self) -> bool:
        pass
        
    @abstractmethod
    def process_input(self) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        pass
