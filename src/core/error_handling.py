
from typing import Any
from .logging_system import logger

def handle_error(error: Exception, message: str) -> None:
    error_details = f"{message}: {str(error)}"
    logger.error(error_details)
    # Aquí puedes agregar más lógica de manejo de errores
