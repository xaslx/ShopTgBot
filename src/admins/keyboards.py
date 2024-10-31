from typing import Any
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram import Bot
from config import env_config



bot: Bot = Bot(token=env_config.TOKEN_BOT)
ADMINS_ID: list[int] = env_config.ADMINS_ID



def get_admin_inline_kb(article: int) -> InlineKeyboardMarkup:
    inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text='Удалить товар', callback_data=f'delete:item:{article}')],
            [InlineKeyboardButton(text='Редактировать название', callback_data=f'edit:title:{article}')],
            [InlineKeyboardButton(text='Редактировать описание', callback_data=f'edit:description:{article}')],
            [InlineKeyboardButton(text='Редактировать цену', callback_data=f'edit:price:{article}')],
            [InlineKeyboardButton(text='Редактировать количество', callback_data=f'edit:quantity:{article}')],
            [InlineKeyboardButton(text='Изменить размеры', callback_data=f'edit:sizes:{article}')],
            [InlineKeyboardButton(text='Изменить фото', callback_data=f'edit:photo:{article}')]
        ]
    )
    return inline_kb


def confirm_delete_item(article: int) -> InlineKeyboardMarkup:
    inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text='Удалить', callback_data=f'confirm:delete:item:{article}'),
                InlineKeyboardButton(text='Отменить', callback_data=f'cancel:delete:item:{article}')
            ]
        ]
    )
    return inline_kb



def admin_commands() -> ReplyKeyboardMarkup:
    kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Сделать рассылку')],
            [KeyboardButton(text='Добавить новый товар')],
            [KeyboardButton(text='Отменить действие')]
        ],
        resize_keyboard=True
    )
    return kb