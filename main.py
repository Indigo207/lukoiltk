from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from init import bot
from keyboards import kb_main,kb_info,kb_awards
from texts import *
import asyncio, logging, rating,day,week
from aiogram.fsm.storage.memory import MemoryStorage
dp = Dispatcher(bot=bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
dp.include_router(rating.rt)
dp.include_router(day.rt)
dp.include_router(week.rt)
keyboard_award=types.ReplyKeyboardMarkup(keyboard=kb_awards,resize_keyboard=True)
keyboard = types.ReplyKeyboardMarkup(keyboard=kb_main,resize_keyboard=True)
keyboard_info = types.ReplyKeyboardMarkup(keyboard=kb_info,resize_keyboard=True)
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(hello, reply_markup=keyboard)
@dp.message(F.text=="ℹ️ Информация")
async def info(message: types.Message):
    await message.answer(info_t, reply_markup=keyboard_info)

@dp.message(F.text=="🆕 Новости")
async def news(message: types.Message):
    await message.answer(news_t,parse_mode="HTML")
@dp.message(F.text == "💰 Премии")
async def awards(message: types.Message):
    await message.answer(awards_t)
@dp.message(F.text=="🆒 Наш чат")
async def chat(message: types.Message):
    await message.answer(chat_t)
@dp.message(F.text == "⏪ В главное меню")
async def news(message: types.Message):
    await start(message)

@dp.message(F.text == "▶️ Контакты")
async def contacts(message: types.Message):
    await message.answer(contacts_t)
@dp.message(F.text == "💸 Подать заявку на премию")
async def contacts(message: types.Message):
    await message.answer("Выберите тип премии", reply_markup=keyboard_award)
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())