from fastapi import Depends

from repositories.dishes_repository import DishesRepository
from schemas.schemas import Dish, DishCreation


class DishesService:

    def __init__(self, repository: DishesRepository = Depends()):
        self.repository = repository

    async def create(self, data: DishCreation, submenu_id: int) -> Dish:
        return await self.repository.create(data, submenu_id)

    async def get_all(self) -> list[Dish] | list:
        return await self.repository.get_all()

    async def get(self, menu_id: int) -> Dish:
        return await self.repository.get(menu_id)

    async def delete(self, menu_id: int) -> dict:
        return await self.repository.delete(menu_id)

    async def update(self, menu_id: int, data: DishCreation) -> Dish:
        return await self.repository.update(menu_id, data)
