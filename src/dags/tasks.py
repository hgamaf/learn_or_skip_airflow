"""Funções para as tasks das DAGs."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

def generate_transactions(n_transactions: int = 1000) -> None:
    """Gera dados de transações e salva em CSV."""
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

def save_to_database() -> None:
    """Lê o CSV e salva no banco de dados."""
    from src.database.db_manager import DatabaseManager
    
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