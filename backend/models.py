from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from typing import List, Optional, Annotated
from bson import ObjectId

# Helper for ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: EmailStr
    hashed_password: str
    colors: List[str] = []

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "hashed_password": "hashed_secret",
                "colors": ["#ffffff"]
            }
        }

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
