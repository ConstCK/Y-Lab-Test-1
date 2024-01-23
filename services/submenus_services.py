from fastapi import HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db
from models.models import SubMenu as SubMenuTable
from schemas.schemas import SubMenu, SubMenuCreation


class SubMenuService:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session

    def create(self, data: SubMenuCreation, menu_id: int) -> SubMenu:
        db_item = SubMenuTable(title=data.title, description=data.description, menu_id=menu_id)

        try:
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            item = SubMenu(id=db_item.id, title=data.title, description=data.description,
                           dishes_count=0)
            return item

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail=f'Запись с таким именем уже существует'
            )

    def get_all(self) -> list[SubMenu] | dict:
        db_items = self.db.query(SubMenuTable).all()
        items_list = list()
        if db_items:
            for item in db_items:
                result = SubMenu(id=item.id, title=item.title, description=item.description)
                result.dishes_count = len(item.dishes)
                items_list.append(result)
            return items_list

        return {'message': 'Нет записей в таблице подменю'}

    def get(self, submenu_id: int) -> SubMenu:
        db_item = self.db.query(SubMenuTable).filter(SubMenuTable.id == submenu_id).first()
        if db_item:
            item = SubMenu(id=db_item.id, title=db_item.title, description=db_item.description)
            item.dishes_count = len(db_item.dishes)
            return item
        raise HTTPException(
            status_code=404,
            detail='submenu not found'
        )

    def delete(self, submenu_id: int) -> dict:
        db_item = self.db.query(SubMenuTable).filter(SubMenuTable.id == submenu_id).first()
        if not db_item:
            raise HTTPException(
                status_code=404,
                detail=f'Записи с id = {submenu_id} не существует'
            )
        self.db.delete(db_item)
        self.db.commit()
        return {'status': True, 'message': 'The submenu has been deleted'}

    def update(self, submenu_id: int, data: SubMenuCreation) -> SubMenu:
        db_item = self.db.query(SubMenuTable).filter(SubMenuTable.id == submenu_id).first()
        if not db_item:
            raise HTTPException(
                status_code=404,
                detail=f'submenu not found'
            )
        db_item.title = data.title
        db_item.description = data.description
        self.db.commit()
        self.db.refresh(db_item)
        item = SubMenu(id=db_item.id, title=data.title, description=data.description,)
        item.dishes_count = len(db_item.dishes)
        return item
