from datetime import datetime, timedelta , timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from Models.BlogModel import User
from sqlalchemy.orm import Session
from Connection.connection import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/send") 
# Secret key (store securely in env variable ideally)
SECRET_KEY = "ytitirirejd40598yu5053g0e^%$3fj9448tufow485uteogwjtj4yhugojwi4utgjwo###"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")