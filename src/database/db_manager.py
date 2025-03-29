"""Gerenciador de banco de dados SQLite."""
import sqlite3
from pathlib import Path
from typing import List
import pandas as pd

from src.models.transaction import Transaction

class DatabaseManager:
    """Classe responsável por gerenciar operações no banco de dados SQLite."""

    def __init__(self, db_path: str = "bank_transactions.db"):
        """Inicializa o gerenciador de banco de dados."""
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """Cria as tabelas necessárias no banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Cria tabela de transações
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY,
                    account_id INTEGER NOT NULL,
                    date DATETIME NOT NULL,
                    amount REAL NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT
                )
            """)
            
            conn.commit()

    def save_transactions(self, transactions: List[Transaction]):
        """Salva uma lista de transações no banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            # Converte as transações para um DataFrame
            df = pd.DataFrame([vars(t) for t in transactions])
            
            # Salva no banco de dados
            df.to_sql('transactions', conn, if_exists='append', index=False)

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