"""Dashboard para visualização de transações bancárias."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
import sys

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.database.db_manager import DatabaseManager

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Transações",
    page_icon="💰",
    layout="wide"
)

# Título
st.title("📊 Dashboard de Transações Bancárias")

# Inicializa o banco de dados
db_manager = DatabaseManager()

# Carrega os dados
df = db_manager.load_transactions()

if df.empty:
    st.warning("Não há dados de transações disponíveis.")
else:
    # Converte a coluna de data para datetime e remove linhas com datas nulas
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    if df.empty:
        st.warning("Não há transações com datas válidas.")
    else:
        # Filtro de datas
        st.sidebar.header("Filtros")

        # Obtém as datas mínima e máxima do DataFrame
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()

        # Cria o widget de seleção de datas
        selected_date_range = st.sidebar.date_input(
            "Selecione o período",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        # Filtra os dados baseado na seleção
        if len(selected_date_range) == 2:
            start_date, end_date = selected_date_range
            mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
            filtered_df = df[mask]
        else:
            filtered_df = df

        # Métricas principais
        col1, col2, col3 = st.columns(3)

        with col1:
            total_transactions = len(filtered_df)
            st.metric("Total de Transações", total_transactions)

        with col2:
            total_amount = filtered_df['amount'].sum()
            st.metric("Valor Total", f"R$ {total_amount:,.2f}")

        with col3:
            avg_amount = filtered_df['amount'].mean()
            st.metric("Valor Médio", f"R$ {avg_amount:,.2f}")

        # Gráficos
        st.subheader("📈 Análise de Transações")

        # Gráfico de linha - Valor das transações ao longo do tempo
        fig_line = px.line(
            filtered_df,
            x='date',
            y='amount',
            title='Valor das Transações ao Longo do Tempo',
            labels={'date': 'Data', 'amount': 'Valor (R$)'}
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Gráfico de pizza - Distribuição por categoria
        fig_pie = px.pie(
            filtered_df,
            values='amount',
            names='category',
            title='Distribuição de Valores por Categoria'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Gráfico de barras - Total por tipo de transação
        fig_bar = px.bar(
            filtered_df.groupby('type')['amount'].sum().reset_index(),
            x='type',
            y='amount',
            title='Total por Tipo de Transação',
            labels={'type': 'Tipo', 'amount': 'Valor Total (R$)'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Tabela de dados
        st.subheader("📋 Detalhes das Transações")
        st.dataframe(
            filtered_df.sort_values('date', ascending=False),
            use_container_width=True
        ) 