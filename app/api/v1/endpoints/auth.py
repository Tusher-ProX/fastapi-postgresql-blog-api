from fastapi import APIRouter, status, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from app.core import database
from app.core import security
from app.models.users import User
from app.schemas.users import Token, CreateUser, ResponseUser

router = APIRouter(
    tags= ["authentication"]
)


@router.post("/resister", response_model=ResponseUser, status_code=status.HTTP_201_CREATED)
def create_User(request: Annotated[CreateUser, Form()], db: Session = Depends(database.get_db)):

    hashed_password = security.hash_password(request.password)
    request.password = hashed_password
    
    new_user = User(**request.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model= Token, status_code=status.HTTP_200_OK) 
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(User).filter(User.email == user_credential.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Invalid Cradentials"
        )
    
    if not security.verify_password(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Invalid Credential"
        )
    
    access_token = security.create_access_token(data= {"user_id": user.userid})

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }