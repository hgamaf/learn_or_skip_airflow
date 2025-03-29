"""Script para gerar dados de transações bancárias."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path

# Configurações
NUM_TRANSACTIONS = 1000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 3, 1)

# Categorias e tipos de transação
CATEGORIES = [
    'Alimentação', 'Transporte', 'Moradia', 'Saúde', 'Educação',
    'Lazer', 'Vestuário', 'Serviços', 'Outros'
]

TRANSACTION_TYPES = ['Receita', 'Despesa']

# Gera dados aleatórios
np.random.seed(42)
random.seed(42)

# Gera datas aleatórias
dates = [START_DATE + timedelta(days=x) for x in range((END_DATE - START_DATE).days + 1)]
transaction_dates = [random.choice(dates) for _ in range(NUM_TRANSACTIONS)]

# Gera outros campos
data = {
    'date': transaction_dates,
    'description': [f'Transação {i+1}' for i in range(NUM_TRANSACTIONS)],
    'amount': np.random.uniform(10, 1000, NUM_TRANSACTIONS),
    'category': [random.choice(CATEGORIES) for _ in range(NUM_TRANSACTIONS)],
    'type': [random.choice(TRANSACTION_TYPES) for _ in range(NUM_TRANSACTIONS)]
}

# Cria DataFrame
df = pd.DataFrame(data)

# Ajusta valores negativos para despesas
df.loc[df['type'] == 'Despesa', 'amount'] = -df.loc[df['type'] == 'Despesa', 'amount']

# Ordena por data
df = df.sort_values('date')

# Cria diretório de dados se não existir
data_dir = Path(__file__).parent.parent.parent / 'data'
data_dir.mkdir(exist_ok=True)

# Salva em CSV
output_file = data_dir / 'transactions.csv'
df.to_csv(output_file, index=False)
print(f"Dados gerados e salvos em: {output_file}") 