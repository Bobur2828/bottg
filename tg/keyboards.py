from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.requests import get_categories, get_category
class CustomKeyboard:
    def __init__(self, buttons):
        self.buttons = buttons

# Boshlang'ich menyuga oid klaviatura
start_buttons = [[KeyboardButton(text="🤖Menu")]]
start = ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

# Asosiy menyuga oid klaviatura
menu_buttons = [
    [KeyboardButton(text="🔎 Qidiruv"), KeyboardButton(text="🤝 Oldi-Sotdi")],
    [ KeyboardButton(text="🚕 Toshkent-Vodil")],
    [ KeyboardButton(text="☀️ Ob-Havo"), KeyboardButton(text="🌙 Namoz Vaqtlari")],

]

KeyboardButton(text="💼 Turli Xizmatlar")
menu = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

# Taxi tugmalariga oid klaviatura
taxi_buttons = [[KeyboardButton(text="🚕Haydovchi"), KeyboardButton(text="🚶Yo'lovchi")],
                [KeyboardButton(text="🤖Menu")]]


taxi = ReplyKeyboardMarkup(keyboard=taxi_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

# Xizmatlar tugmalariga oid klaviatura
xizmat_buttons = [
    [KeyboardButton(text="🚛Yuk tashish"), KeyboardButton(text="👷‍♂️Kunlik ishlar")],
    [ KeyboardButton(text="🛠Akfa Eshik Romlar"),KeyboardButton(text="🪜Yevro remont")],
    [ KeyboardButton(text="🪚Tom yopish"), KeyboardButton(text="🤖Menu")]
]
xizmat = ReplyKeyboardMarkup(keyboard=xizmat_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

# Savdo tugmalariga oid klaviatura
store_buttons = [
    [KeyboardButton(text="📱Telefon Savdo"), KeyboardButton(text="🚘Avto Savdo")],
    [ KeyboardButton(text="🏠Uy Savdo"),KeyboardButton(text="🤖Menu")],
]
store = ReplyKeyboardMarkup(keyboard=store_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

taxi1_buttons = [
    [KeyboardButton(text="✍️Ro'yhatdan o'tish"), KeyboardButton(text="🤖Menu")],
]
taxi1 = ReplyKeyboardMarkup(keyboard=taxi1_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

custom_buttons = [
    [KeyboardButton(text="📞Buyurtma berish"), KeyboardButton(text="🤖Menu")],
]
custom_taxi = ReplyKeyboardMarkup(keyboard=custom_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")


contact_button = [
    [KeyboardButton(text="📞Raqam yuborish",request_contact=True),KeyboardButton(text="❌Bekor qilish")],


]
contact = ReplyKeyboardMarkup(keyboard=contact_button, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

confirm_button = [
    [KeyboardButton(text="✅Tasdiqlash"),KeyboardButton(text="❌Bekor qilish")],


]
confirm = ReplyKeyboardMarkup(keyboard=confirm_button, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

count_custom = [
    [KeyboardButton(text="1️⃣"),KeyboardButton(text="2️⃣"),KeyboardButton(text="3️⃣"),KeyboardButton(text="4️⃣")],
    [KeyboardButton(text="4️⃣➕"),KeyboardButton(text="📦Pochta"),KeyboardButton(text="❌Bekor qilish")],


]
count_custom_button= ReplyKeyboardMarkup(keyboard=count_custom, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

drive_buttons = [
    [KeyboardButton(text="⛪️Farg'ona")],
    [KeyboardButton(text="🏢Toshkent")],
    [KeyboardButton(text="⛰Vodil")],
    [KeyboardButton(text="❌Bekor qilish")]



]
drive = ReplyKeyboardMarkup(keyboard=drive_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

time_buttons = [
    [KeyboardButton(text="06:00-07:00"),KeyboardButton(text="07:00-08:00"),KeyboardButton(text="08:00-09:00"),KeyboardButton(text="09:00-10:00")],
    [KeyboardButton(text="10:00-11:00"),KeyboardButton(text="11:00-12:00"),KeyboardButton(text="12:00-13:00"),KeyboardButton(text="14:00-15:00")],
    [KeyboardButton(text="15:00-16:00"),KeyboardButton(text="16:00-17:00"),KeyboardButton(text="17:00-18:00"),KeyboardButton(text="19:00-20:00")],
    [KeyboardButton(text="20:00-21:00"),KeyboardButton(text="21:00-22:00"),KeyboardButton(text="22:00-23:00"),KeyboardButton(text="23:00-00:00")],
    [KeyboardButton(text="01:00-02:00"),KeyboardButton(text="02:00-03:00"),KeyboardButton(text="03:00-04:00"),KeyboardButton(text="04:00-05:00")],


]
time= ReplyKeyboardMarkup(keyboard=time_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

yesorno_buttons = [
    [KeyboardButton(text="Ha")],
    [KeyboardButton(text="Yo'q")],
    [KeyboardButton(text="🤖Menu")],


]
yesorno = ReplyKeyboardMarkup(keyboard=yesorno_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

avto_buttons = [
    [KeyboardButton(text="💰Sotish "),KeyboardButton(text="🤝Sotib olish")],
    [KeyboardButton(text="🤖Menu")],


]
custom = ReplyKeyboardMarkup(keyboard=avto_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")


home_buttons = [
    [KeyboardButton(text="Hovli uy"), KeyboardButton(text="Kvartira")],
    [KeyboardButton(text="Yer maydoni"), KeyboardButton(text="❌Bekor qilish")],

]
home = ReplyKeyboardMarkup(keyboard=home_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

home_buttons1 = [
    [KeyboardButton(text="Turar joy"), KeyboardButton(text="NoTurar joy")],
    [KeyboardButton(text="❌Bekor qilish")],

]
home1 = ReplyKeyboardMarkup(keyboard=home_buttons1, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

isitish_buttons = [
    [KeyboardButton(text="Bor"), KeyboardButton(text="Yo'q")],
    [KeyboardButton(text="❌Bekor qilish")],

]
isitish = ReplyKeyboardMarkup(keyboard=isitish_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

gas_buttons = [
    [KeyboardButton(text="Metan"), KeyboardButton(text="Propan")],
    [KeyboardButton(text="Qo'shimcha yo'q"),KeyboardButton(text="❌Bekor qilish")],

]
gas = ReplyKeyboardMarkup(keyboard=gas_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")









animal_buttons = [
    [KeyboardButton(text="🐄Mol"), KeyboardButton(text="🐏Qo'y")],
    [ KeyboardButton(text="🐓Tovuq"),KeyboardButton(text="🐕It")],
    [ KeyboardButton(text="Boshqa"), KeyboardButton(text="🤖Menu")]
]
animal = ReplyKeyboardMarkup(keyboard=xizmat_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")







contact_buttons = [
    [KeyboardButton(text="➕Raqam qo'shish"),KeyboardButton(text="🤖Menu")],
    


]
contact1 = ReplyKeyboardMarkup(keyboard=contact_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Qidiruv matnini kiriting")






inline_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Tasdiqlash", callback_data="Tasdiqlash")
            ]
        ]
    )


phone_buttons = [
    [KeyboardButton(text="Sotish"),KeyboardButton(text="Sotib olish")],
    [KeyboardButton(text="🤖Menu")]

]
phone= ReplyKeyboardMarkup(keyboard=phone_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

phone_position = [
    [KeyboardButton(text="🆕Yangi"),KeyboardButton(text="🔃B/U")],
    [KeyboardButton(text="❌Bekor qilish")]

]
position= ReplyKeyboardMarkup(keyboard=phone_position, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

cancel_buttons = [
    [KeyboardButton(text="❌Bekor qilish")]
]
cancel= ReplyKeyboardMarkup(keyboard=cancel_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")

verify_phone_buttons = [
    [KeyboardButton(text="🗳Karobka"),KeyboardButton(text="🧾Passport nusxa")],
    [KeyboardButton(text="🤷Hech nima"),KeyboardButton(text="❌Bekor qilish")]
]
verify_phone= ReplyKeyboardMarkup(keyboard=verify_phone_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")


more_buttons = [
    [KeyboardButton(text="👀Yana ko'rish")],
    [KeyboardButton(text="💰Sotish"),KeyboardButton(text="🤖Menu")],

]
more= ReplyKeyboardMarkup(keyboard=more_buttons, resize_keyboard=True,is_persistent=True,input_field_placeholder="Tugmalardan birini tanlang")


async def categorys():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name,callback_data=f'category_{category.id}'))
        
    return keyboard.adjust(2).as_markup()



async def phones(category_id:int):
    items = await get_category(category_id)
    print(items)
    keyboard = InlineKeyboardBuilder()
    for item in items:
        print(item)
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))

    return keyboard.adjust(2).as_markup()


