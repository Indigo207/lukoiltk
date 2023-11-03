import sqlite3
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import kb_cancel, kb_main
keyboard = types.ReplyKeyboardMarkup(keyboard=kb_main,resize_keyboard=True)
keyboard_cn = types.ReplyKeyboardMarkup(keyboard=kb_cancel,resize_keyboard=True)
rt=Router()
class States(StatesGroup):
    nick_lk=State()
    bank_lk=State()
class Lk:
    def __init__(self,db):
        self.conn=sqlite3.connect(db)
        self.cursor=self.conn.cursor()
    def add_user(self,tg_id,nick,bank):
        self.cursor.execute("INSERT INTO 'users' ('tg_id','nick','bank') VALUES (?, ?, ?)",(tg_id,nick,bank,))
        return self.conn.commit()
    def get_nick(self,tg_id):
        result=self.cursor.execute("SELECT nick FROM 'users' WHERE tg_id=?",(tg_id,)).fetchone()
        return ''.join(result)
    def find(self,tg_id):
        result=self.cursor.execute("SELECT tg_id FROM 'users' WHERE tg_id=?",(tg_id,))
        return result.fetchall()
    def get_bank(self,tg_id):
        result=self.cursor.execute("SELECT bank FROM 'users' WHERE tg_id=?",(tg_id,)).fetchone()
        return ''.join(result)
    def close(self):
        self.conn.close()
lk=Lk("users.db")
@rt.message(F.text == "⏪ Отмена")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись в главное меню", reply_markup=keyboard)
@rt.message(F.text == "🆔 Личный кабинет")
async def kab(message: types.Message, state: FSMContext):
    if lk.find(message.from_user.id)==[]:
        await message.answer("Вам нужно создать личный кабинет. Введите ваш NickName", reply_markup=keyboard_cn)
        await state.set_state(States.nick_lk)
    else:
        tg_id=message.from_user.id
        nick=lk.get_nick(tg_id)
        bank=lk.get_bank(tg_id)
        await message.answer(f"Вы вошли в личный кабинет\n"
                             f"Ваш идентификатор: {tg_id}\n"
                             f"Ваш NickName: {nick}\n"
                             f"Ваш счёт в банке: {bank}")
@rt.message(States.nick_lk)
async def nick(message: types.Message, state: FSMContext):
    await state.update_data(nick=message.text)
    await message.answer("Введите номер вашего банковского счёта")
    await state.set_state(States.bank_lk)
@rt.message(States.bank_lk)
async def bank(message: types.Message, state: FSMContext):
    await state.update_data(bank=message.text)
    user_data = await state.get_data()
    lk.add_user(message.from_user.id,user_data['nick'],user_data['bank'])
    await state.clear()
    await message.answer("Ваш личный кабинет был успешно создан", reply_markup=keyboard)