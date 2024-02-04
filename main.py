import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from controllers.dishes_routing import router as dish_router
from controllers.menus_routing import router as menu_router
from controllers.submenus_routing import router as submenu_router
from database.database import Base, engine

load_dotenv()
tags_metadata = [
    {
        'name': 'users',
        'description': 'Operations with users. The **login** logic is also here.',
    },

]

app = FastAPI()


@app.get('/', description='Приветственная надпись', )
async def greetings() -> dict:
    return {'message': 'Greetings, sir'}


@app.on_event('startup')
async def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(menu_router, prefix='/api/v1/menus', tags=['menus'])
app.include_router(submenu_router, prefix='/api/v1/menus/{menu_id}/submenus', tags=['submenus'])
app.include_router(dish_router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
                   tags=['dishes'])

if __name__ == '__main__':
    uvicorn.run('main:app', host=os.getenv('HOST'), port=8000, reload=True)
