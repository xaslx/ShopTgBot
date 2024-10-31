from aiogram.fsm.state import State, StatesGroup


class NewItem(StatesGroup):
    title: State = State()
    description: State = State()
    price: State = State()
    quantity: State = State()
    photo_id: State = State()


class EditItemTitle(StatesGroup):
    new_title: State = State()