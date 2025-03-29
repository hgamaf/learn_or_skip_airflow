"""DAG para salvar dados de transações no banco de dados."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from pathlib import Path

from src.database.db_manager import DatabaseManager
import pandas as pd

# Argumentos padrão da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def save_to_database():
    """Função que lê o CSV e salva no banco de dados."""
    # Caminho do arquivo CSV
    data_dir = Path("/usr/local/airflow/data")
    csv_file = data_dir / "transactions.csv"
    
    try:
        # Lê o CSV
        df = pd.read_csv(csv_file)
        
        # Converte a coluna de data para datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Inicializa o gerenciador de banco de dados
        db_manager = DatabaseManager()
        
        # Limpa transações antigas
        db_manager.clear_transactions()
        
        # Salva no banco de dados
        db_manager.save_transactions(df.to_dict('records'))
        
        # Verifica se os dados foram salvos corretamente
        df = db_manager.load_transactions()
        print(f"Dados salvos com sucesso no banco de dados!")
        print(f"Total de transações no banco: {len(df)}")
        
    except FileNotFoundError:
        raise Exception(f"Arquivo {csv_file} não encontrado! Execute primeiro a DAG generate_transactions.")
    except Exception as e:
        raise Exception(f"Erro ao processar os dados: {str(e)}")

# Define a DAG
dag = DAG(
    'save_to_database',
    default_args=default_args,
    description='Salva dados de transações no banco de dados',
    schedule_interval='0 1 * * *',  # Executa todo dia às 1h da manhã
    start_date=days_ago(1),
    tags=['transactions', 'database'],
)

# Define a task
save_to_database_task = PythonOperator(
    task_id='save_to_database',
    python_callable=save_to_database,
    dag=dag,
)

# Define o fluxo da DAG
save_to_database_task 