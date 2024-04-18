from fastapi import APIRouter
from controllers.user import (
    find_all_users,
    create_user,
    update_user,
    delete_user,
)
from models.user import User

user = APIRouter()

@user.get('/')
async def get_all_users():
    return find_all_users()

@user.post('/')
async def post_user(user: User):
    return create_user(user)

@user.put('/{id}')
async def put_user(id, user: User):
    return update_user(id, user)

@user.delete('/{id}')
async def delete_user_route(id):
    return delete_user(id)
