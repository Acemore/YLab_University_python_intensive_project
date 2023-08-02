import pytest

from .file_parser import get_file_content, parse_json
from menu_app_tests import (
    DISH_1_DATA_TO_CREATE_FILE_PATH,
    DISH_1_DATA_TO_UPDATE_FILE_PATH,
    DISH_2_DATA_TO_CREATE_FILE_PATH,
    DISH_2_DATA_TO_UPDATE_FILE_PATH,
    MENU_DATA_TO_CREATE_FILE_PATH,
    MENU_DATA_TO_UPDATE_FILE_PATH,
    SUBMENU_DATA_TO_CREATE_FILE_PATH,
    SUBMENU_DATA_TO_UPDATE_FILE_PATH,
)


@pytest.fixture(scope='package')
def dish_1_data_to_create():
    return parse_json(get_file_content(DISH_1_DATA_TO_CREATE_FILE_PATH))


@pytest.fixture(scope='package')
def dish_1_data_to_update():
    return parse_json(get_file_content(DISH_1_DATA_TO_UPDATE_FILE_PATH))


@pytest.fixture(scope='package')
def dish_2_data_to_create():
    return parse_json(get_file_content(DISH_2_DATA_TO_CREATE_FILE_PATH))


@pytest.fixture(scope='package')
def dish_2_data_to_update():
    return parse_json(get_file_content(DISH_2_DATA_TO_UPDATE_FILE_PATH))


@pytest.fixture(scope='package')
def menu_data_to_create():
    return parse_json(get_file_content(MENU_DATA_TO_CREATE_FILE_PATH))


@pytest.fixture(scope='package')
def menu_data_to_update():
    return parse_json(get_file_content(MENU_DATA_TO_UPDATE_FILE_PATH))


@pytest.fixture(scope='package')
def submenu_data_to_create():
    return parse_json(get_file_content(SUBMENU_DATA_TO_CREATE_FILE_PATH))


@pytest.fixture(scope='package')
def submenu_data_to_update():
    return parse_json(get_file_content(SUBMENU_DATA_TO_UPDATE_FILE_PATH))
