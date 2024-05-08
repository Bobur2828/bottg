from typing import Any
from sqlalchemy import BigInteger,String,ForeignKey,Column,Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship,Mapped,mapped_column,DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs,async_sessionmaker,create_async_engine
from config import SQLALCHEMY_URL
from typing import List
engine=create_async_engine(SQLALCHEMY_URL,echo=True)
async_session= async_sessionmaker(engine)

class Base(AsyncAttrs,DeclarativeBase):
    pass


class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)  
    tg_id: Mapped[int]=mapped_column(BigInteger,unique=True)

    def __reduce__(self):
        return self.tg_id


class Driver(Base):
    __tablename__ = 'drivers'
    id: Mapped[int]=mapped_column(primary_key=True)  
    tg_id: Mapped[int]=mapped_column(BigInteger,unique=True)
    tg_username: Mapped[str]=mapped_column()
    phone: Mapped[str]=mapped_column()
    car_name: Mapped[str]=mapped_column()
    car_number: Mapped[str]=mapped_column()

    def __repr__(self):
        return f"<Driver(id={self.id}, tg_username={self.tg_username})>"
    


class Phone(Base):
    __tablename__ = 'phone'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    price = Column(String)
    documents = Column(String)
    comment = Column(String)
    phone = Column(String)
    usernames = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))  # ForeignKey ile Category tablosuna bağlantı oluşturuldu.
    address = Column(String)
    position = Column(String)
    tg_id= Column(Integer)

    data = Column(String, server_default=func.now())

    category_phone = relationship('Category', foreign_keys=[category_id], back_populates='phone_rel')


    def __repr__(self):
        return self.name

class Cars(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    version = Column(String)
    detail = Column(String)
    color = Column(String)
    year = Column(String)
    probeg = Column(String)
    oil = Column(String)
    gas = Column(String)
    price = Column(String)
    usernames = Column(String)
    phone = Column(String)
    address = Column(String)
    image = Column(String)
    data = Column(String, server_default=func.now())
    tg_id= Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))  # ForeignKey ile Category tablosuna bağlantı oluşturuldu.
    category_cars = relationship('Category', back_populates='cat_cars')

    def __repr__(self):
        return self.name

class Home(Base):
    __tablename__ = 'home'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    xona = Column(String)
    kvadrat = Column(String)
    status = Column(String)
    address = Column(String)
    isitish = Column(String)
    phone = Column(String)
    image = Column(String)
    usernames = Column(String)
    electro = Column(String)
    gas = Column(String)
    water = Column(String)
    price = Column(String)
    document = Column(String)
    data = Column(String, server_default=func.now())
    comment = Column(String)
    tg_id= Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))  # ForeignKey ile Category tablosuna bağlantı oluşturuldu.
    category_home = relationship('Category', back_populates='cat_home')

    def __repr__(self):
        return self.name





class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(50))
    phone_rel: Mapped['Phone'] = relationship(back_populates='category_phone')
    cat_cars: Mapped['Cars'] = relationship(back_populates='category_cars')
    cat_home: Mapped['Home'] = relationship(back_populates='category_home')
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    tg_id = Column(Integer)

    def __repr__(self):
        return self.name


