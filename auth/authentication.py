from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from db.database import get_db
from sqlalchemy.orm.session import Session
from db.models import DbUser
from db.hashing import Hash
from auth.oauth2 import create_access_token

router = APIRouter(
  tags=['authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  user = db.query(DbUser).filter(DbUser.username == request.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail='Invalid credentials')
  if not Hash.verify(user.password, request.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail='Incorrect password')
  
  access_token = create_access_token(data={'username': user.username})

  return {
    'access_token': access_token,
    'token_type': 'bearer',
    'user_id': user.id,
    'username': user.username
  }