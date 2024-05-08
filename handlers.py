from aiogram import Router,F,Bot
from aiogram.types import Message,CallbackQuery
import keyboards as kb
from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from register.drive_register import *
from register.customtaxi import *
from register.register_phone import *
from register.car_register import *
from register.register_home import *
from register.contact_register import *
from register.weather import weather,namoz
from database.requests import create_driver,create_user,get_user
from states import *
from config import TOKEN
from aiogram.types import BotCommand
router=Router()
bot=Bot(token=TOKEN)
# @router.message(CommandStart())
# async def start_reply(message:Message):
    
#     await message.answer("Assalomu alaykum Hurmatli Sizni ko'rib turganimizdan xursandmisz\n Bot bilan tanishish uchun \n Menyu tugmasini bosin", reply_markup=start)
# router.message.register(CommandStart())

@router.message(CommandStart())
async def start_reply(message: Message):
    username = message.from_user.full_name
    user_id = message.from_user.id
    result = await get_user()
    await bot.send_message(1327096215,f"{result}")
    try:
        await create_user(user_id) 
    finally:
        await message.answer("🔥Assalomu alaykum!\n"
                             f"Hurmatli  {username} ❗️\n"
                             "Sizni ko'rib turganimizdan xursandmiz.🙂\n", 
                             reply_markup=kb.menu)
        


@router.message(F.text=="/obunachilar")
async def count_user(message: Message):
    username = message.from_user.full_name
    user_id = message.from_user.id
    result = await get_user()
    try:
        await create_user(user_id) 
    finally:
        await message.answer(f"Bizning botimizning hozirgi kunda faol foydalanuvchilari soni {result} ta", 
                             reply_markup=kb.menu)
@router.message(F.text=="🤖Menu")
async def menu_reply(message:Message,state: FSMContext):
    current_state = await state.get_state()
    
    if current_state:
        await state.clear()
        await message.reply('Tugmalardan birini tanlang', reply_markup=kb.menu)
    else:
        await message.reply('Tugmalardan birini tanlang', reply_markup=kb.menu)

 
@router.message(F.text=="🚕 Toshkent-Vodil")
async def taxi_reply(message:Message):
    await message.reply('Tugmalardan birini tanlang', reply_markup=kb.taxi)

@router.message(F.text=="💼 Turli Xizmatlar")
async def xizmat_reply(message:Message):
    await message.reply('Tugmalardan birini tanlang', reply_markup=kb.xizmat)

@router.message(F.text=="🤝 Oldi-Sotdi")
async def xizmat_reply(message:Message):
    await message.reply('Tugmalardan birini tanlang', reply_markup=kb.store)

@router.message(F.text=="🚕Haydovchi")
async def taxi1_reply(message:Message):
    await message.reply("🔥Assalomu alaykum Hurmatli👨🏻‍💼 Haydovchi Agar Siz Toshkent-Vodil yo'nalishida qatnaydigan bo'lsangiz🚕 marhamat Ro'yhatdan o'ting✅", reply_markup=kb.taxi1)



@router.message(F.text=="Ishonch raqamlari")
async def get_reply(message:Message):
    res=await kb.categorys()
    await message.answer("Text", reply_markup=res)

@router.callback_query(F.data.startswith('category_'))
async def category(callback:CallbackQuery):
    await callback.answer("")
    res=await kb.phones(callback.data.split('_')[1])
    await callback.message.answer("salom dunyo",reply_markup=res)

# Register Drivers
router.message.register(start_register,F.text=="✍️Ro'yhatdan o'tish")
router.message.register(dr_cancel,F.text=="❌Bekor qilish")

router.message.register(register_name,Drive_reg.name)
router.message.register(register_phone,Drive_reg.phone)
router.message.register(register_carname,Drive_reg.car_name)
router.message.register(register_carnumber,Drive_reg.car_number)
router.message.register(register_verify,Drive_reg.verify)
# RegisterCustomer
@router.message(F.text == "🚶Yo'lovchi")
async def custom_reply(message: Message):
    custom_message = """\
Bu yerda buyurtma berish orqali🙂
O'z safaringiz haqida buyurtma berasiz🙃
Sizning buyurtmangiz 🤖botimizdan ro'yhatdan
o'tgan haydovchilarga 👨🏻‍💼avtomatik tarzda yuboriladi
    """
    await message.answer(custom_message, parse_mode="Markdown", reply_markup=kb.custom_taxi)
router.message.register(start_custom_register,F.text=="📞Buyurtma berish")

router.message.register(start_custom_register,F.text=="📞Buyurtma berish")
router.message.register(custom_name,CustomTaxi.name)
router.message.register(custom_addressA,CustomTaxi.adressA)
router.message.register(custom_addressB,CustomTaxi.adressB)
router.message.register(custom_time,CustomTaxi.time)
router.message.register(custom_count,CustomTaxi.count)
router.message.register(custom_phone,CustomTaxi.phone)
router.message.register(custom_comment,CustomTaxi.comment)
router.message.register(custom_verify,CustomTaxi.verify)

router.message.register(weather,F.text=="☀️ Ob-Havo")
router.message.register(namoz,F.text=="🌙 Namoz Vaqtlari")

router.message.register(cancel,F.text=="❌Bekor qilish")
router.message.register(start_phone,F.text=='📱Telefon Savdo')
router.message.register(add_phone,Phone.start)
router.message.register(register_phone_name, Phone.name)
router.message.register(register_position_phone, Phone.position)
router.message.register(register_price_document, Phone.document)
router.message.register(register_phone_price, Phone.price)
router.message.register(register_phone_address, Phone.address)
router.message.register(register_phone_comment, Phone.comment)
router.message.register(register_phone_num, Phone.phone)
router.message.register(register_phone_image, Phone.image)
router.message.register(phone_verify, Phone.verify)


router.message.register(start_cars,F.text=='🚘Avto Savdo')
router.message.register(add_cars,Cars.start)
router.message.register(register_car_name,Cars.name)
router.message.register(register_car_version,Cars.version)
router.message.register(register_car_color,Cars.color)
router.message.register(register_car_detail,Cars.detail)
router.message.register(register_car_year,Cars.year)
router.message.register(register_car_probeg,Cars.probeg)
router.message.register(register_car_oil,Cars.oil)
router.message.register(register_car_gas,Cars.gas)
router.message.register(register_car_price,Cars.price)
router.message.register(register_car_phone,Cars.phone)
router.message.register(register_car_address,Cars.address)
router.message.register(register_car_image,Cars.image)
router.message.register(cars_verify,Cars.verify)

router.message.register(start_home,F.text=='🏠Uy Savdo')
router.message.register(add_home, Home.start)
router.message.register(register_home_type, Home.type)
router.message.register(register_home_xona, Home.xona)
router.message.register(register_home_kvadrat, Home.kvadrat)
router.message.register(register_home_status, Home.status)
router.message.register(register_home_address, Home.address)
router.message.register(register_home_isitish, Home.isitish)
router.message.register(register_home_electro, Home.electro)
router.message.register(register_home_gas, Home.gas)
router.message.register(register_home_water, Home.water)
router.message.register(register_home_document, Home.document)
router.message.register(register_home_price, Home.price)
router.message.register(register_home_phone, Home.phone)
router.message.register(register_home_add, Home.add)
router.message.register(register_home_image, Home.image)
router.message.register(home_verify, Home.verify)



router.message.register(start_contact,F.text=='🔎 Qidiruv')
router.message.register(add_contact, Contact.start)
router.message.register(register_contact_name,Contact.name)
router.message.register(register_contact_phone, Contact.phone)
router.message.register(contact_verify, Contact.verify)










