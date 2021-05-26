
import json
import logging
from dataclasses import asdict
import redis

import config
from domain import events

logger = logging.getLogger(__name__)

r = redis.Redis(**config.get_redis_host_and_port())

import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        
        return json.JSONEncoder.default(self, obj)


def publish(channel, event: events.Event):
    logging.debug("publishing: channel=%s, event=%s", channel, event)
    r.publish(channel, json.dumps(event.dict(), cls=UUIDEncoder))