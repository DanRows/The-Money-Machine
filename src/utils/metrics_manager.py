from typing import Dict, Any
import json
from datetime import datetime

class MetricsManager:
    def __init__(self):
        self.metrics = {
            'tokens_used': 0,
            'total_cost': 0.0,
            'workflows_executed': 0,
            'last_updated': None
        }
    
    def update_metrics(self, workflow_metrics: Dict[str, Any]):
        self.metrics['tokens_used'] += workflow_metrics.get('total_tokens', 0)
        self.metrics['total_cost'] += workflow_metrics.get('total_cost', 0.0)
        self.metrics['workflows_executed'] += 1
        self.metrics['last_updated'] = datetime.now().isoformat()
    
    def get_metrics_display(self) -> Dict[str, str]:
        return {
            "Tokens Consumidos": f"{self.metrics['tokens_used']:,}",
            "Costo Total": f"${self.metrics['total_cost']:.2f}",
            "Workflows Ejecutados": str(self.metrics['workflows_executed'])
        }
    
    def save_metrics(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(self.metrics, f)
    
    @classmethod
    def load_metrics(cls, filepath: str):
        instance = cls()
        try:
            with open(filepath, 'r') as f:
                instance.metrics = json.load(f)
        except FileNotFoundError:
            pass
        return instance 