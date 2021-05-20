from adapters.repository import Deliveryrepository, ShippingRepository
from domain import commands
from domain.models import Shipping
from service_layer import abstract, handlers, unit_of_work
from service_layer.unit_of_work import ShippingUnitOfWork


async def add_shipping(cmd: commands.AddShipping,
                       uow: unit_of_work.AbstractUnitOfWork,
                       ) -> None:
    with uow:
        shipping = await handlers.add_shipping(cmd)
        repo = ShippingRepository()
        repo.add(shipping)
        uow.commit()


async def get_shipping(cmd: commands.GetShipping,
                       uow: unit_of_work.AbstractUnitOfWork) -> Shipping:
    with uow:
        repo = ShippingRepository()
        result = repo.get(cmd.id_)
        dic = await handlers.get_shipping(result)
        uow.commit()
        return dic


# async def update_shipping_date(cmd: commands.Update_date_to_ship, uow: unit_of_work.AbstractUnitOfWork,
#                                id_: UUID,) -> None:
#     uow = ShippingUOW
#     with uow:
#         model = uow.shipping.get(id_)
#         shipping = handlers.update_shipping(
#             command.UpdadteShQuantity(
#                 model=model, quantity=validated_data.quatity
#             )
#         )
#         uow.shipping.update(shipping)
#         uow.commit()


async def add_delivery(cmd:commands.AddDelivery, 
                        uow:unit_of_work.DeliveryUnitOfWork) -> None:
    with uow:
        delivery = await handlers.add_delivery(cmd)
        repo = Deliveryrepository()
        repo.add(delivery)
        uow.commit()


        