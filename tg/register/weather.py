from aiogram.types import Message
import requests
import keyboards as kb

async def weather(message:Message):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Vodil,UZ&units=metric&appid=a9d86a9dc54f8caf39ac424735ffc2e6')
    text = f"📍Lokatsiya: {r.json()['name']}\n🌡️ Havo harorati: {r.json()['main']['temp']} C\n💦 Namlik: {r.json()['main']['humidity']}%\n🌬️Shamol tezligi: {r.json()['wind']['speed']}m/s"
    await message.answer(f"{text}",reply_markup=kb.menu)



import aiohttp

async def namoz(message: Message):
    r = requests.get("https://islomapi.uz/api/present/day?region=Farg'ona")
    data = r.json()

    region = data['region']
    date = data['date']
    weekday = data['weekday']
    hijri_month = data['hijri_date']['month']
    hijri_day = data['hijri_date']['day']
    tong_saharlik = data['times']['tong_saharlik']
    quyosh = data['times']['quyosh']
    peshin = data['times']['peshin']
    asr = data['times']['asr']
    shom_iftor = data['times']['shom_iftor']
    hufton = data['times']['hufton']

    text = f"📍Lokatsiya: {region}\n📅 Sana: {date} ({weekday})\n🌙 Hijriy Sana: {hijri_day} {hijri_month}\n\n⏰ Namoz Vaqtlari:\n🌅 Tong Saharlik: {tong_saharlik}\n🌞 Quyosh: {quyosh}\n🕌 Peshin: {peshin}\n🕒 Asr: {asr}\n🌆 Shom Iftor: {shom_iftor}\n🌌 Hufton: {hufton}"
    await message.answer(text, reply_markup=kb.menu)
