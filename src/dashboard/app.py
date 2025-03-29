"""Dashboard para visualização de transações bancárias."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
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

# Carrega os dados
db_manager = DatabaseManager()
df = db_manager.load_transactions()

# Filtro de data
col1, col2 = st.columns([1, 4])
with col1:
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    date_range = st.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

# Filtra os dados pelo período selecionado
if len(date_range) == 2:
    mask = (df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])
    df_filtered = df[mask]
else:
    df_filtered = df

# Métricas principais
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_transactions = len(df_filtered)
    st.metric("Total de Transações", total_transactions)

with col2:
    total_amount = df_filtered['amount'].sum()
    st.metric("Saldo Total", f"R$ {total_amount:,.2f}")

with col3:
    total_credits = df_filtered[df_filtered['type'] == 'credit']['amount'].abs().sum()
    st.metric("Total de Créditos", f"R$ {total_credits:,.2f}")

with col4:
    total_debits = df_filtered[df_filtered['type'] == 'debit']['amount'].abs().sum()
    st.metric("Total de Débitos", f"R$ {total_debits:,.2f}")

# Gráficos em duas colunas
col1, col2 = st.columns(2)

with col1:
    # Gráfico de evolução do saldo
    df_filtered['cumsum'] = df_filtered['amount'].cumsum()
    fig_balance = px.line(
        df_filtered,
        x='date',
        y='cumsum',
        title='Evolução do Saldo',
        height=300
    )
    fig_balance.update_layout(
        xaxis_title="Data",
        yaxis_title="Saldo Acumulado",
        showlegend=False
    )
    st.plotly_chart(fig_balance, use_container_width=True)

    # Gráfico de pizza de categorias
    category_data = df_filtered.groupby('category')['amount'].sum().reset_index()
    fig_categories = px.pie(
        category_data,
        values='amount',
        names='category',
        title='Distribuição por Categoria',
        height=300
    )
    st.plotly_chart(fig_categories, use_container_width=True)

with col2:
    # Gráfico de barras de transações por dia
    daily_transactions = df_filtered.groupby(df_filtered['date'].dt.date).size().reset_index()
    daily_transactions.columns = ['date', 'count']
    fig_daily = px.bar(
        daily_transactions,
        x='date',
        y='count',
        title='Transações por Dia',
        height=300
    )
    fig_daily.update_layout(
        xaxis_title="Data",
        yaxis_title="Número de Transações",
        showlegend=False
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    # Gráfico de barras de valores por categoria
    category_amounts = df_filtered.groupby('category')['amount'].sum().reset_index()
    fig_category_amounts = px.bar(
        category_amounts,
        x='category',
        y='amount',
        title='Valores por Categoria',
        height=300
    )
    fig_category_amounts.update_layout(
        xaxis_title="Categoria",
        yaxis_title="Valor Total",
        showlegend=False
    )
    st.plotly_chart(fig_category_amounts, use_container_width=True)

# Tabela de transações
st.subheader("Últimas Transações")
st.dataframe(
    df_filtered.sort_values('date', ascending=False).head(10),
    use_container_width=True,
    hide_index=True
) 