
from enum import Enum 

from pydantic import BaseModel, ConfigDict
from app.enums import PriorityEnum
class TaskCreate(BaseModel):
    for_user_id: int | None = None
    title: str 
    description: str
    priority: PriorityEnum
    

class TaskPutUpdate(BaseModel):
    for_user_id: int
    title: str 
    description: str
    priority: PriorityEnum

class TaskPatchUpdate(BaseModel):
    for_user_id: int | None = None
    title: str | None = None
    description: str | None = None
    priority: PriorityEnum | None = None
    
    model_config = ConfigDict(from_attributes=True)