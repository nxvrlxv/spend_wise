from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup ,InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.db import show_earns, show_earnings_details


main_keyboard = InlineKeyboardBuilder()
main_keyboard.button(text='Добавить трату', callback_data='add')
main_keyboard.button(text='Посмотреть траты', callback_data='watch')
main_keyboard.button(text='Накопления', callback_data='earning')
main_keyboard.button(text='Выделенный бюджет', callback_data='budget')
main_keyboard.adjust(2)





# клавиатура выбора категории траты
category_keyboard = InlineKeyboardBuilder()
category_keyboard.button(text='Фастфуд', callback_data='fastfood')
category_keyboard.button(text='Супермаркеты', callback_data='groceries')
category_keyboard.button(text='Рестораны', callback_data='restaurants')
category_keyboard.button(text='Маркетплейсы', callback_data='marketplace')
category_keyboard.button(text='Развлечения',callback_data='entertainment')
category_keyboard.button(text='Разное', callback_data='other')
category_keyboard.adjust(2)



# клава с одной кнопкой для описания
description_keyboard = InlineKeyboardBuilder()
description_keyboard.button(text='пропустить', callback_data='skip')



# Клавиатура для выбора временных промежутков трат
time_period_keyboard = InlineKeyboardBuilder()
time_period_keyboard.button(text='Текущий месяц', callback_data='this_month')
time_period_keyboard.button(text='Год', callback_data='year')
time_period_keyboard.button(text='Произвольный интервал', callback_data='interval')
time_period_keyboard.adjust(2)



# кнопка добавления накопления
earn_keyboard = InlineKeyboardBuilder()
earn_keyboard.button(text='Добавить', callback_data='add_earning')



def goals_keyboard(user_id: int):
    goals = show_earns(user_id)
    gl_kb = InlineKeyboardBuilder()

    for goal in goals:
        gl_kb.button(text=f'{goal[1]}', callback_data=f'goal_{goal[0]}')

    gl_kb.adjust(1)
    gl_kb.row(InlineKeyboardButton(
        text="➕ Новая цель",
        callback_data="add_earning"
    ))

    return gl_kb.as_markup()



goal_detail_keyboard = InlineKeyboardBuilder()
goal_detail_keyboard.button(text="Вложить", callback_data= 'add_money')
goal_detail_keyboard.button(text="◀️ Назад", callback_data="back_to_goals")
goal_detail_keyboard.adjust(1)