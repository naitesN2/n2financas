import streamlit as st
import plotly.express as px
from controllers.transaction_controller import get_transactions, calculate_balances
import pandas as pd

def show_dashboard():
    st.title("Dashboard")
    
    # Obter transações e calcular saldos
    transactions = get_transactions(st.session_state['username'])
    balances = calculate_balances(st.session_state['username'])

    
    # Exibir saldos e despesas em quatro cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Saldo Utilizável", f"R$ {balances['saldo_util']:.2f}")
    with col2:
        st.metric("Saldo de Investimentos", f"R$ {balances['investimento']:.2f}")
    with col3:
        total_expenses = transactions[transactions['Valor'] < 0]['Valor'].sum() if not transactions.empty else 0
        st.metric("Despesas Totais", f"R$ {abs(total_expenses):.2f}")
    with col4:
        st.metric("Patrimônio Total", f"R$ {balances['patrimonio']:.2f}")
    
    # Gráfico de pizza para distribuição de gastos por categoria
    if not transactions.empty:
        expenses = transactions[transactions['Valor'] < 0]
        expenses['Valor'] = abs(expenses['Valor'])
        if not expenses.empty:
            fig_pie = px.pie(expenses, values='Valor', names='Categoria', title='Distribuição de Gastos por Categoria')
            st.plotly_chart(fig_pie)
        else:
            st.info("Ainda não há despesas registradas.")
        
        # Gráfico de linha para evolução do saldo ao longo do tempo
        transactions['Data'] = pd.to_datetime(transactions['Data'])
        transactions = transactions.sort_values('Data')
        transactions['Saldo Acumulado'] = transactions['Valor'].cumsum()
        fig_line = px.line(transactions, x='Data', y='Saldo Acumulado', title='Evolução do Saldo ao Longo do Tempo')
        st.plotly_chart(fig_line)
    else:
        st.info("Ainda não há transações registradas.")
