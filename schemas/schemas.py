from decimal import Decimal

from pydantic import BaseModel, Field


class BaseMenu(BaseModel):
    title: str
    description: str | None = None


class Menu(BaseMenu):
    id: str
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        from_attributes = True


class MenuCreation(BaseMenu):
    pass


class BaseSubMenu(BaseModel):
    title: str
    description: str | None = None


class SubMenu(BaseSubMenu):
    id: str
    dishes_count: int = 0

    class Config:
        from_attributes = True


class SubMenuCreation(BaseSubMenu):
    pass


class BaseDish(BaseModel):
    title: str
    description: str | None = None
    price: Decimal = Field(gt=0)


class Dish(BaseDish):
    id: str

    class Config:
        from_attributes = True


class DishCreation(BaseDish):
    pass
