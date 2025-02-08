from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from app.keyboard import main_keyboard, category_keyboard, description_keyboard, time_period_keyboard, earn_keyboard, goals_keyboard, goal_detail_keyboard
import asyncio

from app.db  import add_expense, show_expenses_this_month, show_expenses_this_year, show_earnings_details, add_earns, show_earns, add_money_to_earn
from datetime import timedelta


router = Router()

class AddToExpense(StatesGroup):
    category = State()
    price = State()
    description = State()

class AddEarning(StatesGroup):
    goal = State()
    price_goal = State()


class AddMoney(StatesGroup):
    ad_mon = State()


@router.message(CommandStart())
async def get_started(message: Message):
    await message.answer('Привет, давай начнем распределять деньги правильно!', reply_markup=main_keyboard.as_markup())


# Добавление трат
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
                                                   expense[message.from_user.id]['price'], expense[message.from_user.id]['description'], message.date)
    await get_started(message)


@router.callback_query(F.data == 'skip')
async def skip_of_description(callback: CallbackQuery, state: FSMContext):
    await callback.answer('описание не задано')
    expense[callback.from_user.id]['description'] = ''
    await asyncio.get_event_loop().run_in_executor(None, add_expense, callback.from_user.id,
                                                   expense[callback.from_user.id]['category'],
                                                   expense[callback.from_user.id]['price'],
                                                   expense[callback.from_user.id]['description'], callback.message.date + timedelta(hours=3))

    await get_started(callback.message)



# Просмотр трат
@router.callback_query(F.data == 'watch')
async def show_exp(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Выберите период:', reply_markup=time_period_keyboard.as_markup())



@router.callback_query(F.data == 'this_month')
async def show_this_month(callback: CallbackQuery):
    await callback.answer()
    all_exp = show_expenses_this_month(callback.from_user.id)
    if not all_exp:
        await callback.message.answer('Вы еще ничего не тратили в этом месяце')
    formatted_expenses = "\n".join(
        [
            f"📌 *Категория:* {category}\n💰 *Сумма:* {price} ₽\n📝 *Описание:* {description if description else '—'}\n📅 *Дата:* {time[:10]}\n"
            for category, price, description, time in all_exp]
    )

    await callback.message.answer(f"📊 *Ваши траты за месяц:*\n\n{formatted_expenses}", parse_mode="Markdown")



@router.callback_query(F.data == 'year')
async def show_this_year(callback: CallbackQuery):
    await callback.answer()
    all_exp = show_expenses_this_year(callback.from_user.id)
    if not all_exp:
        await callback.message.answer('Вы еще ничего не тратили в этом году')
    formatted_expenses = "\n".join(
        [
            f"📌 *Категория:* {category}\n💰 *Сумма:* {price} ₽\n📝 *Описание:* {description if description else '—'}\n📅 *Дата:* {time[:10]}\n"
            for category, price, description, time in all_exp]
    )

    await callback.message.answer(f"📊 *Ваши траты за год:*\n\n{formatted_expenses}", parse_mode="Markdown")



# Накопления
earning = {}
@router.callback_query(F.data == 'earning')
async def earnings(callback: CallbackQuery):
    await callback.answer()
    show = show_earns(callback.from_user.id)
    if not show:
        await callback.message.answer('У вас еще нет накоплений', reply_markup=earn_keyboard.as_markup())
    else:
        await callback.message.answer('📌Вот ваши накопления:', reply_markup= goals_keyboard(callback.from_user.id))


@router.callback_query(F.data.startswith('goal_'))
async def earn_details(callback: CallbackQuery):
    await callback.answer()
    goal_id = int(callback.data.split('_')[1])
    goal = show_earnings_details(goal_id)
    progress = goal[1] / goal[2] * 100
    text = (
        f'🎯 Цель: {goal[0]}\n'
        f'💵 Целевая сумма: {goal[2]}руб.\n'
        f'💰 Накоплено: {goal[1]}руб.\n'
        f'🔄 Прогресс: {int(progress)}%'
    )

    await callback.message.answer(text,
                                  reply_markup= goal_detail_keyboard.as_markup())


@router.callback_query(F.data == 'back_to_goals')
async def back_to_goals_list(callback: CallbackQuery):
    await callback.answer()
    await earnings(callback)


@router.callback_query(F.data == 'add_earning')
async def add_earnings(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    earning[callback.from_user.id] = {}
    await callback.message.answer('Напишите цель')
    await state.set_state(AddEarning.goal)

# добавление суммы денег в накопление
@router.callback_query(F.data == 'add_money')
async def add_money(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('💵 Напишите сумму денег, которые хотите отложить')
    await state.set_state(AddMoney.ad_mon)


@router.message(AddMoney.ad_mon)
async def adding_money(message: Message, state: FSMContext):
    amount = message.text
    data = await state.get_data()
    await message.answer(f"{data}")



@router.message(AddEarning.goal)
async def earning_goal(message: Message, state: FSMContext):
    goal = message.text
    earning[message.from_user.id]['description'] = goal
    await message.answer('Напишите сумму, которую хотите накопить')
    await state.set_state(AddEarning.price_goal)


@router.message(AddEarning.price_goal)
async def earning_price_goal(message: Message):
    price_goal = int(message.text)
    earning[message.from_user.id]['price_goal'] = price_goal
    await message.answer('Накопление добавлено, спасибо')
    await asyncio.get_event_loop().run_in_executor(None, add_earns, message.from_user.id,
                                                   earning[message.from_user.id]['description'],
                                                   earning[message.from_user.id]['price_goal'])
    await get_started(message)
