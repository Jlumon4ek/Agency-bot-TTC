from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger
from dao import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username}, full_name={self.full_name})>"
    
    
    