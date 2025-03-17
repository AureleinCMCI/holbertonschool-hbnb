class User:
    def __init__(self, id, email, password_hash, is_admin):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin

    def verify_password(self, password):
        # This is a dummy implementation; replace with real password verification
        return password == self.password_hash  # Simplified for the example

# Fake database of users
users_db = [
    User(id=1, email="john.doe@example.com", password_hash="password123", is_admin=False),
    User(id=2, email="admin@example.com", password_hash="adminpassword", is_admin=True)
]

def get_user_by_email(email):
    # Search the fake database for a user with the given email
    for user in users_db:
        if user.email == email:
            return user
    return None
