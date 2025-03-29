"""Script para salvar dados de transações no banco de dados."""
import pandas as pd
from pathlib import Path
import sqlite3
from datetime import datetime
from src.database.db_manager import DatabaseManager

def save_to_database():
    # Caminho do arquivo CSV
    data_dir = Path(__file__).parent.parent / 'data'
    csv_file = data_dir / 'transactions.csv'
    
    # Verifica se o arquivo existe
    if not csv_file.exists():
        print(f"Erro: Arquivo {csv_file} não encontrado.")
        print("Execute primeiro o script generate_transactions.py para gerar os dados.")
        return
    
    # Lê o CSV
    df = pd.read_csv(csv_file)
    
    # Converte a coluna de data para datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Inicializa o gerenciador de banco de dados
    db_manager = DatabaseManager()
    
    # Salva os dados
    db_manager.save_transactions(df.to_dict('records'))
    
    print(f"Dados salvos com sucesso no banco de dados: {db_manager.db_path}")

if __name__ == "__main__":
    save_to_database() 