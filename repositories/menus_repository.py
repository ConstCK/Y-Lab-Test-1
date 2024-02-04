import json

from fastapi import Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db
from models.models import Dish as DishTable
from models.models import Menu as MenuTable
from models.models import SubMenu as SubMenuTable
from repositories.cache_repository import CacheRepository
from schemas.schemas import Menu, MenuCreation


class MenuRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session
        self.name = 'menu'
        self.cache = CacheRepository(self.name)

    async def create(self, data: MenuCreation) -> Menu:
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
                detail='Запись с таким именем уже существует'
            )

    async def get_all(self) -> list[Menu] | list:
        all_cache = await self.cache.get_items()
        if all_cache:
            print('cache data...')
            return all_cache

        db_items = (self.db.query(MenuTable,
                                  func.count(SubMenuTable.id.distinct()).label('submenus_count'),
                                  func.count(DishTable.id.distinct()).label('dishes_count'))
                    .select_from(MenuTable).outerjoin(SubMenuTable).outerjoin(DishTable).group_by(MenuTable.id).all())
        items_list = list()
        for item in db_items:
            if item[0]:
                result = Menu(id=str(item[0].id), title=item[0].title, description=item[0].description,
                              submenus_count=item.submenus_count, dishes_count=item.dishes_count)
                items_list.append(result)
                await self.cache.set_items(json.dumps(dict(result)))

        return items_list

    async def get(self, menu_id: int) -> Menu:
        cache_one = await self.cache.get_item(menu_id)
        if cache_one:
            print('cache data...')
            print(Menu(**json.loads(cache_one)))
            return Menu(**json.loads(cache_one))

        db_item = (self.db.query(MenuTable,
                                 func.count(SubMenuTable.id.distinct()).label('submenus_count'),
                                 func.count(DishTable.id.distinct()).label('dishes_count'))
                   .select_from(MenuTable).filter(MenuTable.id == menu_id).outerjoin(SubMenuTable).outerjoin(
            DishTable).group_by(MenuTable.id).first())

        if db_item:
            item = Menu(id=str(db_item[0].id), title=db_item[0].title, description=db_item[0].description,
                        submenus_count=db_item.submenus_count, dishes_count=db_item.dishes_count)
            await self.cache.set_item(db_item[0].id, json.dumps(dict(item)), 60)

            return item
        raise HTTPException(
            status_code=404,
            detail='menu not found'
        )

    async def delete(self, menu_id: int) -> dict:
        db_item = self.db.query(MenuTable).filter(MenuTable.id == menu_id).first()
        if not db_item:
            raise HTTPException(
                status_code=404,
                detail=f'Записи с id = {menu_id} не существует'
            )
        self.db.delete(db_item)
        self.db.commit()
        await self.cache.remove_item(menu_id)
        await self.cache.remove_item('all')
        return {'status': True, 'message': 'The menu has been deleted'}

    async def update(self, menu_id: int, data: MenuCreation) -> Menu:
        db_item = (self.db.query(MenuTable,
                                 func.count(SubMenuTable.id.distinct()).label('submenus_count'),
                                 func.count(DishTable.id.distinct()).label('dishes_count'))
                   .select_from(MenuTable).filter(MenuTable.id == menu_id).outerjoin(SubMenuTable).outerjoin(
            DishTable).group_by(MenuTable.id).first())

        if not db_item:
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
        await self.cache.set_item(db_item[0].id, json.dumps(dict(item)), 60)
        return item
