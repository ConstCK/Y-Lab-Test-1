from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from database.database import get_db
from models.models import Dish as DishTable
from schemas.schemas import Dish, DishCreation


class DishesService:
    def __init__(self):
        self.db = next(get_db())

    def create(self, data: DishCreation, submenu_id: int) -> DishTable:
        item = DishTable(title=data.title, description=data.description,
                         price=data.price, submenu_id=submenu_id)
        try:
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            self.db.close()
            return item
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail=f'Запись с таким именем уже существует'
            )

    def get_all(self) -> list[Dish] | dict:
        items = self.db.query(DishTable).all()
        if items:
            return items
        return {'message': 'Нет записей в таблице блюд'}

    def get(self, dish_id: int) -> Dish:
        item = self.db.query(DishTable).filter(DishTable.id == dish_id).first()
        if item:
            result = Dish(id=item.id, title=item.title,
                          description=item.description, price=item.price)
            return result
        raise HTTPException(
            status_code=404,
            detail=f'Записи с id = {dish_id} не существует'
        )

    def delete(self, dish_id: int) -> None:
        item = self.db.query(DishTable).filter(DishTable.id == dish_id).first()
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f'Записи с id = {dish_id} не существует'
            )
        self.db.delete(item)
        self.db.commit()

    def update(self, submenu_id: int, data: DishCreation) -> None:
        item = self.db.query(DishTable).filter(DishTable.id == submenu_id).first()
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f'Записи с id = {submenu_id} не существует'
            )
        item.title = data.title
        item.description = data.description
        item.price = data.price
        self.db.commit()
        self.db.refresh(item)
