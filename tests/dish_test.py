import pytest
from fastapi.testclient import TestClient

from database.database import Base, engine
from main import app

from .constants import BASE_URL, MY_DISH_1, MY_DISH_2, MY_MENU_1, MY_SUBMENU_1

client = TestClient(app)

MENUS_URL = f"{BASE_URL}/menus"
SUBMENUS_URL = ''
DISHES_URL = ''


@pytest.fixture(autouse=True)
def test_clear_db():
    Base.metadata.create_all(bind=engine)


# 1


def test_create_menu():
    # Создание нового меню
    response = client.post(MENUS_URL, json=MY_MENU_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('submenus_count') == 0
    assert response.json().get('dishes_count') == 0
    assert MY_MENU_1['title'] == response.json().get('title')
    assert MY_MENU_1['description'] == response.json().get('description')

    global SUBMENUS_URL
    MY_MENU_1['id'] = response.json().get('id')
    SUBMENUS_URL = f"{BASE_URL}/menus/{MY_MENU_1.get('id')}/submenus"


# 2
def test_create_submenu():
    # Создание нового подменю
    response = client.post(SUBMENUS_URL, json=MY_SUBMENU_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('dishes_count') == 0
    assert MY_SUBMENU_1['title'] == response.json().get('title')
    assert MY_SUBMENU_1['description'] == response.json().get('description')

    global DISHES_URL
    MY_SUBMENU_1['id'] = response.json().get('id')
    DISHES_URL = f"{BASE_URL}/menus/{MY_MENU_1.get('id')}/submenus/{MY_SUBMENU_1.get('id')}/dishes"


# 3
def test_initial_get_dishes():
    # Получение пустого списка блюд
    response = client.get(DISHES_URL)
    assert response.status_code == 200
    assert response.json() == []


# 4
def test_create_dish():
    # Создание нового блюда
    response = client.post(DISHES_URL, json=MY_DISH_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert MY_DISH_1['title'] == response.json().get('title')
    assert MY_DISH_1['description'] == response.json().get('description')
    assert MY_DISH_1['price'] == response.json().get('price')

    MY_DISH_1['id'] = response.json().get('id')


# 5
def test_duplicate_dish():
    # Создание уже существующего блюда
    response = client.post(DISHES_URL, json=MY_DISH_1)
    assert response.status_code == 409


# 6
def test_get_dishes():
    # Получение списка подменю
    response = client.get(DISHES_URL)
    assert response.status_code == 200
    assert len(response.json()) > 0


# 7
def test_get_dish():
    # Получение указанного блюда
    response = client.get(f"{DISHES_URL}/{MY_DISH_1.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == MY_DISH_1.get('id')
    assert response.json().get('title') == MY_DISH_1.get('title')
    assert response.json().get('description') == MY_DISH_1.get('description')
    assert response.json().get('price') == MY_DISH_1.get('price')


# 8
def test_get_none_dish():
    # Получение указанного блюда
    response = client.get(f"{DISHES_URL}/0")
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


# 9
def test_update_dish():
    # Обновление указанного блюда
    response = client.patch(f"{DISHES_URL}/{MY_DISH_1.get('id')}",
                            json=MY_DISH_2)
    assert response.status_code == 200
    assert response.json().get('id') == MY_DISH_1.get('id')
    assert response.json().get('title') == MY_DISH_2.get('title')
    assert response.json().get('description') == MY_DISH_2.get('description')
    assert response.json().get('price') == MY_DISH_2.get('price')


# 10
def test_update_none_dish():
    # Обновление несуществующего блюда
    response = client.patch(f"{DISHES_URL}/0",
                            json=MY_DISH_2)
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


# 11
def test_get_updated_dish():
    # Получение обновленного блюда
    response = client.get(f"{DISHES_URL}/{MY_DISH_1.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == MY_DISH_1.get('id')
    assert response.json().get('title') == MY_DISH_2.get('title')
    assert response.json().get('description') == MY_DISH_2.get('description')
    assert response.json().get('price') == MY_DISH_2.get('price')


# 12
def test_delete_dish():
    # Удаление указанного блюда
    response = client.delete(f"{DISHES_URL}/{MY_DISH_1.get('id')}")
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The dish has been deleted'}


# 13
def test_delete_none_dish():
    # Удаление несуществующего блюда
    response = client.delete(f"{DISHES_URL}/0")
    assert response.status_code == 404


# 14
def test_final_get_dishes():
    # Получение пустого списка блюд
    response = client.get(DISHES_URL)
    assert response.status_code == 200
    assert response.json() == []


# 15
def test_final_get_none_dish():
    # Получение удаленного блюда
    response = client.get(f"{DISHES_URL}/{MY_DISH_1.get('id')}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


# 16
def test_delete_submenu():
    # Удаление указанного подменю
    response = client.delete(f"{SUBMENUS_URL}/{MY_SUBMENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The submenu has been deleted'}


# 17
def test_final_get_submenus():
    # Получение пустого списка подменю
    response = client.get(SUBMENUS_URL)
    assert response.status_code == 200
    assert response.json() == []


# 17
def test_delete_menu():
    # Удаление указанного меню
    response = client.delete(f"{MENUS_URL}/{MY_MENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


# 18
def test_final_get_menus():
    # Получение пустого списка меню
    response = client.get(MENUS_URL)
    assert response.status_code == 200
    assert response.json() == []
