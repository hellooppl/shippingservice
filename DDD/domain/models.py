import uuid
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from domain.events import Event


class Shipping(BaseModel):
    id_: UUID
    category: str
    cost: float
    regionId: int
    orderId: int
    insurance: float
    date_to_ship: Optional[str] = "ss"
    is_deleted: Optional[bool] = False
    events: List[Event] = []

    class Config:
        title = "Shipping"
        allow_mutations = False

    # @property
    # def id(self):
    #     return self._id
    #
    def __hash__(self):
        return hash((type(self)))


def shipping_factory(
        category: str,
        cost: float,
        regionId: int,
        orderId: int,
        insurance: float,
        date_to_ship: str,
        is_deleted: bool = False,
) -> Shipping:
    return Shipping(
        id_=uuid.uuid4(),
        category=category,
        cost=cost,
        regionId=regionId,
        orderId=orderId,
        insurance=insurance,
        date_to_shi=date_to_ship,
        is_deleted=is_deleted
    )
