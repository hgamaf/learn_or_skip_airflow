"""DAG para salvar dados de transações no banco de dados."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from src.database.db_manager import DatabaseManager
from src.models.transaction import Transaction
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

def csv_to_transactions(csv_path: str) -> list[Transaction]:
    """Converte dados do CSV para objetos Transaction."""
    df = pd.read_csv(csv_path)
    transactions = []
    
    for _, row in df.iterrows():
        transaction = Transaction(
            transaction_id=row['transaction_id'],
            account_id=row['account_id'],
            date=datetime.fromisoformat(row['date']),
            amount=row['amount'],
            type=row['type'],
            category=row['category'],
            description=row['description']
        )
        transactions.append(transaction)
    
    return transactions

def save_to_database():
    """Função que lê o CSV e salva no banco de dados."""
    # Caminho do arquivo CSV
    csv_path = "bank_transactions.csv"
    
    # Inicializa o gerenciador de banco de dados
    db_manager = DatabaseManager()
    
    try:
        # Lê as transações do CSV
        transactions = csv_to_transactions(csv_path)
        
        # Limpa transações antigas
        db_manager.clear_transactions()
        
        # Salva no banco de dados
        db_manager.save_transactions(transactions)
        
        # Verifica se os dados foram salvos corretamente
        df = db_manager.load_transactions()
        print(f"Dados salvos com sucesso no banco de dados!")
        print(f"Total de transações no banco: {len(df)}")
        
    except FileNotFoundError:
        raise Exception(f"Arquivo {csv_path} não encontrado! Execute primeiro a DAG generate_transactions.")
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