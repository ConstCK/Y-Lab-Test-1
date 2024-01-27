from fastapi import HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db
from models.models import Dish as DishTable
from models.models import Menu as MenuTable
from models.models import SubMenu as SubMenuTable
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
        db_items = (self.db.query(MenuTable,
                                  func.count(SubMenuTable.id.distinct()).label('submenus_count'),
                                  func.count(DishTable.id.distinct()).label('dishes_count'))
                    .select_from(MenuTable).outerjoin(SubMenuTable).outerjoin(DishTable).group_by(MenuTable.id).all())
        items_list = list()

        if db_items:
            for item in db_items:
                result = Menu(id=str(item[0].id), title=item[0].title, description=item[0].description,
                              submenus_count=item.submenus_count, dishes_count=item.dishes_count)
                items_list.append(result)
        return items_list

    def get(self, menu_id: int) -> Menu:
        db_item = (self.db.query(MenuTable,
                                 func.count(SubMenuTable.id.distinct()).label('submenus_count'),
                                 func.count(DishTable.id.distinct()).label('dishes_count'))
                   .select_from(MenuTable).filter(MenuTable.id == menu_id).outerjoin(SubMenuTable).outerjoin(
            DishTable).group_by(MenuTable.id).first())

        if db_item[0]:
            item = Menu(id=str(db_item[0].id), title=db_item[0].title, description=db_item[0].description,
                        submenus_count=db_item.submenus_count, dishes_count=db_item.dishes_count)

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
        # db_item = self.db.query(MenuTable).filter(MenuTable.id == menu_id).first()
        db_item = (self.db.query(MenuTable,
                                 func.count(SubMenuTable.id.distinct()).label('submenus_count'),
                                 func.count(DishTable.id.distinct()).label('dishes_count'))
                   .select_from(MenuTable).filter(MenuTable.id == menu_id).outerjoin(SubMenuTable).outerjoin(
            DishTable).group_by(MenuTable.id).first())

        if not db_item[0]:
            raise HTTPException(
                status_code=404,
                detail='menu not found'
            )
        db_item[0].title = data.title
        db_item[0].description = data.description
        item = Menu(id=str(db_item[0].id), title=data.title, description=data.description,
                    submenus_count=db_item.submenus_count, dishes_count=db_item.dishes_count)
        self.db.commit()
        self.db.refresh(db_item[0])
        return item
