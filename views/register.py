import streamlit as st
from controllers.auth_controller import save_user
from models.user import User

def show_register():
    st.title("Criar uma conta")
    
    with st.form("register_form"):
        new_username = st.text_input("Nome de usuário")
        new_name = st.text_input("Nome completo")
        new_email = st.text_input("Email")
        new_password = st.text_input("Senha", type="password")
        new_password_repeat = st.text_input("Repita a senha", type="password")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            submit_button = st.form_submit_button("Registrar")
        with col2:
            if st.form_submit_button("Voltar ao Login"):
                st.session_state['page'] = 'login'
                st.rerun()
        
        if submit_button:
            if new_password != new_password_repeat:
                st.error("As senhas não coincidem")
            else:
                try:
                    new_user = User(new_username, new_name, new_email, new_password)
                    save_user(new_user)
                    st.success("Usuário registrado com sucesso! Faça login para continuar.")
                    st.session_state['page'] = 'login'
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))