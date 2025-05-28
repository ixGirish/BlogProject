from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from Models.BlogModel import User
from passlib.context import CryptContext
from Connection.connection import get_db
from Security.auth import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES

router=APIRouter(prefix='/login' , tags=['Security'])

@router.post('/send')
def loginfunction(db:Session=Depends(get_db),form_data:OAuth2PasswordRequestForm = Depends()):
    user=db.query(User).filter(form_data.username==User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Password incorrect') 
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }