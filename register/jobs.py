from aiogram import Dispatcher, Bot, types
from aiogram.types import Message,CallbackQuery
from asyncio import run
from states import DriverJobs
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from keyboards import inline_markup
from database.requests import create_home,get_home,get_homes
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

async def start_jobs(message: Message, bot: Bot, state: FSMContext):
    await message.answer("Siz bu yerda sotuv joylarini ko'rishingiz mumkin yoki o'zingizning eloningizni taqdim etishingiz mumkin.\n Ma'lumotlar yetarli emas bo'lsa, sotuvchilar bilan aloqaga chiqib, batafsil ma'lumot olishingiz mumkin.",reply_markup=kb.custom)

    await state.set_state(DriverJobs.start)
async def add_home(message: Message, bot: Bot, state: FSMContext):
    
    if message.text == "💰Sotish":
        await message.answer("🤖Tugmalardan birini tanlang", reply_markup=kb.home)
        await state.set_state(Home.type)
    elif message.text == "🤝Sotib olish":
        phone = await get_homes()
        if not phone:
            await message.answer("🤖Hozircha mahsulotlar mavjud emas",reply_markup=kb.start)
            await state.clear()
        else:
            await send_car_info(message, bot, phone)
            

    if message.text == "👀Yana ko'rish":
        home = await get_homes()
        if not home:
            await message.answer("🤖Keyingi mahsulot topilmadi.",reply_markup=kb.start)
        else:
            await send_car_info(message, bot, home)
        
       

async def send_car_info(message: Message, bot: Bot, home):
    data = f"""
    🏠 {home.type} SOTILADI:
    📍 Manzil: {home.address}
    🚗 Xonalar son: {home.xona} ta
    📏 Maydoni: {home.kvadrat}
    🔥 Isitish tizimi: {home.isitish}
    ⚡ Elektr Tarmogi: {home.electro}
    💡 Gaz Tarmogi: {home.gas}
    💧 Ichimlik suvi: {home.water}
    📍 Maqomi: {home.status}
    📄 Hujjatlari: {home.document}
    💰 Sotilish narxi: {home.price}
    📱 Telefon: {home.phone}
    👤 Sotuvchi telegrami: @{home.usernames}
    🕒 E'lon berilgan kun: {home.data[0:10]}

    💬 Qo'shimcha malumot:
      {home.comment}

    """
    photo = home.image
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=data, reply_markup=kb.more)
    


async def register_home_type(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(type=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Xonalar sonini kiriting",reply_markup=kb.cancel)
    await state.set_state(Home.xona)  

async def register_home_xona(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(xona=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Maydonni kiriting masalan 8 Sotix yoki 78 kvadrat",reply_markup=kb.cancel)
    await state.set_state(Home.kvadrat)  

async def register_home_kvadrat(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(kvadrat=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Maqomni tanlang", reply_markup=kb.home1)
    await state.set_state(Home.status)  

async def register_home_status(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(status=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Manzilni kiriting", reply_markup=kb.cancel)
    await state.set_state(Home.address)  

async def register_home_address(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(address=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Isitish tizimi bor yo'qligini belgilang", reply_markup=kb.isitish)
    await state.set_state(Home.isitish)  

async def register_home_isitish(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(isitish=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Elektr tarmoqlari bor yo'qligini belgilang", reply_markup=kb.isitish)
    await state.set_state(Home.electro)  

async def register_home_electro(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(electro=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Gaz tarmoqlari bor yo'qligini belgilang", reply_markup=kb.isitish)
    await state.set_state(Home.gas)  

async def register_home_gas(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(gas=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Ichimlik suvi bor yo'qligini belgilang", reply_markup=kb.isitish)
    await state.set_state(Home.water)  

async def register_home_water(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(water=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖HUjjatlari bor yo'qligini belgilang", reply_markup=kb.isitish)
    await state.set_state(Home.document)  

async def register_home_document(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(document=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Sotish narxini kiriting valyuta belgisi bilan misol uchun 12000$",reply_markup=kb.cancel)
    await state.set_state(Home.price)

async def register_home_price(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(price=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Aloqa uchun telefon raqam kiriting", reply_markup=kb.contact)
    await state.set_state(Home.phone)

async def register_home_phone(message: Message, bot: Bot, state: FSMContext):
    if message.contact:
        phone=message.contact.phone_number
        await message.answer("🤖Telefon raqamingiz qabul qilindi✅")
        await message.answer("🤖Qo'shimcha ma'lumot kiriting", reply_markup=kb.cancel)
        await state.update_data(phone=phone)
        await state.set_state(Home.add)
    else:
        phone_number = message.text.strip(" ")
        phone_number1 = phone_number[1:-1]
        if phone_number1.isdigit():
            if len(phone_number) == 13:
                if phone_number.startswith('+998'):
                    await message.answer("🤖Telefon raqamingiz qabul qilindi✅")
                    await message.answer("🤖Qo'shimcha ma'lumot kiriting", reply_markup=kb.cancel)
                    await state.update_data(phone=message.text)
                    await state.set_state(Home.add)
                else:
                    await message.answer("Telefon raqamingiz +998 bilan boshlanishi kerak.❌")
            else:
                await message.answer("Telefon raqamingiz 13 ta raqamdan iborat bo'lishi kerak.❌")
        else:
            await message.answer("Telefon raqamingiz faqat raqamlardan iborat bo'lishi kerak.❌")


async def register_home_add(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(add=message.text)  
    await message.answer("🤖Malumot qabul qilindi ✅")
    await message.answer("🤖Foto surat yuboring 1 dona", reply_markup=kb.cancel)
    await state.set_state(Home.image)


async def register_home_image(message: Message, bot: Bot, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id
        await state.update_data(image=file_id)
        await message.answer("🤖Rasm qabul qilindi✅")
        data = await state.get_data()
        a=""
        if message.from_user.username: 
            a = message.from_user.username
        else:
            a= "Mavjud emas"
        b= data.get('image')
        register_data = (
    f"🏠 **{data.get('type')} SOTILADI\n"
    f"🚪 **Xonalar soni {data.get('xona')}\n"
    f"📏 **Maydon {data.get('kvadrat')}\n"
    f"📍 **Maqomi {data.get('status')}\n"
    f"🏠 **Manzil {data.get('address')}\n"
    f"🔥 **Isitish tizimlari {data.get('isitish')}\n"
    f"⚡ **Elektr tarmoqlari {data.get('electro')}\n"
    f"💡 **Gaz tarmoqlari {data.get('gas')}\n"
    f"💧 **Ichimlik suvi {data.get('water')}\n"  # Bu
    f"📄 **Hujjatlari {data.get('document')}\n"
    f"💰 **Narx {data.get('price')}\n"
    f"☎️ **Telefon {data.get('phone')}\n"
    f"👤 **Sotuvchi Telegrami: @{a}\n"
    f"☎️ **Qo'shimcha ma'lumot {data.get('add')}\n"

)

        await bot.send_photo(chat_id=message.from_user.id, photo=b,caption=register_data,reply_markup=kb.confirm)

        await state.set_state(Home.verify)
    else:
        await message.answer("🤖Rasm yuborilmadi. Iltimos, rasm yuboring")



async def home_verify(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == "✅tasdiqlash":
        data = await state.get_data()
        name= data.get('type')
        type= data.get('type')
        xona= data.get('xona')
        kvadrat= data.get('kvadrat')
        status= data.get('status')
        address= data.get('address')
        isitish= data.get('isitish')
        phone= data.get('phone')
        image= data.get('image')
        usernames= data.get('usernmes')
        electro= data.get('electro')
        gas= data.get('gas')
        price= data.get('price')
        document= data.get('document')
        water=data.get('water')
        comment= data.get('add')
        tg_id =  message.from_user.id
        usernames = ""
        if message.from_user.username: 
            usernames = message.from_user.username
        else:
            usernames = "Mavjud emas"


        try:
            await create_home(name=name,type=type,xona=xona,kvadrat=kvadrat,status=status,
                              address=address,isitish=isitish,
                              phone=phone,image=image,usernames=usernames,
                              electro=electro,gas=gas,price=price,
                              document=document,water=water,comment=comment,tg_id=tg_id)

            await message.answer(f"🤖Ma'lumotlaringiz bizning bazamizga saqlandi",reply_markup=kb.start)
            await state.clear()
        except Exception as e:
            await state.clear()




    