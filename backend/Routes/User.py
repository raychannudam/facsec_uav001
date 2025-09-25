from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import UserModel, get_db
from Schemas import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from Services.User import UserService
from Security.jwt import get_current_user

router = APIRouter()

@router.get("/users/me", response_model=UserResponseSchema)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return UserResponseSchema(**current_user.__dict__)

@router.post("/users/register", response_model=UserResponseSchema)
def user_register(user: UserCreateSchema, db: Session = Depends(get_db)):
    result = UserService.register(user, db)
    if isinstance(result, dict) and "error" in result:
        return result
    return result


# Get all users
@router.get("/users", response_model=list[UserResponseSchema])
def get_users(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    users = UserService.get_users(db)
    return [UserResponseSchema(**u.__dict__) for u in users]


# Get user by ID
@router.get("/users/{user_id}", response_model=UserResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    user = UserService.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseSchema(**user.__dict__)


# Update user
@router.put("/users/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: int, user_update: UserUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    user = UserService.update_user(user_id, update_data, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseSchema(**user.__dict__)


# Delete user
@router.delete("/users/{user_id}", response_model=UserResponseSchema)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    user = UserService.delete_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseSchema(**user.__dict__)

