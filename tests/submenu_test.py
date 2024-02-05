from fastapi.testclient import TestClient

from main import app

from .constants import BASE_URL, MY_MENU_1, MY_SUBMENU_1, MY_SUBMENU_2

client = TestClient(app)

MENU_ID = None
SUBMENU_ID = None
MENUS_URL = f"{BASE_URL}/menus"
SUBMENUS_URL = f"{BASE_URL}/menus/{MENU_ID}/submenus"


# 1
def test_create_menu():
    # Создание нового меню
    response = client.post(app.url_path_for('menus_url'), json=MY_MENU_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('submenus_count') == 0
    assert response.json().get('dishes_count') == 0
    assert MY_MENU_1['title'] == response.json().get('title')
    assert MY_MENU_1['description'] == response.json().get('description')

    global MENU_ID
    MENU_ID = response.json().get('id')


# 2
def test_initial_get_submenus():
    # Получение пустого списка подменю
    response = client.get(app.url_path_for('submenus_url', menu_id=MENU_ID))
    assert response.status_code == 200
    assert response.json() == []


# 3
def test_create_submenu():
    # Создание нового подменю
    response = client.post(app.url_path_for('submenus_url', menu_id=MENU_ID), json=MY_SUBMENU_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('dishes_count') == 0
    assert MY_SUBMENU_1['title'] == response.json().get('title')
    assert MY_SUBMENU_1['description'] == response.json().get('description')

    global SUBMENU_ID
    SUBMENU_ID = response.json().get('id')


# 4
def test_duplicate_submenu():
    # Создание уже существующего подменю
    response = client.post(app.url_path_for('submenus_url', menu_id=MENU_ID), json=MY_SUBMENU_1)
    assert response.status_code == 409


# 5
def test_get_submenus():
    # Получение списка подменю
    response = client.get(app.url_path_for('submenus_url', menu_id=MENU_ID))
    assert response.status_code == 200
    assert len(response.json()) > 0


# 6
def test_get_submenu():
    # Получение указанного подменю
    response = client.get(app.url_path_for('submenu_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID))
    assert response.status_code == 200
    assert response.json().get('id') == SUBMENU_ID
    assert response.json().get('title') == MY_SUBMENU_1.get('title')
    assert response.json().get('description') == MY_SUBMENU_1.get('description')
    assert 'dishes_count' in response.json()


# 7
def test_get_none_submenu():
    # Получение указанного подменю
    response = client.get(app.url_path_for('submenu_url', menu_id=MENU_ID, submenu_id=0))
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


# 8
def test_update_submenu():
    # Обновление указанного подменю
    response = client.patch(app.url_path_for('submenu_url', menu_id=MENU_ID,
                                             submenu_id=SUBMENU_ID),
                            json=MY_SUBMENU_2)
    assert response.status_code == 200
    assert response.json().get('id') == SUBMENU_ID
    assert response.json().get('title') == MY_SUBMENU_2.get('title')
    assert response.json().get('description') == MY_SUBMENU_2.get('description')
    assert 'dishes_count' in response.json()


# 9
def test_update_none_submenu():
    # Обновление несуществующего подменю
    response = client.patch(f"{SUBMENUS_URL}/0",
                            json=MY_SUBMENU_2)
    # response = client.patch(app.url_path_for("submenu_url", menu_id=MENU_ID, submenu_id=0,
    #                         json=MY_SUBMENU_2))
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


# 10
def test_get_updated_submenu():
    # Получение обновленного подменю
    # response = client.get(f"{SUBMENUS_URL}/{MY_SUBMENU_1.get('id')}")
    response = client.get(app.url_path_for('submenu_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID))
    assert response.status_code == 200
    assert response.json().get('id') == SUBMENU_ID
    assert response.json().get('title') == MY_SUBMENU_2.get('title')
    assert response.json().get('description') == MY_SUBMENU_2.get('description')
    assert 'dishes_count' in response.json()


# 11
def test_delete_submenu():
    # Удаление указанного подменю
    response = client.delete(app.url_path_for('submenu_url', menu_id=MENU_ID,
                                              submenu_id=SUBMENU_ID))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The submenu has been deleted'}


# 12
def test_delete_none_submenu():
    # Удаление несуществующего подменю
    response = client.delete(app.url_path_for('submenu_url', menu_id=MENU_ID, submenu_id=0))
    assert response.status_code == 404


# 13
def test_final_get_submenus():
    # Получение пустого списка подменю
    response = client.get(app.url_path_for('submenus_url', menu_id=MENU_ID))
    assert response.status_code == 200
    assert response.json() == []


# 14
def test_final_get_none_submenu():
    # Получение указанного подменю
    response = client.get(app.url_path_for('submenu_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID))
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


# 15
def test_delete_menu():
    # Удаление указанного меню
    response = client.delete(app.url_path_for('menu_url', menu_id=MENU_ID))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


# 16
def test_final_get_menus():
    # Получение пустого списка меню
    response = client.get(app.url_path_for('menus_url'))
    assert response.status_code == 200
    assert response.json() == []
