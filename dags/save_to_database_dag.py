"""DAG para salvar dados de transações no banco de dados."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.database.operations import save_transactions_to_db

# Argumentos padrão da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='save_to_database',
    default_args=default_args,
    description='Salva dados de transações no banco de dados',
    schedule_interval='0 1 * * *',  # Executa todo dia às 1h da manhã
    start_date=days_ago(1),
    tags=['transactions', 'database'],
)
def save_to_database_dag():
    """DAG para salvamento no banco de dados."""
    save_to_database_task = PythonOperator(
        task_id='save_to_database',
        python_callable=save_transactions_to_db,
    )

# Cria a DAG
dag = save_to_database_dag() 