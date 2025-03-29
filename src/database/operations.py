"""Operações de banco de dados."""
import pandas as pd
from pathlib import Path
from src.database.db_manager import DatabaseManager

def save_transactions_to_db() -> None:
    """Lê o CSV e salva no banco de dados."""
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