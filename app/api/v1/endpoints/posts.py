from fastapi import APIRouter, Depends, Path, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Annotated, Optional

from app.schemas.posts import CreatePosts, ResponsePost, Post as shemasPost
from app.core.database import get_db
from app.models.posts import Post, Vote
from app.models.users import User
from app.core.security import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/", response_model=list[ResponsePost])
def get_all_posts(
    search: str = "",
    limit: int = 100,
    skip: int = 0,
    db: Session = Depends(get_db),
    get_current_user: User = Depends(get_current_user)
):
    posts = (
        db.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Vote.post_id == Post.post_id, isouter=True)
        .group_by(Post.post_id)
        .filter(Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    if not posts:
        raise HTTPException(
            status_code=404,
            detail="No Post Found"
        )

    return [
        {
            "post": post_obj,
            "votes": votes
        }
        for post_obj, votes in posts
    ]

@router.get("/{post_id}", response_model=ResponsePost, status_code=status.HTTP_200_OK)
def get_post(
    post_id: Annotated[int, Path()],
    db: Session = Depends(get_db),
    get_current_user: User = Depends(get_current_user)
):
    result = (
        db.query(
            Post,
            func.count(Vote.post_id).label("votes")
        )
        .join(
            Vote,
            Vote.post_id == Post.post_id,
            isouter=True
        )
        .group_by(Post.post_id)
        .filter(Post.post_id == post_id)
        .first()
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found"
        )

    post_obj, votes = result

    return {
        "post": post_obj,
        "votes": votes
    }

@router.post('/', response_model=shemasPost, status_code=status.HTTP_201_CREATED)
def create_post(
    request: CreatePosts, 
    db: Session = Depends(get_db), 
    get_current_user: User = Depends(get_current_user) 
    ):

    new_post = Post(**request.model_dump(), user_id = get_current_user.userid)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: Annotated[int, Path()], 
    db: Session = Depends(get_db),
    get_current_user: User = Depends(get_current_user)
):

    post = db.query(Post).filter(Post.post_id == post_id)

    deleted_post = post.first()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'No post found'
        )

    if deleted_post.user_id != get_current_user.userid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", response_model=shemasPost, status_code=status.HTTP_200_OK)
def update_post(
    post_id: Annotated[int, Path()], 
    request: CreatePosts, 
    db: Session = Depends(get_db),
    get_current_user: User = Depends(get_current_user)
):

    post_query = db.query(Post).filter(Post.post_id == post_id)

    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'No post found'
        )

    if post.user_id != get_current_user.userid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.update(request.model_dump(), synchronize_session=False)  # type: ignore[arg-type]
    db.commit()
    db.refresh(post)

    return post