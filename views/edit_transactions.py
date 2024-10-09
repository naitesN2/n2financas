import streamlit as st
import pandas as pd
from controllers.transaction_controller import get_transactions, update_transaction, delete_transaction
from models.transaction import Transaction

def show_edit_transactions():
    st.title("Alterar ou Excluir Transações")

    # Obter transações existentes
    transactions = get_transactions(st.session_state['username'])

    if not transactions.empty:
        # Mostrar todas as transações em uma tabela
        st.subheader("Transações Existentes")
        st.dataframe(transactions)

        # Seleção da transação para editar ou excluir
        transaction_index = st.number_input("Selecione o índice da transação para editar ou excluir:", 
                                            min_value=0, 
                                            max_value=len(transactions)-1, 
                                            value=0)

        selected_transaction = transactions.iloc[transaction_index]

        # Formulário para editar a transação selecionada
        with st.form("edit_transaction"):
            st.subheader(f"Editar Transação {transaction_index}")
            date = st.date_input("Data", pd.to_datetime(selected_transaction['Data']))
            category = st.selectbox("Categoria", ["Alimentação", "Educação", "Cartões", "Transporte", "Moradia","Salário", "Saúde", "Lazer", "Investimento", "Outros"], index=["Alimentação", "Educação", "Cartões", "Transporte", "Moradia","Salário", "Saúde", "Lazer", "Investimento", "Outros"].index(selected_transaction['Categoria']))
            description = st.text_input("Descrição", selected_transaction['Descrição'])
            amount = st.number_input("Valor", value=abs(float(selected_transaction['Valor'])), step=0.01)
            transaction_type = st.selectbox("Tipo", ["Receita", "Despesa", "Investimento"], index=["Receita", "Despesa", "Investimento"].index(selected_transaction['Tipo']))

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Atualizar Transação"):
                    transaction = Transaction(date, category, description, amount, transaction_type)
                    update_transaction(transaction_index, transaction, st.session_state['username'])
                    st.success("Transação atualizada com sucesso!")
                    st.rerun()
            
            with col2:
                if st.form_submit_button("Excluir Transação"):
                    delete_transaction(transaction_index, st.session_state['username'])
                    st.success("Transação excluída com sucesso!")
                    st.rerun()

    else:
        st.info("Ainda não há transações registradas.")