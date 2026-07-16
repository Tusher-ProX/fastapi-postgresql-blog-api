from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas import posts
from core import database, security
from models import users, posts as modelPost

router = APIRouter(
    prefix= "/vote",
    tags= ["vote"]
)

@router.post("/")
def vote(
    vote: posts.Vote, 
    db: Session = Depends(database.get_db), 
    current_user: users.User = Depends(security.get_current_user)
    ):

    post = db.query(modelPost.Post).filter(modelPost.Post.post_id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exist")
    
    vote_query = db.query(modelPost.Vote).filter(
        modelPost.Vote.post_id == vote.post_id, modelPost.Vote.user_id == current_user.userid)
    
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.userid} has alredy voted on post {vote.post_id}")
        
        new_vote = modelPost.Vote(post_id=vote.post_id, user_id=current_user.userid)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
