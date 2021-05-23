import uuid
from typing import Optional, List, Set
from uuid import UUID

from pydantic import BaseModel
from domain.events import NotAvailable

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

    def __hash__(self):
        return hash((type(self.id_)))


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


class Delivery(BaseModel):
    user: UUID
    name: str
    post: str
    permission: str
    available:bool=True
    task : List[UUID] = []
    is_deleted:bool = False
    events : List[Event]=[]


    def __hash__(self):
        return hash((type(self.user)))
        
    class Config:
        title = "Delivery"
        allow_mutations = False

    def allocate(self, order:UUID):
        if self.available == False:
            print("Event is added*********************")
            self.events.append(NotAvailable(user=self.user))
            return None
        else:
            self.task.append(order)
            self.available=False

    
    def can_deliver(self, order:Shipping) -> bool:
        return self.available

    def remove_shipping(self, order:Shipping):
        if order in self.task:
            self.task.remove(order)
            self.available = True

    def mark_completed(self, order:Shipping):
        if order in self.task:
            self.task.remove(order)
            self.task.order.status = "Completed"



def delivery_factory(
    name: str,
    post: str,
    permission: str,
) -> Delivery : 
    return Delivery(
    user= uuid.uuid4(),
    name= name,
    post= post,
    permission= permission,
    available=True,
    task = [],
    is_deleted=False
    )