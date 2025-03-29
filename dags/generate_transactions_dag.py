"""DAG para gerar dados de transações bancárias diariamente."""
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

from src.data_generators.transactions import generate_transactions

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
    dag_id='generate_transactions',
    default_args=default_args,
    description='Gera dados de transações bancárias diariamente',
    schedule_interval='0 0 * * *',  # Executa todo dia à meia-noite
    start_date=days_ago(1),
    tags=['transactions', 'data_generation'],
)
def generate_transactions_dag():
    """DAG para geração de transações."""
    generate_transactions_task = PythonOperator(
        task_id='generate_transactions',
        python_callable=generate_transactions,
    )

# Cria a DAG
dag = generate_transactions_dag() 