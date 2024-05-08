from aiogram import Dispatcher, Bot, types
from aiogram.types import Message,CallbackQuery
from asyncio import run
from states import Phone
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from keyboards import inline_markup
from database.requests import create_phone,get_phones
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

async def start_phone(message: Message, bot: Bot, state: FSMContext):
    await message.answer("Siz bu yerda sotuvdagi telefonlarni korishingiz mumkin yoki ozingiz Elon berishingiz mumkin",reply_markup=kb.custom)

    await state.set_state(Phone.start)
async def add_phone(message: Message, bot: Bot, state: FSMContext):
    
    if message.text == "💰Sotish":
        await message.answer("Maxsulot nomini kiriting, masalan, Iphone X", reply_markup=kb.cancel)
        await state.set_state(Phone.name)
    elif message.text == "🤝Sotib olish":
        phone = await get_phones()
        if not phone:
            await message.answer("Hozircha mahsulotlar mavjud emas",reply_markup=kb.start)
            await state.clear()
        else:
            await send_phone_info(message, bot, phone)
            


    if message.text == "👀Yana ko'rish":
        phone = await get_phones()
        if not phone:
            await message.answer("Keyingi mahsulot topilmadi.")
        else:
            await send_phone_info(message, bot, phone)
 
       

async def send_phone_info(message: Message, bot: Bot, phone):
    data = f"""
        📱 Telefon nomi: {phone.name}
        💼 Sotuvchi telegrami: @{phone.usernames}
        📝 Hujjat turi: {phone.documents}
        💰 Narxi: {phone.price}
        📞 Tel raqam: {phone.phone}
        🏠 Address: {phone.address}
        💬 Haqida: {phone.comment}
        🕒 Elon berilgan kun: {phone.data[0:10]}
    """
    photo = phone.image
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=data, reply_markup=kb.more)
    

async def register_phone_name(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text)  
    await message.answer("Telefon nomi qabul qilindi ✅")
    
    await message.answer("Mahsulot holati", reply_markup=kb.position)
    

    await state.set_state(Phone.position)  


async def register_position_phone(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(position=message.text)  
    await message.answer("Mahsulot holati qabul qilindi ✅")
    
    await message.answer("Hujjat sifatida nima taqdim etasiz, Karopka yoki Pasport kopiya", reply_markup=kb.verify_phone)
    

    await state.set_state(Phone.document) 



async def register_price_document(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(document=message.text)
    await message.answer("Hujjat turi qabul qilindi✅")
    await message.answer("Narx kiriting songida valyuta belgisini ham  Misol uchun: 150$ yoki 1 000 000 so'm✅",reply_markup=kb.cancel)
    await state.set_state(Phone.price)
 

async def register_phone_price(message: Message, bot: Bot, state: FSMContext):
    await message.answer("Narx qabul qilindi✅")
    await state.update_data(price=message.text)  
    await message.answer("Manzilingizni kiriting",reply_markup=kb.cancel)
    await state.set_state(Phone.address)  

async def register_phone_address(message: Message, bot: Bot, state: FSMContext):

    await state.update_data(address=message.text)
    await message.answer("Manzil qabul qilindi.✅")
    await message.answer("Telefon haqida qo'shimcha ma'lumot kiriting ",reply_markup=kb.cancel)
    await state.set_state(Phone.comment)

async def register_phone_comment(message: Message, bot: Bot, state: FSMContext): 
    await state.update_data(comment=message.text)
    await message.answer("Ma'lumot qabul qilindi.✅")
    await message.answer("Bog'lanish uchun telefon raqam", reply_markup=kb.contact)
    await state.set_state(Phone.phone)

async def register_phone_num(message: Message, bot: Bot, state: FSMContext): 
    if message.contact:
        phone=message.contact.phone_number
        await message.answer("Telefon raqamingiz qabul qilindi✅")
        await message.answer("Telefon rasmini jonating faqat 1 dona",reply_markup=kb.cancel)
        await state.update_data(phone=phone)
        await state.set_state(Phone.image)
    else:
        phone_number = message.text.strip(" ")
        phone_number1 = phone_number[1:-1]
        if phone_number1.isdigit():
            if len(phone_number) == 13:
                if phone_number.startswith('+998'):
                    await message.answer("Telefon rasmini jonating faqat 1 dona",reply_markup=kb.cancel)
                    await state.update_data(phone=message.text)
                    await state.set_state(Phone.image)
                else:
                    await message.answer("Telefon raqamingiz +998 bilan boshlanishi kerak.❌")
            else:
                await message.answer("Telefon raqamingiz 13 ta raqamdan iborat bo'lishi kerak.❌")
        else:
            await message.answer("Telefon raqamingiz faqat raqamlardan iborat bo'lishi kerak.❌")

async def register_phone_image(message: Message, bot: Bot, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id
        await message.answer("Rasm qabul qilindi✅")
        await state.update_data(image=file_id)
        data = await state.get_data()
        a=""
        if message.from_user.username: 
            a = message.from_user.username
        else:
            a= "Mavjud emas"
        b= data.get('image')

        register_data = (
        f"👨‍✈️ **Telefon nomi: {data.get('name')}\n"
        f"📱 **Sotuvchi Telegrami: @{a}\n"
        f"☎️ **Mahsulot holat: {data.get('position')}\n"

        f"☎️ **HUjjat turi: {data.get('document')}\n"
        f"🚗 **Narxi:: {data.get('price')}\n"
        f"🚘 **Sotuvchi raqami: {data.get('phone')}\n"
        f"🚘 **Manzil: {data.get('address')}\n"
        f"🚘 **Telefon haqida: {data.get('comment')}\n"



 

        f"Malumotlarni tasdiqlaysizmi"
    )
        # Foydalanuvchiga kelgan rasmini qayta jonatish
        await bot.send_photo(chat_id=message.from_user.id, photo=b,caption=register_data,reply_markup=kb.confirm)
        await state.set_state(Phone.verify)

    else:
        await message.answer("Rasm qo'shish tugmasini bosing")

async def phone_verify(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == "✅tasdiqlash":
        data = await state.get_data()
        name= data.get('name')
        documents= data.get('document')
        image= data.get('image')
        price= data.get('price')
        comment= data.get('comment')
        phone= data.get('phone')
        address= data.get('address')
        position= data.get('position')
        usernames = ""
        tg_id =  message.from_user.id
        if message.from_user.username: 
            usernames = message.from_user.username
        else:
            usernames = "Mavjud emas"


        try:
            await create_phone(name=name, image=image, price=price, documents=documents, comment=comment, usernames=usernames,phone=phone,address=address,position=position,tg_id=tg_id)

            await message.answer(f"Ma'lumotlaringiz bizning bazamizga saqlandi",reply_markup=kb.start)
            await state.clear()
        except Exception as e:
            await message.answer(f"{e}",reply_markup=kb.start)

            await state.clear()



    