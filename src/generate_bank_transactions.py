"""Script principal para gerar dados de transações bancárias."""
from datetime import datetime, timedelta
import pandas as pd

from src.data_generators.bank_transaction_generator import BankTransactionGenerator
from src.utils.constants import DEFAULT_DAYS_BACK

def main():
    """Função principal que gera e salva os dados de transações."""
    # Define o período de transações
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DEFAULT_DAYS_BACK)
    
    # Inicializa o gerador
    generator = BankTransactionGenerator()
    
    # Gera as transações
    transactions = generator.generate_transactions(start_date, end_date)
    
    # Converte para DataFrame
    df = pd.DataFrame([vars(t) for t in transactions])
    
    # Ordena por data
    df = df.sort_values("date")
    
    # Salva em CSV
    output_file = "bank_transactions.csv"
    df.to_csv(output_file, index=False)
    print(f"Dados salvos em {output_file}")
    print(f"Total de transações geradas: {len(transactions)}")

if __name__ == "__main__":
    main() 