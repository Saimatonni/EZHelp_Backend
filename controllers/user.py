from bson import ObjectId
from config.db import db
from models.user import User
from schemas.user import serializeDict, serializeList

def find_all_users():
    return serializeList(db.get_collection("user").find())

def create_user(user: User):
    db.get_collection("user").insert_one(dict(user))
    return serializeList(db.get_collection("user").find())

def update_user(id, user: User):
    db.get_collection("user").find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)}
    )
    return serializeDict(db.get_collection("user").find_one({"_id": ObjectId(id)}))

def delete_user(id):
    return serializeDict(db.get_collection("user").find_one_and_delete({"_id": ObjectId(id)}))