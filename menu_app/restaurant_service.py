from typing import List
from pydantic import parse_obj_as
from uuid import UUID

from .restaurant_repo import RestaurantRepository
from .schemas.menu import Menu as MenuSchema


class RestaurantService:
    def __init__(self, repo: RestaurantRepository):
        self.repo = repo

    def read_menus(self):
        menu_model_list = self.repo.read_menus()
        return parse_obj_as(List[MenuSchema], menu_model_list)
    
    def read_menu(self, menu_id: UUID):
        menu_model = self.repo.read_menu(menu_id)
        return parse_obj_as(MenuSchema, menu_model)
