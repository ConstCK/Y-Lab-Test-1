from fastapi.testclient import TestClient

from main import app

from .constants import MY_DISH_1, MY_DISH_2, MY_MENU_1, MY_SUBMENU_1

client = TestClient(app)

MENU_ID = None
SUBMENU_ID = None
DISH_1_ID = None
DISH_2_ID = None


# 1
def test_create_menu():
    # Создание нового меню
    response = client.post(app.url_path_for('create_menu_url'), json=MY_MENU_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('submenus_count') == 0
    assert response.json().get('dishes_count') == 0
    assert MY_MENU_1['title'] == response.json().get('title')
    assert MY_MENU_1['description'] == response.json().get('description')

    global MENU_ID
    MENU_ID = response.json().get('id')


# 2
def test_create_submenu():
    # Создание нового подменю
    response = client.post(app.url_path_for('create_submenu_url', menu_id=MENU_ID), json=MY_SUBMENU_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json().get('dishes_count') == 0
    assert MY_SUBMENU_1['title'] == response.json().get('title')
    assert MY_SUBMENU_1['description'] == response.json().get('description')

    global SUBMENU_ID
    SUBMENU_ID = response.json().get('id')


# 3
def test_create_first_dish():
    # Создание первого блюда
    response = client.post(app.url_path_for('create_dish_url', menu_id=MENU_ID,
                                            submenu_id=SUBMENU_ID), json=MY_DISH_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert MY_DISH_1['title'] == response.json().get('title')
    assert MY_DISH_1['description'] == response.json().get('description')
    assert MY_DISH_1['price'] == response.json().get('price')

    MY_DISH_1['id'] = response.json().get('id')


# 4
def test_create_second_dish():
    # Создание второго блюда
    response = client.post(app.url_path_for('create_dish_url', menu_id=MENU_ID,
                                            submenu_id=SUBMENU_ID), json=MY_DISH_2)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert MY_DISH_2['title'] == response.json().get('title')
    assert MY_DISH_2['description'] == response.json().get('description')
    assert MY_DISH_2['price'] == response.json().get('price')

    global DISH_2_ID
    DISH_2_ID = response.json().get('id')


# 5
def test_get_menu():
    # Получение указанного меню
    response = client.get(app.url_path_for('get_menu_url', menu_id=MENU_ID))
    assert response.status_code == 200
    assert response.json().get('id') == MENU_ID
    assert response.json().get('title') == MY_MENU_1.get('title')
    assert response.json().get('description') == MY_MENU_1.get('description')
    assert response.json().get('submenus_count') == 1
    assert response.json().get('dishes_count') == 2


# 6
def test_get_submenu():
    # Получение указанного подменю
    response = client.get(app.url_path_for('get_submenu_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID))
    assert response.status_code == 200
    assert response.json().get('id') == SUBMENU_ID
    assert response.json().get('title') == MY_SUBMENU_1.get('title')
    assert response.json().get('description') == MY_SUBMENU_1.get('description')
    assert response.json().get('dishes_count') == 2


# 7
def test_delete_submenu():
    # Удаление указанного подменю
    response = client.delete(app.url_path_for('delete_submenu_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The submenu has been deleted'}


# 8
def test_final_get_submenus():
    # Получение пустого списка подменю
    response = client.get(app.url_path_for('get_submenus_url', menu_id=MENU_ID))
    assert response.status_code == 200
    assert response.json() == []


# 9
def test_final_get_dishes():
    # Получение пустого списка блюд
    response = client.get(app.url_path_for('get_dishes_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID))
    assert response.status_code == 200
    assert response.json() == []


# 10
def test_final_get_menu():
    # Получение указанного меню
    response = client.get(app.url_path_for('get_menu_url', menu_id=MENU_ID))
    assert response.status_code == 200
    assert response.json().get('id') == MENU_ID
    assert response.json().get('title') == MY_MENU_1.get('title')
    assert response.json().get('description') == MY_MENU_1.get('description')
    assert response.json().get('submenus_count') == 0
    assert response.json().get('dishes_count') == 0


# 11
def test_delete_menu():
    # Удаление указанного меню
    response = client.delete(app.url_path_for('delete_menu_url', menu_id=MENU_ID))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


# 12
def test_final_get_menus():
    # Получение пустого списка меню
    response = client.get(app.url_path_for('get_menus_url'))
    assert response.status_code == 200
    assert response.json() == []
