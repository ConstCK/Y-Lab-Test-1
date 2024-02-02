import json
from typing import Any

from fastapi import HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db
from models.models import Dish as DishTable
from models.models import SubMenu as SubMenuTable
from repositories.cache_repository import CacheRepository
from schemas.schemas import SubMenu, SubMenuCreation


class SubMenuRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session
        self.name = 'submenu'
        self.cache = CacheRepository(self.name)

    async def create(self, data: SubMenuCreation, menu_id: int) -> SubMenu:
        db_item = SubMenuTable(title=data.title, description=data.description, menu_id=menu_id)

        try:
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            item = SubMenu(id=str(db_item.id), title=data.title, description=data.description,
                           dishes_count=0)
            await self.cache.set_item(db_item.id, json.dumps(dict(item)), 60)
            return item

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail=f'Запись с таким именем уже существует'
            )

    async def get_all(self) -> list[SubMenu] | list | Any:
        all_cache = await self.cache.get_items(f'{self.name}-all')
        if all_cache:
            print('cache data...')
            return all_cache

        db_items = (self.db.query(SubMenuTable, func.count(DishTable.id.distinct())
                                  .label('dishes_count'))
                    .select_from(SubMenuTable).outerjoin(DishTable)
                    .group_by(SubMenuTable.id).all())
        items_list = list()
        for item in db_items:
            if item[0]:
                result = SubMenu(id=str(item[0].id), title=item[0].title,
                                 description=item[0].description, dishes_count=item.dishes_count)
                items_list.append(result)
                await self.cache.set_items(json.dumps(dict(result)))

        return items_list

    async def get(self, submenu_id: int) -> SubMenu:
        one_cache = await self.cache.get_item(f'{self.name}-{submenu_id}')
        if one_cache:
            print('cache data...')
            return SubMenu(**json.loads(one_cache))

        db_item = (self.db.query(SubMenuTable,
                                 func.count(DishTable.id.distinct()).label('dishes_count'))
                   .select_from(SubMenuTable).filter(SubMenuTable.id == submenu_id).outerjoin(
            DishTable).group_by(SubMenuTable.id).first())
        if db_item:
            item = SubMenu(id=str(db_item[0].id), title=db_item[0].title,
                           description=db_item[0].description, dishes_count=db_item.dishes_count)
            await self.cache.set_item(db_item[0].id, json.dumps(dict(item)), 60)
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

    async def update(self, submenu_id: int, data: SubMenuCreation) -> SubMenu:
        db_item = (self.db.query(SubMenuTable,
                                 func.count(DishTable.id.distinct()).label('dishes_count'))
                   .select_from(SubMenuTable).filter(SubMenuTable.id == submenu_id).outerjoin(
            DishTable).group_by(SubMenuTable.id).first())
        if not db_item:
            raise HTTPException(
                status_code=404,
                detail=f'submenu not found'
            )
        db_item[0].title = data.title
        db_item[0].description = data.description
        item = SubMenu(id=str(db_item[0].id), title=data.title,
                       description=data.description, dishes_count=db_item.dishes_count)
        self.db.commit()
        self.db.refresh(db_item[0])
        await self.cache.set_item(db_item[0].id, json.dumps(dict(item)), 60)
        return item
