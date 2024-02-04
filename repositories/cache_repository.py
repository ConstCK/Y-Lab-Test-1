import json

from redis import asyncio as aioredis


class CacheRepository:
    def __init__(self, name) -> None:
        self.red = aioredis.from_url('redis://redis:6379/0',
                                     encoding='utf8',
                                     decode_responses=True)
        self.name = name

    async def set_item(self, key_id: int, item: str, expire_time: int = 60) -> None:
        # Создание объекта в БД типа str
        key = f"{self.name}-{key_id}"
        await self.red.set(key, item, expire_time)

    async def set_items(self, item: str, expire_time: int = 60) -> None:
        # Создание объекта в БД типа set
        key = f"{self.name}-all"
        await self.red.sadd(key, item)
        await self.red.expire(key, expire_time)

    async def get_item(self, key_id: int) -> str | None:
        # Получение объекта из БД
        key = f"{self.name}-{key_id}"
        result = await self.red.get(key)
        return result

    async def get_items(self) -> list:
        # Создание объектов в БД в виде списка
        result = await self.red.smembers(f"{self.name}-all")
        if result:
            return [json.loads(item) for item in result]
        return []

    async def remove_item(self, key: int | str) -> None:
        key = f"{self.name}-{key}"
        await self.red.delete(key)

    async def remove_parent(self, key: str) -> None:
        await self.red.delete(key)

    async def show_all_keys(self):
        # Получение всех ключей БД
        return await self.red.keys()
