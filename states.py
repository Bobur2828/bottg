from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext


class Drive_reg(StatesGroup):
    name=State()
    phone=State()
    car_name=State()
    car_number=State()
    verify=State()

class CustomTaxi(StatesGroup):
    name=State()
    adressA=State()
    adressB=State()
    time=State()
    count=State()
    phone=State()
    comment=State()
    verify=State()

class Phone(StatesGroup):
    start=State()
    name=State()
    document=State()
    position=State()
    price=State()
    address=State()
    comment=State()
    phone=State()
    image=State()
    verify=State()



class Cars(StatesGroup):
    start=State()
    name=State()
    version=State()
    color=State()
    detail=State()
    year=State()
    probeg=State()
    oil=State()
    gas=State()
    price=State()
    phone=State()
    address=State()
    image=State()
    verify=State()

class Home(StatesGroup):
    start=State()
    name=State()
    type=State()
    xona=State()
    kvadrat=State()
    status=State()
    address=State()
    isitish=State()
    electro=State()
    gas=State()
    water=State()
    document=State()
    price=State()
    phone=State()
    image=State()
    add=State()
    verify=State()

class Contact(StatesGroup):
    start=State()
    name=State()
    phone=State()
    verify=State()

class AI(StatesGroup):
    talk = State()

class DriverJobs(StatesGroup):
    start = State()
    name = State()
    carname = State()
    xizmat  = State()
    image = State()
    verify = State()
    