from datetime import datetime
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from api import get_tasks
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.inline import get_callback_btns
from keyboards.reply import get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


class AddTask(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        'AddTask:name': 'Введите название заново:',
        'AddTask:description': 'Введите описание заново:',
        'AddTask:price': 'Введите стоимость заново:',
        'AddTask:image': 'Этот стейт последний, поэтому...',
    }


@admin_router.message(F.text == "Список задач")
async def tasks(message: types.Message, session: AsyncSession):
    await message.answer('погоди секунду')
    try:
        tasks = await get_tasks(session, message)
    except:
        await message.answer(f"Ошибка при получении данных. Проверьте ваши права доступа.")
    print(tasks)
    for task in tasks:
        await message.answer(
            f"\
            id: {task['id']}\n\
            Название: {task['name']}\n\
            Описание: {task['description']}\n\
            Статус: {task['status']}\n\
            Автор: {task['author']}\n\
            Исполнитель: {task['executor']}\n\
            Метки: {task['labels'] if task['labels'] != [] else 0 }\n\
            Дата создания: {datetime.fromisoformat(task['created_at']).strftime('%d.%m.%Y %H:%M')}",
            # reply_markup=get_callback_btns(
            #     btns={
            #         "Удалить": f"delete_{task['id']}",
            #         "Изменить": f"change_{task['id']}",
            #     }
            # ),
        )
    await message.answer("ОК, вот список задач ⏫")


# @admin_router.callback_query(F.data.startswith('delete_'))
# async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    
#     product_id = callback.data.split("_")[-1]
#     await orm_delete_product(session, int(product_id))
    
#     await callback.answer("Товар удален")
#     await callback.message.answer("Товар удален")

# #Код ниже для машины состояний (FSM)

# @admin_router.callback_query(StateFilter(None), F.data.startswith('change_'))
# async def change_product_callback(
#     callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
#     product_id = callback.data.split("_")[-1]

#     product_for_change = await orm_get_product(session, int(product_id))

#     AddTask.product_for_change = product_for_change

#     await callback.answer()
#     await callback.message.answer(
#         "Введите название задачи", reply_markup=types.ReplyKeyboardRemove()
#     )
#     await state.set_state(AddTask.name)


# @admin_router.message(StateFilter(None), F.text == "Добавить задачу")
# async def add_task(message: types.Message, state: FSMContext):
#     await message.answer(
#         "Введите название задачи", reply_markup=types.ReplyKeyboardRemove()
#     )
#     await state.set_state(AddTask.name)


# @admin_router.message(StateFilter('*'), Command("отмена"))
# @admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
# async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    
#     current_state = await state.get_state()
#     if current_state is None:
#         return
    
#     await state.clear()
#     await message.answer("Действия отменены", reply_markup=ADMIN_KB)


# @admin_router.message(StateFilter('*'), Command("назад"))
# @admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
# async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    
#     current_state = await state.get_state()
    
#     if current_state == AddTask.name:
#         await message.answer('Предидущего шага нет, или введите название товара или напишите "отмена"')
#         return

#     previous = None
#     for step in AddTask.__all_states__:
#         if step.state == current_state:
#             await state.set_state(previous)
#             await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddTask.texts[previous.state]}")
#             return
#         previous = step
    
#     await message.answer(f"ок, вы вернулись к прошлому шагу")

# @admin_router.message(AddTask.name, F.text)
# async def add_name(message: types.Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Введите описание задачи")
#     await state.set_state(AddTask.description)

# #Хендлер для отлова некорректных вводов для состояния name
# # @admin_router.message(AddTask.name)
# # async def add_name2(message: types.Message, state: FSMContext):
# #     await message.answer("Вы ввели не допустимые данные, введите текст названия товара")


# @admin_router.message(AddTask.description, F.text)
# async def add_description(message: types.Message, state: FSMContext):
#     await state.update_data(description=message.text)
#     await message.answer("Введите стоимость задачу")
#     await state.set_state(AddTask.price)


# @admin_router.message(AddTask.price, F.text)
# async def add_price(message: types.Message, state: FSMContext):
#     await state.update_data(price=message.text)
#     await message.answer("Загрузите изображение задачи")
#     await state.set_state(AddTask.image)


# @admin_router.message(AddTask.image, F.photo)
# async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
#     await state.update_data(image=message.photo[-1].file_id)
#     data = await state.get_data()
#     try:
#         await orm_add_product(session, data)
#         await message.answer("задача добавлена", reply_markup=ADMIN_KB)
#         await state.clear()

#     except:
#         await message.answer(f"Error")
#         await state.clear()