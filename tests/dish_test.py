from fastapi.testclient import TestClient

from main import app

from .constants import BASE_URL, MY_DISH_1, MY_DISH_2, MY_MENU_1, MY_SUBMENU_1

client = TestClient(app)

MENUS_URL = f"{BASE_URL}/menus"
SUBMENUS_URL = ''
SUBMENUS_URL = f"{BASE_URL}/menus/{MY_MENU_1.get('id')}/submenus"
DISHES_URL = f"{BASE_URL}/menus/{MY_MENU_1.get('id')}/submenus/{MY_SUBMENU_1.get('id')}/dishes"
DISHES_URL = ''
MENU_ID = None
SUBMENU_ID = None
DISH_ID = None


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


# 3
def test_initial_get_dishes():
    # Получение пустого списка блюд
    response = client.get(app.url_path_for('dishes_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID))
    assert response.status_code == 200
    assert response.json() == []


# 4
def test_create_dish():
    # Создание нового блюда
    response = client.post(app.url_path_for('dishes_url', menu_id=MENU_ID,
                                            submenu_id=SUBMENU_ID), json=MY_DISH_1)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert MY_DISH_1['title'] == response.json().get('title')
    assert MY_DISH_1['description'] == response.json().get('description')
    assert MY_DISH_1['price'] == response.json().get('price')

    global DISH_ID
    DISH_ID = response.json().get('id')


# 5
def test_duplicate_dish():
    # Создание уже существующего блюда
    response = client.post(app.url_path_for('dishes_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID), json=MY_DISH_1)
    assert response.status_code == 409


# 6
def test_get_dishes():
    # Получение списка подменю
    response = client.get(app.url_path_for('dishes_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID))
    assert response.status_code == 200
    assert len(response.json()) > 0


# 7
def test_get_dish():
    # Получение указанного блюда
    response = client.get(app.url_path_for('dish_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID, dish_id=DISH_ID))
    assert response.status_code == 200
    assert response.json().get('id') == DISH_ID
    assert response.json().get('title') == MY_DISH_1.get('title')
    assert response.json().get('description') == MY_DISH_1.get('description')
    assert response.json().get('price') == MY_DISH_1.get('price')


# 8
def test_get_none_dish():
    # Получение указанного блюда
    response = client.get(app.url_path_for('dish_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID,
                                           dish_id=0))
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


# 9
def test_update_dish():
    # Обновление указанного блюда
    response = client.patch(app.url_path_for('dish_url', menu_id=MENU_ID,
                                             submenu_id=SUBMENU_ID, dish_id=DISH_ID),
                            json=MY_DISH_2)
    assert response.status_code == 200
    assert response.json().get('id') == DISH_ID
    assert response.json().get('title') == MY_DISH_2.get('title')
    assert response.json().get('description') == MY_DISH_2.get('description')
    assert response.json().get('price') == MY_DISH_2.get('price')


# 10
def test_update_none_dish():
    # Обновление несуществующего блюда
    # response = client.patch(f"{DISHES_URL}/0",
    #                         json=MY_DISH_2)
    response = client.patch(app.url_path_for('dish_url', menu_id=MENU_ID,
                                             submenu_id=SUBMENU_ID, dish_id=0),
                            json=MY_DISH_2)
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


# 11
def test_get_updated_dish():
    # Получение обновленного блюда
    response = client.get(app.url_path_for('dish_url', menu_id=MENU_ID,
                                           submenu_id=SUBMENU_ID, dish_id=DISH_ID))
    assert response.status_code == 200
    assert response.json().get('id') == DISH_ID
    assert response.json().get('title') == MY_DISH_2.get('title')
    assert response.json().get('description') == MY_DISH_2.get('description')
    assert response.json().get('price') == MY_DISH_2.get('price')


# 12
def test_delete_dish():
    # Удаление указанного блюда
    response = client.delete(app.url_path_for('dish_url', menu_id=MENU_ID,
                                              submenu_id=SUBMENU_ID, dish_id=DISH_ID))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The dish has been deleted'}


# 13
def test_delete_none_dish():
    # Удаление несуществующего блюда
    response = client.delete(app.url_path_for('dish_url', menu_id=MENU_ID,
                                              submenu_id=SUBMENU_ID, dish_id=0))
    assert response.status_code == 404


# 14
def test_final_get_dishes():
    # Получение пустого списка блюд
    response = client.get(app.url_path_for('dishes_url', menu_id=MENU_ID,
                                           submenu_id=SUBMENU_ID))
    assert response.status_code == 200
    assert response.json() == []


# 15
def test_final_get_none_dish():
    # Получение удаленного блюда
    response = client.get(app.url_path_for('dish_url', menu_id=MENU_ID,
                                           submenu_id=SUBMENU_ID, dish_id=DISH_ID))
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


# 16
def test_delete_submenu():
    # Удаление указанного подменю
    response = client.delete(app.url_path_for('submenu_url', menu_id=MENU_ID, submenu_id=SUBMENU_ID))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The submenu has been deleted'}


# 17
def test_final_get_submenus():
    # Получение пустого списка подменю
    response = client.get(app.url_path_for('submenus_url', menu_id=MENU_ID))
    assert response.status_code == 200
    assert response.json() == []


# 17
def test_delete_menu():
    # Удаление указанного меню
    response = client.delete(app.url_path_for('menu_url', menu_id=MENU_ID))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


# 18
def test_final_get_menus():
    # Получение пустого списка меню
    response = client.get(app.url_path_for('menus_url'))
    assert response.status_code == 200
    assert response.json() == []
