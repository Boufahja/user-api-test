from fastapi import FastAPI, HTTPException, status, Depends
from typing import Dict
from models import User, UserCreate, UserUpdate
from auth import authenticate

app = FastAPI(
    title="User Management API",
    description="Une API REST pour gérer les utilisateurs (CRUD) avec authentification basique.",
    version="1.0.0",
)

# Stockage en mémoire
users_db: Dict[int, User] = {}
next_id = 1

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, username: str = Depends(authenticate)):
    global next_id
    new_user = User(id=next_id, **user.dict(exclude={"password"}))
    users_db[next_id] = new_user
    next_id += 1
    return new_user

@app.get("/users", response_model=list[User])
def list_users(username: str = Depends(authenticate)):
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, username: str = Depends(authenticate)):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: UserCreate, username: str = Depends(authenticate)):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = User(id=user_id, **updated_user.dict(exclude={"password"}))
    users_db[user_id] = user
    return user

@app.patch("/users/{user_id}", response_model=User)
def partial_update_user(user_id: int, updated_fields: UserUpdate, username: str = Depends(authenticate)):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_data = updated_fields.dict(exclude_unset=True)
    user_data = user.dict()
    user_data.update(updated_data)
    updated_user = User(**user_data)
    users_db[user_id] = updated_user
    return updated_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, username: str = Depends(authenticate)):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return None
