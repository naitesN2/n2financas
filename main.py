import streamlit as st
import yaml
from streamlit_authenticator import Authenticate
from controllers.auth_controller import load_users, save_user
from views.login import show_login
from views.register import show_register
from views.dashboard import show_dashboard
from views.transactions import show_transactions
from views.analysis import show_analysis
from streamlit_option_menu import option_menu
from views.edit_transactions import show_edit_transactions

st.set_page_config(page_title="Finanças Pessoais", layout="wide")

# Carregando o estilo personalizado
with open('styles/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Carregando configurações de autenticação
with open('config.yaml') as file:
    config = yaml.safe_load(file)

# Inicializando o autenticador
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Gerenciamento de sessão
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# Fluxo principal da aplicação
def main():
    if st.session_state['authentication_status']:
        # Usuário autenticado
        st.sidebar.title(f"Bem-vindo, {st.session_state['name']}!")
        
        # Menu de navegação atualizado
        with st.sidebar:
            selected = option_menu(
                "Menu Principal", 
                ["Dashboard", "Transações", "Alterar Transações", "Análise"],  # Adicionada nova opção
                icons=['house', 'currency-dollar', 'pencil-square', 'graph-up'],  # Adicionado novo ícone
                menu_icon="cast",
                default_index=0,
            )
        
        # Navegação baseada na seleção do menu
        if selected == "Dashboard":
            show_dashboard()
        elif selected == "Transações":
            show_transactions()
        elif selected == "Alterar Transações":  # Nova condição
            show_edit_transactions()
        elif selected == "Análise":
            show_analysis()
        
        # Botão de logout (mantido como estava)
        btn = authenticator.logout(button_name='Sair', location='sidebar')
        if btn:
            show_login(authenticator)
            st.rerun()
    else:
        # Usuário não autenticado
        if st.session_state['page'] == 'login':
            show_login(authenticator)
        elif st.session_state['page'] == 'register':
            show_register()

if __name__ == "__main__":
    main()