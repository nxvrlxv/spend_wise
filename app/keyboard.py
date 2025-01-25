from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup ,InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


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
