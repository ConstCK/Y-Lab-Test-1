from fastapi import APIRouter, Depends

from schemas.schemas import Dish, DishCreation
from services.dishes_services import DishesService

router = APIRouter()

@router.get('/', description='Получение списка всех блюд')
async def get_dishes(service: DishesService = Depends()) -> list[Dish] | dict:
    return service.get_all()


@router.get('/{dish_id}', description='Получение выбранного блюда')
async def get_dish(dish_id: int, service: DishesService = Depends()) -> Dish:
    return service.get(dish_id)


@router.post('/', description='Создание нового блюда')
async def create_dish(data: DishCreation, submenu_id: int, service: DishesService = Depends()) -> dict:
    result = service.create(data, submenu_id)
    return {'message': f'Успешное создание блюда -> {result.title}'}


@router.patch('/{dish_id}', description='Изменение выбранного блюда')
async def update_dish(dish_id: int, data: DishCreation, service: DishesService = Depends()) -> dict:
    service.update(dish_id, data)
    return {'message': f'Запись с id = {dish_id} успешно изменена'}


@router.delete('/{dish_id}', description='Удаление выбранного блюда')
async def delete_dish(dish_id: int, service: DishesService = Depends()) -> dict:
    service.delete(dish_id)
    return {'message': f'Запись с id = {dish_id} успешно удалена'}


