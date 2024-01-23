from pydantic import BaseModel


class BaseMenu(BaseModel):
    title: str
    description: str | None = None


class Menu(BaseMenu):
    id: int
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True


class MenuCreation(BaseMenu):
    pass


class BaseSubMenu(BaseModel):
    title: str
    description: str | None = None


class SubMenu(BaseSubMenu):
    id: int
    dishes_count: int = 0

    class Config:
        orm_mode = True


class SubMenuCreation(BaseSubMenu):
    pass


class BaseDish(BaseModel):
    title: str
    description: str | None = None
    price: float


class Dish(BaseDish):
    id: int

    class Config:
        orm_mode = True


class DishCreation(BaseDish):
    pass
