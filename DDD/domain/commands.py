from typing import List
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


class AddDelivery(Command):
    name: str
    post: str
    permission: str


class DeliveryCommand(BaseModel):
    delivery: Delivery


class Allocate(Command):
    user:UUID
    task:UUID
class AddTask(DeliveryCommand):
    user:UUID
    task:UUID
