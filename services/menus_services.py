from fastapi import HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db
from models.models import Menu as MenuTable
from models.models import SubMenu as SubMenuTable
from models.models import Dish as DishTable
from schemas.schemas import Menu, MenuCreation


class MenuService:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session

    def create(self, data: MenuCreation) -> Menu:
        db_item = MenuTable(title=data.title, description=data.description)
        try:
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            item = Menu(id=str(db_item.id), title=data.title, description=data.description,
                        submenus_count=0, dishes_count=0)
            return item
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail=f'Запись с таким именем уже существует'
            )

    def get_all(self) -> list[Menu] | list:
        db_items = self.db.query(MenuTable).all()
        items_list = list()
        if db_items:
            for item in db_items:
                # submenu_counter = (self.db.query(SubMenuTable)
                #                    .filter(SubMenuTable.menu_id == item.id).count())
                # dishes_counter = (self.db.query(DishTable)
                #                   .filter(DishTable.submenu_id.in_(item.submenus)).count())
                result = Menu(id=str(item.id), title=item.title, description=item.description)
                result.submenus_count = len(item.submenus)
                result.dishes_count = sum(len(s.dishes) for s in item.submenus)
                # result.submenus_count = submenu_counter
                # result.dishes_count = dishes_counter
                items_list.append(result)
        return items_list

    def get(self, menu_id: int) -> Menu:
        db_item = self.db.query(MenuTable).filter(MenuTable.id == menu_id).first()
        if db_item:
            item = Menu(id=str(db_item.id), title=db_item.title, description=db_item.description)
            item.submenus_count = len(db_item.submenus)
            item.dishes_count = sum(len(s.dishes) for s in db_item.submenus)
            return item
        raise HTTPException(
            status_code=404,
            detail='menu not found'
        )

    def delete(self, menu_id: int) -> dict:
        db_item = self.db.query(MenuTable).filter(MenuTable.id == menu_id).first()
        if not db_item:
            raise HTTPException(
                status_code=404,
                detail=f'Записи с id = {menu_id} не существует'
            )
        self.db.delete(db_item)
        self.db.commit()
        return {'status': True, 'message': 'The menu has been deleted'}

    def update(self, menu_id: int, data: MenuCreation) -> Menu:
        db_item = self.db.query(MenuTable).filter(MenuTable.id == menu_id).first()
        if not db_item:
            raise HTTPException(
                status_code=404,
                detail='menu not found'
            )
        db_item.title = data.title
        db_item.description = data.description
        self.db.commit()
        self.db.refresh(db_item)
        item = Menu(id=str(db_item.id), title=data.title, description=data.description, )
        item.submenus_count = len(db_item.submenus)
        item.dishes_count = sum(len(s.dishes) for s in db_item.submenus)
        return item
