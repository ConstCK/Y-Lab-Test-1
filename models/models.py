from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from database.database import Base


class MenuTable(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), unique=True, nullable=False)
    description = Column(String(128))
    submenus = relationship('SubMenu', back_populates='menu', cascade='all, delete')


class SubMenuTable(Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), unique=True, nullable=False)
    description = Column(String(128))
    menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'))

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete')


class DishTable(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), unique=True, nullable=False)
    description = Column(String(256))
    # test it
    price = Column(Float(precision=8, decimal_return_scale=2), nullable=False)
    submenu_id = Column(Integer, ForeignKey('submenus.id', ondelete='CASCADE'))

    submenu = relationship('SubMenu', back_populates='dishes')