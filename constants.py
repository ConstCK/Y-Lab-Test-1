import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = f"http://{os.getenv('HOST')}:8000/api/v1"

MY_MENU = {
    'title': 'My menu 1',
    'description': 'My menu description 1'
}

MY_SUBMENU = {
    'title': 'My submenu 1',
    'description': 'My submenu description 1'
}

MY_DISH = {
    'title': 'My dish 1',
    'description': 'My dish description 1',
    'price': '12.50'
}