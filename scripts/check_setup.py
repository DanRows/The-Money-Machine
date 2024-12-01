import os
import sys
from pathlib import Path

def check_setup():
    """Verifica la configuración del proyecto"""
    required_files = [
        ".env",
        "config/inference_providers.yaml",
        "config/default_config.yaml"
    ]
    
    required_dirs = [
        "logs",
        "data/metrics",
        "data/cache",
        "config"
    ]
    
    # Verificar directorios
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"❌ Falta directorio: {directory}")
            return False
    
    # Verificar archivos
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Falta archivo: {file}")
            return False
    
    # Verificar variables de entorno
    required_env_vars = [
        "OPENAI_API_KEY",
        "GROQ_API_KEY",
        "ANTHROPIC_API_KEY"
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print("❌ Faltan variables de entorno:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    
    print("✅ Configuración correcta")
    return True

if __name__ == "__main__":
    if not check_setup():
        sys.exit(1) 