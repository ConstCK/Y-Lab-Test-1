from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from database.database import get_db
from models.models import Menu as MenuTable
from schemas.schemas import Menu, MenuCreation


class MenuService:
    def __init__(self):
        self.db = next(get_db())

    def create(self, data: MenuCreation) -> MenuCreation:
        item = MenuCreation(title=data.title, description=data.description)
        db_item = MenuTable(**dict(item))
        try:
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail=f'Запись с таким именем уже существует'
            )
        return item

    def get_all(self) -> list[Menu] | dict:
        items = self.db.query(MenuTable).all()
        items_list = list()
        if items:
            for item in items:
                result = Menu(id=item.id, title=item.title, description=item.description)
                result.submenus_quantity = len(item.submenus)
                result.dishes_quantity = sum(len(s.dishes) for s in item.submenus)
                items_list.append(result)
                return items_list

        return {'message': 'Нет записей в таблице меню'}

    def get(self, menu_id: int) -> Menu:
        item = self.db.query(MenuTable).filter(MenuTable.id == menu_id).first()
        if item:
            result = Menu(id=item.id, title=item.title, description=item.description)
            result.submenus_quantity = len(item.submenus)
            item.dishes_count = sum(len(s.dishes) for s in item.submenus)
            return result
        raise HTTPException(
            status_code=404,
            detail=f'Записи с id = {menu_id} не существует'
        )

    def delete(self, menu_id: int) -> None:
        item = self.db.query(MenuTable).filter(MenuTable.id == menu_id).first()
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f'Записи с id = {menu_id} не существует'
            )
        self.db.delete(item)
        self.db.commit()

    def update(self, menu_id: int, data: MenuCreation) -> None:
        item = self.db.query(MenuTable).filter(MenuTable.id == menu_id).first()
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f'Записи с id = {menu_id} не существует'
            )
        item.title = data.title
        item.description = data.description
        self.db.commit()
        self.db.refresh(item)

