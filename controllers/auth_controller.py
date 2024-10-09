import yaml
import bcrypt
from models.user import User

def load_users():
    with open('config.yaml') as file:
        config = yaml.safe_load(file)
    return config['credentials']['usernames']

def save_user(user: User):
    users = load_users()
    
    # Verificar se o usuário já existe
    if user.username in users:
        raise ValueError("Nome de usuário já existe")
    
    # Criar hash da senha
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    
    # Adicionar novo usuário
    users[user.username] = {
        'email': user.email,
        'name': user.name,
        'password': hashed_password.decode()
    }
    
    # Salvar as alterações no arquivo YAML
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    config['credentials']['usernames'] = users
    
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)

def verify_password(username: str, password: str) -> bool:
    users = load_users()
    if username not in users:
        return False
    
    stored_password = users[username]['password'].encode()
    return bcrypt.checkpw(password.encode(), stored_password)