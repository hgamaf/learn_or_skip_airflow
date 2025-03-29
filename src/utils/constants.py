"""Constantes utilizadas no projeto."""

TRANSACTION_TYPES = [
    "Transferência",
    "Pagamento",
    "Depósito",
    "Saque",
    "Pix",
    "Cartão de Crédito",
    "Cartão de Débito"
]

CATEGORIES = [
    "Alimentação",
    "Transporte",
    "Moradia",
    "Saúde",
    "Educação",
    "Entretenimento",
    "Serviços",
    "Outros"
]

# Configurações padrão
DEFAULT_NUM_ACCOUNTS = 5
DEFAULT_TRANSACTIONS_PER_DAY = 10
DEFAULT_AMOUNT_MIN = -5000
DEFAULT_AMOUNT_MAX = 5000
DEFAULT_DAYS_BACK = 30 