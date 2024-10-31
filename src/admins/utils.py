from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from src.repositories.item import ItemRepository




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


async def update_item(message: Message, state: FSMContext, session: AsyncSession, item_type: str, **values):
    data: dict = await state.get_data()
    await state.clear()
    res: Item | None = await ItemRepository.update(session=session, article=int(data['article']), **values)
    if res:
        await message.answer(f'Вы успешно поменяли {item_type} для товара\nАртикул: <b>{data["article"]}</b>\nТовар теперь выглядит так:\n')
        await message.answer_photo(
        photo=res.photo_id,
        caption=
        f'Артикул: <b>{res.article}</b>\n\n'
        f'Название: <b>{res.title}</b>\n\n'
        f'Описание: <b>{res.description}</b>\n\n'
        f'Цена: <b>{res.price}</b>\n\n'
        f'Количество: <b>{res.quantity}</b>',
    )
    else:
        await message.answer(f'Не удалось изменить {item_type}')