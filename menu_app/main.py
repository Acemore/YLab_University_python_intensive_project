from uuid import UUID

from fastapi import BackgroundTasks, Depends, FastAPI, status
from fastapi.responses import PlainTextResponse
from menu_app.database import get_db  # , init_models, engine

# from menu_app.models import dish as dish_model
# from menu_app.models import menu as menu_model
# from menu_app.models import submenu as submenu_model
from menu_app.restaurant_export import restaurant_menu_export
from menu_app.restaurant_repo import RestaurantRepository
from menu_app.restaurant_service import RestaurantService
from menu_app.schemas import dish as dish_schema
from menu_app.schemas import menu as menu_schema
from menu_app.schemas import submenu as submenu_schema

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

# init_models()
# dish_model.Base.metadata.create_all(engine)
# menu_model.Base.metadata.create_all(engine)
# submenu_model.Base.metadata.create_all(engine)

app: FastAPI = FastAPI()


# def get_db() -> Session:
#     db = async_session()
#     try:
#         yield db
#     finally:
#         db.close()


def get_repo(db: AsyncSession = Depends(get_db)) -> RestaurantRepository:
    return RestaurantRepository(db)


def get_service(
    bg_tasks: BackgroundTasks,
    repo: RestaurantRepository = Depends(get_repo),
) -> RestaurantService:
    return RestaurantService(repo, bg_tasks)


@app.get('/api/v1/menus')
async def read_menus(
    svc: RestaurantService = Depends(get_service),
) -> list[menu_schema.Menu]:
    return await svc.read_menus()


@app.get('/api/v1/menus/{menu_id}/submenus')
async def read_submenus(
    menu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> list[submenu_schema.Submenu]:
    return await svc.read_submenus(menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
async def read_dishes(
    menu_id: UUID,
    submenu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> list[dish_schema.Dish]:
    return await svc.read_dishes(menu_id, submenu_id)


@app.get('/api/v1/menus/{menu_id}')
async def read_menu(
    menu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> menu_schema.Menu:
    return await svc.read_menu(menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def read_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> submenu_schema.Submenu:
    return await svc.read_submenu(menu_id, submenu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def read_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> dish_schema.Dish:
    return await svc.read_dish(menu_id, submenu_id, dish_id)


@app.post('/api/v1/menus', status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu: menu_schema.MenuCreate,
    svc: RestaurantService = Depends(get_service),
) -> menu_schema.Menu:
    return await svc.create_menu(menu)


@app.post(
    '/api/v1/menus/{menu_id}/submenus',
    status_code=status.HTTP_201_CREATED,
)
async def create_submenu(
    submenu: submenu_schema.SubmenuCreate,
    menu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> submenu_schema.Submenu:
    return await svc.create_submenu(menu_id, submenu)


@app.post(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    status_code=status.HTTP_201_CREATED,
)
async def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish: dish_schema.DishCreate,
    svc: RestaurantService = Depends(get_service),
) -> dish_schema.Dish:
    return await svc.create_dish(menu_id, submenu_id, dish)


@app.patch('/api/v1/menus/{menu_id}')
async def update_menu(
    menu_id: UUID,
    menu_update: menu_schema.MenuUpdate,
    svc: RestaurantService = Depends(get_service),
) -> menu_schema.Menu:
    return await svc.update_menu(menu_id, menu_update)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def update_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_update: submenu_schema.SubmenuUpdate,
    svc: RestaurantService = Depends(get_service),
) -> submenu_schema.Submenu:
    return await svc.update_submenu(menu_id, submenu_id, submenu_update)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def update_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_update: dish_schema.DishUpdate,
    svc: RestaurantService = Depends(get_service),
) -> dish_schema.Dish:
    return await svc.update_dish(menu_id, submenu_id, dish_id, dish_update)


@app.delete('/api/v1/menus/{menu_id}')
async def delete_menu(
    menu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> dict[str, bool]:
    return await svc.delete_menu(menu_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> dict[str, bool]:
    return await svc.delete_submenu(menu_id, submenu_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    svc: RestaurantService = Depends(get_service),
) -> dict[str, bool]:
    return await svc.delete_dish(menu_id, submenu_id, dish_id)


@app.get('/api/v1/export', response_class=PlainTextResponse)
async def export(db: AsyncSession = Depends(get_db)) -> str:
    return await restaurant_menu_export(db)
