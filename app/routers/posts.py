from ..db_code import db_connect, db_close
from ..schema import Post, PostResponse
from fastapi import status, HTTPException, APIRouter, Depends
from typing import List
from ..oath2 import get_current_user

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=List[(PostResponse)])
def get_posts(current_user: dict = Depends(get_current_user), limit: int = 10, offset: int = 0, search: str = ""):
    con, cursor = db_connect()
    cursor.execute('''SELECT title, content, posts.created_at, count(post_id) as votes, users.email from posts
	left join votes on posts.id = votes.post_id
	INNER join users on posts.user_id = users.id
    WHERE title LIKE %s
    GROUP by posts.id, users.email
    LIMIT %s OFFSET %s''', (f'%{search}%', limit, offset))
    posts = cursor.fetchall()
    print(posts)
    db_close(con)
    return posts    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: Post, current_user: dict = Depends(get_current_user)):   
    con, cursor = db_connect()
    cursor.execute('INSERT INTO posts (title, content, user_id) VALUES (%s, %s, %s) RETURNING *', (post.title, post.content, current_user['id']))
    new_post = cursor.fetchone()
    db_close(con)
    return new_post

@router.get("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def get_post(id: int, current_user: dict = Depends(get_current_user)):
    con, cursor = db_connect()
    cursor.execute('''SELECT title, content, posts.created_at, count(post_id) as votes, users.id, users.email from posts
	left join votes on posts.id = votes.post_id
	INNER join users on posts.user_id = users.id
    WHERE posts.id = %s
    GROUP by posts.id, users.email, users.id
    ''', (id,))
    post = cursor.fetchone()
    db_close(con)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id = {id} not found')
    post = dict(post)
    if post['id'] != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user: dict = Depends(get_current_user)):
    con, cursor = db_connect()
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (id,))
    deleted_post = cursor.fetchone()
    db_close(con)
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id = {id} does not exist')
    deleted_post = dict(deleted_post)
    if deleted_post['user_id'] != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    
@router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def update_post(id: int, post: Post, current_user: dict = Depends(get_current_user)):
    con, cursor = db_connect()
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    db_close(con)   
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id = {id} does not exist')
    updated_post = dict(updated_post)
    if updated_post['user_id'] != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    return updated_post