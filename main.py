import json
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from controllers.dishes_routing import router as dish_router
from controllers.menus_routing import router as menu_router
from controllers.submenus_routing import router as submenu_router
from database.database import engine, Base
from repositories.cache_repository import CacheRepository
from schemas.schemas import Menu

load_dotenv()
app = FastAPI()


@app.get('/', description="Приветственная надпись", )
async def greetings() -> dict:
    return {'message': 'Greetings, sir'}


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    a = CacheRepository('menu')
    # await a.set_item(1, json.dumps(dict(Menu(id='1', title='t -1', description='d-1',
    #                                          submenus_count=0, dishes_count=11))), 10)
    await a.set_items(json.dumps(dict(Menu(id='1', title='t -1',
                                           description='d-1',
                                           submenus_count=0,
                                           dishes_count=11))), 20)
    await a.set_items(json.dumps(dict(Menu(id='2', title='t -2',
                                           description='d-2',
                                           submenus_count=3,
                                           dishes_count=6))), 10)

    await a.set_item(1, json.dumps(dict(Menu(id='3', title='t -3 alone',
                                             description='d-3 alone',
                                             submenus_count=77,
                                             dishes_count=66))), 30)


@app.get('/test')
async def test():
    b = CacheRepository('menu')
    return await b.show_all_keys()


# @app.get('/all')
# async def test():
#     b = CacheRepository('test')
#     result = await b.get_items('test-all')
#     # new = [json.loads(x) for x in result]
#     # result = json.loads(result)
#     print(result)
#     print(type(result))
#     # print(type(new))
#     # print(new)
#     # print(result['dishes_count'])
#     if result:
#         return result
#     await asyncio.sleep(2)
#     return {'key': 'bye'}
#
#
# @app.get('/one')
# async def test():
#     b = CacheRepository('test')
#     result = await b.get_item('test-1')
#     print(type(result))
#     print(result)
#     if result is not None:
#         return str(result)
#     await asyncio.sleep(2)
#     return {'key': 'bye'}


app.include_router(menu_router, prefix='/api/v1/menus')
app.include_router(submenu_router, prefix='/api/v1/menus/{menu_id}/submenus')
app.include_router(dish_router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')

# Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run("main:app", host=os.getenv('HOST'), port=8000, reload=True)
