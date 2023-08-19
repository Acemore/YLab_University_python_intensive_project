import json
import os
from typing import Any

from pydantic import parse_obj_as
from pydantic.json import pydantic_encoder
from redis.asyncio import Redis

REDIS_HOST: str = str(os.getenv('REDIS_HOST'))
redis: Redis = Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


class RedisCache:
    @staticmethod
    async def read(key, schema_class, model_loader) -> Any:
        if not await redis.exists(key):
            print(f'Cache miss. Key: {key}')

            data_for_dump = parse_obj_as(schema_class, await model_loader())

            await redis.set(key, json.dumps(data_for_dump, default=pydantic_encoder))
        else:
            print(f'Cache hit. Key: {key}')

        loaded_data = json.loads(str(await redis.get(key)))

        return parse_obj_as(schema_class, loaded_data)

    @staticmethod
    async def delete(key: str) -> None:
        await redis.delete(key)

        _, child_keys = await redis.scan(0, match=key + '/*')

        if len(child_keys) > 0:
            await redis.delete(*child_keys)
