from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import kb_cancel, kb_main,keyboard_choise
from init import bot
rt=Router()
id_u=None
keyboard = types.ReplyKeyboardMarkup(keyboard=kb_main,resize_keyboard=True)
keyboard_cn = types.ReplyKeyboardMarkup(keyboard=kb_cancel,resize_keyboard=True)
class States(StatesGroup):
    nick=State()
    screen=State()
    rate=State()
    bank=State()
@rt.message(F.text == "⏪ Отмена")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись в главное меню", reply_markup=keyboard)

@rt.message(F.text == "Рейтинговая")
async def nick(message: types.Message, state: FSMContext):
    await message.answer("Введите ваш NickName", reply_markup=keyboard_cn)
    await state.set_state(States.nick)
@rt.message(States.nick)
async def screen(message: types.Message, state: FSMContext):
    await state.update_data(nick=message.text)
    await message.answer("Пришлите скриншот вашей личной карточки с /time")
    await state.set_state(States.screen)
@rt.message(States.screen)
async def screen(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(screen=message.photo[-1].file_id)
        await message.answer("Введите количество вашего рейтинга")
        await state.set_state(States.rate)
    else:
        await message.answer("Вы отправили не фото")
@rt.message(States.rate)
async def rate(message: types.Message, state: FSMContext):
    await state.update_data(rate=message.text)
    await message.answer("Введите номер вашего банковского счёта")
    await state.set_state(States.bank)
@rt.message(States.bank)
async def rate(message: types.Message, state: FSMContext):
    await state.update_data(bank=message.text)
    global id_u
    id_u = message.from_user.id
    user_data = await state.get_data()
    await bot.send_photo(photo=user_data["screen"],chat_id="-1002047550383",caption=f"1.NickName: {user_data['nick']}\n"
                                                                                    f"2.Количество рейтинга: {user_data['rate']}\n"
                                                                                    f"3.Счёт в банке: {user_data['bank']}\n"
                                                                                    f"4.Контакт отправившего: @{message.from_user.username}\n"
                                                                                    f"5.Тип премии: рейтинговая\n")
    await bot.send_message(text="Одобрить заявку сверху?",chat_id="-1002047550383", reply_markup=keyboard_choise)
    await state.clear()
    await message.answer("Ваша заявка отправлена на обработку. Ожидайте",reply_markup=keyboard)
@rt.callback_query(F.data == 'rejection')
async def reject(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("❌Вы отклонили заявку")
    await bot.send_message(text="❌Ваша заявка получила отказ. Если вы не согласны с решением, напишите нам по контактам", chat_id=id_u)
@rt.callback_query(F.data == 'approved')
async def approv(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("✅Вы одобрили заявку")
    await bot.send_message(text="✅Ваша заявка одобрена. Ожидайте выплату в ближайшее время", chat_id=id_u)