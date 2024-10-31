from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from src.models.user import User
from src.repositories.item import ItemRepository
from src.repositories.user import UserRepository
from src.utils import get_item_into
import asyncio
from aiogram import Bot
from config import env_config
from aiogram.client.default import DefaultBotProperties



bot: Bot = Bot(token=env_config.TOKEN_BOT, default=DefaultBotProperties(parse_mode='HTML'))
ADMINS_ID: list[int] = env_config.ADMINS_ID


async def edit_item(callback: CallbackQuery, state: FSMContext, item_type: str, state_type):
    _, _, article = callback.data.split(':')
    await state.update_data({'article': article})
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        text=f'Введите новое {item_type} для товара\n'
             'Или <b>/acancel</b> чтобы отменить'
    )
    await state.set_state(state_type)


async def update_item(
        message: Message, 
        state: FSMContext, 
        session: AsyncSession,
        item_type: str, 
        notify: bool | None = None, 
        text: str | None = None, 
        photo_id: str | None = None,
        **values
    ):
    data: dict = await state.get_data()
    await state.clear()
    item: Item | None = await ItemRepository.update(session=session, article=int(data.get('article')), **values)
    item_info: str = get_item_into(item=item)
    if item:
        await message.answer(f'Вы успешно поменяли {item_type} для товара\nАртикул: <b>{data.get('article')}</b>\nТовар теперь выглядит так:\n')
        await message.answer_photo(
        photo=item.photo_id,
        caption=item_info
    )
        if notify:
            all_users: list[User] = await get_all_users(session=session)
            asyncio.create_task(notify_user_new_item_edit_item(text=text, all_users=all_users, photo_id=photo_id))
    else:
        await message.answer(f'Не удалось изменить {item_type}')




def add_sizes(text: str) -> list[int]:
    sizes: list[int]= []
    try:
        sizes = list(map(int, text.split(',')))
    except:
        sizes.append(int(text))
    return sizes



async def notify_user_new_item_edit_item(text: str, all_users: list[User], photo_id: str | None = None):
    if photo_id:
        await notify_user_with_photo(text=text, all_users=all_users, photo_id=photo_id)
    else:
        await notify_user_text(text=text, all_users=all_users)


    
    

async def send_message_for_admin(good: int, bad: int):
    text_for_admin: str = f'Успешно отправлено для: {good} пользователей.\nНеудачно для: {bad}'

    for admin in ADMINS_ID:
        try:
            await bot.send_message(chat_id=admin, text=text_for_admin)
            await asyncio.sleep(0.5)
        except:
            pass



async def get_all_users(session: AsyncSession) -> list[User]:
    all_users: list[User] = await UserRepository.find_all(session=session)
    return all_users


async def notify_user_text(text: str, all_users: list[User]):
    good: int = 0
    bad: int = 0
    for user in all_users:
        try:
            await bot.send_message(chat_id=user.user_telegram_id, text=text)
            good += 1
            await asyncio.sleep(0.5)
        except:
            bad += 1
    asyncio.create_task(send_message_for_admin(good=good, bad=bad))



async def notify_user_with_photo(text: str, all_users: list[User], photo_id: str):
    good: int = 0
    bad: int = 0
    for user in all_users:
        try:
            await bot.send_photo(chat_id=user.user_telegram_id, photo=photo_id, caption=text)
            good += 1
            await asyncio.sleep(0.5)
        except:
            bad += 1
    asyncio.create_task(send_message_for_admin(good=good, bad=bad))