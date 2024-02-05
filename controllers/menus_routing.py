from fastapi import APIRouter, Depends, status

from schemas.schemas import Menu, MenuCreation
from services.menus_services import MenuService

router = APIRouter()


@router.get('/', description='Получение списка всех меню', response_model=list[Menu],
            status_code=status.HTTP_200_OK, name='menus_url')
async def get_menus(service: MenuService = Depends()) -> list[Menu] | list:
    result = await service.get_all()
    return result


@router.get('/{menu_id}', description='Получение выбранного меню', response_model=Menu,
            status_code=status.HTTP_200_OK, name='menu_url')
async def get_menu(menu_id: int, service: MenuService = Depends()) -> Menu:
    result = await service.get(menu_id)
    return result


@router.post('/', description='Создание нового меню', response_model=Menu,
             status_code=status.HTTP_201_CREATED)
async def create_menu(data: MenuCreation, service: MenuService = Depends()) -> Menu:
    result = await service.create(data)
    return result


@router.delete('/{menu_id}', description='Удаление выбранного меню', status_code=status.HTTP_200_OK)
async def delete_menu(menu_id: int, service: MenuService = Depends()) -> dict:
    result = service.delete(menu_id)
    return await result


@router.patch('/{menu_id}', description='Изменение выбранного меню', response_model=Menu,
              status_code=status.HTTP_200_OK)
async def update_menu(menu_id: int, data: MenuCreation, service: MenuService = Depends()) -> Menu:
    result = await service.update(menu_id, data)
    return result
