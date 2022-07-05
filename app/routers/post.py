from app import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import oath2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostWithVotes])
def see_posts(db: Session = Depends(get_db),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

#    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts_votes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostUser)
def launch_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user=Depends(oath2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    print(current_user.email)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostWithVotes)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).\
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).\
        filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user=Depends(oath2.get_current_user)):
    del_post_query = db.query(models.Post).filter(models.Post.id == id)

    if del_post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")

    if del_post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")

    del_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostUser)
def upd_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
             current_user=Depends(oath2.get_current_user)):

    upd_post_query = db.query(models.Post).filter(models.Post.id == id)

    upd_post = upd_post_query.first()

    if upd_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")

    if upd_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")

    upd_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return upd_post_query.first()
