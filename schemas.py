from pydantic import BaseModel
from datetime import datetime

class PlantBase(BaseModel):
    plant_name: str
    species : str
    height : int = 30
    grow_stage : str = "SoSo"

class PlantCreate(PlantBase):
    pass

class CommentBase(BaseModel):
    target_plant_name : str
    comment : str
    time_stamp : datetime

class CommentCreate(CommentBase):
    pass




'''

Pydantic Data Validation Schemas (Response and Request)

'''