from fastapi import APIRouter

from schemas.schemas import Dish

router = APIRouter()


@router.get('/dish', description='Получение списка всех блюд')
async def get_dishes() -> list[Dish]:
    pass


@router.get('/dish/{dish_id}', description='Получение выбранного блюда')
async def get_dish(dish_id: int) -> dict:
    pass


@router.post('/dish', description='Создание нового блюда')
async def create_dish(dish: Dish) -> dict:
    pass


@router.put('/dish/{dish_id}', description='Изменение выбранного блюда')
async def update_dish(dish_id: int) -> dict:
    pass


@router.delete('/dish/{dish_id}', description='Удаление выбранного блюда')
async def delete_dish(dish_id: int) -> dict:
    pass


@router.delete('/dish', description='Удаление всех блюд')
async def delete_dishes() -> dict:
    pass