from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
import asyncio
import logging
import sys

from handlers import router
from database.models import async_main
from config import TOKEN

import requests


async def main(dp: Dispatcher, token: str):
    await async_main()
    bot = Bot(token=token)
    dp.include_router(router)
    
    # Register your commands here
    commands = [
        BotCommand(command="/start", description="Botni qayta ishga tushirish"),
        # BotCommand(command="/yordam", description="Botni ishlatish bo'yicha qo'llanma"),
        BotCommand(command="/obunachilar", description="Botning aktiv foydalanuvchilar soni"),
        # BotCommand(command="/reklama", description="Reklama berish hizmati"),
        # BotCommand(command="/contact", description="Bot ma'muriyati bilan bog'lanish"),
        # BotCommand(command="/taklif", description="Taklif va etirozlar"),

        # Add more custom commands here
    ]

    # Set the bot commands
    await bot.set_my_commands(commands)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        dp = Dispatcher()
        asyncio.run(main(dp, TOKEN))
    except KeyboardInterrupt:
        print('Exit')