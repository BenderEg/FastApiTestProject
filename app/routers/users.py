from ..db_code import db_connect, db_close
from ..schema import User, UserResponse
from .. import utility
from fastapi import status, HTTPException, APIRouter

router = APIRouter(prefix='/users', tags=['Users']) 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_post(user: User):
    con, cursor = db_connect()
    user.password = utility.get_password_hash(user.password)
    try:
        cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *', (user.email, user.password))
        user = cursor.fetchone()
        return user
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'email already exists')
    finally:
        db_close(con)

@router.get("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=UserResponse)
def get_user(id: int):
    con, cursor = db_connect()
    cursor.execute('''SELECT * FROM users WHERE id = %s''', (id,))
    user = cursor.fetchone()
    db_close(con)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id = {id} not found')
    return user
