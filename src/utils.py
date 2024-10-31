from src.models.item import Item



def get_item_into(item: Item) -> str:
    sizes: list[str] = ', '.join(str(i) for i in item.sizes)
    item_info: str =  (
        f'Артикул: <b>{item.article}</b>\n\n'
        f'Название: <b>{item.title}</b>\n\n'
        f'Описание: <b>{item.description}</b>\n\n'
        f'Цена: <b>{item.price}</b>\n\n'
        f'Количество: <b>{item.quantity}</b>\n\n'
        f'Размеры: <b>{sizes}</b>'
    )
    return item_info