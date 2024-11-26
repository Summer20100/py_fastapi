from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    id: int
    title: str
    body: str

posts = [
    {'id': 1, 'title': 'News 1', 'body': 'Text 1'},
    {'id': 2, 'title': 'News 2', 'body': 'Text 2'},
    {'id': 3, 'title': 'News 3', 'body': 'Text 3'},
]

@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]
    # return posts

@app.get("/items/{id}")
async def items(id: int) -> Post:
    for post in posts:
        if post['id'] == id:
            # return post
            return Post(**post)
    raise HTTPException(status_code=404, detail='Post not found')

@app.get("/search")
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:
    if post_id is not None:
        for post in posts:
            if post['id'] == post_id:
                return {'data' : Post(**post)} 
                # return post
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {'data' : None}
    
    # raise HTTPException(status_code=400, detail="No post id provided")