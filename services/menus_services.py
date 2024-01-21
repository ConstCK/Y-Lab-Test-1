from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from database.database import SessionLocal
from models.models import MenuTable
from schemas.schemas import Menu, MenuCreation


class MenuService:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, data: MenuCreationSchema) -> MenuCreationSchema:
        item = MenuCreationSchema(title=data.title, description=data.description)
        db_item = Menu(**dict(item))
        try:
            self.db.add(db_item)
            self.db.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail=f'Запись с таким именем уже существует'
            )
        return item

    def get_all(self) -> list[MenuSchema] | dict:
        items = self.db.query(Menu).all()
        items_list = list()
        for item in items:
            result = MenuSchema(id=item.id, title=item.title, description=item.description)
            result.submenus_quantity = len(item.submenus)
            result.dishes_quantity = sum(len(s.dishes) for s in item.submenus)
            items_list.append(result)

        if items_list:
            return items_list

        return {'message': 'Нет записей в таблице меню'}