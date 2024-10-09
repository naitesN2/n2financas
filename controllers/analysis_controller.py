import pandas as pd
import plotly.express as px
from controllers.transaction_controller import get_transactions

def get_monthly_summary(username: str):
    df = get_transactions(username)
    df['Data'] = pd.to_datetime(df['Data'])
    df['Mês'] = df['Data'].dt.to_period('M')
    
    monthly_summary = df.groupby('Mês').agg({
        'Valor': 'sum'
    }).reset_index()
    monthly_summary['Mês'] = monthly_summary['Mês'].astype(str)
    
    return monthly_summary

def get_category_summary(username: str):
    df = get_transactions(username)
    category_summary = df.groupby('Categoria').agg({
        'Valor': 'sum'
    }).reset_index()
    
    return category_summary

def generate_monthly_chart(monthly_summary):
    fig = px.bar(monthly_summary, x='Mês', y='Valor', title='Resumo Mensal')
    return fig

def generate_category_chart(category_summary):
    fig = px.pie(category_summary, values='Valor', names='Categoria', title='Distribuição por Categoria')
    return fig

def get_financial_health(username: str, start_date=None, end_date=None):
    df = get_transactions(username)
    df['Data'] = pd.to_datetime(df['Data'])
    
    if start_date and end_date:
        df = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]
    
    receita = df[df['Tipo'] == 'Receita']['Valor'].sum()
    investmento = df[df['Tipo'] == 'Investimento']['Valor'].sum()
    despesa = df[df['Tipo'] == 'Despesa']['Valor'].sum()
    saldo_utill = receita - (despesa * -1) - investmento
    patrimonio = saldo_utill + investmento

    
    if receita == 0:
        savings_rate = 0
    else:
        savings_rate = (receita - abs(despesa)) / receita * 100
    
    return {
        'total_income': receita,
        'total_expenses': despesa,
        'savings_rate': savings_rate
    }