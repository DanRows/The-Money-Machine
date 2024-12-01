from typing import Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum, auto
import asyncio
from src.core.logging_system import logger

class AgentStatus(Enum):
    IDLE = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()

@dataclass
class Agent:
    """Clase base para agentes automatizados"""
    id: str
    name: str
    service_type: str
    status: AgentStatus = field(default=AgentStatus.IDLE)
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Método de ejecución base para cada agente"""
        raise NotImplementedError("Cada agente debe implementar su propia lógica de ejecución")

class ContentOrchestrator:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.workflow_queue: asyncio.Queue = asyncio.Queue()
        self.workflow_order: List[str] = []
    
    def register_agent(self, agent: Agent):
        """Registra un nuevo agente en el sistema"""
        self.agents[agent.id] = agent
        logger.info(f"Agente registrado: {agent.name}")
    
    async def process_workflow(self, initial_context: Dict[str, Any]):
        """Procesa el flujo de trabajo a través de múltiples agentes"""
        context = initial_context.copy()
        
        for agent_id in self.workflow_order:
            agent = self.agents[agent_id]
            try:
                agent.status = AgentStatus.PROCESSING
                logger.info(f"Iniciando ejecución de agente: {agent.name}")
                context = await agent.execute(context)
                agent.status = AgentStatus.COMPLETED
                logger.info(f"Agente completado: {agent.name}")
            except Exception as e:
                agent.status = AgentStatus.ERROR
                logger.error(f"Error en agente {agent.name}: {e}")
                break
        
        return context
    
    def set_workflow_order(self, agent_ids: List[str]):
        """Establece el orden de ejecución de los agentes"""
        self.workflow_order = agent_ids
        logger.info(f"Orden de workflow establecido: {agent_ids}") 