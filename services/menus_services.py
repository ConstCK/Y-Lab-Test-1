from fastapi import Depends

from repositories.menus_repository import MenuRepository
from schemas.schemas import Menu, MenuCreation


class MenuService:
    def __init__(self, repository: MenuRepository = Depends()):
        self.repository = repository

    async def create(self, data: MenuCreation) -> Menu:
        return await self.repository.create(data)

    async def get_all(self) -> list[Menu] | list:
        return await self.repository.get_all()

    async def get(self, menu_id: int) -> Menu:
        return await self.repository.get(menu_id)

    async def delete(self, menu_id: int) -> dict:
        return await self.repository.delete(menu_id)

    async def update(self, menu_id: int, data: MenuCreation) -> Menu:
        return await self.repository.update(menu_id, data)
