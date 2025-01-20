from aiogram.fsm.state import StatesGroup, State

class UserRequest(StatesGroup):
    request = State()