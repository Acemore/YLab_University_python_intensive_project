import requests

from menu_app_tests import APP_ROOT_URL

dish_1_id = None
dish_2_id = None
menu_id = None
submenu_id = None


def test_create_menu(menu_data_to_create):
    created_menu_resp = requests.post(APP_ROOT_URL, json=menu_data_to_create)
    created_menu = created_menu_resp.json()

    global menu_id
    menu_id = created_menu['id']

    assert created_menu_resp.status_code == 201
    assert created_menu['title'] == menu_data_to_create['title']
    assert created_menu['description'] == menu_data_to_create['description']


def test_create_submenu(submenu_data_to_create):
    created_submenu_resp = requests.post(
        f'{APP_ROOT_URL}/{menu_id}/submenus',
        json=submenu_data_to_create,
    )
    created_submenu = created_submenu_resp.json()

    global submenu_id
    submenu_id = created_submenu['id']

    assert created_submenu_resp.status_code == 201
    assert created_submenu['title'] == submenu_data_to_create['title']
    assert created_submenu['description'] == submenu_data_to_create['description']


def test_create_dish_1(dish_1_data_to_create):
    created_dish_1_resp = requests.post(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes',
        json=dish_1_data_to_create,
    )
    created_dish_1 = created_dish_1_resp.json()

    global dish_1_id
    dish_1_id = created_dish_1['id']

    assert created_dish_1_resp.status_code == 201
    assert created_dish_1['title'] == dish_1_data_to_create['title']
    assert created_dish_1['description'] == dish_1_data_to_create['description']
    assert created_dish_1['price'] == str(dish_1_data_to_create['price'])


def test_create_dish_2(dish_2_data_to_create):
    created_dish_2_resp = requests.post(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes',
        json=dish_2_data_to_create,
    )
    created_dish_2 = created_dish_2_resp.json()

    global dish_2_id
    dish_2_id = created_dish_2['id']

    assert created_dish_2_resp.status_code == 201
    assert created_dish_2['title'] == dish_2_data_to_create['title']
    assert (
        created_dish_2['description'] == dish_2_data_to_create['description']
    )
    assert created_dish_2['price'] == str(dish_2_data_to_create['price'])


def test_read_menu(menu_data_to_create):
    menu_resp = requests.get(f'{APP_ROOT_URL}/{menu_id}')
    menu = menu_resp.json()

    assert menu_resp.status_code == 200
    assert menu['id'] == menu_id
    assert menu['title'] == menu_data_to_create['title']
    assert menu['description'] == menu_data_to_create['description']
    assert menu['submenus_count'] == 1
    assert menu['dishes_count'] == 2


def test_read_submenu(submenu_data_to_create):
    submenu_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}'
    )
    submenu = submenu_resp.json()

    assert submenu_resp.status_code == 200
    assert submenu['id'] == submenu_id
    assert submenu['title'] == submenu_data_to_create['title']
    assert submenu['description'] == submenu_data_to_create['description']
    assert submenu['dishes_count'] == 2


def test_delete_submenu():
    resp = requests.delete(f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}')

    assert resp.status_code == 200
    assert resp.json() == {'ok': True}


def test_read_submenus_list_after_deleting():
    submenus_list_resp = requests.get(f'{APP_ROOT_URL}/{menu_id}/submenus')

    assert submenus_list_resp.status_code == 200
    assert submenus_list_resp.json() == []


def test_read_dishes_list_after_deleting():
    dishes_list_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes'
    )

    assert dishes_list_resp.status_code == 200
    assert dishes_list_resp.json() == []


def test_read_updated_menu(menu_data_to_create):
    menu_resp = requests.get(f'{APP_ROOT_URL}/{menu_id}')
    menu = menu_resp.json()

    assert menu_resp.status_code == 200
    assert menu['id'] == menu_id
    assert menu['title'] == menu_data_to_create['title']
    assert menu['description'] == menu_data_to_create['description']
    assert menu['submenus_count'] == 0
    assert menu['dishes_count'] == 0


def test_delete_menu():
    resp = requests.delete(f'{APP_ROOT_URL}/{menu_id}')

    assert resp.status_code == 200
    assert resp.json() == {'ok': True}


def test_read_menus_list_after_deleting():
    menus_list_resp = requests.get(APP_ROOT_URL)

    assert menus_list_resp.status_code == 200
    assert menus_list_resp.json() == []
