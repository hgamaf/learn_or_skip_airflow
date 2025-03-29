"""DAG para gerar dados de transações bancárias diariamente."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from pathlib import Path
import pandas as pd
import numpy as np

# Argumentos padrão da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_transactions(n_transactions=1000):
    """Função que gera as transações e salva em CSV."""
    # Cria diretório de dados se não existir
    data_dir = Path("/usr/local/airflow/data")
    data_dir.mkdir(exist_ok=True)
    
    # Gera datas aleatórias
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, periods=n_transactions)
    
    # Lista de descrições comuns
    descriptions = [
        "Supermercado", "Restaurante", "Transporte", "Energia", "Água",
        "Internet", "Telefone", "Netflix", "Spotify", "Amazon",
        "Farmácia", "Posto de Gasolina", "Shopping", "Cinema", "Teatro",
        "Academia", "Médico", "Dentista", "Escola", "Faculdade"
    ]
    
    # Lista de categorias
    categories = [
        "Alimentação", "Moradia", "Transporte", "Saúde", "Educação",
        "Lazer", "Serviços", "Compras", "Outros"
    ]
    
    # Gera dados aleatórios
    data = {
        'date': dates,
        'description': np.random.choice(descriptions, n_transactions),
        'amount': np.random.normal(100, 50, n_transactions).round(2),
        'category': np.random.choice(categories, n_transactions),
        'type': np.random.choice(['credit', 'debit'], n_transactions)
    }
    
    # Cria DataFrame
    df = pd.DataFrame(data)
    
    # Ajusta valores negativos para débitos
    df.loc[df['type'] == 'debit', 'amount'] = -abs(df.loc[df['type'] == 'debit', 'amount'])
    df.loc[df['type'] == 'credit', 'amount'] = abs(df.loc[df['type'] == 'credit', 'amount'])
    
    # Salva em CSV
    csv_file = data_dir / 'transactions.csv'
    df.to_csv(csv_file, index=False)
    
    print(f"Dados gerados com sucesso: {csv_file}")
    print(f"Total de transações: {len(df)}")
    print(f"Período: {df['date'].min().strftime('%Y-%m-%d')} até {df['date'].max().strftime('%Y-%m-%d')}")

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