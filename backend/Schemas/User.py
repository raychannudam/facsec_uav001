from pydantic import BaseModel, Field

class UserCreateSchema(BaseModel):
    email: str = Field(..., description="The email of the user")
    username: str = Field(..., description="The username of the user")
    password: str = Field(..., description="The password of the user")
    fullname: str = Field(..., description="The full name of the user")
    age: int = Field(..., description="The age of the user")
    gender: str = Field(..., description="The gender of the user")

class UserUpdateSchema(BaseModel):
    email: str = Field(..., description="The email of the user")
    username: str = Field(..., description="The username of the user")
    fullname: str = Field(..., description="The full name of the user")
    age: int = Field(..., description="The age of the user")
    gender: str = Field(..., description="The gender of the user")

class UserResponseSchema(BaseModel):
    id: int = Field(..., description="The ID of the user")
    email: str = Field(..., description="The email of the user")
    username: str = Field(..., description="The username of the user")
    fullname: str = Field(..., description="The full name of the user")
    age: int = Field(..., description="The age of the user")
    gender: str = Field(..., description="The gender of the user")
