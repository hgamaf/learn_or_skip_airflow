"""Script para gerar dados de transações bancárias."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

def generate_transactions(n_transactions=1000):
    # Cria diretório de dados se não existir
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Gera datas aleatórias
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, periods=n_transactions)
    
    # Lista de descrições comuns
    descriptions = [
        "Supermercado", "Restaurante", "Transporte", "Energia", "Água",
        "Internet", "Telefone", "Netflix", "Spotify", "Amazon",
        "Farmácia", "Posto de Gasolina", "Shopping", "Cinema", "Teatro",
        "Academia", "Médico", "Dentista", "Escola", "Faculdade"
    ]
    
    # Lista de categorias
    categories = [
        "Alimentação", "Moradia", "Transporte", "Saúde", "Educação",
        "Lazer", "Serviços", "Compras", "Outros"
    ]
    
    # Gera dados aleatórios
    data = {
        'date': dates,
        'description': np.random.choice(descriptions, n_transactions),
        'amount': np.random.normal(100, 50, n_transactions).round(2),
        'category': np.random.choice(categories, n_transactions),
        'type': np.random.choice(['credit', 'debit'], n_transactions)
    }
    
    # Cria DataFrame
    df = pd.DataFrame(data)
    
    # Ajusta valores negativos para débitos
    df.loc[df['type'] == 'debit', 'amount'] = -abs(df.loc[df['type'] == 'debit', 'amount'])
    df.loc[df['type'] == 'credit', 'amount'] = abs(df.loc[df['type'] == 'credit', 'amount'])
    
    # Salva em CSV
    csv_file = data_dir / 'transactions.csv'
    df.to_csv(csv_file, index=False)
    
    print(f"Dados gerados com sucesso: {csv_file}")
    print(f"Total de transações: {len(df)}")
    print(f"Período: {df['date'].min().strftime('%Y-%m-%d')} até {df['date'].max().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    generate_transactions() 