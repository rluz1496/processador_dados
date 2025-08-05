import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class MetricsDB:
    """Classe para salvar métricas no PostgreSQL silenciosamente"""
    
    def __init__(self):
        self.db_config = {
            'dbname': os.getenv("POSTGRES_DB"),
            'user': os.getenv("POSTGRES_USER"),
            'password': os.getenv("POSTGRES_PASSWORD"),
            'host': os.getenv("POSTGRES_HOST"),
            'port': os.getenv("POSTGRES_PORT", "5432")
        }
    
    def _get_connection(self):
        """Cria conexão com o PostgreSQL"""
        try:
            return psycopg2.connect(**self.db_config)
        except Exception:
            return None
    
    def salvar_metricas(self, metrics_data: Dict[str, Any]) -> bool:
        """
        Salva apenas as métricas essenciais no PostgreSQL
        """
        try:
            conn = self._get_connection()
            if not conn:
                return False
            
            cur = conn.cursor()
            
            # Extrair apenas os valores necessários
            detailed_analysis = metrics_data.get('detailed_analysis', {})
            
            input_tokens = detailed_analysis.get('input_tokens', 0)
            output_tokens = detailed_analysis.get('output_tokens', 0)
            total_tokens = detailed_analysis.get('total_tokens', 0)
            cached_tokens = detailed_analysis.get('cached_tokens', 0)
            model_name = metrics_data.get('model_name', '')
            agent_name = metrics_data.get('agent_name', '')
            reasoning_tokens = detailed_analysis.get('reasoning_tokens', 0)
            time_seconds = metrics_data.get('processing_time_seconds', 0)
            created_at = datetime.now()
            
            # Inserir apenas os campos necessários
            cur.execute("""
                INSERT INTO session_metrics (
                    input_tokens, output_tokens, total_tokens, 
                    reasoning_tokens, cached_tokens, time, 
                    model_name, agent_name, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                input_tokens, output_tokens, total_tokens,
                reasoning_tokens, cached_tokens, time_seconds,
                model_name, agent_name, created_at
            ))
            conn.commit()
            cur.close()
            conn.close()
            
            return True
            
        except Exception:
            return False

# Instância global
metrics_db = MetricsDB()