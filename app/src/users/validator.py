from aiogram.filters import BaseFilter
from aiogram.types import Message
from .models import User
from .service import user_service

class UserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        telegram_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name

        user_filter = {"telegram_id": telegram_id}

        user_record = await user_service.find_one_or_none(user_filter)

        if user_record is None:
            new_user_data = {
                "telegram_id": telegram_id,
                "username": username,
                "full_name": full_name
            }
            await user_service.add(new_user_data)
            
        return True
