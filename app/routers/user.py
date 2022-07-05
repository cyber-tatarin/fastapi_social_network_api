from app import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/users", tags=["Users"]
)

@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.RespUser)
def create_user(newuser: schemas.NewUser, db: Session = Depends(get_db)):

    hashed_pwd = utils.pwd_context.hash(newuser.password)
    newuser.password = hashed_pwd

    new_user = models.User(**newuser.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.SeeUser)
def get_post(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} was not found")
    return user
