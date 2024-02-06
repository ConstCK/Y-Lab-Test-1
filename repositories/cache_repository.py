import json
import os

from redis import asyncio as aioredis  # type: ignore


class CacheRepository:
    def __init__(self, name) -> None:
        self.red = aioredis.from_url(f"redis://{os.getenv('REDIS')}:6379/0", encoding='utf8',  # noqa: E231
                                     decode_responses=True)  # noqa: E231

    async def set_item(self, key: str, item: str, expire_time: int = 60) -> None:
        # Создание объекта в БД типа str
        await self.red.set(key, item, expire_time)

    async def set_items(self, key: str, item: str, expire_time: int = 60) -> None:
        # Создание объекта в БД типа set
        await self.red.sadd(key, item)
        await self.red.expire(key, expire_time)

    async def get_item(self, key: str) -> str | None:
        # Получение объекта из БД
        result = await self.red.get(key)
        return result

    async def get_items(self, key: str) -> list:
        # Создание объектов в БД в виде списка
        result = await self.red.smembers(key)
        if result:
            return [json.loads(item) for item in result]
        return []

    async def remove_item(self, key: str) -> None:
        await self.red.delete(key)

    async def remove_all(self) -> None:
        await self.red.flushall()

    async def show_all_keys(self):
        # Получение всех ключей БД
        return await self.red.keys()
