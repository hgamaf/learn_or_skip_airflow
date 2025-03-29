"""DAG para gerar dados de transações bancárias diariamente."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from src.data_generators.bank_transaction_generator import BankTransactionGenerator
from src.utils.constants import DEFAULT_DAYS_BACK

# Argumentos padrão da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_transactions():
    """Função que gera as transações e salva em CSV."""
    # Define o período de transações (últimos 30 dias)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DEFAULT_DAYS_BACK)
    
    # Inicializa o gerador
    generator = BankTransactionGenerator()
    
    # Gera as transações
    transactions = generator.generate_transactions(start_date, end_date)
    
    # Converte para DataFrame
    import pandas as pd
    df = pd.DataFrame([vars(t) for t in transactions])
    
    # Ordena por data
    df = df.sort_values("date")
    
    # Salva em CSV
    output_file = "bank_transactions.csv"
    df.to_csv(output_file, index=False)
    print(f"Dados salvos em {output_file}")
    print(f"Total de transações geradas: {len(transactions)}")

# Define a DAG
dag = DAG(
    'generate_transactions',
    default_args=default_args,
    description='Gera dados de transações bancárias diariamente',
    schedule_interval='0 0 * * *',  # Executa todo dia à meia-noite
    start_date=days_ago(1),
    tags=['transactions', 'data_generation'],
)

# Define a task
generate_transactions_task = PythonOperator(
    task_id='generate_transactions',
    python_callable=generate_transactions,
    dag=dag,
)

# Define o fluxo da DAG
generate_transactions_task 