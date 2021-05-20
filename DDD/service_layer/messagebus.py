from tenacity import Retrying, RetryError, stop_after_attempt, wait_exponential
from domain import commands, events
from typing import List, Union

from service_layer import unit_of_work, handlers, services

Message = Union[commands.Command, events.Event]


async def handle(
        message: Message,
        uow: unit_of_work.AbstractUnitOfWork,
):
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, events.Event):
            await handle_event(message, queue, uow)

        elif isinstance(message, commands.Command):
            cmd_result = await handle_command(message, queue, uow)
            results.append(cmd_result)

        else:
            raise Exception(f"{message} was not an Event or Command")
    return results


async def handle_event(event: events.Event,
                       queue: List[Message],
                       uow: unit_of_work.AbstractUnitOfWork):
    for handler in HANDLERS[type(event)]:
        try:
            for attempt in Retrying(
                    stop=stop_after_attempt(3),
                    wait=wait_exponential()
            ):
                with attempt:
                    await handler(event, uow=uow)
                    queue.extend(uow.collect_new_events())
        except RetryError as retry_failure:
            continue


async def handle_command(
        command: commands.Command,
        queue: List[Message],
        uow: unit_of_work.AbstractUnitOfWork,
):
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = await handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        raise


HANDLERS = {
    # events.NotAvailable: handlers.not_available,
}

COMMAND_HANDLERS = {
    commands.AddShipping: services.add_shipping,
    commands.GetShipping: services.get_shipping,
    commands.AddDelivery: services.add_delivery,
    # commands.Update_date_to_ship: services.Update_date_to_ship,
    # commands.Update_task: handlers.update_task,
}