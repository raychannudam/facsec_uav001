from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import UserModel, get_db
from Schemas import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from Services.User import UserService
from Security.jwt import get_current_user

router = APIRouter()

def serialize_user(user: UserModel) -> UserResponseSchema:
    return UserResponseSchema(
        id=user.id,
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        age=user.age,
        gender=user.gender,
        roles=[{"id": r.id, "name": r.name, "description": r.description, 
                "created_at": str(r.created_at), "updated_at": str(r.updated_at)} 
               for r in user.roles]
    )

@router.get("/users/me", response_model=UserResponseSchema)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return serialize_user(current_user)

@router.post("/users/register", response_model=UserResponseSchema)
def user_register(user: UserCreateSchema, db: Session = Depends(get_db)):
    result = UserService.register(user.dict(), db)
    return serialize_user(result)

@router.get("/users", response_model=list[UserResponseSchema])
def get_users(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    users = UserService.get_users(db)
    return [serialize_user(u) for u in users]

@router.get("/users/{user_id}", response_model=UserResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    user = UserService.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)

@router.put("/users/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: int, user_update: UserUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    user = UserService.update_user(user_id, user_update.dict(), db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)

@router.delete("/users/{user_id}", response_model=UserResponseSchema)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    user = UserService.delete_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)
