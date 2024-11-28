from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List, Dict, Annotated
from model import Post, User, PostCreate, UserCreate


app = FastAPI()

users = [
    {'id': 1, 'name': 'Дима', 'age': 40},
    {'id': 2, 'name': 'Кристина', 'age': 35},
    {'id': 3, 'name': 'Лёша', 'age': 42},
]

posts = [
    {'id': 1, 'title': 'News 1', 'body': 'Text 1', 'author': users[2]},
    {'id': 2, 'title': 'News 2', 'body': 'Text 2', 'author': users[0]},
    {'id': 3, 'title': 'News 3', 'body': 'Text 3', 'author': users[1]},
]

@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]
    # return posts
    
@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next(
        (user for user in users if user["id"] == post.author_id), 
        None)
    if not author:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {post.author_id} not found"
        )
    
    print(post.title)
    
    new_post = {
        "id": len(posts) + 1,
        "title": post.title,
        "body": post.body,
        "author": author
    }
    
    # new_post = Post(
    #     id = len(posts) + 1,
    #     title = post.title,
    #     body = post.body,
    #     author = author
    # )
        
    posts.append(new_post)
    
    return Post(**new_post)
    # return new_post

@app.post("/user/add")
async def add_user(user: Annotated[
    UserCreate,
    Body(
        ..., 
        example = {
            "name": "UserName",
            "age": 40
        }
    )
]) -> User:
    new_user = User(
        id = len(users) + 1,
        name = user.name,
        age = user.age
    )
        
    users.append(new_user)
    return new_user
    
@app.get("/items/{id}")
async def items(id: Annotated[int, Path(..., title='ID post here must be', ge=1, )]) -> Post:
    for post in posts:
        if post['id'] == id:
            # return post
            return Post(**post)
    raise HTTPException(status_code=404, detail='Post not found')

@app.get("/search")
async def search( post_id: Annotated[
    Optional[int],
    Query(title='ID post for searching', ge=1 )
]) -> Dict[str, Optional[Post]]:
    if post_id is not None:
        for post in posts:
            if post['id'] == post_id:
                return {'data' : Post(**post)} 
                # return post
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {'data' : None}
    
    # raise HTTPException(status_code=400, detail="No post id provided")