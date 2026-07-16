from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Annotated

from .users import ResponseUser

class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePosts(BasePost):
    pass

class Post(BasePost):
    post_id: int
    user_id: int
    created_time: datetime
    user: ResponseUser

    model_config = ConfigDict(from_attributes=True)

class ResponsePost(BaseModel):
    post: Post
    votes: int
    
    model_config = ConfigDict(from_attributes=True)

    
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]