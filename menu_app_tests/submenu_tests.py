import requests

from menu_app_tests import APP_ROOT_URL

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


def test_read_empty_submenus_list():
    empty_submenus_list_resp = requests.get(f'{APP_ROOT_URL}/{menu_id}/submenus')

    assert empty_submenus_list_resp.status_code == 200
    assert empty_submenus_list_resp.json() == []


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


def test_read_submenus_list():
    submenus_list_resp = requests.get(f'{APP_ROOT_URL}/{menu_id}/submenus')

    assert submenus_list_resp.status_code == 200
    assert submenus_list_resp.json() != []


def test_read_submenu(submenu_data_to_create):
    submenu_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}'
    )
    submenu = submenu_resp.json()

    assert submenu_resp.status_code == 200
    assert submenu['id'] == submenu_id
    assert submenu['title'] == submenu_data_to_create['title']
    assert submenu['description'] == submenu_data_to_create['description']


def test_update_submenu(submenu_data_to_update):
    not_updated_submenu_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}'
    )
    not_updated_submenu = not_updated_submenu_resp.json()

    assert not_updated_submenu['id'] == submenu_id
    assert not_updated_submenu['title'] != submenu_data_to_update['title']
    assert not_updated_submenu['description'] != submenu_data_to_update['title']

    updated_submenu_resp = requests.patch(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}',
        json=submenu_data_to_update,
    )
    updated_submenu = updated_submenu_resp.json()

    assert updated_submenu_resp.status_code == 200
    assert updated_submenu['id'] == submenu_id
    assert updated_submenu['title'] == submenu_data_to_update['title']
    assert updated_submenu['description'] == submenu_data_to_update['description']


def test_read_updated_menu(submenu_data_to_update):
    retrieved_updated_submenu_resp = requests.get(
        f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}'
    )
    retrieved_updated_submenu = retrieved_updated_submenu_resp.json()

    assert retrieved_updated_submenu_resp.status_code == 200
    assert retrieved_updated_submenu['id'] == submenu_id
    assert (
        retrieved_updated_submenu['title'] == submenu_data_to_update['title']
    )
    assert retrieved_updated_submenu['description'] == (
        submenu_data_to_update['description']
    )


def test_delete_submenu():
    resp = requests.delete(f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}')

    assert resp.status_code == 200
    assert resp.json() == {'ok': True}


def test_read_submenus_list_after_deleting():
    submenus_list_resp = requests.get(f'{APP_ROOT_URL}/{menu_id}/submenus/')

    assert submenus_list_resp.status_code == 200
    assert submenus_list_resp.json() == []


def test_read_deleted_submenu():
    resp = requests.get(f'{APP_ROOT_URL}/{menu_id}/submenus/{submenu_id}')

    assert resp.status_code == 404
    assert resp.json()['detail'] == 'submenu not found'


def test_delete_menu():
    resp = requests.delete(f'{APP_ROOT_URL}/{menu_id}')

    assert resp.status_code == 200
    assert resp.json() == {'ok': True}


def test_read_menus_list_after_deleting():
    menus_list_resp = requests.get(APP_ROOT_URL)

    assert menus_list_resp.status_code == 200
    assert menus_list_resp.json() == []
