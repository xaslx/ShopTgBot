from typing import Any
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from src.models.user import User
from src.repositories.item import ItemRepository
from src.repositories.user import UserRepository
from src.users.keyboards import get_user_inline_kb
from src.admins.keyboards import get_admin_inline_kb
from config import env_config
from src.utils import get_item_into




user_handler: Router = Router(name='User Router')
ADMINS_ID: list[int] = env_config.ADMINS_ID


@user_handler.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего.\n\n')


@user_handler.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы отменили действие'
    )
    await state.clear()



@user_handler.message(StateFilter(default_state), CommandStart())
async def start_cmd(message: Message, session: AsyncSession):
    user: User = await UserRepository.find_one_or_none(session=session, user_telegram_id=message.from_user.id)
    await message.answer('<b>Введите артикул</b>')
    if not user:
        await UserRepository.add(session=session, user_telegram_id=message.from_user.id)
    




@user_handler.message(StateFilter(default_state))
async def echo(message: Message, session: AsyncSession):
    item: None | Item = None
    inline_kb: InlineKeyboardMarkup | None = None
    try:
        article: int = int(message.text)
        item: Item = await ItemRepository.find_one_or_none(session=session, article=article)
        item_info: str = get_item_into(item=item)
        if message.from_user.id not in ADMINS_ID:
            inline_kb = get_user_inline_kb()
        else:
            inline_kb = get_admin_inline_kb(article=item.article)
        await message.answer_photo(
            photo=item.photo_id,
            caption=item_info,
            reply_markup=inline_kb
        )
    except:
        await message.answer(text='Товар не найден, или удален')