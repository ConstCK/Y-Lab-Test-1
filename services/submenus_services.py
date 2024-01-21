from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from database.database import get_db
from models.models import SubMenu as SubMenuTable
from schemas.schemas import SubMenu, SubMenuCreation


class SubMenuService:
    def __init__(self):
        self.db = next(get_db())

    def create(self, data: SubMenuCreation, menu_id: int) -> SubMenuTable:
        item = SubMenuTable(title=data.title, description=data.description, menu_id=menu_id)

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

    def get_all(self) -> list[SubMenu] | dict:
        items = self.db.query(SubMenuTable).all()
        items_list = list()
        if items:
            for item in items:
                result = SubMenu(id=item.id, title=item.title, description=item.description)
                result.dishes_quantity = len(item.dishes)
                items_list.append(result)
            return items_list

        return {'message': 'Нет записей в таблице меню'}

    def get(self, submenu_id: int) -> SubMenu:
        item = self.db.query(SubMenuTable).filter(SubMenuTable.id == submenu_id).first()
        if item:
            result = SubMenu(id=item.id, title=item.title, description=item.description)
            return result
        raise HTTPException(
            status_code=404,
            detail=f'Записи с id = {submenu_id} не существует'
        )

    def delete(self, submenu_id: int) -> None:
        item = self.db.query(SubMenuTable).filter(SubMenuTable.id == submenu_id).first()
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f'Записи с id = {submenu_id} не существует'
            )
        self.db.delete(item)
        self.db.commit()

    def update(self, submenu_id: int, data: SubMenuCreation) -> None:
        item = self.db.query(SubMenuTable).filter(SubMenuTable.id == submenu_id).first()
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f'Записи с id = {submenu_id} не существует'
            )
        item.title = data.title
        item.description = data.description
        self.db.commit()
        self.db.refresh(item)
