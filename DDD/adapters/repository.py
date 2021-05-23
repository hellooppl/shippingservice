import abc

from typing import List, Dict
from uuid import UUID
from domain.models import Shipping,Delivery
from domain import models
from storage import shipping_list,delivery_list


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()
        # seen stores which objects of the model are used during the session seen is set data type


    def add(self, base: models.BaseModel):
        self._add(base)
        self.seen.add(base)

    def get(self, reference) -> models.BaseModel:
        base = self._get(reference)
        if base:
            self.seen.add(base)
        return base

    def update(self, base: models.BaseModel):
        result = self._update(base)
        if result:
            self.seen.add(result)
        return result

    def delete(self, base: models.BaseModel):
        result = self._delete(base)
        if result:
            self.seen.add(result)
        return result

    @abc.abstractmethod
    def _add(self, base: models.BaseModel):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, reference):
        raise NotImplementedError

    @abc.abstractmethod
    def _update(self, base: models.BaseModel):
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, reference):
        raise NotImplementedError


class ShippingRepository(AbstractRepository):
    # Product model add , update and delete operations

    def __init__(self) -> None:
        super().__init__()

    def _get(self, _id: UUID) -> Shipping:
        for i in shipping_list:
            if i['_id'] == _id:
                ss = i

        return Shipping.construct(**ss)

    def _add(self, shipping: models.Shipping):
        values = {
            "_id": shipping.id_,
            "category": shipping.category,
            "cost": shipping.cost,
            "regionId": shipping.regionId,
            "orderId": shipping.orderId,
            "insurance": shipping.insurance,
            "date_to_ship": shipping.date_to_ship,
        }
        shipping_list.append(values)

    def _update(self, model: Shipping) -> None:
        values = {
            "id_": model.id,
            "category": model.category,
            "cost": model.cost,
            "regionId": model.regionId,
            "orderId": model.orderId,
            "insurance": model.insurance,
            "date_to_ship": model.date_to_ship,
        }
        for i in range(len(self) + 1):
            if self[i]["id_"] == values.id_:
                self[i].update(values)

    def _delete(self, model: Shipping):
        values = {
            "id_": model.id_,
            "category": model.category,
            "cost": model.cost,
            "regionId": model.regionId,
            "orderId": model.orderId,
            "insurance": model.insurance,
            "date_to_ship": model.date_to_ship,
        }

        for i in range(len(self) + 1):
            if self[i]["id_"] == values.user:
                self[i]["is_deleted"] = False
            return "{user} is deleted successfully"

class Deliveryrepository(AbstractRepository):
    def _get(self, user: UUID) -> Delivery:
        for i in delivery_list:
            if i['user'] == user:
                ss = i
        return Delivery.construct(**ss)

    def _add(self, model: Delivery):
        values = {
            "user": model.user,
            "name": model.name,
            "post": model.post,
            "permission": model.permission,
            "available": model.available,
            "task": model.task,
            "events":model.events,
            "is_deleted":model.is_deleted
        }
        delivery_list.append(values)

    def _update(self, model: Delivery):
        values = {
            "user": model.user,
            "name": model.name,
            "post": model.post,
            "permission": model.permission,
            "available": model.available,
            "task": model.task,
        }


        for i in delivery_list:
            if i['user'] == model.user:
                i['task'].append(model.task)
                i['available']=model.available


    def _delete(self, model: Shipping):
        values = {
            "id_": model.id_,
            "category": model.category,
            "cost": model.cost,
            "regionId": model.regionId,
            "orderId": model.orderId,
            "insurance": model.insurance,
            "date_to_ship": model.date_to_ship,
        }

        for i in range(len(self) + 1):
            if self[i]["user"] == values.user:
                self[i]["is_deleted"] == False
            return "{user} is deleted successfully"

