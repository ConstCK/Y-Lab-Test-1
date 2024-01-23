from fastapi import APIRouter, Depends

from schemas.schemas import MenuCreation, Menu
from services.menus_services import MenuService

router = APIRouter()


# service = MenuService()


@router.get('/', description='Получение списка всех меню')
async def get_menus(service: MenuService = Depends()) -> list[Menu] | list:
    result = service.get_all()
    return result


@router.get('/{menu_id}', description='Получение выбранного меню')
async def get_menu(menu_id: int, service: MenuService = Depends()) -> Menu:
    result = service.get(menu_id)
    return result


@router.post('/', description='Создание нового меню', status_code=201)
async def create_menu(data: MenuCreation, service: MenuService = Depends()) -> Menu:
    result = service.create(data)
    return result


@router.delete('/{menu_id}', description='Удаление выбранного меню')
async def delete_menu(menu_id: int, service: MenuService = Depends()) -> dict:
    result = service.delete(menu_id)
    return result


@router.patch('/{menu_id}', description='Изменение выбранного меню')
async def update_menu(menu_id: int, data: MenuCreation, service: MenuService = Depends()) -> Menu:
    result = service.update(menu_id, data)
    return result
