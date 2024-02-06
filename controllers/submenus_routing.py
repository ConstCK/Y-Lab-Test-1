from fastapi import APIRouter, Depends, status

from schemas.schemas import SubMenu, SubMenuCreation
from services.submenus_services import SubMenuService

router = APIRouter()


@router.get('/', description='Получение списка всех подменю', response_model=list[SubMenu],
            status_code=status.HTTP_200_OK, name='get_submenus_url',
            responses={200: {'description': 'Успешное получение объектов'}})
async def get_submenus(service: SubMenuService = Depends()) -> list[SubMenu] | list:
    result = await service.get_all()
    return result


@router.get('/{submenu_id}', description='Получение выбранного подменю', response_model=SubMenu,
            status_code=status.HTTP_200_OK, name='get_submenu_url',
            responses={200: {'description': 'Успешное получение объекта'},
                       404: {'description': 'Объект не найден'},
                       422: {'description': 'Ошибка валидации данных'}}
            )
async def get_submenu(submenu_id: int, service: SubMenuService = Depends()) -> SubMenu:
    result = await service.get(submenu_id)
    return result


@router.post('/', description='Создание нового подменю', response_model=SubMenu,
             status_code=status.HTTP_201_CREATED, name='create_submenu_url',
             responses={201: {'description': 'Успешное создание объекта'},
                        409: {'description': 'Ошибка создания объекта. Объект уже существует'},
                        422: {'description': 'Ошибка валидации данных'}}
             )
async def create_submenu(data: SubMenuCreation, menu_id: int, service: SubMenuService = Depends()) -> SubMenu:
    result = await service.create(data, menu_id)
    return result


@router.delete('/{submenu_id}', description='Удаление выбранного подменю',
               status_code=status.HTTP_200_OK, name='delete_submenu_url',
               responses={200: {'description': 'Успешное удаление объекта'},
                          404: {'description': 'Объект не найден'},
                          422: {'description': 'Ошибка валидации данных'}}
               )
async def delete_submenu(submenu_id: int, service: SubMenuService = Depends()) -> dict:
    result = await service.delete(submenu_id)
    return result


@router.patch('/{submenu_id}', description='Изменение выбранного подменю', response_model=SubMenu,
              status_code=status.HTTP_200_OK, name='update_submenu_url',
              responses={200: {'description': 'Успешное обновление объекта'},
                         404: {'description': 'Объект не найден'},
                         422: {'description': 'Ошибка валидации данных'}}
              )
async def update_submenu(submenu_id: int, data: SubMenuCreation, service: SubMenuService = Depends()) -> SubMenu:
    result = await service.update(submenu_id, data)
    return result
