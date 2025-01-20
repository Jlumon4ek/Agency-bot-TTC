from aiogram import (
    F,
    types,
    Bot,
    Router
)
from aiogram.fsm.context import FSMContext
from config import settings
from aiogram.filters import Command, CommandObject
from aiogram.types.message import ContentType
from users import UserRequest, UserFilter
from agents.supervisor import super_visor

bot = Bot(token=settings.BOT_TOKEN)

router = Router()

@router.message(Command("start"), UserFilter())
async def start(message: types.Message, command: CommandObject, state: FSMContext):
    await message.answer(
        "Привет, это бот для Тестового задания в TTC, отправьте задание для обработки", 
    )
    await state.set_state(UserRequest.request)


@router.message(UserRequest.request, UserFilter())
async def request(message: types.Message, state: FSMContext):
    userMessage = message.text
    
    await message.answer("Задание принято на обработку")

    best_variant = await super_visor.process_task(userMessage)
    
    await message.answer(best_variant)

    await state.clear()
    