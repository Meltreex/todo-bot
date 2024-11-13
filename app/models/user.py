from pydantic import BaseModel

class UserCreate(BaseModel):
    first_name: str
    username: str