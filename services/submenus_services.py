from typing import Any

from fastapi import Depends

from repositories.submenus_repository import SubMenuRepository
from schemas.schemas import SubMenu, SubMenuCreation


class SubMenuService:
    def __init__(self, repository: SubMenuRepository = Depends()):
        self.repository = repository

    async def create(self, data: SubMenuCreation, menu_id: int) -> SubMenu | Any:
        return await self.repository.create(data, menu_id)

    async def get_all(self) -> list[SubMenu] | list | Any:
        return await self.repository.get_all()

    async def get(self, menu_id: int) -> SubMenu:
        return await self.repository.get(menu_id)

    def delete(self, menu_id: int) -> dict:
        return self.repository.delete(menu_id)

    async def update(self, menu_id: int, data: SubMenuCreation) -> SubMenu:
        return await self.repository.update(menu_id, data)
