from aiogram import Dispatcher, Bot, types
from aiogram.types import Message
from asyncio import run
from states import CustomTaxi
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from keyboards import inline_markup
from database.requests import create_driver
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import Driver,async_session 
from sqlalchemy.ext.asyncio import AsyncSession
import keyboards as kb
# from database.requests import get_driver_tg_ids

async def start_custom_register(message:Message,bot:Bot, state:FSMContext):
    await message.answer(f"   Ismingizni kiriting ",reply_markup=kb.start)
    await state.set_state(CustomTaxi.name)

async def custom_name(message: Message, bot: Bot, state: FSMContext):
    name = message.text.strip()  
    if any(char.isdigit() for char in name):
        await message.answer("Ismingiz raqamdan iborat. Iltimos, faqat harfli ism kiriting.❌")
    else:
        await state.update_data(name=name)  
        await message.answer("Ismingiz qabul qilingdi ✅")
        
        await message.answer("Jo'nab Ketishi Manzilini tanlang",reply_markup=kb.drive)

        await state.set_state(CustomTaxi.adressA)  

async def custom_addressA(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(adressA=message.text)  
    await message.answer("Jo'nab ketish manzili qabul qilindi ✅",reply_markup=kb.start)
    
    await message.answer("Borish manzilini tanlang",reply_markup=kb.drive)

    await state.set_state(CustomTaxi.adressB)  

async def custom_addressB(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(adressB=message.text)  
    await message.answer("Yakuniy Manzil qabul qilindi ✅")
    await message.answer("Jo'nab ketish vaqtini tanlang",reply_markup=kb.time)
    await state.set_state(CustomTaxi.time) 

async def custom_time(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(time=message.text)  
    await message.answer("Jo'nat ketish vaqti qabul qilindi ✅")
    await message.answer("Yo'lovchi sonini tanlang ",reply_markup=kb.count_custom_button)

    await state.set_state(CustomTaxi.count) 


async def custom_count(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(count=message.text)  
    await message.answer("Yo'lovchilar soni qabul qilindi ✅")
    await message.answer("Telefon raqamingizni kiriting.", reply_markup=kb.contact)
    await state.set_state(CustomTaxi.phone) 

async def custom_phone(message: Message, bot: Bot, state: FSMContext):
    if message.contact:
        phone=message.contact.phone_number
        await message.answer("Telefon raqamingiz qabul qilindi✅")
        await message.answer("Haydovchi safar bo'yicha izoh yozish",reply_markup=kb.cancel)

        # Ma'lumotlarni saqlash va keyingi holatga o'tish
        await state.update_data(phone=phone)
        await state.set_state(CustomTaxi.comment)
 
    # Faqat raqam belgilari bo'lishini tekshirish
    else:
        phone_number = message.text.strip(" ")
        phone_number1 = phone_number[1:-1]
        # Faqat raqam belgilari bo'lishini tekshirish
        if phone_number1.isdigit():
            if len(phone_number) == 13:
                # Raqam +998 bilan boshlanishi kerak
                if phone_number.startswith('+998'):
                    await message.answer("Haydovchi safar bo'yicha izoh yozish",reply_markup=kb.cancel)

                    # Ma'lumotlarni saqlash va keyingi holatga o'tish
                    await state.update_data(phone=message.text)
                    await state.set_state(CustomTaxi.comment)
                else:
                    await message.answer("Telefon raqamingiz +998 bilan boshlanishi kerak.❌")
            else:
                await message.answer("Telefon raqamingiz 13 ta raqamdan iborat bo'lishi kerak.❌")
        else:
            await message.answer("Telefon raqamingiz faqat raqamlardan iborat bo'lishi kerak.❌")

async def custom_comment(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(comment=message.text)  
    await message.answer("Sizning izohingiz qabul qilindi ✅")
    data= await state.get_data()
    register_data = (
            f"👨‍✈️ **Yo'lovchi Ismi: {data.get('name')}\n"
            f"📱 **Yo'lovchi Telegrami:: @{message.from_user.username}\n"
            f"☎️ **Qayerdan: {data.get('adressA')}\n"
            f"🚗 **Qayerga:: {data.get('adressB')}\n"
            f"🚘 **Ketish vaqti: {data.get('time')}\n"
            f"🚘 **Yo'lovchi soni: {data.get('count')}\n"
            f"🚘 **Bog'lanish uchun : {data.get('phone')}\n"
            f"🚘 **Safar uchun izoh : {data.get('comment')}\n"

            )
    await message.answer(register_data)
    await message.answer("Buyurtmani Tasdiqlang",reply_markup=kb.confirm)

    await state.set_state(CustomTaxi.verify) 




async def custom_verify(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == "✅tasdiqlash":
        data = await state.get_data()
        register_data = (
            f"👨‍✈️ **Yo'lovchi Ismi: {data.get('name')}\n"
            f"📱 **Yo'lovchi Telegrami:: @{message.from_user.username}\n"
            f"☎️ **Qayerdan: {data.get('adressA')}\n"
            f"🚗 **Qayerga:: {data.get('adressB')}\n"
            f"🚘 **Ketish vaqti: {data.get('time')}\n"
            f"🚘 **Yo'lovchi soni: {data.get('count')}\n"
            f"🚘 **Bog'lanish uchun: {data.get('phone')}\n"
            f"🚘 **Safar uchun izoh: {data.get('comment')}\n"
        )

        
        try:
            driver_info = await get_driver_info()

            for driver in driver_info:
                tg_id = driver['tg_id']
                await bot.send_message(tg_id, register_data)
                await message.answer("Tez orada haydovchilar siz bilan bog'lanishadi",reply_markup=kb.menu)
                await state.clear()

        except Exception as e:
                await message.answer("Qandaydir hatolik yuz berdi yana urinib ko'ring",reply_markup=kb.custom)

async def get_driver_info():
    query = select(Driver)

    try:
        async with async_session() as session:
            result = await session.execute(query)
            drivers = result.scalars().all()
            driver_info = [{
                'tg_id': driver.tg_id
                
            } for driver in drivers if driver.tg_id is not None]

            return driver_info
            
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return []