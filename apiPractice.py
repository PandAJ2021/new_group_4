from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from hashlib import sha224


app = FastAPI()

class User(BaseModel):
    id: int
    username: str = Field(max_length=20)
    password: str = Field(max_length=25)


class UserOutput(BaseModel):
    id: int
    username: str


users: list[User] = []


@app.get("/user/{user_id}")
async def get_user(user_id: int) -> UserOutput:
    user = list(filter(lambda user: user.id == user_id, users))
    if user:
        found_user: User = user[0]
        return UserOutput(**found_user.dict())
    raise HTTPException(status_code=404, detail="User not found.")


@app.post("/user/create")
async def add_user(user: User):
    passowrd = sha224(user.password.encode())
    users.append(user)
