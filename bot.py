from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, file
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import io
import json
import urllib.request 
import socket
import struct
import os
from config import PORT_FOR_SERVER, HOST






#Connected API
token = "6985975373:AAFODgMeCWBSSt6XmkCr4frqPjSKO6FzX7Y"
bot = Bot(token=token)
dp = Dispatcher(bot)
headers = {"Accept_Language":"ru"}
file_name = ""

#Create buttons
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton("Прикрепите файл чека"),
    KeyboardButton("Что у меня в холодильнике")
)

def send_file(sck: socket.socket, filename):
    # Получение размера файла.
    filesize = os.path.getsize(filename)
    # В первую очередь сообщим серверу,
    # сколько байт будет отправлено.
    sck.sendall(struct.pack("<Q", filesize))
    # Отправка файла блоками по 1024 байта.
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)

def Json_read(filename):
    with io.open(filename, encoding='utf-8') as f: 
        d = json.load(f) 
     
    l = [] 
 
    for elem in d[0]["ticket"]["document"]["receipt"]["items"]: 
        new_d = {elem["name"]: elem["quantity"]} 
        l.append(new_d) 
 
    return l



@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в свой холодильник", reply_markup = keyboard1)


@dp.message_handler(Text(equals='Прикрепите файл чека'))
async def ans_for_but_fake(message: types.Message):
    await message.answer("Теперь отправь файл чека")


@dp.message_handler(Text(equals='Что у меня в холодильнике'))
async def list_fridge(message: types.Message):
    global file_name
    for i in Json_read(file_name):
        name_product = list(i.keys())[0]
        text = f"Осталось {name_product} в количестве {i[name_product]}"
        await bot.send_message(message.chat.id, text)




@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def bot_ans_pull_json(message: types.Message ):
    documend_id = message.document.file_id
    file_info = await bot.get_file(documend_id)
    fi = file_info.file_path
    global file_name
    name = message.document.file_name
    file_name = name
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{token}/{fi}', f'{name}')

    conn = socket.create_connection((HOST, PORT_FOR_SERVER))
    send_file(conn, file_name)
    print("GOOOOD BLIAT")
    


if __name__ ==  '__main__':
    executor.start_polling(dp, skip_updates=True)