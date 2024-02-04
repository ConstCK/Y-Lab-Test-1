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
def test_create_first_dish():
    # Создание первого блюда
    response = client.post(DISHES_URL, json=MY_DISH_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert MY_DISH_1['title'] == response.json().get('title')
    assert MY_DISH_1['description'] == response.json().get('description')
    assert MY_DISH_1['price'] == response.json().get('price')

    MY_DISH_1['id'] = response.json().get('id')


# 4
def test_create_second_dish():
    # Создание второго блюда
    response = client.post(DISHES_URL, json=MY_DISH_2)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert MY_DISH_2['title'] == response.json().get('title')
    assert MY_DISH_2['description'] == response.json().get('description')
    assert MY_DISH_2['price'] == response.json().get('price')

    MY_DISH_2['id'] = response.json().get('id')


# 5
def test_get_menu():
    # Получение указанного меню
    response = client.get(f"{MENUS_URL}/{MY_MENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == MY_MENU_1.get('id')
    assert response.json().get('title') == MY_MENU_1.get('title')
    assert response.json().get('description') == MY_MENU_1.get('description')
    assert response.json().get('submenus_count') == 1
    assert response.json().get('dishes_count') == 2


# 6
def test_get_submenu():
    # Получение указанного подменю
    response = client.get(f"{SUBMENUS_URL}/{MY_SUBMENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == MY_SUBMENU_1.get('id')
    assert response.json().get('title') == MY_SUBMENU_1.get('title')
    assert response.json().get('description') == MY_SUBMENU_1.get('description')
    assert response.json().get('dishes_count') == 2


# 7
def test_delete_submenu():
    # Удаление указанного подменю
    response = client.delete(f"{SUBMENUS_URL}/{MY_SUBMENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The submenu has been deleted'}


# 8
def test_final_get_submenus():
    # Получение пустого списка подменю
    response = client.get(SUBMENUS_URL)
    assert response.status_code == 200
    assert response.json() == []


# 9
def test_final_get_dishes():
    # Получение пустого списка блюд
    response = client.get(DISHES_URL)
    assert response.status_code == 200
    assert response.json() == []


# 10
def test_final_get_menu():
    # Получение указанного меню
    response = client.get(f"{MENUS_URL}/{MY_MENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == MY_MENU_1.get('id')
    assert response.json().get('title') == MY_MENU_1.get('title')
    assert response.json().get('description') == MY_MENU_1.get('description')
    assert response.json().get('submenus_count') == 0
    assert response.json().get('dishes_count') == 0


# 11
def test_delete_menu():
    # Удаление указанного меню
    response = client.delete(f"{MENUS_URL}/{MY_MENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


# 12
def test_final_get_menus():
    # Получение пустого списка меню
    response = client.get(MENUS_URL)
    assert response.status_code == 200
    assert response.json() == []
