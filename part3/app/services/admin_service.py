from app.models.user import User
from app import db

class AdminService:
    @staticmethod
    def create_user(data):
        user = User(
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return user
