import json
import os
from typing import Any

from redis import asyncio as aioredis

from schemas.schemas import Menu


class CacheRepository:
    def __init__(self, name) -> None:
        self.redis = aioredis.from_url(os.getenv("CACHE"),
                                       encoding="utf8",
                                       decode_responses=True)
        self.name = name

    async def set_item(self, key_id: int, item: str, expire_time: int = 60) -> None:
        # Создание объекта в БД типа str
        key = f"{self.name}-{key_id}"
        await self.redis.set(key, item, expire_time)

    async def set_items(self, item: str, expire_time: int = 60) -> None:
        # Создание объекта в БД типа set
        key = f"{self.name}-all"
        await self.redis.sadd(key, item)
        await self.redis.expire(key, expire_time)

    async def get_item(self, key: str) -> str | None:
        # Получение объекта из БД
        result = await self.redis.get(key)
        return result

    async def get_items(self, key: str) -> list:
        # Создание объектов в БД в виде списка
        result = await self.redis.smembers(key)
        return [json.loads(item) for item in result]


    async def show_all_keys(self):
        # Получение всех ключей БД
        return await self.redis.keys()
