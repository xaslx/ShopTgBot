from pydantic import BaseModel




class NewItemSchema(BaseModel):
    title: str
    description: str
    price: float
    quantity: int
    sizes: list[int]
    photo_id: str