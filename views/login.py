import streamlit as st

def show_login(authenticator):
    st.header('Realize sua Autenticação', divider=True)
   
    # Inicializa as variáveis
    name = None
    authentication_status = None
    username = None

    # Login
    result = authenticator.login('main')
    if result is not None:
        name, authentication_status, username = result

    if authentication_status == False:
        st.error('Nome de usuário/senha incorretos')
    elif authentication_status == None:
        st.warning('Por favor, insira seu nome de usuário e senha')
    elif authentication_status:
        st.success(f'Bem-vindo *{name}*')
        st.session_state['name'] = name
        st.session_state['username'] = username
        st.session_state['authentication_status'] = True
   
    # Link para a página de registro
    col1, col2 = st.columns([2, 1])
    with col2:
        if st.button("Criar uma conta"):
            st.session_state['page'] = 'register'
            st.rerun()
