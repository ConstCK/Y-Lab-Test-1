from fastapi import APIRouter

from schemas.schemas import Menu

router = APIRouter()


@router.get('/submenu', description='Получение списка всех подменю')
async def get_menus() -> list[Menu]:
    pass


@router.get('/submenu/{submenu_id}', description='Получение выбранного подменю')
async def get_menu(submenu_id: int) -> dict:
    pass


@router.post('/submenu', description='Создание нового подменю')
async def create_menu(menu: Menu) -> dict:
    pass


@router.put('/submenu/{submenu_id}', description='Изменение выбранного подменю')
async def update_menu(submenu_id: int) -> dict:
    pass


@router.delete('/submenu/{submenu_id}', description='Удаление выбранного подменю')
async def delete_menu(submenu_id: int) -> dict:
    pass


@router.delete('/submenu', description='Удаление всех подменю')
async def delete_menus() -> dict:
    pass
