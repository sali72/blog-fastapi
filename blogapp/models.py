from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str

class BlogPost(BaseModel):
    title: str
    content: str
    author_id: str

class Comment(BaseModel):
    content: str
    post_id: str
    author_id: str
    comment_count: int = 0