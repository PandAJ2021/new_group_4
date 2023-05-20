from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import hashlib


app = FastAPI()


class User(BaseModel):
    id: int
    username: str = Field(min_length=5 , max_length=20)
    password: str #= Field(regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")
    email: Optional[str] = None


class UserOutput(BaseModel):
    username: str
    email: Optional[str]


users: list[User] = []


@app.get('/user/get-user/{user_id}')
async def get_user(user_id):
    the_user = list(filter(lambda user : user.id == int(user_id), users)) 
    if the_user:
        return UserOutput(username=the_user[0].username, email=the_user[0].email)
    raise HTTPException(status_code=404 , detail= "user not found!")


@app.post('/user/create-user')
async def set_user(new_user: dict):
    if list(filter(lambda user: user.username == new_user['username'], users)):
        raise HTTPException(status_code=409, detail="Username already taken.")
    new_user['password'] = hashlib.sha512(new_user['password'].encode('utf-8')).hexdigest()
    users.append(User(**new_user))
    return "register done"
