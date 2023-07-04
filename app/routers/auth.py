from ..db_code import db_connect, db_close
from ..schema import Token
from .. import utility, oath2
from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/login', tags=['login user']) 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
def create_post(user: OAuth2PasswordRequestForm = Depends()): #OAuth2PasswordRequestForm = Depends() return query in form: username, password
    con, cursor = db_connect()
    cursor.execute('SELECT * FROM users WHERE email = %s', (user.username,))
    try:
        db_user = dict(cursor.fetchone())
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    finally:
        db_close(con)
    if not utility.verify_password(user.password, db_user['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    access_token = oath2.create_access_token({"id" : db_user['id']})
    return {"access_token" : access_token}