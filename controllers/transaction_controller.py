import pandas as pd
import os
from models.transaction import Transaction

def save_transaction(transaction: Transaction, username: str):
    filename = f"data/{username}_transactions.csv"
    
    
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor', 'Tipo'])
    
    # Ajuste o valor para negativo se for uma despesa
    amount = transaction.amount if transaction.type != 'Despesa' else -transaction.amount
    
    new_row = pd.DataFrame({
        'Data': [transaction.date],
        'Categoria': [transaction.category],
        'Descrição': [transaction.description],
        'Valor': [amount],  # Usando o valor ajustado
        'Tipo': [transaction.type]
    })
    
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(filename, index=False)

def get_transactions(username: str):
    filename = f"data/{username}_transactions.csv"
    
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor', 'Tipo'])

def update_transaction(index: int, transaction: Transaction, username: str):
    filename = f"data/{username}_transactions.csv"
    df = pd.read_csv(filename)
    
    # Ajuste o valor para negativo se for uma despesa
    amount = transaction.amount if transaction.type != 'Despesa' else -transaction.amount
    
    df.loc[index, 'Data'] = transaction.date
    df.loc[index, 'Categoria'] = transaction.category
    df.loc[index, 'Descrição'] = transaction.description
    df.loc[index, 'Valor'] = amount  # Usando o valor ajustado
    df.loc[index, 'Tipo'] = transaction.type
    
    df.to_csv(filename, index=False)

def delete_transaction(index: int, username: str):
    filename = f"data/{username}_transactions.csv"
    df = pd.read_csv(filename)
    
    df = df.drop(index)
    df = df.reset_index(drop=True)
    
    df.to_csv(filename, index=False)

def calculate_balances(username: str):
    df = get_transactions(username)
    
    receita = df[df['Tipo'] == 'Receita']['Valor'].sum()
    investmento = df[df['Tipo'] == 'Investimento']['Valor'].sum()
    despesa = df[df['Tipo'] == 'Despesa']['Valor'].sum()
    saldo_utill = receita - (despesa * -1) - investmento
    patrimonio = saldo_utill + investmento

    return {
        'receita': receita,
        'despesa': despesa,
        'investimento': investmento,
        'saldo_util': saldo_utill,
        'patrimonio' : patrimonio
    }