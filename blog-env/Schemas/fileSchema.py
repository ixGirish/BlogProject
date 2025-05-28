from pydantic import BaseModel

class fileresponse(BaseModel):
    id:int
    name:str
    type:str

    class Config():
        orm_mode=True

