import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TG_TOKEN


bot = Bot(token=TG_TOKEN)
dispatcher = Dispatcher()


@dispatcher.message(F.text == 'привет')
async def greeting(message: Message):
    await message.answer('Приятно встретить воспитанного человека. Не так часто боту говорят Привет. '
                         'А мы так любим вежливых людей')

@dispatcher.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять комманды \n'
                         '/start - запуск \n'
                         '/help - помощь \n'
                         '/joke - шутка \n'
                         '/forecast - прогноз погоды')

@dispatcher.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!!! Я бот, меня зовут Ларс')


async def main():
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
