"""Gerenciador de banco de dados SQLite."""
import sqlite3
from pathlib import Path
from typing import List
import pandas as pd

class DatabaseManager:
    """Classe responsável por gerenciar operações no banco de dados SQLite."""

    def __init__(self):
        """Inicializa o gerenciador de banco de dados."""
        # Define o caminho do banco de dados
        data_dir = Path(__file__).parent.parent.parent / 'data'
        self.db_path = data_dir / 'transactions.db'
        self._create_tables()

    def _create_tables(self):
        """Cria as tabelas necessárias no banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Cria tabela de transações
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    date DATETIME NOT NULL,
                    description VARCHAR(255),
                    amount DECIMAL(10,2) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    type VARCHAR(10) NOT NULL
                )
            """)
            
            conn.commit()

    def save_transactions(self, transactions: List[dict]):
        """Salva uma lista de transações no banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            # Converte as transações para um DataFrame
            df = pd.DataFrame(transactions)
            
            # Garante que a coluna de data está no formato correto
            df['date'] = pd.to_datetime(df['date'])
            
            # Salva no banco de dados
            df.to_sql('transactions', conn, if_exists='replace', index=False)

    def load_transactions(self) -> pd.DataFrame:
        """Carrega todas as transações do banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query("SELECT * FROM transactions", conn)

    def clear_transactions(self):
        """Remove todas as transações do banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions")
            conn.commit() 