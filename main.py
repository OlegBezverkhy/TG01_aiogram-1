import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TG_TOKEN, OPEN_WEATHERMAP
from jokes import JOKES
from random import choice
import requests


bot = Bot(token=TG_TOKEN)
dispatcher = Dispatcher()


def get_weather(city, city_ru):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHERMAP}&units=metric"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        main = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        weather_report = (
            f"Погода в городе {city_ru}:\n"
            f"Описание: {main}\n"
            f"Температура: {temp}°C\n"
            f"Ощущается как: {feels_like}°C\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
        return weather_report
    else:
        return "Не удалось получить данные о погоде."


@dispatcher.message(F.text == 'Привет')
async def greeting(message: Message):
    await message.answer('Приятно встретить воспитанного человека. Не так часто боту говорят Привет. '
                             'А мы так любим вежливых людей')

@dispatcher.message(F.photo )
async def ansewer_photo(message: Message):
    answer_list = ['Классное фото', 'Что это?', 'Не надо мне это показывать больше',
                   'Фотографу руки оторвать', 'Удачный кадр!']
    await message.answer(choice(answer_list))


@dispatcher.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять комманды \n'
                         '/start - запуск \n'
                         '/help - помощь \n'
                         '/joke - шутка \n'
                         '/forecast - прогноз погоды \n'
                         '/photo - пришлет тебе фото')


@dispatcher.message(Command('joke'))
async def jokes(message: Message):
    await message.answer(choice(JOKES))


@dispatcher.message(Command('forecast'))
async def wether_forecast(message: Message):
    city = 'Kaliningrad'
    city_ru = 'Калининград'
    weather = get_weather(city, city_ru)
    await message.answer(weather)


@dispatcher.message(Command('photo'))
async def photo(message: Message):
    photo_list =['https://avatars.mds.yandex.net/i?id=d42bb4fccc692c80c905a00ab0d7e1aa3b673f35-9856182-images-thumbs&n=13',
                 'https://yandex.ru/images/search?source=related-0&text=улицы+калининграда&pos=1&rpt='
                 'simage&nomisspell=1&img_url=https%3A%2F%2Fsun9-79.userapi.com%2Fs%2Fv1%2Fif1%2F6VEk13scq5OndMVX_'
                 'iff1yFuUq_36bxC0yqgl9YrPQsgZ5-UvgeIpXpkm5IwsDAnlyWjRl1R.jpg%3Fsize%3D604x340%26quality%3D96'
                 '%26type%3Dalbum&from=tabbar&lr=117683',
                 'https://yandex.ru/images/search?p=1&source=related-0&text=улицы+калининграда&pos=2&rpt=simage&nomisspell=1&img_url=https%3A%2F%2Fpro-dachnikov.com%2Fuploads%2Fposts%2F2021-10%2F1633497152_3-p-dom-v-kaliningrade-foto-3.jpg&from=tabbar&lr=117683',
                 'https://yandex.ru/images/search?p=1&source=related-0&text=улицы+калининграда&pos=24&rpt=simage&nomisspell=1&img_url=https%3A%2F%2Fpp.userapi.com%2Fc844720%2Fv844720275%2Fb597%2FUdbQpFm5UTA.jpg&from=tabbar&lr=117683',
                 'https://yandex.ru/images/search?p=1&source=related-0&text=улицы+калининграда&pos=28&rpt=simage&nomisspell=1&img_url=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F3a%2Fde%2Fb3%2F3adeb380cf5aed12f4029ccccb80b95e.jpg&from=tabbar&lr=117683']
    await message.answer_photo(photo=choice(photo_list), caption='Калинград - это мой любимый город')


@dispatcher.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!!! Я бот, меня зовут Ларс')


async def main():
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
