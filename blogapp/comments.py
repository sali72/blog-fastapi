from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from models import Comment
from database import db

router = APIRouter()

@router.post("/comments/")
async def create_comment(comment: Comment):
    result = db.comments.insert_one(comment.dict())
    # Update the comment count on the associated blog post
    db.blogposts.update_one({"_id": ObjectId(comment.post_id)}, {"$inc": {"comment_count": 1}})
    return JSONResponse(status_code=201, content={"message": "Comment created successfully", "id": str(result.inserted_id)})


@router.get("/comments/{comment_id}")
async def read_comment(comment_id: str):
    comment = db.comments.find_one({"_id": ObjectId(comment_id)})
    # Retrieve the author of this comment
    author = db.users.find_one({"_id": ObjectId(comment["author_id"])})
    comment["author"] = author
    if comment:
        comment["_id"] = str(comment["_id"])
        return JSONResponse(status_code=200, content=comment)
    else:
        raise HTTPException(status_code=404, detail="Comment not found")

@router.get("/comments/")
async def read_comments():
    comments = []
    for comment in db.comments.find():
        # Retrieve the author of this comment
        author = db.users.find_one({"_id": ObjectId(comment["author_id"])})
        comment["author"] = author
        comment["_id"] = str(comment["_id"])
        comments.append(comment)
    if comments == []:
        raise HTTPException(status_code=404, detail="There are no posts")
    else:
        return JSONResponse(status_code=200, content=comments)
        

@router.put("/comments/{comment_id}")
async def update_comment(comment_id: str, comment: Comment):
    result = db.comments.update_one({"_id": ObjectId(comment_id)}, {"$set": comment.dict()})
    if result.modified_count == 1:
        return JSONResponse(status_code=200, content={"message": "Comment updated successfully"})
    else:
        raise HTTPException(status_code=404, detail="Comment post not found")

@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: str):
    result = db.comments.delete_one({"_id": ObjectId(comment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Comment not found")
    # Decrement the comment count on the associated blog post
    db.blogposts.update_one({"_id": ObjectId(comment["post_id"])}, {"$inc": {"comment_count": -1}})
    if result.deleted_count == 1:
        return JSONResponse(status_code=200, content={"message": "Comment deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Comment not found")

