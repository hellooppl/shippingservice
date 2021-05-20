from pydantic.main import BaseModel


class AddShipping(BaseModel):
    category: str
    cost: float
    regionId: int
    orderId: int
    insurance: float
    date_to_ship: str
