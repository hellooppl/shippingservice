from typing import AsyncContextManager
from uuid import UUID

from sanic import request
import config
import json
import logging
import redis
from domain import commands
from service_layer import unit_of_work
import asyncio
from service_layer import messagebus
import requests

logger = logging.getLogger(__name__)

r = redis.Redis(**config.get_redis_host_and_port())


async def main():
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("task_completed")

    for m in pubsub.listen():
        await handle_user_available(m)


async def handle_user_available(m):
    logging.debug("handling %s", m)
    
    a = m['data'].decode("utf-8")
    user_id = json.loads(a)['user']
    cmd = commands.FreeUser(
        user=user_id
    )
    uow = unit_of_work.DeliveryUnitOfWork()
    await messagebus.handle(cmd,uow)
    
    # if u are testing in local server try this and comment from line 31 to 37
    # response = requests.get('http://127.0.0.1:8000/list/'+user_id)


if __name__ == "__main__":
    asyncio.run(main())