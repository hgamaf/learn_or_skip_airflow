"""Script para salvar dados de transações no banco de dados."""
import pandas as pd
from pathlib import Path
import sqlite3
from datetime import datetime

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
    
    # Cria conexão com o banco de dados
    db_path = data_dir / 'transactions.db'
    conn = sqlite3.connect(db_path)
    
    # Salva os dados
    df.to_sql('transactions', conn, if_exists='replace', index=False)
    
    # Fecha a conexão
    conn.close()
    
    print(f"Dados salvos com sucesso no banco de dados: {db_path}")

if __name__ == "__main__":
    save_to_database() 