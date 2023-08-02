import requests

from menu_app_tests import APP_ROOT_URL

dish_id = None
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
    assert created_submenu['description'] == (
        submenu_data_to_create['description']
    )


def test_read_empty_dishes_list():
    empty_dishes_list_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes'
    )

    assert empty_dishes_list_resp.status_code == 200
    assert empty_dishes_list_resp.json() == []


def test_create_dish(dish_1_data_to_create):
    created_dish_resp = requests.post(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes',
        json=dish_1_data_to_create,
    )
    created_dish = created_dish_resp.json()

    global dish_id
    dish_id = created_dish['id']

    assert created_dish_resp.status_code == 201
    assert created_dish['title'] == dish_1_data_to_create['title']
    assert created_dish['description'] == dish_1_data_to_create['description']
    assert created_dish['price'] == str(dish_1_data_to_create['price'])


def test_read_dishes_list():
    dishes_list_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes'
    )

    assert dishes_list_resp.status_code == 200
    assert dishes_list_resp.json() != []


def test_read_dish(dish_1_data_to_create):
    dish_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    dish = dish_resp.json()

    assert dish_resp.status_code == 200
    assert dish['id'] == dish_id
    assert dish['title'] == dish_1_data_to_create['title']
    assert dish['description'] == dish_1_data_to_create['description']
    assert dish['price'] == str(dish_1_data_to_create['price'])


def test_update_dish(dish_1_data_to_update):
    not_updated_dish_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    )
    not_updated_dish = not_updated_dish_resp.json()

    not_updated_dish['id'] == dish_id
    not_updated_dish['title'] != dish_1_data_to_update['title']
    not_updated_dish['description'] != dish_1_data_to_update['description']
    not_updated_dish['price'] != str(dish_1_data_to_update['price'])

    updated_dish_resp = requests.patch(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        json=dish_1_data_to_update,
    )
    updated_dish = updated_dish_resp.json()

    assert updated_dish_resp.status_code == 200
    assert updated_dish['id'] == dish_id
    assert updated_dish['title'] == dish_1_data_to_update['title']
    assert updated_dish['description'] == dish_1_data_to_update['description']
    assert updated_dish['price'] == str(dish_1_data_to_update['price'])


def test_read_updated_dish(dish_1_data_to_update):
    retrieved_updated_dish_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    retrieved_updated_dish = retrieved_updated_dish_resp.json()

    assert retrieved_updated_dish_resp.status_code == 200
    assert retrieved_updated_dish['id'] == dish_id
    assert retrieved_updated_dish['title'] == dish_1_data_to_update['title']
    assert retrieved_updated_dish['description'] == dish_1_data_to_update['description']
    assert retrieved_updated_dish['price'] == str(dish_1_data_to_update['price'])


def test_delete_dish():
    resp = requests.delete(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )

    assert resp.status_code == 200
    assert resp.json() == {'ok': True}


def test_read_dishes_list_after_deleting():
    dishes_list_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes'
    )

    assert dishes_list_resp.status_code == 200
    assert dishes_list_resp.json() == []


def test_read_deleted_dish():
    resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )

    assert resp.status_code == 404
    assert resp.json()['detail'] == 'dish not found'


def test_delete_submenu():
    resp = requests.delete(f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}')

    assert resp.status_code == 200
    assert resp.json() == {'ok': True}


def test_read_submenus_list_after_deleting():
    submenus_list_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus'
    )

    assert submenus_list_resp.status_code == 200
    assert submenus_list_resp.json() == []


def test_delete_menu():
    resp = requests.delete(f'{APP_ROOT_URL}/{menu_id}')

    assert resp.status_code == 200
    assert resp.json() == {'ok': True}


def test_read_menus_list_after_deleting():
    menus_list_resp = requests.get(APP_ROOT_URL)

    assert menus_list_resp.status_code == 200
    assert menus_list_resp.json() == []
