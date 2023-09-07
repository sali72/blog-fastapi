from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from models import User
from database import db


router = APIRouter()

@router.post("/users/")
async def create_user(user: User):
    result = db.users.insert_one(user.dict())
    return JSONResponse(status_code=201, content={"message": "User created successfully", "id": str(result.inserted_id)})


@router.get("/users/{user_id}")
async def read_user(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return JSONResponse(status_code=200, content=user)
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/users/")
async def read_users():
    users = []
    for user in db.users.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    if users == []:
        raise HTTPException(status_code=404, detail="There are no users")
    else:
        return JSONResponse(status_code=200, content=users)

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
    if result.modified_count == 1:
        return JSONResponse(status_code=200, content={"message": "User updated successfully"})
    else:
        raise HTTPException(status_code=404, detail="User post not found")

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    result = db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return JSONResponse(status_code=200, content={"message": "User deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="User not found")


