from aiogram import Dispatcher, Bot, types
from aiogram.types import Message
from asyncio import run
from states import Drive_reg
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from keyboards import inline_markup
from database.requests import create_driver


async def register_user(message:Message,bot:Bot):
    data= await message.from_user.username
    print(data)
    
    # if message.text.lower() == "ha":
    #     data= await state.get_data()
    #     data1= state.get_data()
    #     print(data1)
    #     # register_data = (
        #     f"👨‍✈️ **Haydovchi Ismi: {data.get('name')}\n"
        #     f"📱 **Haydovchi Telegrami:: @{message.from_user.username}\n"
        #     f"☎️ **Telefon Raqam: {data.get('phone')}\n"
        #     f"🚗 **Mashina Turi:: {data.get('car_name')}\n"
        #     f"🚘 **Mashina Raqami: {data.get('car_number')}\n"
        #     )
        # await bot.send_message(1327096215,register_data)
        # try:
        #     saqlash = await create_driver(message.from_user.id, f"@{message.from_user.username}",f"{data.get('phone')}", f"{data.get('car_name')}", f"{data.get('car_number')}")
        #     await message.answer(f"Ma'lumotlaringiz bizning bazamizga saqlandi\n Yangi buyurtmalar bo'lsa sizga xabar beramiz",)
        #     await state.finish()
        # except Exception as e:
        #     await message.answer(f"Sizning malumotlaringiz bizning bazamizda mavjud")