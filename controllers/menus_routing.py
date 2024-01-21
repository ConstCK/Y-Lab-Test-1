from fastapi import APIRouter

from schemas.schemas import MenuCreation, Menu
from services.menus_services import MenuService

router = APIRouter()
service = MenuService()

@router.get('/', description='Получение списка всех меню')
async def get_menus() -> list[Menu] | dict:
    return service.get_all()


@router.get('/{menu_id}', description='Получение выбранного меню')
async def get_menu(menu_id: int) -> Menu:
    return service.get(menu_id)


@router.post('/', description='Создание нового меню', response_model=dict)
async def create_menu(data: MenuCreation) -> dict:
    result = service.create(data)
    return {'message': f'Успешное создание объекта меню -> {result.title}'}


@router.delete('/{menu_id}', description='Удаление выбранного меню')
async def delete_menu(menu_id: int) -> dict:
    service.delete(menu_id)
    return {'message': f'Запись с id = {menu_id} успешно удалена'}


@router.patch('/{menu_id}', description='Изменение выбранного меню')
async def update_menu(menu_id: int, data: MenuCreation) -> dict:
    service.update(menu_id, data)
    return {'message': f'Запись с id = {menu_id} успешно изменена'}





