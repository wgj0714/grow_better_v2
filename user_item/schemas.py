from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class UserBase(BaseModel):
    email: str
    is_active: bool

class UserCreate(UserBase):
    pass




'''

Pydantic Data Validation Schemas (Response and Request)

'''