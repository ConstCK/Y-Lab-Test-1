import pytest
from fastapi.testclient import TestClient

from database.database import Base, engine
from main import app

from .constants import BASE_URL, MY_MENU_1, MY_SUBMENU_1, MY_SUBMENU_2

client = TestClient(app)

MENUS_URL = f"{BASE_URL}/menus"
SUBMENUS_URL = ''


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
def test_initial_get_submenus():
    # Получение пустого списка подменю
    response = client.get(SUBMENUS_URL)
    assert response.status_code == 200
    assert response.json() == []


# 3
def test_create_submenu():
    # Создание нового подменю
    response = client.post(SUBMENUS_URL, json=MY_SUBMENU_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('dishes_count') == 0
    assert MY_SUBMENU_1['title'] == response.json().get('title')
    assert MY_SUBMENU_1['description'] == response.json().get('description')

    MY_SUBMENU_1['id'] = response.json().get('id')


# 4
def test_duplicate_submenu():
    # Создание уже существующего подменю
    response = client.post(SUBMENUS_URL, json=MY_SUBMENU_1)
    assert response.status_code == 409


# 5
def test_get_submenus():
    # Получение списка подменю
    response = client.get(SUBMENUS_URL)
    assert response.status_code == 200
    assert len(response.json()) > 0


# 6
def test_get_submenu():
    # Получение указанного подменю
    response = client.get(f"{SUBMENUS_URL}/{MY_SUBMENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == MY_SUBMENU_1.get('id')
    assert response.json().get('title') == MY_SUBMENU_1.get('title')
    assert response.json().get('description') == MY_SUBMENU_1.get('description')
    assert 'dishes_count' in response.json()


# 7
def test_get_none_submenu():
    # Получение указанного подменю
    response = client.get(f"{SUBMENUS_URL}/0")
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


# 8
def test_update_submenu():
    # Обновление указанного подменю
    response = client.patch(f"{SUBMENUS_URL}/{MY_SUBMENU_1.get('id')}",
                            json=MY_SUBMENU_2)
    assert response.status_code == 200
    assert response.json().get('id') == MY_SUBMENU_1.get('id')
    assert response.json().get('title') == MY_SUBMENU_2.get('title')
    assert response.json().get('description') == MY_SUBMENU_2.get('description')
    assert 'dishes_count' in response.json()


# 9
def test_update_none_submenu():
    # Обновление несуществующего подменю
    response = client.patch(f"{SUBMENUS_URL}/0",
                            json=MY_SUBMENU_2)
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


# 10
def test_get_updated_submenu():
    # Получение обновленного подменю
    response = client.get(f"{SUBMENUS_URL}/{MY_SUBMENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == MY_SUBMENU_1.get('id')
    assert response.json().get('title') == MY_SUBMENU_2.get('title')
    assert response.json().get('description') == MY_SUBMENU_2.get('description')
    assert 'dishes_count' in response.json()


# 11
def test_delete_submenu():
    # Удаление указанного подменю
    response = client.delete(f"{SUBMENUS_URL}/{MY_SUBMENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The submenu has been deleted'}


# 12
def test_delete_none_submenu():
    # Удаление несуществующего подменю
    response = client.delete(f"{MENUS_URL}/0")
    assert response.status_code == 404


# 13
def test_final_get_submenus():
    # Получение пустого списка подменю
    response = client.get(SUBMENUS_URL)
    assert response.status_code == 200
    assert response.json() == []


# 14
def test_final_get_none_submenu():
    # Получение указанного подменю
    response = client.get(f"{SUBMENUS_URL}/{MY_SUBMENU_1.get('id')}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


# 15
def test_delete_menu():
    # Удаление указанного меню
    response = client.delete(f"{MENUS_URL}/{MY_MENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


# 16
def test_final_get_menus():
    # Получение пустого списка меню
    response = client.get(MENUS_URL)
    assert response.status_code == 200
    assert response.json() == []
