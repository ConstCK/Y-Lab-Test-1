import pytest
from fastapi.testclient import TestClient

from database.database import Base, engine
from main import app

from .constants import BASE_URL, MY_MENU_1, MY_MENU_2

client = TestClient(app)

MENUS_URL = f"{BASE_URL}/menus"


@pytest.fixture(autouse=True)
def test_clear_db():
    Base.metadata.create_all(bind=engine)


# 1
def test_initial_get_menus():
    # Получение пустого списка меню
    response = client.get(MENUS_URL)
    assert response.status_code == 200
    assert response.json() == []


# 2
def test_create_menu():
    # Создание нового меню
    response = client.post(MENUS_URL, json=MY_MENU_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('submenus_count') == 0
    assert response.json().get('dishes_count') == 0
    assert MY_MENU_1['title'] == response.json().get('title')
    assert MY_MENU_1['description'] == response.json().get('description')

    MY_MENU_1['id'] = response.json().get('id')


# 3
def test_duplicate_menu():
    # Создание уже существующего меню
    response = client.post(MENUS_URL, json=MY_MENU_1)
    assert response.status_code == 409


# 4
def test_get_menus():
    # Получение списка меню
    response = client.get(MENUS_URL)
    assert response.status_code == 200
    assert len(response.json()) > 0


# 5
def test_get_menu():
    # Получение указанного меню
    response = client.get(f"{MENUS_URL}/{MY_MENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == MY_MENU_1.get('id')
    assert response.json().get('title') == MY_MENU_1.get('title')
    assert response.json().get('description') == MY_MENU_1.get('description')
    assert 'submenus_count' in response.json()
    assert 'dishes_count' in response.json()


# 6
def test_get_none_menu():
    # Получение несуществующего меню
    response = client.get(f"{MENUS_URL}/0")
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


# 7
def test_update_menu():
    # Обновление указанного меню
    response = client.patch(f"{MENUS_URL}/{MY_MENU_1.get('id')}",
                            json=MY_MENU_2)
    assert response.status_code == 200
    assert response.json().get('id') == MY_MENU_1.get('id')
    assert response.json().get('title') == MY_MENU_2.get('title')
    assert response.json().get('description') == MY_MENU_2.get('description')
    assert 'submenus_count' in response.json()
    assert 'dishes_count' in response.json()


# 8
def test_update_none_menu():
    # Обновление несуществующего меню
    response = client.patch(f"{MENUS_URL}/0",
                            json=MY_MENU_2)
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}


# 9
def test_get_updated_menu():
    # Получение обновленного меню
    response = client.get(f"{MENUS_URL}/{MY_MENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json().get('id') == MY_MENU_1.get('id')
    assert response.json().get('title') == MY_MENU_2.get('title')
    assert response.json().get('description') == MY_MENU_2.get('description')
    assert 'submenus_count' in response.json()
    assert 'dishes_count' in response.json()


# 10
def test_delete_menu():
    # Удаление указанного меню
    response = client.delete(f"{MENUS_URL}/{MY_MENU_1.get('id')}")
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


# 11
def test_delete_none_menu():
    # Удаление несуществующего меню
    response = client.delete(f"{MENUS_URL}/0")
    assert response.status_code == 404


# 12
def test_final_get_menus():
    # Получение пустого списка меню
    response = client.get(MENUS_URL)
    assert response.status_code == 200
    assert response.json() == []


# 13
def test_final_get_none_menu():
    # Получение уже удаленного меню
    response = client.get(f"{MENUS_URL}/{MY_MENU_1.get('id')}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}
