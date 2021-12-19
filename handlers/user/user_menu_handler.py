from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.dispatcher import FSMContext

import keyboards

from StateMachine import NewStateMachine
import config
import TGCalendar.telegramcalendar as tgcalendar
from aiogram import Dispatcher, types
from handlers.user.table_reserve_handler import TableReserveStateMachine


async def reserve(message: types.Message, state: FSMContext):
    calendar_keyboard = tgcalendar.create_calendar()
    await message.answer("Пожалуйста, выберите дату:", reply_markup=calendar_keyboard)
    # await state.set_state(TableReserveStateMachine.main_state.set())


# функция перехода в режим админа
async def set_admin_state(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in config.ADMIN_IDS:
        admin_kb = keyboards.admin_keyboard()
        await state.set_state(NewStateMachine.ADMIN)  # set admin state
        await message.answer("Вы вошли в режим админа", reply_markup=admin_kb)
    else:
        await message.answer("Эта функция недоступна для вас")


def register_user_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(set_admin_state, commands=['admin'])
    dp.register_message_handler(reserve, lambda m: m.text.startswith('🪑Забронировать столик'))
    dp.register_message_handler(reserve, commands=['reserve'])

