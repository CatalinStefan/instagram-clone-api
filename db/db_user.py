from fastapi import HTTPException, status
from db.models import DbUser
from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.hashing import Hash

def create_user(db: Session, request: UserBase):
  new_user = DbUser(
    username = request.username,
    email = request.email,
    password = Hash.bcrypt(request.password)
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def get_user_by_username(db: Session, username: str):
  user = db.query(DbUser).filter(DbUser.username == username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {username} not found')
  return user