import uuid

from domain import models
from domain.commands import AddShipping, GetShipping


async def add_shipping(cmd: AddShipping) -> models.Shipping:
    return models.shipping_factory(
        category=cmd.category,
        cost=cmd.cost,
        regionId=cmd.regionId,
        orderId=cmd.orderId,
        insurance=cmd.insurance,
        date_to_ship=cmd.date_to_ship,
    )


async def get_shipping(model: models.Shipping) -> dict:
    return {
        'cat': model.category,
        'cost': model.cost,
        'regionId': model.regionId,
        'orderId': model.orderId,
        'insurance': model.insurance,
        'date_to_ship': model.date_to_ship
    }
