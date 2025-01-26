from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.keyboard import main_keyboard, category_keyboard, description_keyboard, time_period_keyboard
import asyncio

from app.db  import add_expense, show_expenses_this_month


router = Router()

class AddToExpense(StatesGroup):
    category = State()
    price = State()
    description = State()

@router.message(CommandStart())
async def get_started(message: Message):
    await message.answer('Привет, давай начнем распределять деньги правильно!', reply_markup=main_keyboard.as_markup())

expense = {}
@router.callback_query(F.data == 'add')
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    expense[callback.from_user.id] = {}
    await callback.message.answer('Выберите категорию траты', reply_markup=category_keyboard.as_markup())

@router.callback_query(F.data.in_(['fastfood', 'groceries', 'restaurants', 'marketplace', 'entertainment', 'other']))
async def choosing_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    category = callback.data
    expense[callback.from_user.id]['category'] = category
    await state.set_state(AddToExpense.price)
    await callback.message.answer('Введите сумму траты')


@router.message(AddToExpense.price)
async def calc_price(message: Message, state: FSMContext):
    price = float(message.text)
    expense[message.from_user.id]['price'] = price
    await state.set_state(AddToExpense.description)
    await message.answer('Опишите покупку (опционально)', reply_markup=description_keyboard.as_markup())


@router.message(AddToExpense.description)
async def get_description(message: Message):
    description = message.text
    expense[message.from_user.id]['description'] = description
    await message.answer('Описание добавлено')
    await asyncio.get_event_loop().run_in_executor(None, add_expense, message.from_user.id, expense[message.from_user.id]['category'],
                                                   expense[message.from_user.id]['price'], expense[message.from_user.id]['description'])
    await get_started(message)


@router.callback_query(F.data == 'skip')
async def skip_of_description(callback: CallbackQuery, state: FSMContext):
    await callback.answer('описание не задано')
    expense[callback.from_user.id]['description'] = ''
    await asyncio.get_event_loop().run_in_executor(None, add_expense, callback.from_user.id,
                                                   expense[callback.from_user.id]['category'],
                                                   expense[callback.from_user.id]['price'],
                                                   expense[callback.from_user.id]['description'])
    await get_started(callback.message)



@router.callback_query(F.data == 'watch')
async def show_exp(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Выберите период:', reply_markup=time_period_keyboard.as_markup())



@router.callback_query(F.data == 'this_month')
async def show_this_month(callback: CallbackQuery):
    await callback.answer()
    all_exp = show_expenses_this_month(callback.from_user.id)
    await callback.message.answer(f'Вот ваши добавленные траты: {all_exp}')
