from pydantic import BaseModel, Field


# -----------user----------
class UserCreat(BaseModel): 
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(mix_length=4, max_length= 128)


class UserRead(BaseModel):
    id: int 
    username: str
    
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -----------Tasks----------
class Taskbase(TaskBase):
    title: str = Field(min_length=1, max_length= 200)
    description: str | None = None
    is_done: bool = False


class TaskCreate(TaskModel):
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None


class TaskRead(TaskBase):
    id: int
    ower_id: int 

    model_config = {"from_attributes": True}