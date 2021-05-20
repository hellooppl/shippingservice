from uuid import UUID

from pydantic import BaseModel

from domain.models import Shipping, Delivery


class Command(BaseModel):
    pass


class AddShipping(Command):
    category: str
    cost: float
    regionId: int
    orderId: int
    insurance: float
    date_to_ship: str


class ShippingCommand(BaseModel):
    shipping: Shipping


class GetShipping(Command):
    id_: UUID


class Update_date_to_ship(ShippingCommand):
    date_to_ship: str


class AddDelivery(BaseModel):
    name: str
    post: str
    permission: str
    available:bool
    task : set() = None


class DeliveryCommand(BaseModel):
    delivery: Delivery

class UpdateTask(DeliveryCommand):
    _id:UUID
    task:set()