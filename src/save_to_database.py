"""Script para salvar dados do CSV no banco de dados SQLite."""
import pandas as pd
from datetime import datetime

from src.database.db_manager import DatabaseManager
from src.models.transaction import Transaction

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

def main():
    """Função principal que lê o CSV e salva no banco de dados."""
    # Caminho do arquivo CSV
    csv_path = "bank_transactions.csv"
    
    # Inicializa o gerenciador de banco de dados
    db_manager = DatabaseManager()
    
    try:
        # Lê as transações do CSV
        transactions = csv_to_transactions(csv_path)
        
        # Salva no banco de dados
        db_manager.save_transactions(transactions)
        
        # Verifica se os dados foram salvos corretamente
        df = db_manager.load_transactions()
        print(f"Dados salvos com sucesso no banco de dados!")
        print(f"Total de transações no banco: {len(df)}")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo {csv_path} não encontrado!")
        print("Execute primeiro o script generate_bank_transactions.py")
    except Exception as e:
        print(f"Erro ao processar os dados: {str(e)}")

if __name__ == "__main__":
    main() 