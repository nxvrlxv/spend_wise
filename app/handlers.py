from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.keyboard import main_keyboard, category_keyboard, description_keyboard


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


@router.callback_query(F.data == 'skip')
async def skip_of_description(callback: CallbackQuery, state: FSMContext):
    await callback.answer('описание не задано')
    expense[callback.from_user.id]['description'] = ''
    await get_started(callback.message)

