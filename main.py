from aiogram import Dispatcher, types, F
from aiogram.types import ChatMemberUpdated
from aiogram.filters import Command, IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.methods import DeleteWebhook
from init import bot
from keyboards import kb_main,kb_info,kb_awards
from texts import *
import asyncio, logging, rating,day,week,lk
from aiogram.fsm.storage.memory import MemoryStorage
dp = Dispatcher(bot=bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
dp.include_router(rating.rt)
dp.include_router(day.rt)
dp.include_router(week.rt)
dp.include_router(lk.rt)
keyboard_award=types.ReplyKeyboardMarkup(keyboard=kb_awards,resize_keyboard=True)
keyboard = types.ReplyKeyboardMarkup(keyboard=kb_main,resize_keyboard=True)
keyboard_info = types.ReplyKeyboardMarkup(keyboard=kb_info,resize_keyboard=True)
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(hello, reply_markup=keyboard)
@dp.message(F.text=="ℹ️ Информация")
async def info(message: types.Message):
    await message.answer(info_t, reply_markup=keyboard_info)
@dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    await event.answer(f"Привет, {event.new_chat_member.user.first_name}!\n"
                       f"Я - бот транспортной компании Лукойл на сервере Владикавказ!"
                       f"Если ты с Чебоксар, то ошибся чатом ¯\_(ツ)_/\n"
                       f"С информацией о премиях можно ознакомится в https://t.me/lukoiltk_bot\n"
                       f"Там же можно подать заявку на премию, но перед этим не забудь создать личный кабинет!\n"
                       f"Это можно сделать, нажав на кнопку 'Личный кабинет'\n"
                       f"Спасибо за прочтение")
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
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())