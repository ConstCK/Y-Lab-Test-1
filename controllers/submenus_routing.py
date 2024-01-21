from fastapi import APIRouter

from schemas.schemas import SubMenu, SubMenuCreation
from services.submenus_services import SubMenuService

router = APIRouter()
service = SubMenuService()


@router.get('/', description='Получение списка всех подменю')
async def get_submenus() -> list[SubMenu] | dict:
    return service.get_all()


@router.get('/{submenu_id}', description='Получение выбранного подменю')
async def get_submenu(submenu_id: int) -> SubMenu:
    return service.get(submenu_id)


@router.post('/', description='Создание нового подменю')
async def create_submenu(data: SubMenuCreation, menu_id: int) -> dict:
    result = service.create(data, menu_id)
    return {'message': f'Успешное создание объекта меню -> {result.title}'}


@router.delete('/{submenu_id}', description='Удаление выбранного подменю')
async def delete_submenu(submenu_id: int) -> dict:
    service.delete(submenu_id)
    return {'message': f'Запись с id = {submenu_id} успешно удалена'}


@router.patch('/{submenu_id}', description='Изменение выбранного подменю')
async def update_submenu(submenu_id: int, data: SubMenuCreation) -> dict:
    service.update(submenu_id, data)
    return {'message': f'Запись с id = {submenu_id} успешно изменена'}



