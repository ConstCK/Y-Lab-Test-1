from fastapi import APIRouter, Depends, status

from schemas.schemas import Dish, DishCreation
from services.dishes_services import DishesService

router = APIRouter()


@router.get('/', description='Получение списка всех блюд', response_model=list[Dish],
            status_code=status.HTTP_200_OK)
async def get_dishes(service: DishesService = Depends()) -> list[Dish] | list:
    result = await service.get_all()
    return result


@router.get('/{dish_id}', description='Получение выбранного блюда', response_model=Dish,
            status_code=status.HTTP_200_OK)
async def get_dish(dish_id: int, service: DishesService = Depends()) -> Dish:
    result = await service.get(dish_id)
    return result


@router.post('/', description='Создание нового блюда', status_code=status.HTTP_201_CREATED,
             response_model=Dish)
async def create_dish(data: DishCreation, submenu_id: int, service: DishesService = Depends()) -> Dish:
    result = await service.create(data, submenu_id)
    return result


@router.patch('/{dish_id}', description='Изменение выбранного блюда', response_model=Dish,
              status_code=status.HTTP_200_OK)
async def update_dish(dish_id: int, data: DishCreation, service: DishesService = Depends()) -> Dish:
    result = await service.update(dish_id, data)
    return result


@router.delete('/{dish_id}', description='Удаление выбранного блюда', status_code=status.HTTP_200_OK)
async def delete_dish(dish_id: int, service: DishesService = Depends()) -> dict:
    result = await service.delete(dish_id)
    return result
