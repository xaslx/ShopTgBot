from typing import Any
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.admins.admin_filter import AdminProtect
from src.admins.states import NewItem, EditItemTitle, EditItemDescription, EditItemPrice, EditItemQuantity, EditItemPhoto, EditItemSizes
from src.models.item import Item
from src.repositories.item import ItemRepository
from src.schemas.item import NewItemSchema
from src.admins.keyboards import confirm_delete_item
from src.admins.utils import update_item, edit_item, add_sizes


admin_handler: Router = Router(name='Admin Router')
CANCEL_ADD_ITEM: str = 'Или <b>/acancel</b> чтобы отменить добавление '
DIGIT_FILTER = r'^(0|[1-9]\d*)(\.\d+)?$'
SIZES_FILTER = r'^[0-9]+(,[0-9]+)*$'



@admin_handler.message(AdminProtect(), Command(commands='acancel'), StateFilter(default_state))
async def process_cancel_command_admin(message: Message):
    await message.answer(text='Отменять нечего, вы не добавляете товар\n\n')


@admin_handler.message(AdminProtect(), Command(commands='acancel'), ~StateFilter(default_state))
async def process_cancel_command_state_admin(message: Message, state: FSMContext):
    await message.answer(
        text='Вы отменили добавление товара'
    )
    await state.clear()


@admin_handler.message(AdminProtect(), StateFilter(default_state), Command('admin_panel'))
async def admin_panel(message: Message):
    await message.answer(
        text=f'<b>/add_item</b> - Добавить новый товар\n'
    )


@admin_handler.message(AdminProtect(), StateFilter(default_state), Command('add_item'))
async def add_new_item(message: Message, state: FSMContext):
    await message.answer(
        text=
        f'Введите название\n'
        f'{CANCEL_ADD_ITEM}'
    )
    await state.set_state(NewItem.title)


@admin_handler.message(AdminProtect(), StateFilter(NewItem.title), F.text)
async def add_title(message: Message, state: FSMContext):
    await state.update_data({'title': message.text})
    await message.answer(
        text=
        'Теперь введите описание товара\n'
        f'{CANCEL_ADD_ITEM}'
    )
    await state.set_state(NewItem.description)


@admin_handler.message(AdminProtect(), StateFilter(NewItem.title), ~F.text)
async def add_title_warning(message: Message):
    await message.answer(text='Название должно быть в виде текста.')


@admin_handler.message(AdminProtect(), StateFilter(NewItem.description), F.text)
async def add_description(message: Message, state: FSMContext):
    await state.update_data({'description': message.text})
    await message.answer(
        text=
        'Теперь введите цену товара\n'
        f'{CANCEL_ADD_ITEM}'
    )
    await state.set_state(NewItem.price)


@admin_handler.message(AdminProtect(), StateFilter(NewItem.description), ~F.text)
async def add_description_warning(message: Message):
    await message.answer(text='Описание должно быть в виде текста.')



@admin_handler.message(AdminProtect(), StateFilter(NewItem.price), F.text.regexp(DIGIT_FILTER))
async def add_price(message: Message, state: FSMContext):
    await state.update_data({'price': message.text})
    await message.answer(
        text=
        'Теперь введите количество товара\n'
        f'{CANCEL_ADD_ITEM}'
    )
    await state.set_state(NewItem.quantity)


@admin_handler.message(AdminProtect(), StateFilter(NewItem.price), ~F.text.regexp(DIGIT_FILTER))
async def add_price_warning(message: Message):
    await message.answer(text='Прайс должно быть в виде цифры.')



@admin_handler.message(AdminProtect(), StateFilter(NewItem.quantity), F.text.regexp(DIGIT_FILTER))
async def add_quantity(message: Message, state: FSMContext):
    await state.update_data({'quantity': message.text})
    await message.answer(
        text=
        'Теперь введите размеры через запятую\nПример: 10,25,30\n'
        f'{CANCEL_ADD_ITEM}'
    )
    await state.set_state(NewItem.sizes)


@admin_handler.message(AdminProtect(), StateFilter(NewItem.quantity), ~F.text.regexp(DIGIT_FILTER))
async def add_quantity_warning(message: Message):
    await message.answer(text='Количество должно быть в виде цифры.')



@admin_handler.message(AdminProtect(), StateFilter(NewItem.sizes), F.text.regexp(SIZES_FILTER))
async def add_quantity(message: Message, state: FSMContext):
    sizes: list[int]= add_sizes()
    await state.update_data({'sizes': sizes})
    await message.answer(
        text=
        'Теперь отправьте фото товара\n'
        f'{CANCEL_ADD_ITEM}'
    )
    await state.set_state(NewItem.photo_id)


@admin_handler.message(AdminProtect(), StateFilter(NewItem.sizes), ~F.text.regexp(SIZES_FILTER))
async def add_quantity_warning(message: Message):
    await message.answer(text='Введите размеры, один или несколько\nПример 10 или 10,25,30')




@admin_handler.message(AdminProtect(), StateFilter(NewItem.photo_id), F.photo)
async def add_quantity(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data({'photo_id': message.photo[-1].file_id})
    await state.set_state(NewItem.photo_id)
    data: dict = await state.get_data()
    new_item: NewItemSchema = NewItemSchema(**data)
    item: Item = await ItemRepository.add(session=session, **new_item.model_dump())
    await message.answer(text=f'Товар успешно добавлен\n<b>Артикул: {item.article}</b>')
    await state.clear()



@admin_handler.message(AdminProtect(), StateFilter(NewItem.photo_id), ~F.photo)
async def add_photo_warning(message: Message):
    await message.answer(text='Отправьте фото товара')



@admin_handler.callback_query(AdminProtect(), StateFilter(default_state), F.data.startswith('delete:item'))
async def delete_item(callback: CallbackQuery):
    _, _, article = callback.data.split(':')
    await callback.answer()
    await callback.message.edit_caption(
        caption='Вы уверенны что хотите удалить товар?',
        reply_markup=confirm_delete_item(article=article)
    )



@admin_handler.callback_query(AdminProtect(), StateFilter(default_state), F.data.startswith('confirm:delete:item'))
async def delete_item(callback: CallbackQuery, session: AsyncSession):
    _, _, _, article = callback.data.split(':')
    res = await ItemRepository.delete(session=session, article=int(article))
    await callback.message.delete()
    if res:
        await callback.message.answer(text='Товар успешно удален')
    else:
        await callback.message.answer(text='Не удалось удалить товар')



@admin_handler.callback_query(AdminProtect(), StateFilter(default_state), F.data.startswith('cancel:delete:item'))
async def delete_item(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('Вы отменили удаление товара')



@admin_handler.callback_query(AdminProtect(), StateFilter(default_state), F.data.startswith('edit:title'))
async def edit_item_title(callback: CallbackQuery, state: FSMContext):
    await edit_item(callback, state, 'название', EditItemTitle.new_title)

@admin_handler.message(AdminProtect(), StateFilter(EditItemTitle.new_title), F.text)
async def new_item_title(message: Message, state: FSMContext, session: AsyncSession):
    await update_item(message, state, session, 'название', title=message.text)

@admin_handler.message(AdminProtect(), StateFilter(EditItemTitle.new_title), ~F.text)
async def new_item_title_warning(message: Message):
    await message.answer(text='Название должно быть в виде текста')



@admin_handler.callback_query(AdminProtect(), StateFilter(default_state), F.data.startswith('edit:description'))
async def edit_item_description(callback: CallbackQuery, state: FSMContext):
    await edit_item(callback, state, 'описание', EditItemDescription.new_description)

@admin_handler.message(AdminProtect(), StateFilter(EditItemDescription.new_description), F.text)
async def new_item_description(message: Message, state: FSMContext, session: AsyncSession):
    await update_item(message, state, session, 'описание', description=message.text)

@admin_handler.message(AdminProtect(), StateFilter(EditItemDescription.new_description), ~F.text)
async def new_item_description_warning(message: Message):
    await message.answer(text='Описание должно быть в виде текста')



@admin_handler.callback_query(AdminProtect(), StateFilter(default_state), F.data.startswith('edit:price'))
async def edit_item_price(callback: CallbackQuery, state: FSMContext):
    await edit_item(callback, state, 'прайс', EditItemPrice.new_price)

@admin_handler.message(AdminProtect(), StateFilter(EditItemPrice.new_price), F.text.regexp(DIGIT_FILTER))
async def new_item_price(message: Message, state: FSMContext, session: AsyncSession):
    await update_item(message, state, session, 'прайс', price=float(message.text))

@admin_handler.message(AdminProtect(), StateFilter(EditItemPrice.new_price), ~F.text.regexp(DIGIT_FILTER))
async def new_item_price_warning(message: Message):
    await message.answer(text='Прайс должен быть в виде цифр')




@admin_handler.callback_query(AdminProtect(), StateFilter(default_state), F.data.startswith('edit:quantity'))
async def edit_item_quantity(callback: CallbackQuery, state: FSMContext):
    await edit_item(callback, state, 'количество', EditItemQuantity.new_quantity)

@admin_handler.message(AdminProtect(), StateFilter(EditItemQuantity.new_quantity), F.text.regexp(DIGIT_FILTER))
async def new_item_quantity(message: Message, state: FSMContext, session: AsyncSession):
    await update_item(message, state, session, 'количество', quantity=int(message.text))

@admin_handler.message(AdminProtect(), StateFilter(EditItemQuantity.new_quantity), ~F.text.regexp(DIGIT_FILTER))
async def new_item_quantity_warning(message: Message):
    await message.answer(text='Количество должен быть в виде цифр')




@admin_handler.callback_query(AdminProtect(), StateFilter(default_state), F.data.startswith('edit:sizes'))
async def edit_item_sizes(callback: CallbackQuery, state: FSMContext):
    await edit_item(callback, state, 'размеры', EditItemSizes.new_sizes)

@admin_handler.message(AdminProtect(), StateFilter(EditItemSizes.new_sizes), F.text.regexp(SIZES_FILTER))
async def new_item_sizes(message: Message, state: FSMContext, session: AsyncSession):
    new_sizes: list[int] = add_sizes(text=message.text)
    await update_item(message, state, session, 'размеры', sizes=new_sizes)

@admin_handler.message(AdminProtect(), StateFilter(EditItemSizes.new_sizes), ~F.text.regexp(SIZES_FILTER))
async def new_item_sizes_warning(message: Message):
    await message.answer(text='Размеры должны быть в виде цифры, или несколько цифр через запятую')



@admin_handler.callback_query(AdminProtect(), StateFilter(default_state), F.data.startswith('edit:photo'))
async def edit_item_photo(callback: CallbackQuery, state: FSMContext):
    await edit_item(callback, state, 'фото', EditItemPhoto.new_Photo)

@admin_handler.message(AdminProtect(), StateFilter(EditItemPhoto.new_Photo), F.photo)
async def new_item_photo(message: Message, state: FSMContext, session: AsyncSession):
    await update_item(message, state, session, 'фото', photo_id=message.photo[-1].file_id)

@admin_handler.message(AdminProtect(), StateFilter(EditItemPhoto.new_Photo), ~F.photo)
async def new_item_photo_warning(message: Message):
    await message.answer(text='Отправьте новое фото')