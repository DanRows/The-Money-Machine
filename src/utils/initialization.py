import os
from dotenv import load_dotenv
from pathlib import Path
import yaml
from src.engines.inference.provider_manager import InferenceProviderManager

def load_config():
    """Carga la configuración inicial"""
    # Cargar variables de entorno
    load_dotenv()
    
    config = {}
    
    # Cargar configuración por defecto
    default_config_path = Path("config/default_config.yaml")
    if default_config_path.exists():
        with open(default_config_path) as f:
            config = yaml.safe_load(f)
    
    # Cargar configuración de proveedores de inferencia
    inference_config_path = Path("config/inference_providers.yaml")
    if inference_config_path.exists():
        with open(inference_config_path) as f:
            config['inference_providers'] = yaml.safe_load(f)
    else:
        # Copiar el archivo de ejemplo si no existe
        example_path = Path("config/inference_providers.example.yaml")
        if example_path.exists():
            import shutil
            shutil.copy(example_path, inference_config_path)
            with open(inference_config_path) as f:
                config['inference_providers'] = yaml.safe_load(f)
    
    return config

def ensure_directories():
    """Asegura que existan los directorios necesarios"""
    directories = [
        "logs",
        "data/metrics",
        "data/cache",
        "config"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def initialize_app():
    """Inicializa la aplicación"""
    try:
        # Asegurar directorios
        ensure_directories()
        
        # Cargar configuración
        config = load_config()
        
        # Inicializar gestor de proveedores
        provider_manager = InferenceProviderManager(config.get('inference_providers', {}))
        
        return {
            'config': config,
            'provider_manager': provider_manager,
            'initialized': True
        }
        
    except Exception as e:
        print(f"Error durante la inicialización: {str(e)}")
        return {
            'config': {},
            'provider_manager': None,
            'initialized': False,
            'error': str(e)
        } 