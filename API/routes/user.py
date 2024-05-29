from fastapi import APIRouter
from models.user import User
from config.db import conn
from bson import ObjectId

from schemas.user import userEntity, usersEntity


user = APIRouter()


@user.get('/')
async def findalluser():
    return usersEntity(conn.local.user.find())


@user.get('/{id}')
async def getuser(id: str):
    try:
        user = conn.local.user.find_one({'_id': ObjectId(id)})
        if not user:
            return {"message": "User not found"}
        return userEntity(user)
    except Exception as e:
        return {"message": f"Error fetching user: {e}"}


@user.post('/')
async def createuser(user: User):
    try:
        inserted_id = conn.local.user.insert_one(user.dict()).inserted_id
        return userEntity(conn.local.user.find_one({'_id': inserted_id}))
    except Exception as e:
        return {"message": f"Error creating user: {e}"}


@user.put('/{id}')
async def updateuser(id: str, user: User):
    try:
        update_result = conn.local.user.find_one_and_update(
            {'_id': ObjectId(id)}, {'$set': user.dict()}
        )
        if not update_result:
            return {"message": "User not found"}
        return userEntity(conn.local.user.find_one({'_id': ObjectId(id)}))
    except Exception as e:
        return {"message": f"Error updating user: {e}"}


@user.delete('/{id}')
async def deleteuser(id: str):
    try:
        delete_result = conn.local.user.find_one_and_delete({'_id': ObjectId(id)})
        if not delete_result:
            return {"message": "User not found"}
        return {"message": "User deleted successfully"}
    except Exception as e:
        return {"message": f"Error deleting user: {e}"}
