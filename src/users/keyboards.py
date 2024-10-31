from typing import Any
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup





def get_user_inline_kb() -> InlineKeyboardMarkup:
    inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text='Оформить заказ', callback_data='user')]
        ]
    )
    return inline_kb