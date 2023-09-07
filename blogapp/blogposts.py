from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from models import BlogPost
from database import db

router = APIRouter()

@router.post("/blogposts/")
async def create_blogpost(blogpost: BlogPost):
    result = db.blogposts.insert_one(blogpost.dict())
    return JSONResponse(status_code=201, content={"message": "Post created successfully", "id": str(result.inserted_id)})

@router.get("/blogposts/{blogpost_id}")
async def read_blogpost(blogpost_id: str):
    blogpost = db.blogposts.find_one({"_id": ObjectId(blogpost_id)})
    if blogpost:
        blogpost["_id"] = str(blogpost["_id"])
        return JSONResponse(status_code=200, content=blogpost)
    else:
        raise HTTPException(status_code=404, detail="Post not found")

@router.get("/blogposts/")
async def read_blogposts():
    blogposts = []
    for post in db.blogposts.find():
        post["_id"] = str(post["_id"])
        blogposts.append(post)
    if blogposts == []:
        raise HTTPException(status_code=404, detail="There are no posts")
    else:
        return JSONResponse(status_code=200, content=blogposts)

@router.put("/blogposts/{blogpost_id}")
async def update_blogpost(blogpost_id: str, blogpost: BlogPost):
    result = db.blogposts.update_one({"_id": ObjectId(blogpost_id)}, {"$set": blogpost.dict()})
    if result.modified_count == 1:
        return JSONResponse(status_code=200, content={"message": "Post updated successfully"})
    else:
        raise HTTPException(status_code=404, detail="Blog post not found")


@router.delete("/blogposts/{blogpost_id}")
async def delete_blogpost(blogpost_id: str):
    result = db.blogposts.delete_one({"_id": ObjectId(blogpost_id)})
    if result.deleted_count == 1:
        return JSONResponse(status_code=200, content={"message": "Post deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Post not found")
