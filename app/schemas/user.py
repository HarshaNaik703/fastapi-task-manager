from pydantic import BaseModel,EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email:EmailStr
    password : str

class UserLogin(BaseModel):
    email: EmailStr
    password : str

class UserRead(BaseModel):
    id : int
    email : EmailStr
    role : str
    is_active : bool
    created_at : datetime

    class config:
        from_attributes = True
        
