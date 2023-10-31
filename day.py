from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import kb_cancel, kb_main,keyboard_choise
from init import bot
from aiogram.types import InputMediaPhoto
rt=Router()
id_u=None
keyboard = types.ReplyKeyboardMarkup(keyboard=kb_main,resize_keyboard=True)
keyboard_cn = types.ReplyKeyboardMarkup(keyboard=kb_cancel,resize_keyboard=True)
class States(StatesGroup):
    nick_d=State()
    screen_d=State()
    screen_day= State()
    rate_d=State()
    bank_d=State()
@rt.message(F.text == "⏪ Отмена")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись в главное меню", reply_markup=keyboard)

@rt.message(F.text == "Топ дня")
async def nick(message: types.Message, state: FSMContext):
    await message.answer("Введите ваш NickName", reply_markup=keyboard_cn)
    await state.set_state(States.nick_d)
@rt.message(States.nick_d)
async def screen(message: types.Message, state: FSMContext):
    await state.update_data(nick=message.text)
    await message.answer("Пришлите скриншот вашей личной карточки с /time")
    await state.set_state(States.screen_d)
@rt.message(States.screen_d)
async def screen(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(screen=message.photo[-1].file_id)
        await message.answer("Пришлите скриншот статистики за день с /time")
        await state.set_state(States.screen_day)
    else:
        await message.answer("Вы отправили не фото")
@rt.message(States.screen_day)
async def screen(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(screen_day=message.photo[-1].file_id)
        await message.answer("Введите количество вашего рейтинга")
        await state.set_state(States.rate_d)
    else:
        await message.answer("Вы отправили не фото")
@rt.message(States.rate_d)
async def rate(message: types.Message, state: FSMContext):
    await state.update_data(rate=message.text)
    await message.answer("Введите номер вашего банковского счёта")
    await state.set_state(States.bank_d)
@rt.message(States.bank_d)
async def rate(message: types.Message, state: FSMContext):
    await state.update_data(bank=message.text)
    global id_u
    id_u = message.from_user.id
    user_data = await state.get_data()
    media =[InputMediaPhoto(media=user_data['screen']), InputMediaPhoto(media=user_data['screen_day'],caption=
                                                       f"1.NickName: {user_data['nick']}\n"
                                                       f"2.Количество рейтинга: {user_data['rate']}\n"
                                                       f"3.Счёт в банке: {user_data['bank']}\n"
                                                       f"4.Контакт отправившего: @{message.from_user.username}\n"
                                                       f"5.Тип премии: топ дня\n")
    ]
    await bot.send_media_group(media=media,chat_id="-1002047550383")
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