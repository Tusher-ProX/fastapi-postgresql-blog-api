from fastapi import APIRouter, status, Depends, HTTPException, Path, Response
from sqlalchemy.orm import Session
from typing import Annotated

from core.database import get_db
from models.users import User
from schemas.users import CreateUser, ResponseUser, UpdateUser
from core.security import hash_password, get_current_user

router = APIRouter(
    prefix="/users",
    tags = ["users"]
)

@router.get("/", response_model=list[ResponseUser], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "No users found"
        )
    
    return users

@router.get("/{user_id}", response_model=ResponseUser, status_code=status.HTTP_200_OK)
def get_user(user_id:Annotated[int, Path()], db: Session = Depends(get_db)):
    users = db.query(User).filter(User.userid == user_id).first()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "No users found"
        )
    
    return users

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id:Annotated[int, Path()], 
    db: Session = Depends(get_db),
    get_current_user: User = Depends(get_current_user)
    ):

    user = db.query(User).filter(User.userid == user_id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "No users found"
        )
    
    user.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{user_id}', response_model= ResponseUser, status_code=status.HTTP_200_OK)
def update_user(
    user_id:Annotated[int, Path()], 
    request: CreateUser, 
    db: Session = Depends(get_db),
    get_current_user: User = Depends(get_current_user)
    ):

    user_query = db.query(User).filter(User.userid == user_id)

    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "No users found"
        )
    
    hashed_password = hash_password(request.password)
    request.password = hashed_password
    
    user_query.update(request.model_dump(), synchronize_session=False) # type: ignore[arg-type]
    db.commit()
    db.refresh(user)

    return user

@router.patch('/{user_id}', response_model= ResponseUser, status_code=status.HTTP_200_OK)
def updates(
    user_id:Annotated[int, Path()], 
    request: UpdateUser, 
    db: Session = Depends(get_db),
    get_current_user: User = Depends(get_current_user)
    ):
    
    user_query = db.query(User).filter(User.userid == user_id)

    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "No users found"
        )
    
    hashed_password = hash_password(request.password)
    request.password = hashed_password
    
    user_query.update(request.model_dump(exclude_unset=True), synchronize_session=False) # type: ignore[arg-type]
    db.commit()
    db.refresh(user)

    return user