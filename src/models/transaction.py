"""Modelo de dados para transações bancárias."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Transaction:
    """Classe que representa uma transação bancária."""
    transaction_id: int
    account_id: int
    date: datetime
    amount: float
    type: str
    category: str
    description: Optional[str] = None

    def __post_init__(self):
        """Inicializa a descrição se não fornecida."""
        if self.description is None:
            self.description = f"{self.type} - {self.category}" 