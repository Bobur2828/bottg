from aiogram import Dispatcher, Bot, types
from aiogram.types import Message,CallbackQuery
from asyncio import run
from states import Contact
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from keyboards import inline_markup
from database.requests import get_cars,create_contact,search_contact
import keyboards as kb
import asyncio
from aiogram import Dispatcher



async def cancel(message: Message, bot: Bot, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is  None:
        await message.answer("Sizda ariza yaratilmagan. Bekor qilish uchun ariza kerak emas.")
    else:
        await state.clear()
        await message.answer("Joriy ariza bekor qilindi.",reply_markup=kb.start)

async def start_contact(message: Message, bot: Bot, state: FSMContext):
    await message.answer("""🤖 Siz qidiruv tizimimiz orqali o'zingizga kerakli shaxs,tashkilot, va joy nomlarini kiritib ularning ishonch raqamlariniolishingiz mumkin. Telefon raqamini kiritib, qaysi shaxs yoki tashkilotga tegishli ekanligingizni aniqlashingiz mumkin. Agarqidiruv tizimimizda ma'lumot topilmasa, demak, bunday ma'lumotbizning bazamizda mavjud emas. Vodil aholisi uchun qulaylik bo'lishimaqsadida, ko'p so'raladigan insonlar yoki joylar telefon raqamlarini qo'shib qo'yishingiz mumkin.""",reply_markup=kb.contact1)

    await state.set_state(Contact.start)
async def add_contact(message: Message, bot: Bot, state: FSMContext):
 
    if message.text == "➕Raqam qo'shish":
        await message.answer("🤖ESLATMA\n Siz tarafingizdan qo'shilayotgan barcha ma'lumotlar hammasi nazorat ostida\n Botimizda yaxshi niyatlarda foydalaning", reply_markup=kb.cancel)

        await message.answer("🤖Shaxs ismi yoki Tashkilot Yoki joy nomini kiriting", reply_markup=kb.cancel)
        await state.set_state(Contact.name)
    
    elif message.text == "🔎Izlash":

        await message.answer("🤖Shaxs ismi qidiring", reply_markup=kb.cancel)
    else:
        search_query = message.text  # Replace this with actual user input
        contacts = await search_contact(search_query)
        print(contacts)
        if not contacts:
            await message.answer("🤖Afsus Ma'lumot topilmadi agar sizda ma'lumot bo'ls boshqalarga foydalik bo'lishi uchun qo'shib qoyishinginz mumkin", reply_markup=kb.start)
        else:
            data = ""
            for contact in contacts:
                data += f"*{contact.name}*, Tel: {contact.phone}\n\n"  # Two newlines for separation
            await message.answer(data, reply_markup=kb.contact1,parse_mode="Markdown") 
       



    


async def register_contact_name(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text)  
    await message.answer("🤖Malumot qabul qilindi✅")
    await message.answer("🤖Telefon Raqam kiriting",reply_markup=kb.cancel)
    await state.set_state(Contact.phone)  



async def register_contact_phone(message: Message, bot: Bot, state: FSMContext):
    if message.contact:
        phone=message.contact.phone_number
        await message.answer("🤖Telefon raqamingiz qabul qilindi✅")
        await message.answer("🤖Manzilingizni kiriting",reply_markup=kb.cancel)
        await state.update_data(phone=phone)
        await state.set_state(Contact.verify)
    else:
        phone_number = message.text.strip(" ")
        phone_number1 = phone_number[1:-1]
        if phone_number1.isdigit():
            if len(phone_number) == 13:
                if phone_number.startswith('+998'):
                    await state.update_data(phone=message.text)

                    await message.answer("🤖Telefon raqamqabul qilindi✅")
                    data = await state.get_data()
                    data1=(
                        f" **Malumotlar \n"
                        f"💼**Nomi: {data.get('name')}\n"
                        f"📞**Telefon raqami: {data.get('phone')}\n"

                        f"Malumotlarni tasdiqlaysizmi"
                    )
                    

                    await message.answer(f"🤖{data1}",reply_markup=kb.confirm)
                    await state.set_state(Contact.verify)
                else:
                    await message.answer("Telefon raqamingiz +998 bilan boshlanishi kerak.❌")
            else:
                await message.answer("Telefon raqamingiz 13 ta raqamdan iborat bo'lishi kerak.❌")
        else:
            await message.answer("Telefon raqamingiz faqat raqamlardan iborat bo'lishi kerak.❌")




async def contact_verify(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == "✅tasdiqlash":
        data = await state.get_data()
        name= data.get('name')
        phone= data.get('phone')
        tg_id =  message.from_user.id

        try:
            await create_contact(name=name,phone=phone,tg_id=tg_id)

            await message.answer(f"🤖Ma'lumotlar bazaga saqlandi",reply_markup=kb.start)
            await state.clear()
            await state.set_state(Contact.start)
        except Exception as e:
            print(e)
            await state.clear()
            await message.answer(f"🤖Ma'lumotlar saqlashda xatolik ro'y berdi qaytadan urinib ko'ring{e}",reply_markup=kb.start)




    