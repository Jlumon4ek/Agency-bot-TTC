from dao import BaseDAO
from .models import User

class UserService(BaseDAO[User]):
    model = User

user_service = UserService()