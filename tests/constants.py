import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = f"http://{os.getenv('HOST')}:8000/api/v1"  # noqa: E231

MY_MENU_1 = {
    'title': 'My menu 1',
    'description': 'My menu description 1'
}

MY_MENU_2 = {
    'title': 'My menu 2',
    'description': 'My menu description 2'
}

MY_SUBMENU_1 = {
    'title': 'My submenu 1',
    'description': 'My submenu description 1'
}

MY_SUBMENU_2 = {
    'title': 'My submenu 2',
    'description': 'My submenu description 2'
}

MY_DISH_1 = {
    'title': 'My dish 1',
    'description': 'My dish description 1',
    'price': '12.50'
}

MY_DISH_2 = {
    'title': 'My dish 2',
    'description': 'My dish description 2',
    'price': '212.55'
}
