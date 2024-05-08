from database.models import User,Driver,Category,Phone,Cars,Home,Contact
from database.models import async_session
from sqlalchemy import select,update,delete,desc
from sqlalchemy.orm import Session
from aiogram import  Bot
from sqlalchemy import func

bot=Bot
async def get_user():
    query = select(User)

    try:
        async with async_session() as session:
            result = await session.execute(query)
            users = result.scalars().all()
            
            # Extract user IDs from the list of users
            user_ids = [user.tg_id for user in users if user.tg_id is not None]
            
            # Count the number of user IDs
            user_count = len(user_ids)
            
            return user_count
            
    except Exception as e:
        print(f"Ma'lumotlar bazasini so'rov bajarishda xatolik yuz berdi: {e}")
        return 0 

async def create_driver(tg_id: int, tg_username: str,phone: str, car_name: str, car_number: str):
    async with async_session() as session:
        try:
            new_driver = Driver(tg_id=tg_id, tg_username=tg_username, phone=phone, car_name=car_name, car_number=car_number)
            session.add(new_driver)
            await session.commit()

            return new_driver
        
        except Exception as e:
            await session.rollback()
            raise e
        
        finally:
            await session.close()


async def create_phone(name: str, image: str, price: str,documents: str, comment: str,phone:str,usernames:str,address:str,position:str,tg_id:int):
    async with async_session() as session:
        try:
            new_phone = Phone(name=name, image=image, price=price,documents=documents, comment=comment,phone=phone,usernames=usernames,category_id=1,address=address,position=position,tg_id=tg_id)
            session.add(new_phone)
            await session.commit()

            return new_phone
        
        except Exception as e:
            await session.rollback()
            raise e
        
        finally:
            await session.close()
async def create_cars(name: str, version: str,detail: str,color: str,year: str,probeg: str,oil: str,gas: str,price: str,usernames:str,phone: str,address: str,image: str,tg_id:int):
    async with async_session() as session:
        try:
            new_car = Cars(name=name, version=version,detail=detail,color=color,year=year,probeg=probeg,oil=oil,gas=gas,price=price,usernames=usernames,phone=phone,address=address,image=image,tg_id=tg_id,category_id=2)
            session.add(new_car)
            await session.commit()

            return new_car
        
        except Exception as e:
            await session.rollback()
            raise e
        
        finally:
            await session.close()
async def create_user(tg_id: int):
    async with async_session() as session:
        try:
            # Check if a user with the given tg_id already exists
            existing_user = await session.execute(select(User).filter(User.tg_id == tg_id))
            existing_user = existing_user.scalar_one_or_none()

            if existing_user:
                # If the user already exists, skip adding a new user
                print(f"User with tg_id {tg_id} already exists. Skipping...")
                return  # Exit the function

            # If the user does not exist, add a new user
            new_user = User(tg_id=tg_id)
            session.add(new_user)
            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e
        
        finally:
            await session.close()

async def create_home(name, type, xona, kvadrat, status, address, isitish, phone, image, usernames, electro, gas, price, document,comment,water, tg_id):
    # Veritabanı oturumu oluştur
    session = Session()

    try:
        # Yeni bir ev nesnesi oluştur
        new_home = Home(
            name=name,
            type=type,
            xona=xona,
            kvadrat=kvadrat,
            status=status,
            address=address,
            isitish=isitish,
            phone=phone,
            image=image,
            usernames=usernames,
            electro=electro,
            gas=gas,
            price=price,
            document=document,
            water=water,
            comment=comment,
            tg_id=tg_id,
            category_id=3
        )

        # Ev nesnesini veritabanına ekle
        session.add(new_home)
        # Değişiklikleri veritabanına uygula
        session.commit()
    except Exception as e:
        # Hata durumunda geri al
        session.rollback()
        raise e
    finally:
        # Oturumu kapat
        session.close()


async def create_home (name:str, type:str, xona:str, kvadrat:str, status:str, address:str, isitish:str, phone:str, image:str, usernames:str, electro:str, gas:str, price:str, document:str,comment:str,water:str, tg_id:int):
    async with async_session() as session:
        try:
            new_home = Home(name=name,type=type,xona=xona,kvadrat=kvadrat,status=status,address=address,isitish=isitish,phone=phone,image=image,usernames=usernames,electro=electro,gas=gas,price=price,document=document,water=water,comment=comment,tg_id=tg_id,category_id=3)
            session.add(new_home)
            await session.commit()

            return new_home
        
        except Exception as e:
            await session.rollback()
            raise e
        
        finally:
            await session.close()
async def get_categories():
    async with async_session() as session:
        categories=await session.scalars(select(Category))
        return categories        
        
async def get_category(category_id:int):
    async with async_session() as session:
        phone=await session.scalars(select(Telefon).where(Telefon.id==category_id))
        return phone
    

async def get_phone(id:int):
    if id:
        async with async_session() as session:
            phone=await session.scalar(select(Phone).where(Phone.id==id))
            return phone  
async def get_home(id:int):
    if id:
        async with async_session() as session:
            home = await session.scalar(select(Home).where(Home.id == id).order_by(desc(Home.data)))
            return home
        



last_index = 0

async def get_homes():
    global last_index
    async with async_session() as session:
        last_index += 1
        query = select(Home).order_by(desc(Home.data)).offset(last_index - 1).limit(1)
        result = await session.execute(query)
        home = result.scalars().first()
        if home is None:
            last_index = 0
        return home
    



async def get_car(id:int):
    if id:
        async with async_session() as session:
            phone=await session.scalar(select(Cars).where(Cars.id==id))
            return phone  


last_cars_index = 0

async def get_cars():
    global last_cars_index
    async with async_session() as session:
        last_cars_index += 1
        query = select(Cars).order_by(desc(Cars.data)).offset(last_cars_index - 1).limit(1)
        result = await session.execute(query)
        cars = result.scalars().first()
        if cars is None:
            last_cars_index = 0
        return cars

last_phone_index = 0

async def get_phones():
    global last_phone_index
    async with async_session() as session:
        last_phone_index += 1
        query = select(Phone).order_by(desc(Phone.data)).offset(last_phone_index - 1).limit(1)
        result = await session.execute(query)
        phone = result.scalars().first()
        if phone is None:
            last_phone_index = 0
        return phone
    


# async def create_contact(name, phone,tg_id):
#     session = Session()

#     try:
#         new_contact = Contact(
#             name=name,
#             phone=phone,
#             tg_id=tg_id,
#         )

#         session.add(new_contact)
#         session.commit()
#     except Exception as e:
#         session.rollback()
#         raise e
#     finally:
#         session.close()


async def create_contact (name:str,  phone:str,  tg_id:int):
    async with async_session() as session:
        try:
            new_contact = Contact(name=name,phone=phone,tg_id=tg_id)
            session.add(new_contact)
            await session.commit()

            return new_contact
        
        except Exception as e:
            await session.rollback()
            raise e
        
        finally:
            await session.close()

async def search_contact(search_query):
    try:
        async with async_session() as session:
            contacts = await session.execute(select(Contact).filter(Contact.name.like(f'%{search_query}%')))
            contacts_list = contacts.scalars().all()
            if contacts_list:
                return contacts_list
            else:
                contacts = await session.execute(select(Contact).filter(Contact.phone.like(f'%{search_query}%')))
                return contacts.scalars().all()
    except Exception as e:
        return None
