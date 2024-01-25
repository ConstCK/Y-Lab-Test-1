from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from database.database import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), unique=True, nullable=False)
    description = Column(String(128))
    submenus = relationship('SubMenu', back_populates='menu', cascade='all, delete')


class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), unique=True, nullable=False)
    description = Column(String(128))
    menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'))

    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete')
    menu = relationship('Menu', back_populates='submenus')


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), unique=True, nullable=False)
    description = Column(String(256))
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    submenu_id = Column(Integer, ForeignKey('submenus.id', ondelete='CASCADE'))

    submenu = relationship('SubMenu', back_populates='dishes')
