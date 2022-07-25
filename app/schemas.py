from typing import List, Optional

from pydantic import BaseModel


class UserDetailBase(BaseModel):
    first_name: str
    last_name: str
    phone : int

class UserDetailCreate(UserDetailBase):
    pass


class UserDetail(UserDetailBase):
    id: int

    class Config:
        orm_mode = True
