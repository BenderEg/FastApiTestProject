from ..db_code import db_connect, db_close
from ..schema import Vote, UserResponse
from .. import utility
from fastapi import status, HTTPException, APIRouter, Depends
from ..oath2 import get_current_user

router = APIRouter(prefix='/vote', tags=['Vote']) 

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, current_user: dict = Depends(get_current_user)):
    con, cursor = db_connect()
    cursor.execute('''SELECT * FROM posts WHERE id = %s''', (vote.post_id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No such post')
    cursor.execute('''SELECT * FROM votes WHERE post_id = %s and user_id = %s''', (vote.post_id, current_user['id']))
    vote_from_db = cursor.fetchone()
    if vote_from_db:
        if vote.dir == 0:
            cursor.execute('''DELETE FROM votes WHERE post_id = %s and user_id = %s''', (vote.post_id, current_user['id']))
            db_close(con)
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Post has already been voted')
    else:
        if vote.dir == 1:
            cursor.execute('''INSERT INTO votes (post_id, user_id) VALUES (%s, %s)''', (vote.post_id, current_user['id']))
            db_close(con)
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Vote does not exist')
    return {"message": "voted"}
