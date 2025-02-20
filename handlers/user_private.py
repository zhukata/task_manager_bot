import os
from aiogram import F, Bot, Router, types
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from api import add_user, auth_user, check_user
from filters.chat_types import ChatTypeFilter
from keyboards import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))
PUBLIC_URL = os.getenv('PUBLIC_URL', '')

LOGIN_KB = reply.get_keyboard(
    "Добавить задачу",
    "Список задач",
    placeholder="Выберите действие",
    sizes=(1, 1),
)


class AddUser(StatesGroup):
    username = State()
    password = State()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    await message.answer(
        "Привет, я твой помощник",
        reply_markup=reply.start_kb.as_markup()
        )


@user_private_router.message(or_f(Command('about'), F.text.contains("О боте")))
async def about(message: types.Message):
    await message.answer(f"Я бот менеджер задач.\n\
Если вы хотите узнать больше перейдите по ссылке:\n\
{PUBLIC_URL}")


# Код машины состояний:

@user_private_router.message(
    StateFilter(None),
    or_f(Command('login'), F.text.contains("Авторизация"))
    )
async def login(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите логин", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddUser.username)


@user_private_router.message(AddUser.username, F.text)
async def add_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Введите пароль")
    await state.set_state(AddUser.password)
    
    
@user_private_router.message(AddUser.password, F.text)
async def add_password(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(password=message.text)
    data = await state.get_data()
    try:
        await auth_user(session, message, data)
        await message.answer("Что хотите сделать?", reply_markup=LOGIN_KB)
        await state.clear()
    except:
        await message.answer(f"Ошибка авторизации")
        await state.clear()

# @user_private_router.message(F.text)
# async def echo(message: types.Message):
#     await message.answer("Не понял...")