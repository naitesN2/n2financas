import streamlit as st
from controllers.transaction_controller import save_transaction, get_transactions
from models.transaction import Transaction

def show_transactions():
    st.title("Gerenciar Transações")
    
    # Formulário para adicionar nova transação
    with st.form("new_transaction"):
        st.subheader("Nova Transação")
        date = st.date_input("Data")
        category = st.selectbox("Categoria", ["Alimentação", "Educação", "Cartões", "Transporte", "Moradia","Salário", "Saúde", "Lazer", "Investimento", "Outros"])
        description = st.text_input("Descrição")
        amount = st.number_input("Valor", step=0.01)
        transaction_type = st.selectbox("Tipo", ["Receita", "Despesa", "Investimento"])
        
        if st.form_submit_button("Adicionar Transação"):
            transaction = Transaction(date, category, description, amount, transaction_type)
            save_transaction(transaction, st.session_state['username'])
            st.success("Transação adicionada com sucesso!")
    
    # Exibir transações existentes
    st.subheader("Transações Existentes")
    transactions = get_transactions(st.session_state['username'])
    
    if not transactions.empty:
        st.dataframe(transactions)
    else:
        st.info("Ainda não há transações registradas.")