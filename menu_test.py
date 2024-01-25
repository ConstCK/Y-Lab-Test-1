from fastapi.testclient import TestClient

from constants import BASE_URL, MY_MENU
from main import app

client = TestClient(app)

MENUS_URL = f"{BASE_URL}/menus"


def test_initial_get_menus():
    # Проверка пустого списка меню
    response = client.get(MENUS_URL)
    assert response.status_code == 200
    assert response.json() == []


def test_create_menu():
    # Создание нового меню
    response = client.post(MENUS_URL, json=MY_MENU)
    assert response.status_code == 201
