from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
kb_main = [
    [types.KeyboardButton(text="ℹ️ Информация")],
    [types.KeyboardButton(text="💸 Подать заявку на премию")],
    [types.KeyboardButton(text="🆔 Личный кабинет")],
    [types.KeyboardButton(text="▶️ Контакты")],
]
kb_info= [
    [types.KeyboardButton(text="🆕 Новости")],
    [types.KeyboardButton(text="💰 Премии")],
    [types.KeyboardButton(text="🆒 Наш чат")],
    [types.KeyboardButton(text="⏪ В главное меню")],
]
kb_cancel=[[types.KeyboardButton(text="⏪ Отмена")]]
kb_awards=[
    [types.KeyboardButton(text="Рейтинговая")],
    [types.KeyboardButton(text="Топ дня")],
    [types.KeyboardButton(text="Топ недели")],
]

reject = InlineKeyboardButton(text='❌ Отказ',callback_data='rejection')
approve = InlineKeyboardButton(text='✅ Одобрено',callback_data='approved')
keyboard_choise = InlineKeyboardMarkup(inline_keyboard=[[reject,approve]])