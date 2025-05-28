from Security.auth import verify_token
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from Connection.connection import get_db
from Models.BlogModel import User
from passlib.context import CryptContext
from Schemas.UserSchema import setUser,getUser

router=APIRouter(prefix="/user", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/send')
def createUser(request:setUser,db:Session=Depends(get_db)):
    hashpassword=pwd_context.hash(request.password)
    new_user= User(name=request.name,email=request.email,password=hashpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=getUser)
def get_user(id: int, db: Session = Depends(get_db), current_user:User= Depends(verify_token)):
    print(current_user.id)
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    userinfo = db.query(User).filter(User.id == id).first()

    if not userinfo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User ID {id} not found')
    return userinfo