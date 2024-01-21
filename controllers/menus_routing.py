from fastapi import APIRouter

from schemas.schemas import MenuCreation
from services.menus_services import MenuService

router = APIRouter()


@router.get('/', description='Получение списка всех меню')
async def get_menus() -> list | dict:
    obj = MenuService()
    return obj.get_all()


@router.get('/{menu_id}', description='Получение выбранного меню')
async def get_menu(menu_id: int) -> dict:
    pass


@router.post('/', description='Создание нового меню', response_model=dict)
async def create_menu(data: MenuCreation) -> dict:
    obj = MenuService()
    result = await obj.create(data)
    return {'message': f'Успешное создание объекта меню -> {result.title}'}


@router.put('/{menu_id}', description='Изменение выбранного меню')
async def update_menu(menu_id: int) -> dict:
    pass


@router.delete('/{menu_id}', description='Удаление выбранного меню')
async def delete_menu(menu_id: int) -> dict:
    pass


@router.delete('/', description='Удаление всех меню')
async def delete_menus() -> dict:
    pass
