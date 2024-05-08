from aiogram import Dispatcher, Bot, types
from aiogram.types import Message,CallbackQuery
from asyncio import run
from states import Cars
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from keyboards import inline_markup
from database.requests import create_cars,get_cars
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

async def start_cars(message: Message, bot: Bot, state: FSMContext):
    await message.answer("🤖Siz bu yerda sotuvdagi avtomobillarni ko'rishingiz mumkin yoki o'zingizning eloningizni taqdim etishingiz mumkin.\n Ma'lumotlar yetarli emas bo'lsa, sotuvchilar bilan aloqaga chiqib, batafsil ma'lumot olishingiz mumkin.",reply_markup=kb.custom)

    await state.set_state(Cars.start)
async def add_cars(message: Message, bot: Bot, state: FSMContext):
    global index_list
    
    if message.text == "💰Sotish":
        await message.answer("🤖Mashina Modelini kiriting masalan: Damas", reply_markup=kb.cancel)
        await state.set_state(Cars.name)
    elif message.text == "🤝Sotib olish":
        car = await get_cars()
        if not car:
            await message.answer("🤖Hozircha mahsulotlar mavjud emas", reply_markup=kb.menu)
        else:
            await send_car_info(message, bot, car)
    if message.text == "👀Yana ko'rish":
        car = await get_cars()
        if not car:
            await message.answer("🤖Keyingi mahsulot topilmadi.", reply_markup=kb.start)
        else:
            await send_car_info(message, bot, car)
    
       

async def send_car_info(message: Message, bot: Bot, car):
    data = f"""
    🚗 Mashina Malumotlari:
    🚗 Modeli: {car.name}
    🏷️ Pozitsiya: {car.version}
    🎨 Kraska detal: {car.detail}
    🎨 Rangi: {car.color}
    📅 Yili: {car.year}
    🛣️ Probeg: {car.probeg}
    🔧 Yoqilgi turi: {car.oil}
    ⛽ Qoshimcha yoqilgi turi: {car.gas}
    💰 Narxi: {car.price}
    🏠 Manzil: {car.address}
    💼 Sotuvchi telegrai: @{car.usernames}
    📞 Telefon raqam: {car.phone}
    🕒 E'lon berilgan kun: {car.data[0:10]}
"""
    photo = car.image
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=data, reply_markup=kb.more)
    


async def register_car_name(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text)  
    await message.answer("🤖Mashina Modeli qabul qilindi ✅")
    await message.answer("🤖Pozitsiyasini kiriting",reply_markup=kb.cancel)
    await state.set_state(Cars.version)  

async def register_car_version(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(version=message.text)  
    await message.answer("🤖Pozitsiya qabul qilindi ✅")
    await message.answer("🤖Rangini kiriting",reply_markup=kb.cancel)
    await state.set_state(Cars.color)  

async def register_car_color(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(color=message.text)  
    await message.answer("🤖Rang qabul qilindi ✅")
    await message.answer("🤖Kraska bo'lgan detallarni kiriting",reply_markup=kb.cancel)
    await state.set_state(Cars.detail)  

async def register_car_detail(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(detail=message.text)  
    await message.answer("🤖Kraska detallar qabul qilindi ✅")
    await message.answer("🤖Ishlab chiqarilgan yilini kiriting",reply_markup=kb.cancel)
    await state.set_state(Cars.year)  

async def register_car_year(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(year=message.text)  
    await message.answer("🤖Ishlab chiqarilgan yil qabul qilindi ✅")
    await message.answer("🤖Probegini kiriting",reply_markup=kb.cancel)
    await state.set_state(Cars.probeg)  


async def register_car_probeg(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(probeg=message.text)  
    await message.answer("🤖Probeg qabul qilindi ✅")
    await message.answer("🤖Zavod holatidagi yoqilgi turi Masalan Benzin",reply_markup=kb.cancel)
    await state.set_state(Cars.oil)  

async def register_car_oil(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(oil=message.text)  
    await message.answer("🤖Yoqilgi turi qabul qilindi ✅")
    await message.answer("🤖Qo'shimcha yoqilgi turi ",reply_markup=kb.gas)
    await state.set_state(Cars.gas)  



async def register_car_gas(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(gas=message.text)  
    await message.answer("🤖Qo'shimca Yoqilgi turi qabul qilindi ✅")
    await message.answer("🤖Sotish narxini kiriting",reply_markup=kb.cancel)
    await state.set_state(Cars.price)  


async def register_car_price(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(price=message.text)  
    await message.answer("🤖Narx qabul qilindi ✅")
    await message.answer("🤖Bog'lanish uchun telefon raqam kiriting",reply_markup=kb.contact)
    await state.set_state(Cars.phone)


async def register_car_phone(message: Message, bot: Bot, state: FSMContext):
    if message.contact:
        phone=message.contact.phone_number
        await message.answer("🤖Telefon raqamingiz qabul qilindi✅")
        await message.answer("🤖Manzilingizni kiriting",reply_markup=kb.cancel)
        await state.update_data(phone=phone)
        await state.set_state(Cars.address)
    else:
        phone_number = message.text.strip(" ")
        phone_number1 = phone_number[1:-1]
        if phone_number1.isdigit():
            if len(phone_number) == 13:
                if phone_number.startswith('+998'):
                    await message.answer("🤖Telefon raqamingiz qabul qilindi✅")

                    await message.answer("🤖Manzilingizni kiriting",reply_markup=kb.cancel)
                    await state.update_data(phone=message.text)
                    await state.set_state(Cars.address)
                else:
                    await message.answer("Telefon raqamingiz +998 bilan boshlanishi kerak.❌")
            else:
                await message.answer("Telefon raqamingiz 13 ta raqamdan iborat bo'lishi kerak.❌")
        else:
            await message.answer("Telefon raqamingiz faqat raqamlardan iborat bo'lishi kerak.❌")


async def register_car_address(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(address=message.text)  
    await message.answer("🤖Manzili qabul qilindi ✅")
    await message.answer("🤖Mashina rasmini yuboring",reply_markup=kb.cancel)
    await state.set_state(Cars.image)  

async def register_car_image(message: Message, bot: Bot, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id
        await state.update_data(image=file_id)
        await message.answer("🤖Rasm qabul qilindi✅")
        await message.answer("🤖Mashina malumotlari:")
        data = await state.get_data()
        a=""
        if message.from_user.username: 
            a = message.from_user.username
        else:
            a= "Mavjud emas"
        b= data.get('image')
        register_data = (
        f"🚗 **Mashina malumotlari"
        f"💼 **Sotuvchi Telegrami: @{a}\n"
        
        f"🚗 **Modeli: {data.get('name')}\n"
        f"🏷️ **Pozitsiyasi: {data.get('version')}\n"
        f"🎨 **Rangi: {data.get('color')}\n"
        f"🎨 **Kraska detallari: {data.get('detail')}\n"
        f"📅 **Yili: {data.get('year')}\n"
        f"⛽ **Asosiy yoqilgi turi: {data.get('oil')}\n"
        f"⛽ **Qo'shimcha yoqilgi turi: {data.get('gas')}\n"
        f"💰 **Narxi: {data.get('price')}\n"
        f"📞 **Telefon raqam: {data.get('phone')}\n"
        f"🏠 **Manzil: {data.get('address')}\n"
        f"Malumotlarni tasdiqlaysizmi"

        )

        await bot.send_photo(chat_id=message.from_user.id, photo=b,caption=register_data,reply_markup=kb.confirm)

        await state.set_state(Cars.verify)
    else:
        await message.answer("🤖Rasm yuborilmadi. Iltimos, rasm yuboring")



async def cars_verify(message: Message, bot: Bot, state: FSMContext):
    if message.text.lower() == "✅tasdiqlash":
        data = await state.get_data()
        name= data.get('name')
        version= data.get('version')
        detail= data.get('detail')
        color= data.get('color')
        probeg= data.get('probeg')
        year= data.get('year')
        oil= data.get('oil')
        gas= data.get('gas')
        price= data.get('price')
        phone= data.get('phone')
        address= data.get('address')
        image= data.get('image')
        tg_id =  message.from_user.id
        usernames = ""
        if message.from_user.username: 
            usernames = message.from_user.username
        else:
            usernames = "🤖Mavjud emas"


        try:
            await create_cars(name=name, version=version,detail=detail,color=color,year=year,probeg=probeg,oil=oil,gas=gas,price=price,usernames=usernames,phone=phone,address=address,image=image,tg_id=tg_id)

            await message.answer(f"🤖Ma'lumotlaringiz e'lon qilindi",reply_markup=kb.start)
            await state.clear()
        except Exception as e:
            await state.clear()
            await message.answer(f"🤖Ma'lumotlar saqlashda xatolik ro'y berdi qaytadan urinib ko'ring",reply_markup=kb.start)




    