from adapters.repository import Deliveryrepository, ShippingRepository
from domain import commands, events
from domain.models import Shipping
from service_layer import abstract, handlers, unit_of_work
from adapters import redis_eventpublisher

async def add_shipping(cmd: commands.AddShipping,
                       uow: unit_of_work.AbstractUnitOfWork,
                       ) -> None:
    with uow:
        shipping = await handlers.add_shipping(cmd)
        uow.shipping.add(shipping)
        uow.commit()


async def get_shipping(cmd: commands.GetShipping,
                       uow: unit_of_work.AbstractUnitOfWork) -> Shipping:
    with uow:
        result = uow.repo.get(cmd.id_)
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
        uow.delivery.add(delivery)
        uow.commit()


async def update_task(cmd:commands.Allocate,
                        uow:unit_of_work.DeliveryUnitOfWork) -> None:

    with uow:
        model = uow.delivery.get(cmd.user)
        model.allocate(cmd.task)
        uow.delivery.update(model)
        uow.commit()


        
async def not_available(event,uow):
    print()
    print("triggered")
    print("THe user is not available right ")
    return None


async def free_user(event:events.TaskCompleted, uow:unit_of_work.AbstractUnitOfWork):
    redis_eventpublisher.publish("task_completed", event)


async def free_delivery(cmd:commands.FreeUser,
                         uow:unit_of_work.DeliveryUnitOfWork) -> None:

      with uow:
        model = uow.delivery._get_user(cmd.user)
        print(model)
        model.free_user()
        uow.delivery.update(model)
        uow.commit()
