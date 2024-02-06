import json

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.database import get_db
from models.models import Dish as DishTable
from repositories.cache_repository import CacheRepository
from schemas.schemas import Dish, DishCreation


class DishesRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.db = session
        self.name = 'dish'
        self.cache = CacheRepository(self.name)

    async def create(self, data: DishCreation, submenu_id: int) -> Dish:
        db_item = DishTable(title=data.title, description=data.description,
                            price=round(data.price, 2), submenu_id=submenu_id)
        try:
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            self.db.close()
            item = Dish(id=str(db_item.id), title=data.title, description=data.description,
                        price=round(data.price, 2))
            return item

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Запись с таким именем уже существует'
            )

    async def get_all(self) -> list[type[Dish]] | list:
        all_cache = await self.cache.get_items(f"{self.name}-all")
        if all_cache:
            print('cache data...')
            return all_cache

        db_items = self.db.query(DishTable).all()
        items = list()

        if db_items:
            for item in db_items:
                result = Dish(id=str(item.id), title=item.title,
                              description=item.description, price=item.price)
                await self.cache.set_items(f"{self.name}-all",
                                           json.dumps(dict(result), default=str))
                items.append(result)

        return items

    async def get(self, dish_id: int) -> Dish:
        one_cache = await self.cache.get_item(f"{self.name}-{dish_id}")
        if one_cache:
            print('cache data...')
            return Dish(**json.loads(one_cache))

        db_item = self.db.query(DishTable).filter(DishTable.id == dish_id).first()
        if db_item:
            item = Dish(id=str(db_item.id), title=db_item.title,
                        description=db_item.description, price=round(db_item.price, 2))
            await self.cache.set_item(f"{self.name}-{db_item.id}", json.dumps(dict(item),
                                                                              default=str), 60)
            return item

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )

    async def delete(self, dish_id: int) -> dict:
        db_item = self.db.query(DishTable).filter(DishTable.id == dish_id).first()
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Записи с id = {dish_id} не существует'
            )
        self.db.delete(db_item)
        self.db.commit()
        await self.cache.remove_item(f"{self.name}-{dish_id}")
        await self.cache.remove_item(f"{self.name}-all")
        await self.cache.remove_item(f'submenu-{db_item.submenu_id}')
        return {'status': True, 'message': 'The dish has been deleted'}

    async def update(self, submenu_id: int, data: DishCreation) -> Dish:
        db_item = self.db.query(DishTable).filter(DishTable.id == submenu_id).first()
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found'
            )
        db_item.title = data.title
        db_item.description = data.description
        db_item.price = round(data.price, 2)
        self.db.commit()
        self.db.refresh(db_item)
        item = Dish(id=str(db_item.id), title=data.title, description=data.description,
                    price=round(data.price, 2))
        await self.cache.set_item(f"{self.name}-{db_item.id}",
                                  json.dumps(dict(item), default=str), 60)
        return item
