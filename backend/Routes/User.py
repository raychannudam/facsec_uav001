from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import UserModel, get_db
from Schemas import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from Services.User import UserService
from Security.jwt import get_current_user
from Schemas.Role import RoleResponseSchema

router = APIRouter()

@router.get("/users/me", response_model=UserResponseSchema)
def get_me(current_user: UserModel = Depends(get_current_user)):
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in current_user.roles.all()]
    return UserResponseSchema(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        fullname=current_user.fullname,
        age=current_user.age,
        gender=current_user.gender,
        roles=roles
    )

@router.post("/users/register", response_model=UserResponseSchema)
def user_register(user: UserCreateSchema, db: Session = Depends(get_db)):
    result = UserService.register(user, db)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in result.roles]
    return UserResponseSchema(
        id=result.id,
        email=result.email,
        username=result.username,
        fullname=result.fullname,
        age=result.age,
        gender=result.gender,
        roles=roles
    )

@router.get("/users", response_model=list[UserResponseSchema])
def get_users(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    users = UserService.get_users(db)
    return [UserResponseSchema(
        id=u.id,
        email=u.email,
        username=u.username,
        fullname=u.fullname,
        age=u.age,
        gender=u.gender,
        roles=[RoleResponseSchema(
            id=role.id,
            name=role.name,
            description=role.description,
            created_at=str(role.created_at),
            updated_at=str(role.updated_at)
        ) for role in u.roles]
    ) for u in users]

@router.get("/users/{user_id}", response_model=UserResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    user = UserService.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    return UserResponseSchema(
        id=user.id,
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        age=user.age,
        gender=user.gender,
        roles=roles
    )

@router.put("/users/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: int, user_update: UserUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    user = UserService.update_user(user_id, update_data, db)
    if isinstance(user, dict) and "error" in user:
        raise HTTPException(status_code=400, detail=user["error"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    return UserResponseSchema(
        id=user.id,
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        age=user.age,
        gender=user.gender,
        roles=roles
    )

@router.delete("/users/{user_id}", response_model=UserResponseSchema)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    user = UserService.delete_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    roles = [RoleResponseSchema(
        id=role.id,
        name=role.name,
        description=role.description,
        created_at=str(role.created_at),
        updated_at=str(role.updated_at)
    ) for role in user.roles]
    return UserResponseSchema(
        id=user.id,
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        age=user.age,
        gender=user.gender,
        roles=roles
    )