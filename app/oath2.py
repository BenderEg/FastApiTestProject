from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Dict
from copy import deepcopy
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.schema import TokenData
from .db_code import db_connect, db_close
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: Dict, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = deepcopy(data)
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt    

def verify_access_token(token: Annotated[str, Depends(oauth2_scheme)], credentials_exeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('id')
        if not id:
            raise credentials_exeption
        token_data = TokenData(id = id)
    except JWTError:
        raise credentials_exeption
    return token_data

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
        credentials_exeption = HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})):
    get_token = verify_access_token(token, credentials_exeption)
    con, cursor = db_connect()
    cursor.execute('''SELECT * FROM users WHERE id = %s''', (get_token.id,))
    user = dict(cursor.fetchone())
    db_close(con)
    return user
