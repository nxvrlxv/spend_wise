import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router
from app.db import init_expense_db, init_earnings_db, drop_table
from aiogram.types import BotCommand
import logging


bot = Bot(token= TOKEN)
dp = Dispatcher()

async def set_bot_commands():
    bot_commands = [
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/add', description='Добавить трату'),
        BotCommand(command='/watch_all', description='Посмотреть все траты')

    ]
    await bot.set_my_commands(bot_commands)

async def main():
    #drop_table()
    init_expense_db()
    init_earnings_db()
    dp.include_router(router)
    await set_bot_commands()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Процесс завершен')
