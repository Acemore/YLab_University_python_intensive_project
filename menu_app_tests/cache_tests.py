import requests
from menu_app_tests import APP_ROOT_URL


def test_cascade_delete() -> None:
    menus_url = APP_ROOT_URL
    menu_create = {
        'title': 'menu1',
        'description': ''
    }
    menu = requests.post(menus_url, json=menu_create).json()
    menu_id = menu['id']
    menu_url = f'{menus_url}/{menu_id}'

    submenus_url = f'{menu_url}/submenus'
    submenu_create = {
        'menu_id': menu_id,
        'title': 'submenu1',
        'description': ''
    }
    submenu = requests.post(submenus_url, json=submenu_create).json()
    submenu_id = submenu['id']
    submenu_url = f'{submenus_url}/{submenu_id}'

    dishes_url = f'{submenu_url}/dishes'
    dish_create = {
        'menu_id': menu_id,
        'submenu_id': submenu_id,
        'title': 'dish1',
        'description': '',
        'price': 123
    }
    dish = requests.post(dishes_url, json=dish_create).json()
    dish_id = dish['id']
    dish_url = f'{dishes_url}/{dish_id}'

    # initialize cache
    requests.get(menus_url)
    requests.get(submenus_url)
    requests.get(dishes_url)
    requests.get(menu_url)
    requests.get(submenu_url)
    requests.get(dish_url)

    requests.delete(menu_url)

    assert requests.get(menus_url).json() == []
    assert requests.get(submenus_url).json() == []
    assert requests.get(dishes_url).json() == []
    assert requests.get(submenu_url).status_code == 404
    assert requests.get(dish_url).status_code == 404
