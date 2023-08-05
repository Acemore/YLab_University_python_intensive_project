import json

import requests
from menu_app_tests import APP_ROOT_URL

menu_id = None


def test_read_empty_menus_list():
    empty_menus_list_resp = requests.get(APP_ROOT_URL)

    assert empty_menus_list_resp.status_code == 200
    assert empty_menus_list_resp.json() == []


def test_create_menu(menu_data_to_create):
    created_menu_resp = requests.post(APP_ROOT_URL, json=menu_data_to_create)
    created_menu = created_menu_resp.json()

    global menu_id
    menu_id = created_menu['id']

    assert created_menu_resp.status_code == 201
    assert created_menu['title'] == menu_data_to_create['title']
    assert created_menu['description'] == menu_data_to_create['description']


def test_read_menus_list():
    menus_list_resp = requests.get(APP_ROOT_URL)

    assert menus_list_resp.status_code == 200
    assert menus_list_resp.json() != json.dumps([])


def test_read_menu(menu_data_to_create):
    menu_resp = requests.get(f'{APP_ROOT_URL}/{menu_id}')
    menu = menu_resp.json()

    assert menu_resp.status_code == 200
    assert menu['id'] == menu_id
    assert menu['title'] == menu_data_to_create['title']
    assert menu['description'] == menu_data_to_create['description']


def test_update_menu(menu_data_to_update):
    not_updated_menu_resp = requests.get(f'{APP_ROOT_URL}/{menu_id}')
    not_updated_menu = not_updated_menu_resp.json()

    assert not_updated_menu['id'] == menu_id
    assert not_updated_menu['title'] != menu_data_to_update['title']
    assert not_updated_menu['description'] != menu_data_to_update['description']

    updated_menu_resp = requests.patch(
        f'{APP_ROOT_URL}/{menu_id}',
        json=menu_data_to_update,
    )
    updated_menu = updated_menu_resp.json()

    assert updated_menu_resp.status_code == 200
    assert updated_menu['id'] == menu_id
    assert updated_menu['title'] == menu_data_to_update['title']
    assert updated_menu['description'] == menu_data_to_update['description']


def test_read_updated_menu(menu_data_to_update):
    retrieved_updated_menu_resp = requests.get(f'{APP_ROOT_URL}/{menu_id}')
    retrieved_updated_menu = retrieved_updated_menu_resp.json()

    assert retrieved_updated_menu_resp.status_code == 200
    assert retrieved_updated_menu['id'] == menu_id
    assert retrieved_updated_menu['title'] == menu_data_to_update['title']
    assert retrieved_updated_menu['description'] == menu_data_to_update['description']


def test_delete_menu():
    resp = requests.delete(f'{APP_ROOT_URL}/{menu_id}')

    assert resp.status_code == 200
    assert resp.json() == {'ok': True}


def test_read_menus_list_after_deleting():
    menus_list_resp = requests.get(APP_ROOT_URL)

    assert menus_list_resp.status_code == 200
    assert menus_list_resp.json() == []


def test_read_deleted_menu():
    resp = requests.get(f'{APP_ROOT_URL}/{menu_id}')

    assert resp.status_code == 404
    assert resp.json()['detail'] == 'menu not found'
