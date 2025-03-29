"""Gerador de dados de transações bancárias."""
import random
from datetime import datetime, timedelta
from typing import List

from src.models.transaction import Transaction
from src.utils.constants import (
    TRANSACTION_TYPES,
    CATEGORIES,
    DEFAULT_NUM_ACCOUNTS,
    DEFAULT_TRANSACTIONS_PER_DAY,
    DEFAULT_AMOUNT_MIN,
    DEFAULT_AMOUNT_MAX,
)

class BankTransactionGenerator:
    """Classe responsável por gerar dados de transações bancárias."""

    def __init__(
        self,
        num_accounts: int = DEFAULT_NUM_ACCOUNTS,
        transactions_per_day: int = DEFAULT_TRANSACTIONS_PER_DAY,
        amount_min: float = DEFAULT_AMOUNT_MIN,
        amount_max: float = DEFAULT_AMOUNT_MAX,
    ):
        """Inicializa o gerador com os parâmetros especificados."""
        self.num_accounts = num_accounts
        self.transactions_per_day = transactions_per_day
        self.amount_min = amount_min
        self.amount_max = amount_max

    def generate_transaction(
        self,
        date: datetime,
        transaction_id: int,
        account_id: int
    ) -> Transaction:
        """Gera uma transação bancária aleatória."""
        amount = round(random.uniform(self.amount_min, self.amount_max), 2)
        transaction_type = random.choice(TRANSACTION_TYPES)
        category = random.choice(CATEGORIES)
        
        return Transaction(
            transaction_id=transaction_id,
            account_id=account_id,
            date=date,
            amount=amount,
            type=transaction_type,
            category=category
        )

    def generate_transactions(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Transaction]:
        """Gera uma lista de transações bancárias para múltiplas contas."""
        transactions = []
        transaction_id = 1
        
        current_date = start_date
        while current_date <= end_date:
            for account_id in range(1, self.num_accounts + 1):
                # Gera um número aleatório de transações por dia para cada conta
                num_transactions = random.randint(1, self.transactions_per_day)
                
                for _ in range(num_transactions):
                    # Gera um horário aleatório para o dia
                    random_hour = random.randint(0, 23)
                    random_minute = random.randint(0, 59)
                    transaction_time = current_date.replace(
                        hour=random_hour,
                        minute=random_minute
                    )
                    
                    transaction = self.generate_transaction(
                        transaction_time,
                        transaction_id,
                        account_id
                    )
                    transactions.append(transaction)
                    transaction_id += 1
            
            current_date += timedelta(days=1)
        
        return transactions 