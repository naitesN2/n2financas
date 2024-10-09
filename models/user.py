class User:
    def __init__(self, username: str, name: str, email: str, password: str):
        self.username = username
        self.name = name
        self.email = email
        self.password = password

    def __str__(self):
        return f"User(username={self.username}, name={self.name}, email={self.email})"