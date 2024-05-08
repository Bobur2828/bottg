from aiogram import Dispatcher, Bot, types
from aiogram.types import Message,CallbackQuery
from asyncio import run
from states import Drive_reg
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from keyboards import inline_markup
from database.requests import create_driver
import keyboards as kb


async def dr_cancel(message: Message, bot: Bot, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is  None:
        await message.answer("Sizda ariza yaratilmagan. Bekor qilish uchun ariza kerak emas.")
    else:
        await state.clear()
        await message.answer("Joriy ariza bekor qilindi.",reply_markup=kb.start)


async def new_command(message:Message,bot:Bot, state:FSMContext):
    await message.answer("Ismingiz kiriting")
    await state.set_state(Drive_reg.name)

async def stop_command(message: Message, bot: Bot, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is  None:
        await message.answer("Sizda ariza yaratilmagan. Bekor qilish uchun ariza kerak emas.")
    else:
        await state.clear()
        await message.answer("Joriy ariza bekor qilindi.")

async def start_register(message:Message,bot:Bot, state:FSMContext):
    await message.answer("Ismingizni kiriting",reply_markup=kb.cancel)
    await state.set_state(Drive_reg.name)

async def register_name(message: Message, bot: Bot, state: FSMContext):
    name = message.text.strip()  
    if any(char.isdigit() for char in name):
        await message.answer("Ismingiz raqamdan iborat. Iltimos, faqat harfli ism kiriting.❌")
    else:
        await state.update_data(name=name)  
        await message.answer("Ismingiz qabul qilingdi ✅")
        
        await message.answer("Telefon raqamingizni kiriting.", reply_markup=kb.contact,)
        
        # await message.answer("To'liq holatda '+99891123456'")

        await state.set_state(Drive_reg.phone)  
# async def ariza_age(message:Message,bot:Bot,state:FSMContext):
#     if message.text.isdigit():
#         if int(message.text)<80 and int(message.text)> 0:
#             await message.answer("Yoshingiz qabul qilindi")
#             await message.answer("Telefon raqamingizni kiriting masalan 998911234567")

#             await state.update_data(age=message.text)
#             await state.set_state(Ariza.phone)
#         else:
#             await message.answer("Yoshingizni to'gri kiriting.")
#     else:
#         await message.answer("Yoshingiz faqatat raqamdan iborat bo'lishi kerak.")
async def register_phone(message: Message, bot: Bot, state: FSMContext):
    if message.contact:
        phone=message.contact.phone_number
        await message.answer("Telefon raqamingiz qabul qilindi✅")
        await message.answer("Mashinangiz markasi 'Lacetti",reply_markup=kb.cancel)

        # Ma'lumotlarni saqlash va keyingi holatga o'tish
        await state.update_data(phone=phone)
        await state.set_state(Drive_reg.car_name)
    else:
        phone_number = message.text.strip(" ")
        phone_number1 = phone_number[1:-1]
        # Faqat raqam belgilari bo'lishini tekshirish
        if phone_number1.isdigit():
            if len(phone_number) == 13:
                # Raqam +998 bilan boshlanishi kerak
                if phone_number.startswith('+998'):
                    await message.answer("Telefon raqamingiz qabul qilindi✅")
                    await message.answer("Mashinangiz markasi 'Lacetti",reply_markup=kb.cancel)

                    # Ma'lumotlarni saqlash va keyingi holatga o'tish
                    await state.update_data(phone=message.text)
                    await state.set_state(Drive_reg.car_name)
                else:
                    await message.answer("Telefon raqamingiz +998 bilan boshlanishi kerak.❌")
            else:
                await message.answer("Telefon raqamingiz 13 ta raqamdan iborat bo'lishi kerak.❌")
        else:
            await message.answer("Telefon raqamingiz faqat raqamlardan iborat bo'lishi kerak.❌")



async def register_carname(message: Message, bot: Bot, state: FSMContext):
    car_name = message.text.strip()  
    if any(char.isdigit() for char in car_name):
        await message.answer("Mashinangiz nomi faqat harflardan iborat bo'lsin.❌")
    else:
        await state.update_data(car_name=car_name)  
        await message.answer("Mashinangiz raqamini kiriting 40A777AA",reply_markup=kb.cancel)
        await state.set_state(Drive_reg.car_number)  

async def register_carnumber(message: Message, bot: Bot, state: FSMContext):
    car_number = message.text.strip()
    print(car_number)
    # 1. Ma'lumot uzunligi 8 belgidan iborat bo'lishi kerak
    if not len(car_number) == 8:
        await message.answer(f"Mashina raqami {car_number} uzunligi noto'g'ri.❌")
       

    # 2. Birinchi ikki belgi faqat raqamlardan iborat bo'lishi kerak
    first_two_digits = car_number[:2]
    if not first_two_digits.isdigit():
        await message.answer(f"Mashina raqami {car_number} birinchi ikki belgisi raqamlardan iborat emas.❌")
        return

    # 3. Keyingi uchta belgi faqat raqamlardan iborat bo'lishi kerak
    middle_digits = car_number[3:5]
    if not middle_digits.isdigit():
        await message.answer(f"Mashina raqami {car_number} keyingi uchta belgilari raqamlardan iborat emas.❌")
        return

    # 4. Oxirgi uchta belgi harflardan iborat bo'lishi kerak
    last_three_chars = car_number[6:7]
    if not last_three_chars.isalpha():
        await message.answer(f"Mashina raqami {car_number} oxirgi 2 ta harfi notog'ri.❌")
        return
    three_chars = car_number[2]
    if not three_chars.isalpha():
        await message.answer(f"Mashina raqami {car_number} oxirgi uchta belgilari harflardan iborat emas❌")
        return
    # Agar barcha shartlar bajarilgan bo'lsa, ma'lumotlarni saqlash va keyingi holatga o'tish
    await state.update_data(car_number=car_number)
    await message.answer("Mashina raqami qabul qilindi.✅")
    data= await state.get_data()
    data1= state.get_data()
    print(data1)
    register_data = (
        f"👨‍✈️ **Haydovchi Ismi: {data.get('name')}\n"
        f"📱 **Haydovchi Telegrami:: @{message.from_user.username}\n"
        f"☎️ **Telefon Raqam: {data.get('phone')}\n"
        f"🚗 **Mashina Turi:: {data.get('car_name')}\n"
        f"🚘 **Mashina Raqami: {data.get('car_number')}\n"
        )
    await message.answer(register_data)
    
    await message.answer("Buyurtmalar qabul qilish uchun\nTasdiqlash tugmasini bosing",reply_markup=kb.confirm)
    await state.set_state(Drive_reg.verify)
# async def ariza_job(message:Message, bot:Bot, state:FSMContext):
#     await state.update_data(job=message.text)
#     await message.answer("Kasbingiz qabul qilindi")
#     data= await state.get_data()
#     ariza = (
#              f"Ariza Beruvchi: {data.get('name')}\n"
#              f"Yoshi: {data.get('age')}\n"
#              f"Telefon raqami: {data.get('phone')}\n"
#              f"Kasbi: {data.get('job')}\n"
#              )
#     await message.answer(ariza)
    
#     await message.answer("Malumotlarni yuborishni tasdiqlaysizmi  Xa yoki Yo'q")
#     await state.set_state(Ariza.verify)

async def register_verify(message:Message,bot:Bot,state:FSMContext):

    if message.text.lower() == "✅tasdiqlash":
        data= await state.get_data()
        data1= state.get_data()
        print(data1)
        register_data = (
            f"👨‍✈️ **Haydovchi Ismi: {data.get('name')}\n"
            f"📱 **Haydovchi Telegrami:: @{message.from_user.username}\n"
            f"☎️ **Telefon Raqam: {data.get('phone')}\n"
            f"🚗 **Mashina Turi:: {data.get('car_name')}\n"
            f"🚘 **Mashina Raqami: {data.get('car_number')}\n"
            )
        await bot.send_message(1327096215,register_data)
        try:
            await create_driver(message.from_user.id, f"@{message.from_user.username}",f"{data.get('phone')}", f"{data.get('car_name')}", f"{data.get('car_number')}")
            await message.answer(f"Ma'lumotlaringiz bizning bazamizga saqlandi\n Yangi buyurtmalar bo'lsa sizga xabar beramiz",)
            # await state.finish()
            await state.clear()
        except Exception as e:
            await message.answer(f"Sizning malumotlaringiz bizning bazamizda mavjud")
            await state.clear()
            

async def confirm_action(callback_data: CallbackQuery):
    await callback_data.answer()  # Funksiya takroriy murojaatni javoblash uchun callback_data obyektiga javob yuboradi
    message_text = "ha"
    return message_text