from src.models.item import Item



def get_item_into(item: Item) -> str:
    item_info: str =  (
        f'Артикул: <b>{item.article}</b>\n\n'
        f'Название: <b>{item.title}</b>\n\n'
        f'Описание: <b>{item.description}</b>\n\n'
        f'Цена: <b>{item.price}</b>\n\n'
        f'Количество: <b>{item.quantity}</b>'
    )
    return item_info