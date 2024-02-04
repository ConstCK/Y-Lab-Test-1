from fastapi import APIRouter, Depends

from schemas.schemas import SubMenu, SubMenuCreation
from services.submenus_services import SubMenuService

router = APIRouter()


@router.get('/', description='Получение списка всех подменю', response_model=list[SubMenu])
async def get_submenus(service: SubMenuService = Depends()) -> list[SubMenu] | list:
    result = await service.get_all()
    return result


@router.get('/{submenu_id}', description='Получение выбранного подменю', response_model=SubMenu)
async def get_submenu(submenu_id: int, service: SubMenuService = Depends()) -> SubMenu:
    result = await service.get(submenu_id)
    return result


@router.post('/', description='Создание нового подменю', status_code=201, response_model=SubMenu)
async def create_submenu(data: SubMenuCreation, menu_id: int, service: SubMenuService = Depends()) -> SubMenu:
    result = await service.create(data, menu_id)
    return result


@router.delete('/{submenu_id}', description='Удаление выбранного подменю')
async def delete_submenu(submenu_id: int, service: SubMenuService = Depends()) -> dict:
    result = await service.delete(submenu_id)
    return result


@router.patch('/{submenu_id}', description='Изменение выбранного подменю', response_model=SubMenu)
async def update_submenu(submenu_id: int, data: SubMenuCreation, service: SubMenuService = Depends()) -> SubMenu:
    result = await service.update(submenu_id, data)
    return result
