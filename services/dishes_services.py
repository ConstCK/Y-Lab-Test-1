from typing import Type

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.models import Dish as DishTable
from schemas.schemas import Dish, DishCreation


class DishesService:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session

    def create(self, data: DishCreation, submenu_id: int) -> Dish:
        db_item = DishTable(title=data.title, description=data.description,
                            price=data.price, submenu_id=submenu_id)
        try:
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            self.db.close()
            item = Dish(id=db_item.id, title=data.title, description=data.description,
                        price=data.price)
            return item

        except AssertionError:
            raise HTTPException(
                status_code=409,
                detail=f'Запись с таким именем уже существует'
            )

    def get_all(self) -> list[Type[Dish]] | dict:
        items = self.db.query(DishTable).all()
        if items:
            return items
        return {'message': 'Нет записей в таблице блюд'}

    def get(self, dish_id: int) -> Dish:
        db_item = self.db.query(DishTable).filter(DishTable.id == dish_id).first()
        if db_item:
            result = Dish(id=db_item.id, title=db_item.title,
                          description=db_item.description, price=db_item.price)
            return result
        raise HTTPException(
            status_code=404,
            detail='dish not found'
        )

    def delete(self, dish_id: int) -> dict:
        item = self.db.query(DishTable).filter(DishTable.id == dish_id).first()
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f'Записи с id = {dish_id} не существует'
            )
        self.db.delete(item)
        self.db.commit()
        return {'status': True, 'message': 'The dish has been deleted'}

    def update(self, submenu_id: int, data: DishCreation) -> Dish:
        db_item = self.db.query(DishTable).filter(DishTable.id == submenu_id).first()
        if not db_item:
            raise HTTPException(
                status_code=404,
                detail='dish not found'
            )
        db_item.title = data.title
        db_item.description = data.description
        db_item.price = data.price
        self.db.commit()
        self.db.refresh(db_item)
        item = Dish(id=db_item.id, title=data.title, description=data.description,
                    price=data.price)
        return item
